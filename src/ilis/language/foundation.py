"""Read-only foundation helpers for Stage 1 Indonesian references.

The JSON files under data/reference remain the sole source of truth.
This module deliberately does not cache, mutate, normalize, or promote them.
Each public operation reads the reference file afresh. There is no instance
initializer or in-memory cache; changes on disk are visible on the next call.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


_WORD_REFERENCE = Path(__file__).resolve().parents[3] / "data/reference/tahap_01_fondasi/kata_dasar.json"
_SPELLING_REFERENCE = Path(__file__).resolve().parents[3] / "data/reference/tahap_01_fondasi/aturan_ejaan.json"


class ReferenceFormatError(ValueError):
    """Raised when a Stage 1 reference file does not match its expected shape."""


def _read_json(path: str | Path) -> dict[str, Any]:
    """Read a JSON reference afresh; no cache and no write path are provided."""
    source = Path(path)
    try:
        with source.open("r", encoding="utf-8") as stream:
            payload = json.load(stream)
    except (OSError, json.JSONDecodeError) as exc:
        raise ReferenceFormatError(f"Unable to read reference JSON: {source}") from exc
    if not isinstance(payload, dict):
        raise ReferenceFormatError("Reference root must be a JSON object.")
    if payload.get("status") != "referensi":
        raise ReferenceFormatError("Stage 1 source must remain status 'referensi'.")
    return payload


def load_word_reference(path: str | Path = _WORD_REFERENCE) -> list[dict[str, Any]]:
    """Return validated lexical entries from the read-only reference file."""
    payload = _read_json(path)
    entries = payload.get("daftar")
    if not isinstance(entries, list):
        raise ReferenceFormatError("Word reference must contain a 'daftar' array.")
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise ReferenceFormatError(f"Word entry {index} must be an object.")
        if not isinstance(entry.get("entri"), str) or not entry["entri"].strip():
            raise ReferenceFormatError(f"Word entry {index} has no valid 'entri'.")
        kinds = entry.get("jenis")
        if not isinstance(kinds, list) or not kinds or not all(
            isinstance(kind, str) and kind for kind in kinds
        ):
            raise ReferenceFormatError(f"Word entry {index} has invalid 'jenis'.")
    return entries


def lookup_word(word: str, path: str | Path = _WORD_REFERENCE) -> dict[str, Any]:
    """Look up an exact reference form without guessing or morphological expansion."""
    if not isinstance(word, str):
        raise TypeError("word must be a string")
    query = word.strip().casefold()
    if not query:
        return {"status": "unknown", "query": query, "classes": [], "entry": None}

    matches = [
        entry for entry in load_word_reference(path)
        if entry["entri"].casefold() == query
    ]
    if not matches:
        return {
            "status": "unknown",
            "query": query,
            "classes": [],
            "entry": None,
            "message": "Bentuk ini belum tercantum dalam referensi Tahap 1.",
        }

    # Duplicate exact forms are not expected, but combine categories conservatively.
    classes = sorted({kind for entry in matches for kind in entry["jenis"]})
    status = "found" if len(classes) == 1 else "ambiguous"
    return {
        "status": status,
        "query": query,
        "classes": classes,
        "entry": matches[0] if len(matches) == 1 else matches,
        "message": (
            "Kelas kata tercantum dalam referensi."
            if status == "found"
            else "Bentuk ini memiliki lebih dari satu kelas; konteks diperlukan."
        ),
    }


def load_spelling_rules(path: str | Path = _SPELLING_REFERENCE) -> list[dict[str, Any]]:
    """Return spelling rules from the read-only reference file."""
    payload = _read_json(path)
    rules = payload.get("daftar_aturan")
    if not isinstance(rules, list):
        raise ReferenceFormatError("Spelling reference must contain 'daftar_aturan'.")
    for index, rule in enumerate(rules):
        if not isinstance(rule, dict) or not all(
            isinstance(rule.get(key), str) and rule[key].strip()
            for key in ("aturan", "contoh_benar", "contoh_salah", "penjelasan")
        ):
            raise ReferenceFormatError(f"Spelling rule {index} is incomplete.")
    return rules


def inspect_spelling(text: str, path: str | Path = _SPELLING_REFERENCE) -> dict[str, Any]:
    """Return the available spelling guidance without silently rewriting input.

    The current reference contains rule descriptions and examples, not a complete
    correction engine. Therefore this function reports the rule inventory and
    explicitly marks the input as not fully assessed rather than inventing fixes.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    rules = load_spelling_rules(path)
    return {
        "status": "reference_guidance_only",
        "input": text,
        "findings": [],
        "rules_available": len(rules),
        "rules": rules,
        "message": (
            "Referensi aturan tersedia, tetapi pemeriksaan menyeluruh dan "
            "koreksi otomatis belum didukung. Masukan tidak diubah."
        ),
    }
