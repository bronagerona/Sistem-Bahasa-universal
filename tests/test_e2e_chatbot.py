"""Application-level end-to-end tests through ILISCore.chatbot()."""

import pytest

from ilis.interfaces import ILISCore


QUESTION = "Apakah api bisa membakar kayu?"
COMMAND = "Bunyikan lonceng"


def _chatbot(seed_core_knowledge=True):
    core = ILISCore(seed_core_knowledge=seed_core_knowledge)
    session_id = core.create_session()
    return core, session_id, core.chatbot()


def test_chatbot_question_runs_semantic_reasoning_and_generation():
    core, session_id, chatbot = _chatbot()
    result = chatbot.respond(QUESTION, session_id)

    assert result["semantic_result"]["status"] == "supported"
    assert result["semantic_result"]["semantics"]["Intent"] == "question"
    assert result["reasoning_result"]["reasoning_type"] == "verified_inference"
    assert result["reasoning_result"]["confidence_score"] == pytest.approx(0.648)
    assert "kemungkinan" in result["answer"].casefold()
    assert result["metadata"]["confidence_score"] == pytest.approx(0.648)


def test_chatbot_command_is_acknowledged_without_claiming_execution():
    core, session_id, chatbot = _chatbot()
    result = chatbot.respond(COMMAND, session_id)

    assert result["semantic_result"]["semantics"]["Intent"] == "command"
    assert result["reasoning_result"]["reasoning_type"] == "command"
    assert "lonceng" in result["answer"].casefold()
    assert result["metadata"]["confidence_score"] == 0.0
    assert "dibunyikan" in result["answer"].casefold()


def test_chatbot_dragon_bell_question_uses_v2_rule_and_three_registers():
    core, session_id, chatbot = _chatbot(seed_core_knowledge=False)
    core.knowledge_engine.add_fact(
        "naga", "fears", "suara_keras", "verified", "e2e_lore"
    )
    core.knowledge_engine.add_fact(
        "lonceng", "produces", "suara_keras", "verified", "e2e_lore"
    )

    outputs = [
        chatbot.respond("Apakah lonceng bisa menakuti naga?", session_id, register=register)
        for register in ("formal", "informal", "slang")
    ]

    assert all(item["semantic_result"]["status"] == "supported" for item in outputs)
    assert all(item["reasoning_result"]["reasoning_type"] == "verified_inference" for item in outputs)
    assert all("naga" in item["answer"].casefold() for item in outputs)
    assert len({item["answer"] for item in outputs}) == 3
    assert all(item["generation"]["uncertainty_preserved"] for item in outputs)


def test_chatbot_conflicting_knowledge_is_reported_not_resolved_arbitrarily():
    core, session_id, chatbot = _chatbot()
    core.knowledge_engine.add_fact(
        "api", "can_burn", "plastik", "verified", "e2e_conflicting_source"
    )

    result = chatbot.respond(QUESTION, session_id)

    assert result["reasoning_result"]["reasoning_type"] == "conflicting"
    assert result["metadata"]["conflict_status"] == "conflicting"
    assert "bertentangan" in result["answer"].casefold()


@pytest.mark.parametrize(
    ("text", "expected_status"),
    [("membakar", "low_confidence"), ("!!!", "unsupported")],
)
def test_chatbot_low_confidence_and_unsupported_inputs_fall_back_gracefully(
    text, expected_status
):
    core, session_id, chatbot = _chatbot()
    result = chatbot.respond(text, session_id)

    assert result["semantic_result"]["status"] == expected_status
    assert result["reasoning_result"]["reasoning_type"] == "unknown"
    assert result["reasoning_result"]["confidence_score"] == 0.0
    assert "belum cukup" in result["answer"].casefold() or "belum ada cukup" in result["answer"].casefold()


def test_chatbot_preserves_legacy_v1_assertion_adapter_behavior():
    core, session_id, chatbot = _chatbot()
    result = chatbot.respond("Api menyentuh rumah kayu", session_id)

    assert result["semantic_result"]["status"] in {"unsupported", "low_confidence"}
    assert result["reasoning_result"]["reasoning_type"] == "verified_inference"
    assert result["metadata"]["confidence_score"] == 0.72
    assert "kemungkinan" in result["answer"].casefold()



def test_chatbot_separates_question_from_trailing_politeness_instruction():
    core, session_id, chatbot = _chatbot()
    result = chatbot.respond("Apakah api bisa membakar kayu? Jawab dengan sopan.", session_id)
    assert result["semantic_result"]["status"] == "supported"
    assert result["semantic_result"]["semantics"]["Patient/Object"] == "kayu"
    assert "kayu" in result["answer"].casefold()
    assert "jawab dengan sopan" not in result["answer"].casefold()


def test_chatbot_acknowledges_standalone_polite_answer_command():
    core, session_id, chatbot = _chatbot()
    result = chatbot.respond("Tolong jawab dengan sopan.", session_id)
    assert result["semantic_result"]["status"] == "supported"
    assert result["semantic_result"]["semantics"]["Predicate"] == "jawab"
    assert "menjawab dengan sopan" in result["answer"].casefold()


def test_chatbot_forwards_polite_instruction_to_formal_language_generation():
    core, session_id, chatbot = _chatbot()
    result = chatbot.respond(
        "Apakah api bisa membakar kayu? Jawab dengan sopan.", session_id
    )

    assert result["semantic_result"]["status"] == "supported"
    assert result["semantic_result"]["semantics"]["Patient/Object"] == "kayu"
    assert result["metadata"]["register"] == "formal"
    assert result["answer"].startswith("Dengan senang hati,")
    assert "kayu" in result["answer"].casefold()
    assert "jawab dengan sopan" not in result["answer"].casefold()


def test_chatbot_maps_casual_instruction_to_informal_register():
    core, session_id, chatbot = _chatbot()
    result = chatbot.respond(
        "Apakah api bisa membakar kayu? Jawab dengan santai.", session_id
    )

    assert result["metadata"]["register"] == "informal"
    assert result["answer"].startswith("Iya, kayaknya")



def test_chatbot_dragon_bell_question_with_polite_instruction_uses_seeded_rule():
    core, session_id, chatbot = _chatbot()
    result = chatbot.respond(
        "Apakah lonceng bisa menakuti naga? Jawab dengan sopan.", session_id
    )

    assert result["semantic_result"]["status"] == "supported"
    assert result["semantic_result"]["semantics"]["Actor"] == "lonceng"
    assert result["semantic_result"]["semantics"]["Predicate"] == "menakuti"
    assert result["semantic_result"]["semantics"]["Patient/Object"] == "naga"
    assert result["reasoning_result"]["reasoning_type"] == "verified_inference"
    assert result["reasoning_result"]["confidence_score"] == pytest.approx(0.648)
    assert len(result["reasoning_result"]["evidence"]) == 2
    assert result["metadata"]["register"] == "formal"
    assert result["answer"].startswith("Dengan senang hati,")
    assert "menakuti naga" in result["answer"].casefold()
    assert result["metadata"]["confidence_score"] == pytest.approx(0.648)



def test_chatbot_handles_leading_politeness_instruction_for_dragon_bell_question():
    core, session_id, chatbot = _chatbot()
    result = chatbot.respond(
        "Tolong jawab dengan sopan, apakah naga takut lonceng?", session_id
    )

    assert result["semantic_result"]["status"] == "supported"
    assert result["semantic_result"]["semantics"]["Intent"] == "question"
    assert result["semantic_result"]["semantics"]["Actor"] == "naga"
    assert result["semantic_result"]["semantics"]["Predicate"] == "takut"
    assert result["semantic_result"]["semantics"]["Patient/Object"] == "lonceng"
    assert result["reasoning_result"]["reasoning_type"] == "verified_inference"
    assert result["reasoning_result"]["confidence_score"] == pytest.approx(0.648)
    assert len(result["reasoning_result"]["evidence"]) == 2
    assert result["metadata"]["register"] == "formal"
    assert result["answer"].startswith("Dengan senang hati,")
    assert "jawab dengan sopan" not in result["answer"].casefold()
