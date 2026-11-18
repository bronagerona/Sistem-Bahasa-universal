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
        "ilve": {"normalized_text": normalized, "tokens": tokens,
                 "variation_hints": hints or []},
    }


def test_gue_lagi_makan_nasi_contract_example(engine):
    payload = make_input("Gue lagi makan nasi.", "saya lagi makan nasi.",
                         ["saya", "lagi", "makan", "nasi", "."],
                         [{"surface": "Gue", "normalized": "saya", "category": "slang"}])
    result = engine.analyze(payload)
    assert result["status"] == "supported"
    assert result["original_text"] == payload["original_text"]
    assert result["ilve"] == payload["ilve"]
    assert set(result["semantics"]) == set(SEMANTIC_FIELDS)
    assert result["semantics"] == {
        "Actor": "saya", "Predicate": "makan", "Patient/Object": "nasi",
        "Recipient": None, "Location": None, "Time": None,
        "Aspect": "progressive", "Negation": "none", "Modality": "none",
        "Intent": "assertion", "Register": "slang", "Confidence": 0.98,
    }


def test_saya_akan_pergi_ke_pasar(engine):
    result = engine.analyze(make_input("Saya akan pergi ke pasar.", "saya akan pergi ke pasar.",
                                       ["saya", "akan", "pergi", "ke", "pasar", "."]))
    assert result["status"] == "supported"
    assert result["semantics"]["Actor"] == "saya"
    assert result["semantics"]["Predicate"] == "pergi"
    assert result["semantics"]["Location"] == "pasar"
    assert result["semantics"]["Aspect"] == "prospective"


def test_aku_belum_makan(engine):
    result = engine.analyze(make_input("Aku belum makan.", "aku belum makan.",
                                       ["aku", "belum", "makan", "."]))
    assert result["status"] == "supported"
    assert result["semantics"]["Negation"] == "not_yet"
    assert result["semantics"]["Register"] == "informal"


@pytest.mark.parametrize(("sentence", "normalized", "tokens", "expected"), [
    ("Saya sudah makan nasi.", "saya sudah makan nasi.", ["saya","sudah","makan","nasi","."],
     {"Aspect":"completed","Patient/Object":"nasi"}),
    ("Aku akan beli buku besok.", "aku akan beli buku besok.", ["aku","akan","beli","buku","besok","."],
     {"Aspect":"prospective","Time":"besok","Patient/Object":"buku"}),
    ("Dia selalu minum air pagi-pagian.", "dia selalu minum air pagi pagian.", ["dia","selalu","minum","air","pagi","pagian","."],
     {"Aspect":"habitual","Time":"pagi-pagian"}),
    ("Saya harus pulang ke rumah.", "saya harus pulang ke rumah.", ["saya","harus","pulang","ke","rumah","."],
     {"Modality":"obligation","Location":"rumah"}),
    ("Kita bisa bermain sepak bola sore.", "kita bisa bermain sepak bola sore.", ["kita","bisa","bermain","sepak","bola","sore","."],
     {"Modality":"ability","Time":"sore","Patient/Object":"sepak bola"}),
    ("Saya belum minum obat.", "saya belum minum obat.", ["saya","belum","minum","obat","."],
     {"Negation":"not_yet","Patient/Object":"obat"}),
])
def test_additional_v1_simple_assertions(engine, sentence, normalized, tokens, expected):
    result = engine.analyze(make_input(sentence, normalized, tokens))
    assert result["status"] == "supported"
    assert set(result["semantics"]) == set(SEMANTIC_FIELDS)
    for field, value in expected.items():
        assert result["semantics"][field] == value


def test_complex_sentence_is_unsupported(engine):
    result = engine.analyze(make_input("Saya makan nasi dan minum air.",
        "saya makan nasi dan minum air.", ["saya","makan","nasi","dan","minum","air","."]))
    assert result["status"] == "unsupported"
    assert result["semantics"] is None


def test_question_and_command_remain_unsupported_in_v1_example_but_supported_v2(engine):
    question = make_input("Apakah api bisa membakar kayu?", "apakah api bisa membakar kayu?",
                          ["apakah","api","bisa","membakar","kayu","?"])
    command = make_input("Bunyikan lonceng", "bunyikan lonceng", ["bunyikan","lonceng"])
    q = engine.analyze(question)
    c = engine.analyze(command)
    assert q["status"] == "supported"
    assert q["semantics"]["Actor"] == "api"
    assert q["semantics"]["Predicate"] == "membakar"
    assert q["semantics"]["Patient/Object"] == "kayu"
    assert q["semantics"]["Modality"] == "ability"
    assert q["semantics"]["Intent"] == "question"
    assert c["status"] == "supported"
    assert c["semantics"]["Actor"] is None
    assert c["semantics"]["Predicate"] == "bunyikan"
    assert c["semantics"]["Patient/Object"] == "lonceng"
    assert c["semantics"]["Intent"] == "command"
    assert set(q["semantics"]) == set(SEMANTIC_FIELDS)
    assert set(c["semantics"]) == set(SEMANTIC_FIELDS)


@pytest.mark.parametrize(("sentence", "expected_negation", "expected_aspect"), [
    ("Api tidak selalu membakar kayu.", "negative", "habitual"),
    ("Api nggak pernah membakar kayu.", "negative", "unspecified"),
    ("Api tak membakar kayu.", "negative", "unspecified"),
    ("Api belum membakar kayu.", "not_yet", "unspecified"),
])
def test_v2_negation_variants(engine, sentence, expected_negation, expected_aspect):
    words = sentence.casefold().replace(".", "").split()
    result = engine.analyze(make_input(sentence, " ".join(words), words))
    assert result["status"] == "supported"
    assert result["semantics"]["Negation"] == expected_negation
    assert result["semantics"]["Aspect"] == expected_aspect


def test_v2_expanded_time_and_location_phrases(engine):
    sentence = "Saya belajar di perpustakaan setiap pagi."
    words = sentence.casefold().replace(".", "").split()
    result = engine.analyze(make_input(sentence, " ".join(words), words))
    assert result["status"] == "supported"
    assert result["semantics"]["Location"] == "perpustakaan"
    assert result["semantics"]["Time"] == "setiap pagi"


def test_uncovered_question_is_low_confidence_or_unsupported(engine):
    sentence = "Mengapa awan berubah warna?"
    words = sentence.casefold().replace("?", "").split()
    result = engine.analyze(make_input(sentence, " ".join(words), words))
    assert result["status"] in {"low_confidence", "unsupported"}


def test_input_validator_rejects_wrong_contract_version():
    payload = make_input("Saya makan.", "saya makan.", ["saya","makan"])
    payload["contract_version"] = "2.0"
    with pytest.raises(ContractValidationError):
        validate_input(payload)


def test_output_validator_rejects_missing_semantic_field():
    result = {"contract_version":"1.0","status":"supported","semantics":{"Actor":"saya"}}
    with pytest.raises(ContractValidationError):
        validate_output(result)


def test_pipeline_adapter_invokes_semantic_engine_and_preserves_source():
    result = analyze_semantics("Gue lagi makan nasi.")
    assert result["status"] == "supported"
    assert result["original_text"] == "Gue lagi makan nasi."
    assert result["ilve"]["normalized_text"] == "saya lagi makan nasi."
    assert result["semantics"]["Actor"] == "saya"
    assert result["semantics"]["Register"] == "slang"


def test_missing_actor_returns_low_confidence_with_all_fields(engine):
    result = engine.analyze(make_input("Makan nasi.", "makan nasi.", ["makan","nasi","."]))
    assert result["status"] == "low_confidence"
    assert set(result["semantics"]) == set(SEMANTIC_FIELDS)
    assert result["semantics"]["Actor"] is None
    assert result["semantics"]["Predicate"] == "makan"


def test_output_validator_rejects_additional_semantic_field():
    payload = make_input("Saya makan.", "saya makan.", ["saya", "makan"])
    payload.update({
        "status": "supported",
        "semantics": {
            "Actor": "saya", "Predicate": "makan", "Patient/Object": None,
            "Recipient": None, "Location": None, "Time": None,
            "Aspect": "unspecified", "Negation": "none", "Modality": "none",
            "Intent": "assertion", "Register": "formal", "Confidence": 0.95,
            "Unexpected": "tidak boleh diterima",
        },
    })
    with pytest.raises(ContractValidationError, match="unexpected: Unexpected"):
        validate_output(payload)



def test_pipeline_separates_trailing_politeness_instruction_from_question():
    result = analyze_semantics("Apakah api bisa membakar kayu? Jawab dengan sopan.")
    assert result["original_text"] == "Apakah api bisa membakar kayu? Jawab dengan sopan."
    assert result["status"] == "supported"
    assert result["semantics"]["Intent"] == "question"
    assert result["semantics"]["Actor"] == "api"
    assert result["semantics"]["Predicate"] == "membakar"
    assert result["semantics"]["Patient/Object"] == "kayu"


def test_pipeline_recognizes_standalone_polite_answer_command():
    result = analyze_semantics("Tolong jawab dengan sopan.")
    assert result["status"] == "supported"
    assert result["semantics"]["Intent"] == "command"
    assert result["semantics"]["Predicate"] == "jawab"
