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
        if not isinstance(meaning, dict):
            raise TypeError("meaning must be a dictionary")
        if register not in self.REGISTERS:
            raise ValueError(f"register must be one of {sorted(self.REGISTERS)}")

        # Register "unknown" is normalized by LanguageGenerator to "formal"
        # before build(); this builder accepts only concrete register values.
        kind = meaning.get("kind", "statement")
        if kind == "burn_risk":
            sentence = self._burn_risk(meaning, register, uncertainty)
        elif kind == "unknown":
            sentence = self._unknown(meaning, register)
        elif kind == "conflicting":
            sentence = self._conflicting(meaning, register)
        elif kind == "question":
            sentence = self._question(meaning, register, uncertainty)
        elif kind == "command":
            sentence = self._command(meaning, register)
        elif kind == "dragon_bell":
            sentence = self._dragon_bell(meaning, register, uncertainty)
        else:
            sentence = self._generic(meaning, register, uncertainty)

        # Only an explicitly supplied grounded referent may personalize wording.
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
                core += f" karena berbahan {material} dan terkena {source}"
            return core + (" lho" if uncertainty else "")

        core = f"Kayaknya {target} bisa kebakaran"
        if material:
            core += f" gara-gara bahannya {material} kena {source}"
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
    def _question(meaning: dict[str, Any], register: str, uncertainty: bool) -> str:
        actor = SentenceBuilder._phrase(meaning.get("actor"), "hal itu")
        predicate = SentenceBuilder._phrase(meaning.get("predicate"), "terjadi")
        patient = SentenceBuilder._phrase(meaning.get("patient"), "")
        modality = meaning.get("modality")
        if predicate in {"membakar", "bakar"} and modality == "ability":
            core = f"{actor} bisa {predicate} {patient}".strip()
        else:
            core = " ".join(part for part in (actor, predicate, patient) if part)
        if uncertainty:
            if register == "formal": return f"Ya, kemungkinan {core}"
            if register == "informal": return f"Iya, kayaknya {core}"
            return f"Iya, kayaknya {core} sih"
        if register == "formal": return f"Ya, berdasarkan fakta yang tersedia, {core}"
        if register == "informal": return f"Iya, {core}"
        return f"Iya, {core} kok"

    @staticmethod
    def _command(meaning: dict[str, Any], register: str) -> str:
        predicate = SentenceBuilder._phrase(meaning.get("predicate"), "")
        patient = SentenceBuilder._phrase(meaning.get("patient"), "")
        if predicate in {"bunyikan", "bunyi"} and patient == "lonceng":
            if register == "formal": return "Baik, lonceng akan dibunyikan"
            if register == "informal": return "Oke, loncengnya akan dibunyikan"
            return "Gas, loncengnya kita bunyiin"
        proposition = SentenceBuilder._phrase(meaning.get("proposition"), "perintah tersebut")
        if register == "formal": return f"Baik, perintah {proposition} akan diproses"
        if register == "informal": return f"Oke, {proposition} akan dijalankan"
        return f"Siap, {proposition} kita jalanin"

    @staticmethod
    def _dragon_bell(meaning: dict[str, Any], register: str, uncertainty: bool) -> str:
        if register == "formal":
            core = "Lonceng dapat menakuti naga karena menghasilkan suara keras yang ditakuti naga"
            return f"Ada kemungkinan bahwa {core}" if uncertainty else core
        if register == "informal":
            core = "Lonceng bisa bikin naga takut karena bunyinya keras"
            return f"Kayaknya {core} lho" if uncertainty else core
        core = "Lonceng bisa bikin naga ciut gara-gara suaranya kenceng"
        return f"Kayaknya {core} deh" if uncertainty else core
    @staticmethod
    def _generic(meaning: dict[str, Any], register: str, uncertainty: bool) -> str:
        proposition = SentenceBuilder._phrase(
            meaning.get("proposition") or meaning.get("conclusion"),
            "Informasi belum tersedia",
        )
        proposition = re.sub(r"\s+", " ", proposition).strip().rstrip(".!?")
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
        sentence = re.sub(r"\s+", " ", sentence).strip()
        if not sentence:
            return sentence
        return sentence[0].upper() + sentence[1:].rstrip(".!?") + "."
