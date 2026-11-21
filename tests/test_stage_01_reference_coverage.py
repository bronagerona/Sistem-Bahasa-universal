"""Expanded behavioral coverage for the isolated Stage 1 foundation API.

These tests exercise only the capabilities currently implemented by foundation.py.
They do not treat the guidance-only spelling API as an automatic spell checker.
"""

import json

import pytest

from ilis.language.foundation import (
    ReferenceFormatError,
    inspect_spelling,
    load_spelling_rules,
    load_word_reference,
    lookup_word,
)

_ENTRIES = load_word_reference()
_EXPECTED_CLASSES = {
    "nomina", "verba", "adjektiva", "adverbia", "pronomina", "numeralia",
    "preposisi", "konjungsi", "interjeksi", "artikula", "partikel",
}


@pytest.mark.parametrize(
    ("entry",),
    [(entry,) for entry in _ENTRIES],
    ids=[f"{entry['entri']}-{index}" for index, entry in enumerate(_ENTRIES)],
)
def test_every_reference_word_is_retrievable(entry):
    result = lookup_word(entry["entri"])
    assert result["status"] in {"found", "ambiguous"}
    assert set(entry["jenis"]).issubset(set(result["classes"]))


def test_all_eleven_word_classes_are_represented():
    actual = {
        kind
        for entry in load_word_reference()
        for kind in entry["jenis"]
    }
    assert actual == _EXPECTED_CLASSES


def test_duplicate_form_dekat_preserves_both_reference_classes():
    result = lookup_word("dekat")
    assert result["status"] == "ambiguous"
    assert set(result["classes"]) == {"adjektiva", "preposisi"}
    assert "konteks" in result["message"].casefold()


@pytest.mark.parametrize("word", ["", "   ", "\n\t"])
def test_blank_input_is_unknown_without_crashing(word):
    result = lookup_word(word)
    assert result["status"] == "unknown"
    assert result["classes"] == []


def test_non_string_word_is_rejected():
    with pytest.raises(TypeError):
        lookup_word(None)


def test_reference_is_reloaded_on_each_lookup(tmp_path):
    source = tmp_path / "words.json"
    payload = {
        "status": "referensi",
        "daftar": [
            {"entri": "uji", "jenis": ["nomina"], "bentuk_dasar": True}
        ],
    }
    source.write_text(json.dumps(payload), encoding="utf-8")
    assert lookup_word("uji", source)["classes"] == ["nomina"]

    payload["daftar"][0]["jenis"] = ["verba"]
    source.write_text(json.dumps(payload), encoding="utf-8")
    assert lookup_word("uji", source)["classes"] == ["verba"]


def test_word_reference_bytes_are_not_modified_by_read_operations():
    from pathlib import Path
    import hashlib

    path = Path(__file__).resolve().parents[1] / "data/reference/tahap_01_fondasi/kata_dasar.json"
    before = hashlib.sha256(path.read_bytes()).hexdigest()
    load_word_reference()
    lookup_word("buku")
    lookup_word("kata-yang-tidak-ada")
    after = hashlib.sha256(path.read_bytes()).hexdigest()
    assert after == before


def test_all_spelling_rules_have_required_fields_and_examples():
    rules = load_spelling_rules()
    assert len(rules) == 12
    for rule in rules:
        assert all(rule[key].strip() for key in (
            "aturan", "contoh_benar", "contoh_salah", "penjelasan"
        ))


@pytest.mark.parametrize(
    "sample",
    ["disekolah", "budi pergi ke bandung", "Apakah kamu tinggal di jakarta?"],
)
def test_spelling_api_reports_partial_scope_and_never_rewrites(sample):
    result = inspect_spelling(sample)
    assert result["status"] == "partial"
    assert result["input"] == sample
    assert result["findings"] == []
    assert result["rules_available"] == 12
    assert result["coverage"]["checked_rules"] == ["EJA-04"]
    assert len(result["coverage"]["deferred_rules"]) == 11
    assert "belum didukung" in result["message"]


def test_spelling_reference_is_reloaded_on_each_inspection(tmp_path):
    source = tmp_path / "spelling.json"
    payload = {
        "status": "referensi",
        "daftar_aturan": [
            {
                "aturan": "Aturan pertama.",
                "contoh_benar": "Bentuk benar.",
                "contoh_salah": "Bentuk salah.",
                "penjelasan": "Penjelasan pertama.",
            }
        ],
    }
    source.write_text(json.dumps(payload), encoding="utf-8")
    assert len(load_spelling_rules(source)) == 1

    payload["daftar_aturan"].append(
        {
            "aturan": "Aturan kedua.",
            "contoh_benar": "Contoh benar.",
            "contoh_salah": "Contoh salah.",
            "penjelasan": "Penjelasan kedua.",
        }
    )
    source.write_text(json.dumps(payload), encoding="utf-8")
    result = inspect_spelling("uji", source)
    assert result["rules_available"] == 2
    assert len(result["rules"]) == 2


def test_spelling_reference_bytes_are_not_modified_by_read_operations():
    from pathlib import Path
    import hashlib

    path = Path(__file__).resolve().parents[1] / "data/reference/tahap_01_fondasi/aturan_ejaan.json"
    before = hashlib.sha256(path.read_bytes()).hexdigest()
    load_spelling_rules()
    inspect_spelling("Contoh masukan.")
    after = hashlib.sha256(path.read_bytes()).hexdigest()
    assert after == before


def test_word_loader_rejects_invalid_json(tmp_path):
    source = tmp_path / "broken.json"
    source.write_text("{not-json", encoding="utf-8")
    with pytest.raises(ReferenceFormatError):
        load_word_reference(source)


@pytest.mark.parametrize(
    "payload",
    [
        [],
        {"status": "aktif", "daftar": []},
        {"status": "referensi", "daftar": "not-a-list"},
        {"status": "referensi", "daftar": [None]},
        {"status": "referensi", "daftar": [{"entri": "", "jenis": ["nomina"]}]},
        {"status": "referensi", "daftar": [{"entri": "uji", "jenis": []}]},
    ],
)
def test_word_loader_rejects_invalid_reference_shapes(tmp_path, payload):
    source = tmp_path / "invalid.json"
    source.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ReferenceFormatError):
        load_word_reference(source,)


def test_spelling_loader_rejects_missing_rule_fields(tmp_path):
    source = tmp_path / "rules.json"
    source.write_text(
        json.dumps({"status": "referensi", "daftar_aturan": [{"aturan": "Kapital."}]}),
        encoding="utf-8",
    )
    with pytest.raises(ReferenceFormatError):
        load_spelling_rules(source)


@pytest.mark.parametrize(
    "payload",
    [
        [],
        {"status": "aktif", "daftar_aturan": []},
        {"status": "referensi", "daftar_aturan": "not-a-list"},
        {"status": "referensi", "daftar_aturan": [None]},
    ],
)
def test_spelling_loader_rejects_invalid_reference_shapes(tmp_path, payload):
    source = tmp_path / "invalid-spelling.json"
    source.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ReferenceFormatError):
        load_spelling_rules(source)


def test_spelling_inspection_rejects_non_string_input():
    with pytest.raises(TypeError):
        inspect_spelling(None)
