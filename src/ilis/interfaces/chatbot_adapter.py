"""Text-chat adapter over the stateless ILIS pipeline."""

from __future__ import annotations

import re
from typing import Any

from ilis.experimental.negation_mapping import map_negation
from ilis.interfaces.ilis_core import ILISCore
from ilis.interfaces.session_manager import SessionManager
from ilis.semantics.contract_validator import validate_output
from ilis.persona import PersonaConfig, PersonaRenderer
from ilis.persona.profiles import MODE_A


class ChatbotAdapter:
    """Run ILIS for one turn while keeping transcript state in SessionManager."""

    _IDENTITY_INTENT = re.compile(
        r"(?<!dengan )\b(?:siapa\s+kamu|apa\s+yang\s+bisa\s+kamu\s+lakukan|"
        r"kemampuanmu|jelaskan\s+kemampuanmu|"
        r"lu\s+siapa|kamu\s+bisa\s+ngapain|"
        r"kemampuan\s+lu\s+apa\s+aja|kemampuan\s+lo\s+apa\s+aja|"
        r"km\s+bs\s+ngapain|eh\s+km\s+bisa\s+ngapain|"
        r"jelasin\s+dong\s+siapa\s+dirimu)\b",
        re.IGNORECASE,
    )
    _RESET_COMMAND = re.compile(
        r"^\s*(?:reset\s+percakapan|hapus\s+riwayat(?:\s+percakapan)?)\s*[.!?]*\s*$",
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

    def __init__(
        self, core: ILISCore, *, persona_config: PersonaConfig | None = None,
        session_manager: SessionManager | None = None,
    ) -> None:
        if not isinstance(core, ILISCore):
            raise TypeError("core must be an ILISCore instance")
        if session_manager is not None and not isinstance(session_manager, SessionManager):
            raise TypeError("session_manager must be a SessionManager instance")
        self.core = core
        self.session_manager = session_manager if session_manager is not None else SessionManager()
        self.persona_config = (
            persona_config if persona_config is not None else PersonaConfig.chatbot_ilis()
        )
        self.persona_renderer = PersonaRenderer(self.persona_config)

    def create_session(self, metadata: dict[str, Any] | None = None) -> str:
        return self.session_manager.create_session(metadata=metadata)

    @classmethod
    def _instruction_register(cls, text: str) -> str | None:
        match = cls._STYLE_INSTRUCTION.search(text)
        if not match:
            return None
        return "formal" if match.group("style").casefold() == "sopan" else "informal"

    def respond(
        self, text: str, session_id: str | None = None, *,
        speaker: str = "user", register: str | None = None,
        context_snapshot: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        if not isinstance(text, str) or not text.strip():
            raise ValueError("text must be a non-empty string")
        if session_id is None:
            session_id = self.create_session()
        if self.session_manager.get_session(session_id) is None:
            # Backward compatibility: an existing Core session ID may be
            # adopted, but its transcript is never read or written here.
            legacy_session = self.core.context_engine.get_context(session_id)["session"]
            self.session_manager.ensure_session(
                session_id, metadata=legacy_session.get("metadata", {})
            )
        else:
            self.session_manager.require_session(session_id)

        prior_turns = self.session_manager.get_recent_turns(session_id)
        negation_result = map_negation(
            text, None, context=[turn.user_message for turn in prior_turns],
        )
        negation_metadata = {
            "negation_type": negation_result["mapping_label"],
            "confidence": negation_result["confidence"],
            "evidence": {
                "detected_cues": negation_result["detected_cues"],
                "scope": negation_result["scope"],
                "reason": negation_result["mapping_reason"],
            },
        }

        if self._RESET_COMMAND.fullmatch(text):
            reset = self.session_manager.reset_session(session_id)
            answer = "Riwayat percakapan sesi ini sudah direset. Kita mulai dari awal, ya."
            return {
                "answer": answer, "text": answer,
                "metadata": {
                    "session_id": session_id, "response_type": "session_reset",
                    "register": "formal", "deleted_turns": reset["deleted_turns"],
                    "negation": negation_metadata,
                },
                "semantic_result": None, "reasoning_result": None, "generation": None,
            }

        managed_snapshot = self.session_manager.get_context_snapshot(session_id)
        if context_snapshot is not None:
            if not isinstance(context_snapshot, dict):
                raise TypeError("context_snapshot must be a dictionary or None")
            if context_snapshot.get("session_id", session_id) != session_id:
                raise ValueError("context_snapshot session_id does not match session_id")
            # SessionManager remains authoritative; optional host context is
            # carried separately and cannot replace or overwrite managed turns.
            snapshot = dict(managed_snapshot)
            snapshot["additional_context"] = dict(context_snapshot)
        else:
            snapshot = managed_snapshot

        normalized_text = " ".join(text.casefold().split())
        if self.persona_config.mode == MODE_A and self._IDENTITY_INTENT.search(normalized_text):
            static_answer = self.persona_renderer.render(
                self._IDENTITY_CAPABILITIES_REPLY, include_identity=True
            )
            self.session_manager.add_turn(session_id, text, static_answer, metadata={
                "response_type": "identity_intent", "speaker": speaker,
            })
            return {
                "answer": static_answer, "text": static_answer,
                "metadata": {
                    "register": "formal", "confidence_score": 1.0,
                    "reasoning_type": "identity_intent", "conflict_status": "clear",
                    "evidence": [], "semantic_status": "identity_intent",
                    "response_type": "identity_intent", "session_id": session_id,
                    "context_turns_used": len(snapshot.get("turns", [])),
                    "negation": negation_metadata,
                },
                "semantic_result": None, "reasoning_result": None, "generation": None,
            }

        semantic = self.core.analyze_text(text, context_snapshot=snapshot)

        # BL-ILIS-002 uses a richer diagnostic label set than Semantic 1.0.
        # Map only labels representable by the stable Semantic.Negation enum;
        # prohibitive is represented as negative, while ambiguous/none leave
        # the parser's value intact rather than inventing a new contract value.
        semantic_negation = {
            "negative": "negative",
            "not_yet": "not_yet",
            "identity_negative": "identity_negative",
            "prohibitive": "negative",
        }.get(negation_result["mapping_label"])
        semantics = semantic.get("semantics")
        if semantic_negation is not None and isinstance(semantics, dict):
            semantics["Negation"] = semantic_negation
            validate_output(semantic)
        negation_metadata["semantic_value"] = (
            semantics.get("Negation") if isinstance(semantics, dict) else None
        )
        negation_metadata["applied_to_semantic"] = (
            semantic_negation is not None and isinstance(semantics, dict)
        )

        reasoning = self.core.reasoning_engine.infer_semantic(
            semantic, context_snapshot=snapshot,
        )

        semantics = semantic.get("semantics")
        confidence = semantics.get("Confidence") if isinstance(semantics, dict) else None
        semantic_confidence = (
            float(confidence) if isinstance(confidence, (int, float))
            and not isinstance(confidence, bool) and 0.0 <= confidence <= 1.0
            else 0.0
        )

        base_confidence = reasoning.get("confidence_score", 0.0)
        if not isinstance(base_confidence, (int, float)) or isinstance(base_confidence, bool):
            base_confidence = 0.0
        reasoning["confidence_score"] = round(
            max(0.0, min(1.0, float(base_confidence))) * semantic_confidence, 6
        )
        reasoning["reasons"] = list(reasoning.get("reasons") or [])
        reasoning["reasons"].append(
            "Confidence akhir = confidence Reasoning × confidence Semantic "
            f"({float(base_confidence):.6f} × {semantic_confidence:.6f})."
        )

        instruction_register = self._instruction_register(text)
        effective_register = register or instruction_register
        session = self.session_manager.require_session(session_id)
        if effective_register is None:
            semantic_register = (semantic.get("semantics") or {}).get("Register")
            if semantic_register not in {"formal", "informal", "slang"}:
                semantic_register = session.metadata.get("register")
            if semantic_register in {"formal", "informal", "slang"}:
                effective_register = semantic_register

        generated = self.core.language_generator.generate(
            reasoning, register=effective_register, semantic_result=semantic,
            context=snapshot, polite=instruction_register == "formal",
        )
        # Mode A identity is added only by the explicit Identity Intent route.
        # Mode B/C retain their configured application/character identity.
        final_answer = self.persona_renderer.render(
            generated["text"], include_identity=False
        )
        self.session_manager.add_turn(session_id, text, final_answer, metadata={
            "response_type": "normal", "speaker": speaker,
            "register": generated["register"],
            "semantic_result": semantic,
        })
        conflicts = self.core.knowledge_engine.detect_conflicts()
        return {
            "answer": final_answer, "text": final_answer,
            "metadata": {
                "register": generated["register"],
                "confidence_score": generated["confidence_score"],
                "reasoning_type": generated["reasoning_type"],
                "conflict_status": "conflicting" if conflicts or reasoning["reasoning_type"] == "conflicting" else "clear",
                "evidence": generated["evidence"],
                "semantic_status": semantic.get("status"),
                "session_id": session_id,
                "context_turns_used": len(snapshot.get("turns", [])),
                "negation": negation_metadata,
            },
            "semantic_result": semantic, "reasoning_result": reasoning,
            "generation": generated, "context_snapshot": snapshot,
        }
