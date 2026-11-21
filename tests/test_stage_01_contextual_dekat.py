"""Tests for the deliberately narrow Stage 1 contextual classifier for dekat."""

import hashlib
from pathlib import Path

import pytest

from ilis.language.foundation import classify_word_in_context


CASES = [
    ("B-DEKAT-001", "Rumah itu dekat.", "classified", ["adjektiva"]),
    ("B-DEKAT-002", "Rumah itu sangat dekat.", "needs_context", ["adjektiva", "preposisi"]),
    ("B-DEKAT-003", "Gedung itu cukup dekat.", "needs_context", ["adjektiva", "preposisi"]),
    ("B-DEKAT-004", "Mereka tinggal dekat sekolah.", "needs_context", ["adjektiva", "preposisi"]),
    ("B-DEKAT-005", "Kami duduk dekat pintu.", "classified", ["preposisi"]),
    ("B-DEKAT-006", "Kantor berada dekat stasiun.", "needs_context", ["adjektiva", "preposisi"]),
    ("B-DEKAT-007", "Dekat rumah itu ada taman.", "needs_context", ["adjektiva", "preposisi"]),
    ("B-DEKAT-008", "dekat rumah", "needs_context", ["adjektiva", "preposisi"]),
    ("B-DEKAT-009", "dekat", "needs_context", ["adjektiva", "preposisi"]),
    ("B-DEKAT-010", "Rumah dekat.", "needs_context", ["adjektiva", "preposisi"]),
    ("B-DEKAT-011", "Dia dekat dengan saya.", "needs_context", ["adjektiva", "preposisi"]),
    ("B-DEKAT-012", "Rumah itu dekat dan nyaman.", "needs_context", ["adjektiva", "preposisi"]),
    ("B-DEKAT-013", "Rumah itu dekat sekolah.", "needs_context", ["adjektiva", "preposisi"]),
    ("B-DEKAT-014", "Rumah itu sangat dekat sekolah.", "needs_context", ["adjektiva", "preposisi"]),
    ("B-DEKAT-015", "Rumah itu dekat sekolah dan pasar.", "needs_context", ["adjektiva", "preposisi"]),
    ("B-DEKAT-016", "Mereka tinggal dekat sekolah; rumahnya jauh.", "needs_context", ["adjektiva", "preposisi"]),
]


def _span(text, token="dekat", occurrence=0):
    start = -1
    search_from = 0
    for _ in range(occurrence + 1):
        start = text.casefold().index(token.casefold(), search_from)
        search_from = start + len(token)
    return {"start": start, "end": start + len(token)}


@pytest.mark.parametrize(
    ("case_id", "text", "expected_status", "expected_classes"),
    CASES,
    ids=[case[0] for case in CASES],
)
def test_sixteen_approved_dekat_cases(case_id, text, expected_status, expected_classes):
    result = classify_word_in_context(text, _span(text))
    assert result["input"] == text
    assert result["target"].casefold() == "dekat"
    assert result["status"] == expected_status
    assert result["classes"] == expected_classes
    assert result["reference_match"] == ["adjektiva", "preposisi"]
    if expected_status == "classified":
        assert result["evidence"]
    else:
        assert result["status"] == "needs_context"


def test_explicit_target_span_selects_second_occurrence_only():
    text = "Rumah itu dekat dan dekat."
    span = _span(text, occurrence=1)
    result = classify_word_in_context(text, span)
    assert result["target_span"] == span
    assert result["target"] == "dekat"
    assert result["status"] == "needs_context"


def test_unknown_target_returns_unknown_without_inventing_a_class():
    text = "Mereka tinggal sekolah."
    result = classify_word_in_context(text, _span(text, token="sekolah"))
    assert result["status"] == "unknown"
    assert result["classes"] == []
    assert result["reference_match"] == []


def test_registered_word_outside_classifier_scope_is_not_classified():
    text = "buku"
    result = classify_word_in_context(text, _span(text, token="buku"))
    assert result["status"] == "needs_context"
    assert result["classes"] == ["nomina"]
    assert "hanya mendisambiguasi kata dekat" in result["explanation"]


@pytest.mark.parametrize(
    "span",
    [
        {"start": -1, "end": 4},
        {"start": 0, "end": 0},
        {"start": 0, "end": 99},
        {"start": 0, "end": 4},
        {"start": True, "end": 5},
        {"start": 0, "end": 5.0},
        {},
    ],
)
def test_invalid_or_partial_target_span_is_rejected(span):
    with pytest.raises(ValueError):
        classify_word_in_context("dekat", span)


def test_non_string_text_and_non_mapping_span_are_rejected():
    with pytest.raises(TypeError):
        classify_word_in_context(None, {"start": 0, "end": 5})
    with pytest.raises(TypeError):
        classify_word_in_context("dekat", [0, 5])


def test_unicode_codepoint_offsets_are_respected():
    text = "🙂 Rumah itu dekat."
    span = _span(text)
    result = classify_word_in_context(text, span)
    assert text[span["start"]:span["end"]] == "dekat"
    assert result["status"] == "classified"
    assert result["classes"] == ["adjektiva"]


def test_target_matching_is_case_insensitive_and_preserves_original_text():
    text = "Rumah itu DEKAT."
    result = classify_word_in_context(text, _span(text))
    assert result["target"] == "DEKAT"
    assert result["input"] == text
    assert result["status"] == "classified"


def test_classifier_does_not_modify_reference_json():
    reference = (
        Path(__file__).resolve().parents[1]
        / "data/reference/tahap_01_fondasi/kata_dasar.json"
    )
    before = hashlib.sha256(reference.read_bytes()).hexdigest()
    classify_word_in_context("Kami duduk dekat pintu.", _span("Kami duduk dekat pintu."))
    after = hashlib.sha256(reference.read_bytes()).hexdigest()
    assert after == before
