"""Text-chat adapter over the existing ILIS pipeline."""

from __future__ import annotations

import re
from typing import Any

from ilis.interfaces.ilis_core import ILISCore
from ilis.persona import PersonaConfig, PersonaRenderer
from ilis.persona.profiles import MODE_A


class ChatbotAdapter:
    """Run semantic analysis, reasoning, generation, then chatbot identity."""

    _TOUCHES_WOODEN_HOUSE = re.compile(
        r"^\s*(?P<source>api)\s+menyentuh\s+"
        r"(?P<target>rumah)\s+(?P<material>kayu)\s*[.!?]?\s*$",
        re.IGNORECASE,
    )

    _IDENTITY_INTENT = re.compile(
        r"\b(?:siapa\s+kamu|apa\s+yang\s+bisa\s+kamu\s+lakukan|"
        r"kemampuanmu|jelaskan\s+kemampuanmu)\b",
        re.IGNORECASE,
    )
    _IDENTITY_CAPABILITIES_REPLY = (
        "ILIS dapat membantu memahami pertanyaan berbahasa Indonesia, "
        "mengolah makna kalimat, dan menarik kesimpulan berdasarkan aturan "
        "serta fakta yang tersedia. ILIS juga dapat menyusun jawaban dalam "
        "ragam bahasa yang didukung, seperti formal dan santai.\n\n"
        "ILIS bekerja secara deterministik tanpa menggunakan model bahasa "
        "besar (LLM). Karena itu, jawaban bergantung pada aturan, pengetahuan, "
        "dan informasi yang tersedia di dalam sistem."
    )

    _STYLE_INSTRUCTION = re.compile(
        r"(?:jawab|jelaskan|uraikan|terangkan)\s+(?:dengan\s+)?(?P<style>sopan|santai)",
        re.IGNORECASE,
    )

    @classmethod
    def _instruction_register(cls, text: str) -> str | None:
        """Map explicit response-style instructions to generator registers."""
        match = cls._STYLE_INSTRUCTION.search(text)
        if not match:
            return None
        return "formal" if match.group("style").casefold() == "sopan" else "informal"

    def __init__(
        self, core: ILISCore, *, persona_config: PersonaConfig | None = None
    ) -> None:
        if not isinstance(core, ILISCore):
            raise TypeError("core must be an ILISCore instance")
        self.core = core
        self.persona_config = (
            self.persona_config
        )
        # Chatbot integrations identify as ILIS unless the host supplies
        # another explicitly validated chatbot/application profile.
        self.persona_renderer = PersonaRenderer(
            persona_config if persona_config is not None else PersonaConfig.chatbot_ilis()
        )

    def respond(
        self, text: str, session_id: str, *, speaker: str = "user",
        register: str | None = None,
    ) -> dict[str, Any]:
        if not isinstance(text, str) or not text.strip():
            raise ValueError("text must be a non-empty string")

        # Identity questions belong to the chatbot integration, not ILIS Core.
        # Only the canonical Mode A chatbot may answer as ILIS; host applications
        # and game characters continue through the ordinary Core pipeline.
        normalized_text = " ".join(text.casefold().split())
        if (
            self.persona_config.mode == MODE_A
            and self._IDENTITY_INTENT.search(normalized_text)
        ):
            # Preserve the adapter's invalid-session behavior without running
            # Semantic, Reasoning, Language Generator, or storage mutations.
            self.core.context_engine.get_context(session_id)
            static_answer = self._IDENTITY_CAPABILITIES_REPLY
            final_answer = self.persona_renderer.render(static_answer)
            return {
                "answer": final_answer,
                "text": final_answer,
                "metadata": {
                    "register": "formal",
                    "confidence_score": 1.0,
                    "reasoning_type": "identity_intent",
                    "conflict_status": "clear",
                    "evidence": [],
                    "semantic_status": "identity_intent",
                    "response_type": "identity_intent",
                    "session_id": session_id,
                },
                "semantic_result": None,
                "reasoning_result": None,
                "generation": None,
            }

        processed = self.core.context_engine.process_message(
            session_id, speaker, text, ingest_semantics=False
        )
        semantic = processed["semantic_result"]

        # Always enter the validated Semantic -> Reasoning path first. Unsupported
        # and low-confidence payloads are converted by infer_semantic() to unknown.
        reasoning = self.core.reasoning_engine.infer_semantic(semantic)

        legacy_match = self._TOUCHES_WOODEN_HOUSE.fullmatch(text)
        if legacy_match:
            # Preserve the exact V1 adapter behavior for this legacy sentence.
            # V1 did not expose a usable Semantic confidence for this pattern, so
            # a neutral multiplier (1.0) keeps its historical 0.72 score intact.
            reasoning = self.core.reasoning_engine.infer_burn_risk(
                legacy_match.group("source").casefold(),
                legacy_match.group("target").casefold(),
            )
            semantic_confidence = 1.0
        else:
            semantics = semantic.get("semantics")
            confidence = semantics.get("Confidence") if isinstance(semantics, dict) else None
            if (
                isinstance(confidence, (int, float))
                and not isinstance(confidence, bool)
                and 0.0 <= confidence <= 1.0
            ):
                semantic_confidence = float(confidence)
            else:
                semantic_confidence = 0.0

        # Confidence propagation: final reasoning confidence is the rule-based
        # reasoning score multiplied by Semantic Engine confidence. This adjusts
        # the numeric score only; it never upgrades unknown/conflicting or changes
        # verified/hypothetical reasoning_type.
        base_confidence = reasoning.get("confidence_score", 0.0)
        if not isinstance(base_confidence, (int, float)) or isinstance(base_confidence, bool):
            base_confidence = 0.0
        reasoning["confidence_score"] = round(
            max(0.0, min(1.0, float(base_confidence)))
            * semantic_confidence,
            6,
        )
        reasoning["reasons"] = list(reasoning.get("reasons") or [])
        reasoning["reasons"].append(
            "Confidence akhir = confidence Reasoning × confidence Semantic "
            f"({float(base_confidence):.6f} × {semantic_confidence:.6f})."
        )

        instruction_register = self._instruction_register(text)
        effective_register = register or instruction_register
        if effective_register is None:
            semantic_register = (semantic.get("semantics") or {}).get("Register")
            if semantic_register not in {"formal", "informal", "slang"}:
                session = self.core.context_engine.get_context(session_id)["session"]
                metadata = session.get("metadata", {})
                semantic_register = metadata.get("register") if isinstance(metadata, dict) else None
            if semantic_register in {"formal", "informal", "slang"}:
                effective_register = semantic_register

        generated = self.core.language_generator.generate(
            reasoning, register=effective_register, semantic_result=semantic,
            session_id=session_id, polite=instruction_register == "formal",
        )
        # Persona decorates only the generated text. Semantic, Reasoning,
        # generation metadata, and the raw Language Generator output stay intact.
        final_answer = self.persona_renderer.render(generated["text"])
        conflicts = self.core.knowledge_engine.detect_conflicts()
        return {
            "answer": final_answer,
            "text": final_answer,
            "metadata": {
                "register": generated["register"],
                "confidence_score": generated["confidence_score"],
                "reasoning_type": generated["reasoning_type"],
                "conflict_status": "conflicting" if conflicts or reasoning["reasoning_type"] == "conflicting" else "clear",
                "evidence": generated["evidence"],
                "semantic_status": semantic.get("status"),
                "session_id": session_id,
            },
            "semantic_result": semantic,
            "reasoning_result": reasoning,
            "generation": generated,
        }
