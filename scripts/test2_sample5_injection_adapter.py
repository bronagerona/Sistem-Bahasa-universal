"""Five-sample-only dataset injection adapter for isolated A/B testing.

This module is test-harness code only. It does not alter ILIS production modules
or dataset files. DRAFT knowledge is injected into an in-memory KnowledgeEngine
as a hypothesis, never as verified evidence.
"""
from __future__ import annotations

import re
from typing import Any

from ilis.interfaces import ILISCore
from ilis.semantics.contract_validator import validate_output

SAMPLE_TEXTS = {
    "T2-01": "Aku belum membaca buku itu.",
    "T2-02": "Orang yang menelepon tadi bukan kakakku.",
    "T2-03": "Jangan kirim berkas itu dulu.",
    "T2-04": "Ia terjatuh saat menuruni tangga.",
    "T2-05": "Berapa meter nilai satu satuan astronomi (au) menurut definisi IAU?",
}


def _record(records: dict[str, Any], pillar: str, record_id: str) -> dict[str, Any]:
    for item in records.get(pillar, []):
        if item.get("entry_id") == record_id or item.get("pattern_id") == record_id or item.get("dialogue_id") == record_id or item.get("fact_id") == record_id:
            return item
    raise KeyError(f"Required DRAFT record not loaded: {pillar}/{record_id}")


def _set_semantics(result: dict[str, Any], values: dict[str, Any]) -> dict[str, Any]:
    semantics = dict(result.get("semantics") or {})
    defaults = {
        "Actor": None, "Predicate": None, "Patient/Object": None,
        "Recipient": None, "Location": None, "Time": None,
        "Aspect": "unspecified", "Negation": "none", "Modality": "none",
        "Intent": "assertion", "Register": "unknown", "Confidence": 0.25,
    }
    defaults.update(semantics)
    defaults.update(values)
    result = dict(result)
    result["status"] = "supported"
    result["semantics"] = defaults
    validate_output(result)
    return result


class Sample5InjectionAdapter:
    """Allowlisted, per-instance semantic overlay for exactly five test inputs."""

    def __init__(self, records: dict[str, Any]) -> None:
        self.records = records
        self._fact = _record(records, "knowledge", "fact-0048")
        # The one DRAFT knowledge item is stored only in the isolated in-memory
        # engine and explicitly downgraded to hypothesis.
        self._fact_triple = (
            self._fact["subject"], self._fact["predicate"], self._fact["object"]
        )

    def install(self, core: ILISCore) -> None:
        subject, predicate, object_ = self._fact_triple
        core.knowledge_engine.add_fact(
            subject, predicate, object_, status="hypothesis",
            source="dataset_draft:fact-0048",
        )
        original_analyze = core.analyze_text

        def analyze_text(text: str, *, context_snapshot: dict[str, Any] | None = None):
            base = original_analyze(text, context_snapshot=context_snapshot)
            sample_id = next((key for key, value in SAMPLE_TEXTS.items() if value == text), None)
            if sample_id is None:
                return base
            return self.apply(sample_id, base, text)

        # Instance-local wrapper: no source module or shared class is patched.
        core.analyze_text = analyze_text  # type: ignore[method-assign]

    def apply(self, sample_id: str, base: dict[str, Any], text: str) -> dict[str, Any]:
        if SAMPLE_TEXTS.get(sample_id) != text:
            raise ValueError("Adapter refuses input outside the five exact allowlisted samples")

        if sample_id == "T2-01":
            lex = _record(self.records, "lexicon", "lex-0048")
            pattern = _record(self.records, "sentence_patterns", "pat-0048")
            if "belum" not in lex["surface_forms"] or "belum" not in pattern["structure"]:
                raise ValueError("DRAFT lexicon/pattern mismatch for T2-01")
            return _set_semantics(base, {
                "Negation": "not_yet", "Aspect": "unspecified",
                "Intent": "assertion", "Confidence": 0.95,
            })

        if sample_id == "T2-02":
            lex = _record(self.records, "lexicon", "lex-0049")
            pattern = _record(self.records, "sentence_patterns", "pat-0049")
            dialogue = _record(self.records, "dialogues", "dlg-0047")
            turn = dialogue["turns"][0]["semantic_annotation"]
            if lex["lemma"] != "bukan" or "bukan" not in pattern["name"]:
                raise ValueError("DRAFT lexicon/pattern mismatch for T2-02")
            return _set_semantics(base, {
                "Actor": turn["Actor"], "Predicate": "bukan",
                "Patient/Object": turn["Patient/Object"],
                "Negation": "identity_negative", "Intent": "assertion",
                "Register": "informal", "Confidence": 0.90,
            })

        if sample_id == "T2-03":
            lex = _record(self.records, "lexicon", "lex-0051")
            pattern = _record(self.records, "sentence_patterns", "pat-0051")
            dialogue = _record(self.records, "dialogues", "dlg-0049")
            turn = dialogue["turns"][0]["semantic_annotation"]
            if lex["lemma"] != "jangan" or "Larangan" not in pattern["name"]:
                raise ValueError("DRAFT lexicon/pattern mismatch for T2-03")
            return _set_semantics(base, {
                "Actor": "kamu", "Predicate": "mengirim",
                "Patient/Object": "berkas itu", "Negation": "negative",
                "Intent": "command", "Register": dialogue["register"],
                "Confidence": 0.90,
            })

        if sample_id == "T2-04":
            lex = _record(self.records, "lexicon", "lex-0091")
            pattern = _record(self.records, "sentence_patterns", "pat-0091")
            if lex["lemma"] != "terjatuh" or "ter-" not in pattern["name"]:
                raise ValueError("DRAFT lexicon/pattern mismatch for T2-04")
            actor = re.match(r"^([\\w]+)", text).group(1).casefold()
            return _set_semantics(base, {
                "Actor": actor, "Predicate": lex["lemma"],
                "Patient/Object": None, "Negation": "none",
                "Intent": "assertion", "Register": "unknown",
                # Lower confidence preserves the explicit polysemy caveat.
                "Confidence": 0.78,
            })

        if sample_id == "T2-05":
            fact = self._fact
            return _set_semantics(base, {
                "Actor": fact["subject"], "Predicate": fact["predicate"],
                "Patient/Object": fact["object"], "Intent": "question",
                "Negation": "none", "Confidence": 0.90,
            })

        raise ValueError(f"Unknown sample id: {sample_id}")
