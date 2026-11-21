"""Tests for the isolated, read-only Stage 1 foundation module."""

import json

import pytest

from ilis.language.foundation import (
    ReferenceFormatError,
    inspect_spelling,
    load_spelling_rules,
    load_word_reference,
    lookup_word,
)


def test_word_reference_is_read_only_reference_with_152_entries():
    entries = load_word_reference()
    assert len(entries) == 152
    assert all(entry["bentuk_dasar"] is True for entry in entries)


@pytest.mark.parametrize(
    ("word", "expected"),
    [
        ("buku", "nomina"),
        ("makan", "verba"),
        ("baik", "adjektiva"),
        ("sering", "adverbia"),
        ("aku", "pronomina"),
        ("dua", "numeralia"),
        ("dari", "preposisi"),
        ("karena", "konjungsi"),
        ("aduh", "interjeksi"),
        ("sang", "artikula"),
        ("dong", "partikel"),
    ],
)
def test_lookup_returns_registered_class(word, expected):
    result = lookup_word(word)
    assert result["status"] == "found"
    assert result["classes"] == [expected]


def test_lookup_is_case_insensitive_and_trims_whitespace():
    assert lookup_word("  BUKU ")["classes"] == ["nomina"]


def test_ambiguous_form_is_not_forced_into_one_class():
    result = lookup_word("dekat")
    assert result["status"] == "ambiguous"
    assert result["classes"] == ["adjektiva", "preposisi"]


@pytest.mark.parametrize("word", ["kah", "siswa", "kata-yang-belum-terdaftar"])
def test_unlisted_form_is_unknown_not_declared_non_indonesian(word):
    result = lookup_word(word)
    assert result["status"] == "unknown"
    assert result["classes"] == []
    assert "belum tercantum" in result["message"]


def test_bound_particle_is_registered_only_with_its_hyphen():
    assert lookup_word("-kah")["classes"] == ["partikel"]
    assert lookup_word("kah")["status"] == "unknown"


def test_compound_numeral_is_preserved_as_reference_entry():
    result = lookup_word("lima belas")
    assert result["status"] == "found"
    assert result["classes"] == ["numeralia"]
    assert "majemuk" in result["entry"]["catatan"]


def test_spelling_rules_are_loaded_without_promoting_reference():
    rules = load_spelling_rules()
    assert len(rules) == 12


def test_spelling_inspection_never_rewrites_input_or_claims_full_correction():
    original = "budi pergi ke bandung"
    result = inspect_spelling(original)
    assert result["input"] == original
    assert result["status"] == "reference_guidance_only"
    assert result["findings"] == []
    assert "belum didukung" in result["message"]


def test_loader_rejects_non_reference_status(tmp_path):
    source = tmp_path / "words.json"
    source.write_text(
        json.dumps({"status": "aktif", "daftar": []}),
        encoding="utf-8",
    )
    with pytest.raises(ReferenceFormatError):
        load_word_reference(source)


def test_loader_does_not_mutate_reference_file(tmp_path):
    source = tmp_path / "words.json"
    original = {
        "status": "referensi",
        "daftar": [
            {"entri": "buku", "jenis": ["nomina"], "bentuk_dasar": True}
        ],
    }
    serialized = json.dumps(original, ensure_ascii=False)
    source.write_text(serialized, encoding="utf-8")
    lookup_word("buku", source)
    assert source.read_text(encoding="utf-8") == serialized
