"""Read-only foundation helpers for Stage 1 Indonesian references.

The JSON files under data/reference remain the sole source of truth.
This module deliberately does not cache, mutate, normalize, or promote them.
Each public operation reads the reference file afresh. There is no instance
initializer or in-memory cache; changes on disk are visible on the next call.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


_WORD_REFERENCE = Path(__file__).resolve().parents[3] / "data/reference/tahap_01_fondasi/kata_dasar.json"
_SPELLING_REFERENCE = Path(__file__).resolve().parents[3] / "data/reference/tahap_01_fondasi/aturan_ejaan.json"

_DAYS = (
    "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu",
)
_MONTHS = (
    "Januari", "Februari", "Maret", "April", "Mei", "Juni",
    "Juli", "Agustus", "September", "Oktober", "November", "Desember",
)
_DAY_ALTERNATION = "|".join(re.escape(value) for value in _DAYS)
_MONTH_ALTERNATION = "|".join(re.escape(value) for value in _MONTHS)
_MONTH_DATE_RE = re.compile(
    rf"(?<!\\w)(?P<day>0?[1-9]|[12][0-9]|3[01])[ \\t]+"
    rf"(?P<month>{_MONTH_ALTERNATION})(?!\\w)"
    rf"(?:[ \\t]+(?P<year>[0-9]{{4}})(?!\\w))?",
    re.IGNORECASE,
)
_WEEKDAY_BEFORE_DATE_RE = re.compile(
    rf"(?<!\\w)(?P<weekday>{_DAY_ALTERNATION})[ \\t]*,[ \\t]*$",
    re.IGNORECASE,
)
_DAY_TOKEN_RE = re.compile(
    rf"(?<!\\w)(?P<token>{_DAY_ALTERNATION})(?!\\w)",
    re.IGNORECASE,
)
_MONTH_TOKEN_RE = re.compile(
    rf"(?<!\\w)(?P<token>{_MONTH_ALTERNATION})(?!\\w)",
    re.IGNORECASE,
)
_DEFERRED_SPELLING_RULES = [
    "EJA-01", "EJA-02", "EJA-03",
    "EJA-05", "EJA-06", "EJA-07", "EJA-08", "EJA-09",
    "EJA-10", "EJA-11", "EJA-12",
]


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


def _spelling_finding(
    text: str,
    start: int,
    end: int,
    canonical: str,
    *,
    rule_id: str,
    in_explicit_date: bool,
    label: str,
) -> dict[str, Any]:
    """Build one finding whose span uses Python Unicode code-point offsets."""
    observed = text[start:end]
    if not in_explicit_date:
        status = "needs_context"
        suggestion = None
        explanation = (
            f"Kata {label} dikenali, tetapi konteks tanggal eksplisit belum cukup "
            "untuk memastikan fungsinya."
        )
    elif observed == canonical:
        status = "no_issue"
        suggestion = None
        explanation = (
            f"Kapitalisasi nama {label} sesuai pada pola tanggal eksplisit."
        )
    else:
        status = "issue"
        suggestion = canonical
        explanation = (
            f"Nama {label} pada pola tanggal eksplisit harus diawali huruf kapital."
        )
    return {
        "rule_id": rule_id,
        "span": {"start": start, "end": end},
        "observed": observed,
        "status": status,
        "suggestion": suggestion,
        "explanation": explanation,
    }


def _inspect_explicit_date_capitalization(text: str) -> list[dict[str, Any]]:
    """Inspect only month-after-day and weekday-comma-date patterns."""
    findings: list[dict[str, Any]] = []
    checked_spans: set[tuple[int, int]] = set()

    for date_match in _MONTH_DATE_RE.finditer(text):
        month_start, month_end = date_match.span("month")
        checked_spans.add((month_start, month_end))
        findings.append(
            _spelling_finding(
                text,
                month_start,
                month_end,
                next(month for month in _MONTHS if month.casefold() == date_match.group("month").casefold()),
                rule_id="EJA-04",
                in_explicit_date=True,
                label="bulan",
            )
        )

        prefix = text[:date_match.start()]
        weekday_match = _WEEKDAY_BEFORE_DATE_RE.search(prefix)
        if weekday_match:
            weekday_start, weekday_end = weekday_match.span("weekday")
            checked_spans.add((weekday_start, weekday_end))
            findings.append(
                _spelling_finding(
                    text,
                    weekday_start,
                    weekday_end,
                    next(day for day in _DAYS if day.casefold() == weekday_match.group("weekday").casefold()),
                    rule_id="EJA-04",
                    in_explicit_date=True,
                    label="hari",
                )
            )

    # Recognized day/month words outside an approved date pattern are not
    # silently ignored: they are surfaced as needs_context, never corrected.
    for token_re, vocabulary, label in (
        (_DAY_TOKEN_RE, _DAYS, "hari"),
        (_MONTH_TOKEN_RE, _MONTHS, "bulan"),
    ):
        for token_match in token_re.finditer(text):
            start, end = token_match.span("token")
            if (start, end) in checked_spans:
                continue
            canonical = next(
                item for item in vocabulary
                if item.casefold() == token_match.group("token").casefold()
            )
            findings.append(
                _spelling_finding(
                    text,
                    start,
                    end,
                    canonical,
                    rule_id="EJA-04",
                    in_explicit_date=False,
                    label=label,
                )
            )

    return sorted(findings, key=lambda finding: finding["span"]["start"])


def inspect_spelling(text: str, path: str | Path = _SPELLING_REFERENCE) -> dict[str, Any]:
    """Conservatively inspect EJA-04 capitalization in explicit date patterns.

    The original input is always preserved. Only a day immediately before a
    comma and an explicit numeric day/month date, or a month following a valid
    numeric day, can produce issue/no_issue. Other recognized day/month tokens
    produce needs_context. All other spelling rules remain deferred.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    rules = load_spelling_rules(path)
    findings = _inspect_explicit_date_capitalization(text)
    return {
        "status": "partial",
        "input": text,
        "coverage": {
            "checked_rules": ["EJA-04"],
            "deferred_rules": list(_DEFERRED_SPELLING_RULES),
            "complete": False,
        },
        "findings": findings,
        "rules_available": len(rules),
        "rules": rules,
        "message": (
            "Pemeriksaan parsial hanya mencakup kapitalisasi nama hari dan bulan "
            "pada pola tanggal eksplisit yang didukung. Aturan ejaan lainnya "
            "belum didukung; masukan asli tidak diubah."
        ),
    }
