"""Behavioral tests for the conservative EJA-04 date capitalization checker."""

import pytest

from ilis.language.foundation import inspect_spelling


@pytest.mark.parametrize(
    ("sample", "expected"),
    [
        ("Kami berangkat pada senin, 2 januari 2026.", [("senin", "issue"), ("januari", "issue")]),
        ("Rapat dimulai pada 2 februari 2026.", [("februari", "issue")]),
        ("Acara berlangsung hari selasa.", [("selasa", "needs_context")]),
        ("Senin, 2 Januari 2026.", [("Senin", "no_issue"), ("Januari", "no_issue")]),
        ("Tanggal 17 agustus 1945 diperingati.", [("agustus", "issue")]),
        ("Kami bertemu pada minggu depan.", [("minggu", "needs_context")]),
        ("Minggu, 3 mei 2026.", [("Minggu", "no_issue"), ("mei", "issue")]),
        ("Senin hadir lebih awal.", [("Senin", "needs_context")]),
        ("Kami pulang pada desember.", [("desember", "needs_context")]),
        ("2 desember 2026", [("desember", "issue")]),
        ("2 Desember 2026", [("Desember", "no_issue")]),
        ("Minggu ini kami beristirahat.", [("Minggu", "needs_context")]),
        ("Pada rabu, 4 maret 2026, kami berangkat.", [("rabu", "issue"), ("maret", "issue")]),
        ("Kami bertemu Rabu di kantor.", [("Rabu", "needs_context")]),
        ("Jadwal: 5 november 2026.", [("november", "issue")]),
        ("Bulan depan, pada 5 januari, kegiatan dimulai.", [("januari", "issue")]),
    ],
    ids=[f"A-E04-{number:03d}" for number in range(1, 17)],
)
def test_eja_04_sixteen_approved_cases(sample, expected):
    result = inspect_spelling(sample)
    actual = [(item["observed"], item["status"]) for item in result["findings"]]
    assert actual == expected
    assert result["input"] == sample
    assert result["status"] == "partial"
    assert result["coverage"]["checked_rules"] == ["EJA-04"]
    assert result["coverage"]["complete"] is False
    assert "EJA-04" not in result["coverage"]["deferred_rules"]


@pytest.mark.parametrize(
    "sample",
    [
        "Awas?",
        "Kamu sudah makan.",
        "ibu datang.",
        "budi tinggal di bandung.",
        "Buku itu di baca.",
        "disekolah",
        "Pilihan itu-menurut saya-cukup baik.",
        "05/10/2026",
    ],
)
def test_eja_04_never_changes_other_rules_or_numeric_date_formats(sample):
    result = inspect_spelling(sample)
    assert result["input"] == sample
    assert result["findings"] == []
    assert "corrected_text" not in result


def test_findings_use_exact_unicode_codepoint_spans():
    sample = "🙂 Pada rabu, 4 maret 2026."
    result = inspect_spelling(sample)
    by_observed = {item["observed"]: item for item in result["findings"]}
    for token in ("rabu", "maret"):
        finding = by_observed[token]
        start = finding["span"]["start"]
        end = finding["span"]["end"]
        assert sample[start:end] == token


def test_multiple_dates_are_all_inspected_without_duplicate_spans():
    sample = "2 januari 2026 dan 3 februari 2027"
    result = inspect_spelling(sample)
    spans = [(item["span"]["start"], item["span"]["end"]) for item in result["findings"]]
    assert len(spans) == len(set(spans)) == 2
    assert [item["observed"] for item in result["findings"]] == ["januari", "februari"]


def test_numeric_date_format_is_outside_eja_04_scope():
    result = inspect_spelling("Tanggal 05/10/2026 sudah dicatat.")
    assert result["findings"] == []
    assert result["coverage"]["checked_rules"] == ["EJA-04"]
    assert result["coverage"]["deferred_rules"] == [
        "EJA-01", "EJA-02", "EJA-03", "EJA-05", "EJA-06", "EJA-07",
        "EJA-08", "EJA-09", "EJA-10", "EJA-11", "EJA-12",
    ]
