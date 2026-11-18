"""Text-chat adapter over the existing ILIS pipeline."""

from __future__ import annotations

import re
from typing import Any

from ilis.interfaces.ilis_core import ILISCore


class ChatbotAdapter:
    """Run semantic analysis, reasoning, then register-aware generation."""

    _TOUCHES_WOODEN_HOUSE = re.compile(
        r"^\s*(?P<source>api)\s+menyentuh\s+"
        r"(?P<target>rumah)\s+(?P<material>kayu)\s*[.!?]?\s*$",
        re.IGNORECASE,
    )

    def __init__(self, core: ILISCore) -> None:
        if not isinstance(core, ILISCore):
            raise TypeError("core must be an ILISCore instance")
        self.core = core

    def respond(
        self, text: str, session_id: str, *, speaker: str = "user",
        register: str | None = None,
    ) -> dict[str, Any]:
        if not isinstance(text, str) or not text.strip():
            raise ValueError("text must be a non-empty string")

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

        effective_register = register
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
            session_id=session_id,
        )
        conflicts = self.core.knowledge_engine.detect_conflicts()
        return {
            "answer": generated["text"],
            "text": generated["text"],
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
