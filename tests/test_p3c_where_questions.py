import pytest

from ilis.interfaces import ILISCore


@pytest.mark.parametrize(
    ("message", "fact_id", "expected_object"),
    [
        ("Di mana letak Ceres?", "fact-0044", "sabuk asteroid"),
        (
            "Di mana letak sabuk asteroid utama?",
            "fact-0045",
            "orbit Mars dan Jupiter",
        ),
        (
            "Di mana letak Tata Surya?",
            "fact-0056",
            "dalam Bima Sakti",
        ),
        (
            "Di mana air tanah berada?",
            "fact-0070",
            "bawah permukaan tanah",
        ),
    ],
)
def test_chatbot_answers_where_questions_from_whitelisted_dataset_predicates(
    message, fact_id, expected_object,
):
    core = ILISCore()
    result = core.chatbot().respond(message)

    assert result["reasoning_result"]["reasoning_type"] == "hypothetical_inference", result["reasoning_result"]
    assert result["reasoning_result"]["evidence"] == [fact_id]
    assert expected_object in result["reasoning_result"]["conclusion"]
    assert expected_object in result["answer"]
    assert result["answer"].startswith("Ada kemungkinan bahwa ")
    assert result["semantic_result"]["status"] in {"supported", "low_confidence"}
    assert len(result["semantic_result"]["semantics"]) == 12
    assert set(result["reasoning_result"]) == {
        "conclusion", "confidence_score", "evidence",
        "reasoning_type", "reasons", "uncertainty",
    }
    assert result["reasoning_result"]["confidence_score"] == 0.48
    assert result["metadata"]["confidence_score"] == 0.12


def test_chatbot_does_not_use_non_whitelisted_spring_predicate_for_where_question():
    core = ILISCore()
    result = core.chatbot().respond("Dari mana mata air muncul?")

    assert result["reasoning_result"]["reasoning_type"] == "unknown"
    assert result["reasoning_result"]["evidence"] == []
    assert result["reasoning_result"]["confidence_score"] == 0.0
    assert result["answer"] == "Saya belum memiliki informasi tentang lokasi itu."


def test_chatbot_returns_unknown_when_no_location_fact_matches():
    core = ILISCore()
    result = core.chatbot().respond("Di mana letak Venus?")

    assert result["reasoning_result"]["reasoning_type"] == "unknown"
    assert result["reasoning_result"]["evidence"] == []
    assert result["reasoning_result"]["confidence_score"] == 0.0
    assert result["answer"] == "Saya belum memiliki informasi tentang lokasi itu."


def test_where_question_does_not_use_unlisted_predicate_aliases():
    core = ILISCore()
    result = core.chatbot().respond("Di mana letak Mata Air?")

    assert result["reasoning_result"]["reasoning_type"] == "unknown"
    assert result["reasoning_result"]["evidence"] == []
    assert result["answer"] == "Saya belum memiliki informasi tentang lokasi itu."
