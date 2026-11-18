"""Text-chat adapter over the existing ILIS pipeline."""

from __future__ import annotations

import re
from typing import Any

from ilis.interfaces.ilis_core import ILISCore


class ChatbotAdapter:
    """Run semantic analysis, context storage, reasoning, then generation."""

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
        match = self._TOUCHES_WOODEN_HOUSE.fullmatch(text)
        if match:
            reasoning = self.core.reasoning_engine.infer_burn_risk(
                match.group("source").casefold(), match.group("target").casefold()
            )
        else:
            reasoning = {
                "conclusion": "Belum cukup data untuk menyusun kesimpulan dari kalimat ini.",
                "confidence_score": 0.0, "evidence": [],
                "reasoning_type": "unknown",
                "reasons": ["Pola kalimat ini belum didukung adapter chatbot V1."],
                "uncertainty": "Diperlukan pola semantik atau aturan yang didukung.",
            }
        generated = self.core.language_generator.generate(
            reasoning, register=register, semantic_result=semantic,
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
