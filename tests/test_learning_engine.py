import pytest

from ilis.cognition import KnowledgeEngine
from ilis.cognition.context_engine import ContextEngine
from ilis.learning import LearningEngine


def test_semantic_input_is_stored_as_hypothesis_not_verified():
    knowledge = KnowledgeEngine(seed_core_knowledge=False)
    context = ContextEngine(knowledge)
    learning = LearningEngine(knowledge, context)
    session = context.create_session()
    processed = context.process_message(session, "player", "Saya makan nasi.")
    result = learning.learn_from_semantics(processed["semantic_result"])

    assert result["laporan"] == "hipotesis_baru"
    assert result["aman"] is True
    assert result["fact"]["status"] == "hypothesis"
    assert knowledge.get_provenance(result["fact"]["id"])["status"] == "hypothesis"


def test_required_besi_negative_statement_becomes_hypothesis():
    knowledge = KnowledgeEngine(seed_core_knowledge=False)
    context = ContextEngine(knowledge)
    learning = LearningEngine(knowledge, context)
    session = context.create_session()

    result = learning.learn_from_context_message(
        session, "player", "Besi tidak bisa dibakar"
    )

    assert result["semantic_result"]["status"] in {"unsupported", "low_confidence"}
    assert result["laporan"] == "hipotesis_baru"
    assert result["fact"]["subject"] == "besi"
    assert result["fact"]["relation"] == "can_burn"
    assert result["fact"]["object"] == "false"
    assert result["fact"]["status"] == "hypothesis"


def test_conflict_is_flagged_and_requires_confirmation_not_resolved():
    knowledge = KnowledgeEngine(seed_core_knowledge=False)
    knowledge.add_fact("besi", "can_burn", "true", status="verified", source="core")
    context = ContextEngine(knowledge)
    learning = LearningEngine(knowledge, context)
    session = context.create_session()

    result = learning.learn_from_context_message(session, "player", "Besi tidak bisa dibakar")

    assert result["laporan"] == "conflicting"
    assert result["konflik_ditemukan"] is True
    assert result["aman"] is False
    assert result["fact"]["status"] == "conflicting"
    assert knowledge.fact_store.all()[0]["status"] == "conflicting"
    assert result["hipotesis_baru"]["requires_confirmation"] is True
    with pytest.raises(ValueError):
        learning.confirm_hypothesis(result["hipotesis_baru"]["hypothesis_id"], confirmed_by="user")


def test_episode_input_becomes_hypothesis_with_traceable_source():
    knowledge = KnowledgeEngine(seed_core_knowledge=False)
    context = ContextEngine(knowledge)
    learning = LearningEngine(knowledge, context)
    session = context.create_session()
    episode = context.record_event(
        session, "Pintu terbuka setelah tuas ditarik",
        event_type="game_event", entities=["pintu", "tuas"],
        attributes={"subject": "pintu", "relation": "opened_after", "object": "tuas_ditarik"},
    )

    result = learning.learn_from_episode(session, episode["episode_id"])

    assert result["laporan"] == "hipotesis_baru"
    assert result["fact"]["status"] == "hypothesis"
    assert result["hipotesis_baru"]["origin"] == "episodic"
    assert result["hipotesis_baru"]["source_ref"] == episode["episode_id"]


def test_episode_without_structured_claim_is_recorded_as_experience_hypothesis():
    knowledge = KnowledgeEngine(seed_core_knowledge=False)
    context = ContextEngine(knowledge)
    learning = LearningEngine(knowledge, context)
    session = context.create_session()
    episode = context.record_event(session, "Naga muncul di gerbang", entities=["naga"])

    result = learning.learn_from_episode(session, episode["episode_id"])

    assert result["fact"]["subject"] == "naga"
    assert result["fact"]["relation"] == "experienced_event_event"
    assert result["fact"]["status"] == "hypothesis"


def test_explicit_confirmation_is_the_only_path_to_verified():
    knowledge = KnowledgeEngine(seed_core_knowledge=False)
    context = ContextEngine(knowledge)
    learning = LearningEngine(knowledge, context)
    session = context.create_session()
    processed = context.process_message(session, "player", "Saya makan nasi.")
    result = learning.learn_from_semantics(processed["semantic_result"])
    hypothesis_id = result["hipotesis_baru"]["hypothesis_id"]

    confirmed = learning.confirm_hypothesis(hypothesis_id, confirmed_by="user command")

    assert confirmed["knowledge_status"] == "verified"
    assert confirmed["fact"]["status"] == "verified"
    assert knowledge.get_provenance(confirmed["fact"]["id"])["status"] == "verified"


def test_unsupported_semantic_input_is_not_fabricated_into_fact():
    knowledge = KnowledgeEngine(seed_core_knowledge=False)
    context = ContextEngine(knowledge)
    learning = LearningEngine(knowledge, context)
    session = context.create_session()
    processed = context.process_message(session, "player", "Apakah besi kuat?")
    result = learning.learn_from_semantics(processed["semantic_result"])

    assert result["laporan"] == "tidak_dipelajari"
    assert result["fact"] is None
    assert knowledge.fact_store.all() == []


def test_unknown_episode_and_invalid_dependencies_are_rejected():
    knowledge = KnowledgeEngine(seed_core_knowledge=False)
    context = ContextEngine(knowledge)
    learning = LearningEngine(knowledge, context)
    session = context.create_session()

    with pytest.raises(KeyError):
        learning.learn_from_episode(session, "missing")
    with pytest.raises(TypeError):
        LearningEngine(object())
    with pytest.raises(ValueError):
        LearningEngine(knowledge, ContextEngine(KnowledgeEngine()))


def test_confirm_requires_explicit_nonempty_identity():
    knowledge = KnowledgeEngine(seed_core_knowledge=False)
    context = ContextEngine(knowledge)
    learning = LearningEngine(knowledge, context)
    session = context.create_session()
    processed = context.process_message(session, "player", "Saya makan nasi.")
    result = learning.learn_from_semantics(processed["semantic_result"])

    with pytest.raises(ValueError):
        learning.confirm_hypothesis(result["hipotesis_baru"]["hypothesis_id"], confirmed_by=" ")
