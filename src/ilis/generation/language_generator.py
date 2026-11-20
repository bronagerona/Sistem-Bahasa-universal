"""Deterministic meaning-to-Indonesian generation; no LLM/model AI."""

from __future__ import annotations

import re
from typing import Any

from ilis.cognition.context_engine import ContextEngine
from ilis.generation.sentence_builder import SentenceBuilder


class LanguageGenerator:
    """Generate register-aware Indonesian from reasoning and semantic inputs."""

    _BURN_PATTERN = re.compile(
        r"(?P<source>[\w-]+)\s+yang\s+menyambar\s+"
        r"(?P<target>[\w-]+)\s+berbahan\s+(?P<material>[\w-]+)",
        re.IGNORECASE,
    )

    def __init__(
        self,
        context_engine: ContextEngine | None = None,
        sentence_builder: SentenceBuilder | None = None,
    ) -> None:
        if context_engine is not None and not isinstance(context_engine, ContextEngine):
            raise TypeError("context_engine must be a ContextEngine instance")
        if sentence_builder is not None and not isinstance(sentence_builder, SentenceBuilder):
            raise TypeError("sentence_builder must be a SentenceBuilder instance")
        self.context_engine = context_engine
        self.sentence_builder = sentence_builder or SentenceBuilder()

    def generate(
        self,
        reasoning_result: dict[str, Any],
        *,
        register: str | None = None,
        semantic_result: dict[str, Any] | None = None,
        context: dict[str, Any] | None = None,
        session_id: str | None = None,
        polite: bool = False,
    ) -> dict[str, Any]:
        """Render reasoning using register metadata and optional session context."""
        if not isinstance(reasoning_result, dict):
            raise TypeError("reasoning_result must be a dictionary")
        if register is not None and register not in SentenceBuilder.REGISTERS:
            raise ValueError(f"register must be one of {sorted(SentenceBuilder.REGISTERS)}")
        if semantic_result is not None and not isinstance(semantic_result, dict):
            raise TypeError("semantic_result must be a dictionary")
        if context is not None and not isinstance(context, dict):
            raise TypeError("context must be a dictionary")
        if session_id is not None:
            if self.context_engine is None:
                raise ValueError("ContextEngine is required when session_id is supplied")
            context = self.context_engine.get_context(session_id)

        selected_register = self._select_register(register, semantic_result, context)
        reasoning_type = reasoning_result.get("reasoning_type", "unknown")
        semantics = (semantic_result or {}).get("semantics") or {}
        is_greeting = (
            isinstance(semantics, dict)
            and (semantic_result or {}).get("status") == "supported"
            and semantics.get("Intent") == "greeting"
        )
        evidence = reasoning_result.get("evidence", [])
        conclusion = reasoning_result.get("conclusion", "")
        is_dataset_fact_answer = (
            reasoning_type in {"verified_inference", "hypothetical_inference"}
            and isinstance(evidence, list)
            and any(
                isinstance(item, str) and re.fullmatch(r"fact-\d{4}", item)
                for item in evidence
            )
            and isinstance(conclusion, str)
            and bool(conclusion.strip())
        )
        concept_status = reasoning_type if reasoning_type in {
            "concept_inference_known",
            "concept_inference_partial",
            "concept_inference_unknown",
        } else None
        meaning = self._extract_meaning(reasoning_result, semantic_result)
        uncertain = self._is_uncertain(reasoning_result)
        if is_greeting:
            meaning = {"kind": "greeting"}
            uncertain = False
            if selected_register == "formal":
                sentence = "Halo! Saya siap membantu. Bagaimana kabar Anda?"
            elif selected_register == "informal":
                sentence = "Halo! Aku siap bantu. Apa kabar kamu?"
            else:
                sentence = "Hai! Siap bantu, nih. Apa kabar?"
        elif is_dataset_fact_answer:
            # Dataset fact conclusions already contain the exact record value
            # and qualifiers. Do not pass them through _phrase(), which
            # case-folds text and would alter source values such as "Bumi".
            meaning = {"kind": "statement", "proposition": conclusion}
            uncertain = self._is_uncertain(reasoning_result)
            sentence = conclusion.strip()
        elif concept_status == "concept_inference_unknown":
            meaning = {"kind": "unknown", "target": "pertanyaanmu"}
            uncertain = True
            sentence = "Belum cukup informasi untuk memastikan jawaban atas pertanyaanmu."
        else:
            if concept_status == "concept_inference_partial":
                uncertain = True
            if reasoning_type == "assertion":
                meaning = {"kind": "assertion_acknowledgement"}
                uncertain = False
                if selected_register == "formal":
                    sentence = (
                        "Baik, saya telah memahami pernyataan yang Anda sampaikan"
                        if polite
                        else "Baik, saya sudah memahami pernyataanmu"
                    )
                elif selected_register == "informal":
                    sentence = "Oke, aku paham pernyataanmu"
                else:
                    sentence = "Oke, nangkep pernyataanmu"
            else:
                sentence = self.sentence_builder.build(
                    meaning,
                    register=selected_register,
                    uncertainty=uncertain,
                    context=context,
                    polite=polite,
                )
            if concept_status == "concept_inference_partial":
                sentence = (
                    sentence.rstrip(".!?")
                    + ". Informasi belum lengkap, ini hanya dugaan."
                )
        return {
            "text": sentence,
            "register": selected_register,
            "meaning": meaning,
            "reasoning_type": "greeting" if is_greeting else reasoning_result.get("reasoning_type", "unknown"),
            "confidence_score": reasoning_result.get("confidence_score"),
            "uncertainty_preserved": uncertain,
            "evidence": list(reasoning_result.get("evidence") or []),
            "session_id": context.get("session_id") if context else None,
        }

    @classmethod
    def _extract_meaning(cls, result: dict[str, Any], semantic_result: dict[str, Any] | None = None) -> dict[str, Any]:
        supplied = result.get("meaning")
        if isinstance(supplied, dict):
            return dict(supplied)
        reasoning_type = result.get("reasoning_type", "unknown")
        conclusion = result.get("conclusion", "")
        evidence = result.get("evidence", [])
        if (
            reasoning_type in {"verified_inference", "hypothetical_inference"}
            and isinstance(evidence, list)
            and any(
                isinstance(item, str) and re.fullmatch(r"fact-\d{4}", item)
                for item in evidence
            )
        ):
            return {"kind": "statement", "proposition": conclusion}
        if isinstance(conclusion, str) and "lonceng" in conclusion.casefold() and "naga" in conclusion.casefold() and any(marker in conclusion.casefold() for marker in ("takut", "menakuti")):
            return {"kind": "dragon_bell", "proposition": conclusion}
        if semantic_result and semantic_result.get("status") == "supported":
            semantics = semantic_result.get("semantics")
            if isinstance(semantics, dict):
                intent = semantics.get("Intent")
                if intent == "question":
                    if reasoning_type == "conflicting":
                        return {"kind": "conflicting", "target": semantics.get("Patient/Object") or semantics.get("Actor")}
                    if reasoning_type == "unknown":
                        return {"kind": "unknown", "target": semantics.get("Patient/Object") or semantics.get("Actor")}
                    return {"kind": "question", "actor": semantics.get("Actor"), "predicate": semantics.get("Predicate"), "patient": semantics.get("Patient/Object"), "modality": semantics.get("Modality"), "proposition": conclusion}
                if intent == "command":
                    return {"kind": "command", "predicate": semantics.get("Predicate"), "patient": semantics.get("Patient/Object"), "proposition": conclusion}
        if reasoning_type == "command":
            return {"kind": "command", "proposition": conclusion}
        if not isinstance(conclusion, str):
            conclusion = ""
        if reasoning_type == "conflicting":
            return {"kind": "conflicting", "target": cls._find_target(conclusion)}
        if reasoning_type == "unknown":
            return {"kind": "unknown", "target": cls._find_target(conclusion)}
        match = cls._BURN_PATTERN.search(conclusion)
        if match:
            return {
                "kind": "burn_risk",
                "source": match.group("source"),
                "target": match.group("target"),
                "material": match.group("material"),
                "proposition": conclusion,
            }
        return {"kind": "statement", "proposition": conclusion}

    @staticmethod
    def _select_register(
        register: str | None,
        semantic_result: dict[str, Any] | None,
        context: dict[str, Any] | None,
    ) -> str:
        candidate = register
        if candidate is None and semantic_result:
            semantics = semantic_result.get("semantics") or {}
            candidate = semantics.get("Register") if isinstance(semantics, dict) else None
        if candidate is None and context:
            session = context.get("session") or {}
            metadata = session.get("metadata") if isinstance(session, dict) else {}
            if isinstance(metadata, dict):
                candidate = metadata.get("register")
        if candidate in {"formal", "informal", "slang"}:
            return candidate
        # Missing or unknown Semantic/session register defaults to formal.
        return "formal"

    @staticmethod
    def _is_uncertain(result: dict[str, Any]) -> bool:
        reasoning_type = result.get("reasoning_type", "unknown")
        confidence = result.get("confidence_score")
        uncertainty_note = result.get("uncertainty")
        conclusion = result.get("conclusion", "")
        uncertainty_words = ("mungkin", "kemungkinan", "berpotensi", "potensi")
        has_note = isinstance(uncertainty_note, str) and bool(uncertainty_note.strip())
        has_word = isinstance(conclusion, str) and any(
            word in conclusion.casefold() for word in uncertainty_words
        )
        return (
            reasoning_type in {"hypothetical_inference", "verified_inference"}
            and (has_note or has_word or (isinstance(confidence, (int, float)) and confidence < 1))
        )

    @staticmethod
    def _find_target(conclusion: str) -> str:
        match = re.search(
            r"(?:apakah|tentang|mengenai)\s+([\w-]+)",
            conclusion,
            re.IGNORECASE,
        )
        return match.group(1) if match else "hal itu"
