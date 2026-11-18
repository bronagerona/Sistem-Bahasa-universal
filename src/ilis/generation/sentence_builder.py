"""Dynamic sentence composition from structured meaning and discourse context."""

from __future__ import annotations

import re
from typing import Any


class SentenceBuilder:
    """Compose Indonesian sentences from meaning components, not stored replies."""

    REGISTERS = frozenset({"formal", "informal", "slang"})

    def build(
        self,
        meaning: dict[str, Any],
        *,
        register: str = "formal",
        uncertainty: bool = True,
        context: dict[str, Any] | None = None,
    ) -> str:
        """Build a sentence from a normalized meaning representation."""
        if register not in self.REGISTERS:
            raise ValueError(f"register must be one of {sorted(self.REGISTERS)}")
        if not isinstance(meaning, dict):
            raise TypeError("meaning must be a dictionary")

        kind = meaning.get("kind", "statement")
        if kind == "burn_risk":
            sentence = self._burn_risk(meaning, register, uncertainty)
        elif kind == "unknown":
            sentence = self._unknown(meaning, register)
        elif kind == "conflicting":
            sentence = self._conflicting(meaning, register)
        else:
            sentence = self._generic(meaning, register, uncertainty)

        # Context may resolve a demonstrative only when the caller explicitly
        # supplies a grounded referent. We never infer facts from chat history.
        referent = meaning.get("contextual_referent")
        if isinstance(referent, str) and referent.strip():
            sentence = sentence.replace("{referent}", referent.strip())
        return self._finish(sentence)

    @staticmethod
    def _burn_risk(meaning: dict[str, Any], register: str, uncertainty: bool) -> str:
        target = SentenceBuilder._phrase(meaning.get("target"), "objek tersebut")
        material = SentenceBuilder._phrase(meaning.get("material"), "")
        source = SentenceBuilder._phrase(meaning.get("source"), "sumber panas")
        if register == "formal":
            core = f"Ada kemungkinan {target} akan terbakar"
            if material:
                core += f" karena terbuat dari {material} dan terpapar {source}"
            return core
        if register == "informal":
            core = f"Kayaknya {target} bisa kebakaran"
            if material:
                core += f karena berbahan {material} dan terkena {source}"
            return core + (" lho" if uncertainty else "")
        core = f"Kayaknya {target} bisa kebakaran"
        if material:
            core += f gara-gara bahannya {material} kena {source}"
        return core + (" deh" if uncertainty else "")

    @staticmethod
    def _unknown(meaning: dict[str, Any], register: str) -> str:
        subject = SentenceBuilder._phrase(meaning.get("target"), "hal itu")
        if register == "formal":
            return f"Belum cukup informasi untuk memastikan apakah {subject} dapat terjadi"
        if register == "informal":
            return f"Belum ada cukup info buat memastikan apakah {subject} bisa terjadi"
        return f"Belum cukup info buat tahu {subject} bakal terjadi atau nggak"

    @staticmethod
    def _conflicting(meaning: dict[str, Any], register: str) -> str:
        subject = SentenceBuilder._phrase(meaning.get("target"), "hal itu")
        if register == "formal":
            return f"Ada informasi yang saling bertentangan mengenai {subject}"
        if register == "informal":
            return f"Informasi soal {subject} masih saling bertentangan"
        return f"Info soal {subject} masih beda-beda"

    @staticmethod
    def _generic(meaning: dict[str, Any], register: str, uncertainty: bool) -> str:
        proposition = SentenceBuilder._phrase(
            meaning.get("proposition") or meaning.get("conclusion"),
            "Informasi belum tersedia",
        )
        proposition = re.sub(r"\\s+", " ", proposition).strip().rstrip(".!?")
        if uncertainty and not any(
            marker in proposition.casefold()
            for marker in ("mungkin", "kemungkinan", "berpotensi", "belum cukup")
        ):
            if register == "formal":
                proposition = f"Ada kemungkinan bahwa {proposition[:1].lower() + proposition[1:]}"
            else:
                proposition = f"Kayaknya {proposition[:1].lower() + proposition[1:]}"
        return proposition

    @staticmethod
    def _phrase(value: Any, fallback: str) -> str:
        if not isinstance(value, str) or not value.strip():
            return fallback
        return " ".join(value.casefold().split())

    @staticmethod
    def _finish(sentence: str) -> str:
        sentence = re.sub(r"\\s+", " ", sentence).strip()
        if not sentence:
            return sentence
        return sentence[0].upper() + sentence[1:].rstrip(".!?") + "."
