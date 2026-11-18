"""ILIS V1 beta acceptance suite: full-stack tests through ILISCore.

Run with: python -m pytest tests/beta_suite.py -v
This suite intentionally exercises public orchestration APIs rather than
reaching into engine internals, except for read-only state consistency checks.
"""
from time import perf_counter

import pytest

from ilis.interfaces import ILISCore


BETA_DATASET = [
    {
        "id": "CHAT-001",
        "area": "chatbot",
        "input": "Api menyentuh rumah kayu",
        "register": "formal",
        "expected_reasoning": "verified_inference",
        "expected_status": "Ada kemungkinan",
    },
    {
        "id": "CHAT-002",
        "area": "chatbot",
        "input": "Gue lagi makan nasi.",
        "register": "slang",
        "expected_semantic": "supported",
        "expected_actor": "saya",
    },
    {
        "id": "CHAT-003",
        "area": "chatbot",
        "input": "Apakah naga takut lonceng?",
        "register": "informal",
        "expected_semantic": "unsupported",
    },
    {
        "id": "GAME-001",
        "area": "game",
        "input": "Naga takut lonceng",
        "expected_reasoning": "hypothetical_inference",
        "expected_episode": True,
    },
    {
        "id": "GAME-002",
        "area": "game",
        "input": "Pemain membuka gerbang kuno",
        "expected_reasoning": "unknown",
        "expected_episode": True,
    },
]


def test_beta_chatbot_full_pipeline_and_register():
    core = ILISCore()
    session_id = core.create_session(metadata={"register": "formal"})
    result = core.chatbot().respond("Api menyentuh rumah kayu", session_id)

    assert result["generation"]["text"].startswith("Ada kemungkinan")
    assert result["answer"].startswith("Saya ILIS, sistem kecerdasan bahasa.")
    assert result["metadata"]["reasoning_type"] == "verified_inference"
    assert result["metadata"]["confidence_score"] == 0.72
    assert result["metadata"]["conflict_status"] == "clear"
    assert result["metadata"]["semantic_status"] in {"unsupported", "low_confidence"}
    assert len(core.context_engine.get_context(session_id)["conversation_history"]) == 1


def test_beta_semantic_and_slang_pipeline_preserves_register():
    core = ILISCore()
    session_id = core.create_session(metadata={"register": "slang"})
    result = core.chatbot().respond("Gue lagi makan nasi.", session_id)

    semantic = result["semantic_result"]
    assert semantic["status"] == "supported"
    assert semantic["semantics"]["Actor"] == "saya"
    assert semantic["semantics"]["Predicate"] == "makan"
    assert semantic["semantics"]["Patient/Object"] == "nasi"
    assert semantic["semantics"]["Register"] == "slang"
    assert result["metadata"]["register"] == "slang"


def test_beta_typo_and_abbreviation_variations_are_not_overclaimed():
    core = ILISCore()
    session_id = core.create_session()
    typo = core.chatbot().respond("GAK", session_id)
    slang = core.chatbot().respond("Gue lagi makan nasi.", session_id)

    # Variation hints can normalize known lexical items, but a one-token
    # fragment is not a complete semantic assertion.
    assert typo["semantic_result"]["status"] in {"unsupported", "low_confidence"}
    assert slang["semantic_result"]["status"] == "supported"
    assert slang["semantic_result"]["semantics"]["Register"] == "slang"


def test_beta_game_event_is_episodic_and_yields_cautious_npc_dialogue():
    core = ILISCore()
    session_id = core.create_session(metadata={"register": "informal"})
    result = core.game().handle_event(
        "Naga takut lonceng",
        session_id,
        entities=["naga", "lonceng"],
        npc="penjaga_gua",
    )

    assert result["episode"]["description"] == "Naga takut lonceng"
    assert result["metadata"]["episode_id"] == result["episode"]["episode_id"]
    assert result["metadata"]["reasoning_type"] == "hypothetical_inference"
    assert result["metadata"]["confidence_score"] == 0.48
    assert "naga takut pada lonceng" in result["dialogue"].casefold()
    assert len(core.context_engine.get_context(session_id)["episodic_memory"]) == 1
    assert len(core.knowledge_engine.fact_store.all()) == 2


def test_beta_unknown_game_event_is_retained_without_invented_reasoning():
    core = ILISCore()
    session_id = core.create_session()
    result = core.game().handle_event("Pemain membuka gerbang kuno", session_id)

    assert result["metadata"]["reasoning_type"] == "unknown"
    assert result["episode"]["description"] == "Pemain membuka gerbang kuno"
    assert result["metadata"]["confidence_score"] == 0.0


def test_beta_learning_records_hypothesis_without_auto_verification():
    core = ILISCore()
    session_id = core.create_session()
    processed = core.context_engine.process_message(
        session_id, "player", "Saya makan nasi."
    )
    learned = core.learning_engine.learn_from_semantics(
        processed["semantic_result"]
    )

    assert learned["laporan"] == "hipotesis_baru"
    assert learned["fact"]["status"] == "hypothesis"
    assert core.knowledge_engine.get_provenance(
        learned["fact"]["id"]
    )["status"] == "hypothesis"


def test_beta_context_is_session_isolated_and_working_memory_clears():
    core = ILISCore()
    first = core.create_session()
    second = core.create_session()
    core.context_engine.add_message(first, "user", "Saya makan nasi.")
    core.context_engine.record_event(second, "Naga takut lonceng")

    first_context = core.context_engine.get_context(first)
    second_context = core.context_engine.get_context(second)
    assert len(first_context["conversation_history"]) == 1
    assert first_context["episodic_memory"] == []
    assert second_context["conversation_history"] == []
    assert len(second_context["episodic_memory"]) == 1

    core.close_session(first)
    assert core.context_engine.memory_store.get_working_memory(first) == []


def test_beta_generator_preserves_uncertainty_for_rule_conclusion():
    core = ILISCore()
    result = core.reasoning_engine.infer_burn_risk("api", "rumah")
    generated = core.language_generator.generate(result, register="formal")

    assert generated["uncertainty_preserved"] is True
    assert "kemungkinan" in generated["text"].casefold()


def test_beta_end_to_end_latency_is_measured_without_machine_specific_threshold():
    core = ILISCore()
    session_id = core.create_session()
    started = perf_counter()
    result = core.chatbot().respond("Api menyentuh rumah kayu", session_id)
    elapsed = perf_counter() - started

    assert result["answer"]
    assert elapsed >= 0.0
    # Timing is reported as an observation only; CI hardware is variable.


@pytest.mark.parametrize("case", BETA_DATASET, ids=lambda case: case["id"])
def test_beta_dataset_has_valid_case_definitions(case):
    assert case["input"]
    assert case["area"] in {"chatbot", "game"}
    assert case.get("expected_reasoning") or case.get("expected_semantic")
