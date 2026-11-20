import pytest

from ilis.interfaces import ILISCore


@pytest.mark.parametrize(
    ("message", "fact_id", "expected_object"),
    [
        (
            "Di mana letak sabuk asteroid utama?",
            "fact-0045",
            "Mars dan Jupiter",
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


@pytest.mark.parametrize(
    ("message", "fact_id", "reason_fragment"),
    [
        ("Di mana letak Ceres?", "fact-0044", "predicate faktanya tidak termasuk whitelist"),
        ("Di mana letak Bima Sakti?", "fact-0056", "predicate faktanya tidak termasuk whitelist"),
        ("Di mana air tanah berada?", "fact-0070", "predicate faktanya tidak termasuk whitelist"),
        ("Dari mana mata air muncul?", "fact-0075", "predicate faktanya tidak termasuk whitelist"),
    ],
)
def test_where_questions_reject_facts_whose_predicates_are_not_location_relations(
    message, fact_id, reason_fragment,
):
    core = ILISCore()
    result = core.chatbot().respond(message)

    assert result["reasoning_result"]["reasoning_type"] == "unknown"
    assert result["reasoning_result"]["evidence"] == []
    assert result["reasoning_result"]["confidence_score"] == 0.0
    assert any(reason_fragment in reason for reason in result["reasoning_result"]["reasons"])
    assert result["answer"] == "Saya belum memiliki informasi lokasi untuk itu"


def test_tata_surya_location_question_does_not_reverse_match_fact_object():
    core = ILISCore()
    result = core.chatbot().respond("Di mana letak Tata Surya?")

    assert result["reasoning_result"]["reasoning_type"] == "unknown"
    assert result["reasoning_result"]["evidence"] == []
    assert result["reasoning_result"]["confidence_score"] == 0.0
    assert result["answer"] == "Saya belum memiliki informasi lokasi untuk itu"


def test_chatbot_returns_unknown_when_no_location_fact_matches():
    core = ILISCore()
    result = core.chatbot().respond("Di mana letak Venus?")

    assert result["reasoning_result"]["reasoning_type"] == "unknown"
    assert result["reasoning_result"]["evidence"] == []
    assert result["reasoning_result"]["confidence_score"] == 0.0
    assert result["answer"] == "Saya belum memiliki informasi lokasi untuk itu"


def test_where_question_does_not_use_unlisted_predicate_aliases():
    core = ILISCore()
    result = core.chatbot().respond("Di mana letak Mata Air?")

    assert result["reasoning_result"]["reasoning_type"] == "unknown"
    assert result["reasoning_result"]["evidence"] == []
    assert result["answer"] == "Saya belum memiliki informasi lokasi untuk itu"
