import pytest

from ilis.semantics.constants import SEMANTIC_FIELDS
from ilis.semantics.contract_validator import ContractValidationError, validate_input, validate_output
from ilis.semantics.semantic_engine import SemanticEngine
from ilis.language.pipeline import analyze_semantics


@pytest.fixture
def engine():
    return SemanticEngine()


def make_input(original, normalized, tokens, hints=None):
    return {
        "contract_version": "1.0",
        "original_text": original,
        "ilve": {
            "normalized_text": normalized,
            "tokens": tokens,
            "variation_hints": hints or [],
        },
    }


def test_gue_lagi_makan_nasi_contract_example(engine):
    payload = make_input(
        "Gue lagi makan nasi.",
        "saya lagi makan nasi.",
        ["saya", "lagi", "makan", "nasi", "."],
        [{"surface": "Gue", "normalized": "saya", "category": "slang"}],
    )
    result = engine.analyze(payload)

    assert result["status"] == "supported"
    assert result["original_text"] == "Gue lagi makan nasi."
    assert result["ilve"] == payload["ilve"]
    assert set(result["semantics"]) == set(SEMANTIC_FIELDS)
    assert result["semantics"] == {
        "Actor": "saya",
        "Predicate": "makan",
        "Patient/Object": "nasi",
        "Recipient": None,
        "Location": None,
        "Time": None,
        "Aspect": "progressive",
        "Negation": "none",
        "Modality": "none",
        "Intent": "assertion",
        "Register": "slang",
        "Confidence": 0.98,
    }


def test_saya_akan_pergi_ke_pasar(engine):
    payload = make_input(
        "Saya akan pergi ke pasar.",
        "saya akan pergi ke pasar.",
        ["saya", "akan", "pergi", "ke", "pasar", "."],
    )
    result = engine.analyze(payload)

    assert result["status"] == "supported"
    assert result["semantics"]["Actor"] == "saya"
    assert result["semantics"]["Predicate"] == "pergi"
    assert result["semantics"]["Location"] == "pasar"
    assert result["semantics"]["Aspect"] == "prospective"
    assert result["semantics"]["Time"] is None


def test_aku_belum_makan(engine):
    payload = make_input(
        "Aku belum makan.",
        "aku belum makan.",
        ["aku", "belum", "makan", "."],
    )
    result = engine.analyze(payload)

    assert result["status"] == "supported"
    assert result["semantics"]["Actor"] == "aku"
    assert result["semantics"]["Predicate"] == "makan"
    assert result["semantics"]["Negation"] == "not_yet"
    assert result["semantics"]["Aspect"] == "unspecified"
    assert result["semantics"]["Register"] == "informal"


def test_complex_sentence_is_unsupported(engine):
    payload = make_input(
        "Saya makan nasi dan minum air.",
        "saya makan nasi dan minum air.",
        ["saya", "makan", "nasi", "dan", "minum", "air", "."],
    )
    result = engine.analyze(payload)

    assert result["status"] == "unsupported"
    assert result["semantics"] is None
    assert result["original_text"] == payload["original_text"]


def test_input_validator_rejects_wrong_contract_version():
    payload = make_input("Saya makan.", "saya makan.", ["saya", "makan"])
    payload["contract_version"] = "2.0"
    with pytest.raises(ContractValidationError):
        validate_input(payload)


def test_output_validator_rejects_missing_semantic_field():
    result = {
        "contract_version": "1.0",
        "status": "supported",
        "semantics": {"Actor": "saya"},
    }
    with pytest.raises(ContractValidationError):
        validate_output(result)


def test_pipeline_adapter_invokes_semantic_engine_and_preserves_source():
    result = analyze_semantics("Gue lagi makan nasi.")

    assert result["status"] == "supported"
    assert result["original_text"] == "Gue lagi makan nasi."
    assert result["ilve"]["normalized_text"] == "saya lagi makan nasi."
    assert result["semantics"]["Actor"] == "saya"
    assert result["semantics"]["Register"] == "slang"
