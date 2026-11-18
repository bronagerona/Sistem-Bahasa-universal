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
        meaning = self._extract_meaning(reasoning_result)
        uncertain = self._is_uncertain(reasoning_result)
        sentence = self.sentence_builder.build(
            meaning,
            register=selected_register,
            uncertainty=uncertain,
            context=context,
        )
        return {
            "text": sentence,
            "register": selected_register,
            "meaning": meaning,
            "reasoning_type": reasoning_result.get("reasoning_type", "unknown"),
            "confidence_score": reasoning_result.get("confidence_score"),
            "uncertainty_preserved": uncertain,
            "evidence": list(reasoning_result.get("evidence") or []),
            "session_id": context.get("session_id") if context else None,
        }

    @classmethod
    def _extract_meaning(cls, result: dict[str, Any]) -> dict[str, Any]:
        supplied = result.get("meaning")
        if isinstance(supplied, dict):
            return dict(supplied)
        reasoning_type = result.get("reasoning_type", "unknown")
        conclusion = result.get("conclusion", "")
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
