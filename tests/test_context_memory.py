import pytest

from ilis.cognition import KnowledgeEngine
from ilis.cognition.context_engine import ContextEngine
from ilis.cognition.memory_store import MemoryStore
from ilis.cognition.reasoning_engine import ReasoningEngine


def test_sessions_have_unique_ids_and_can_be_closed():
    context = ContextEngine(KnowledgeEngine())
    first = context.create_session()
    second = context.create_session()

    assert first != second
    closed = context.close_session(first)

    assert closed["active"] is False
    assert closed["closed_at"] is not None
    with pytest.raises(ValueError):
        context.add_message(first, "player", "Halo")


def test_working_memory_tracks_speakers_and_conversation_history():
    context = ContextEngine(KnowledgeEngine())
    session_id = context.create_session()

    context.add_message(session_id, "player", "Aku masuk ke rumah.")
    context.add_message(session_id, "npc_guard", "Hati-hati, ada api!")

    snapshot = context.get_context(session_id)
    assert snapshot["participants"] == ["player", "npc_guard"]
    assert [item["speaker"] for item in snapshot["conversation_history"]] == [
        "player", "npc_guard"
    ]
    assert len(snapshot["conversation_history"]) == 2


def test_episodic_memory_records_events_and_entities():
    context = ContextEngine(KnowledgeEngine())
    session_id = context.create_session()

    episode = context.record_event(
        session_id,
        "Api menyentuh rumah kayu",
        event_type="environment_event",
        entities=["api", "rumah", "kayu"],
    )

    snapshot = context.get_context(session_id)
    assert snapshot["episodic_memory"][0]["episode_id"] == episode["episode_id"]
    assert snapshot["episodic_memory"][0]["entities"] == ["api", "rumah", "kayu"]


def test_long_term_memory_references_knowledge_engine_facts_and_provenance():
    knowledge = KnowledgeEngine()
    context = ContextEngine(knowledge)
    session_id = context.create_session()

    snapshot = context.get_context(session_id)
    facts = snapshot["long_term_memory"]["facts"]

    assert len(facts) == 3
    assert facts[0]["provenance"]["source"] == "core_knowledge"
    assert facts[0]["provenance"]["status"] == "verified"


def test_context_event_is_available_alongside_reasoning_result():
    knowledge = KnowledgeEngine()
    context = ContextEngine(knowledge)
    session_id = context.create_session()
    context.add_message(session_id, "game_system", "Api menyentuh rumah kayu.")
    context.record_event(
        session_id,
        "Api menyentuh rumah kayu",
        event_type="environment_event",
        entities=["api", "rumah", "kayu"],
        attributes={"source": "api", "target": "rumah"},
    )

    result = context.reason_from_context(
        session_id, "api", "rumah", ReasoningEngine(knowledge)
    )

    assert result["context"]["episodic_memory"][0]["description"] == "Api menyentuh rumah kayu"
    assert result["inference"]["reasoning_type"] == "verified_inference"
    assert "berpotensi" in result["inference"]["conclusion"]
    assert result["inference"]["evidence"] == ["fact_1", "fact_2"]


def test_closing_session_clears_working_memory_but_keeps_episodes():
    context = ContextEngine(KnowledgeEngine())
    session_id = context.create_session()
    context.add_message(session_id, "player", "Aku membunyikan lonceng.")
    context.record_event(
        session_id, "Pemain membunyikan lonceng dekat naga",
        entities=["pemain", "lonceng", "naga"]
    )

    context.close_session(session_id)
    snapshot = context.get_context(session_id)

    assert snapshot["conversation_history"] == []
    assert len(snapshot["episodic_memory"]) == 1
    assert snapshot["session"]["active"] is False


def test_working_memory_can_be_retained_explicitly_on_close():
    store = MemoryStore()
    context = ContextEngine(KnowledgeEngine(), store)
    session_id = context.create_session()
    context.add_message(session_id, "player", "uji")

    context.close_session(session_id, clear_working=False)

    assert len(store.get_working_memory(session_id)) == 1


def test_unknown_session_raises_key_error():
    context = ContextEngine(KnowledgeEngine())
    with pytest.raises(KeyError):
        context.get_context("missing-session")


def test_process_message_runs_semantics_and_ingestion_is_opt_in():
    knowledge = KnowledgeEngine(seed_core_knowledge=False)
    context = ContextEngine(knowledge)
    session_id = context.create_session()

    result = context.process_message(
        session_id, "player", "Saya makan nasi.", ingest_semantics=True
    )

    assert result["message"]["speaker"] == "player"
    assert result["semantic_result"]["status"] == "supported"
    assert result["knowledge_ingestion"]["accepted"] is True
    assert result["knowledge_ingestion"]["fact"]["status"] == "hypothesis"


def test_engine_requires_knowledge_engine():
    with pytest.raises(TypeError):
        ContextEngine(object())
