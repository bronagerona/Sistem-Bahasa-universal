"""End-to-end V2 benchmark scenarios for ILIS.

Run with: python -m pytest tests/benchmark_v2_suite.py -v
These tests exercise public engine interfaces and temporary SQLite databases;
they do not modify the core engines.
"""
from __future__ import annotations

import pytest

from ilis.cognition.knowledge_engine import KnowledgeEngine
from ilis.cognition.reasoning_engine import ReasoningEngine
from ilis.generation.language_generator import LanguageGenerator
from ilis.interfaces.ilis_core import ILISCore
from ilis.language.pipeline import analyze_semantics


QUESTION = "Apakah api bisa membakar kayu?"
COMMAND = "Bunyikan lonceng"


def test_v2_question_end_to_end_returns_evidence_aware_answer():
    semantic = analyze_semantics(QUESTION)
    assert semantic["status"] == "supported"
    assert semantic["semantics"]["Intent"] == "question"

    reasoning = ReasoningEngine(KnowledgeEngine()).infer_semantic(semantic)
    assert reasoning["reasoning_type"] == "verified_inference"
    assert reasoning["confidence_score"] == 0.72
    assert reasoning["evidence"]

    answer = LanguageGenerator().generate(
        reasoning, semantic_result=semantic, register="formal"
    )
    assert "api" in answer["text"].casefold()
    assert "kayu" in answer["text"].casefold()
    assert answer["uncertainty_preserved"] is True
    assert answer["evidence"] == reasoning["evidence"]


def test_v2_simple_command_end_to_end_is_acknowledged_as_command():
    semantic = analyze_semantics(COMMAND)
    assert semantic["status"] == "supported"
    assert semantic["semantics"]["Intent"] == "command"

    reasoning = ReasoningEngine(KnowledgeEngine()).infer_semantic(semantic)
    assert reasoning["reasoning_type"] == "command"

    response = LanguageGenerator().generate(reasoning, semantic_result=semantic)
    assert response["text"] == "Baik, lonceng akan dibunyikan."
    assert response["reasoning_type"] == "command"


def test_v2_api_wood_house_scenario_produces_cautious_inference():
    knowledge = KnowledgeEngine()
    reasoning = ReasoningEngine(knowledge).infer_burn_risk("api", "rumah")

    assert reasoning["reasoning_type"] == "verified_inference"
    assert reasoning["confidence_score"] == 0.72
    assert len(reasoning["evidence"]) == 2
    assert "berpotensi" in reasoning["conclusion"]
    assert "bukan kepastian" in reasoning["uncertainty"]

    rendered = LanguageGenerator().generate(reasoning, register="informal")
    assert "rumah" in rendered["text"].casefold()
    assert rendered["uncertainty_preserved"] is True


def test_v2_dragon_bell_scenario_uses_both_premises_and_generates_text():
    knowledge = KnowledgeEngine(seed_core_knowledge=False)
    knowledge.add_fact("naga", "fears", "suara_keras", "verified", "benchmark_lore")
    knowledge.add_fact("lonceng", "produces", "suara_keras", "verified", "benchmark_lore")

    reasoning = ReasoningEngine(knowledge).infer_dragon_bell()
    assert reasoning["reasoning_type"] == "verified_inference"
    assert reasoning["confidence_score"] == 0.72
    assert len(reasoning["evidence"]) == 2
    assert "menakuti naga" in reasoning["conclusion"]

    outputs = [
        LanguageGenerator().generate(reasoning, register=register)
        for register in ("formal", "informal", "slang")
    ]
    assert all("naga" in item["text"].casefold() for item in outputs)
    assert len({item["text"] for item in outputs}) == 3
    assert all(item["uncertainty_preserved"] for item in outputs)


def test_v2_dragon_bell_missing_premise_stays_unknown():
    knowledge = KnowledgeEngine(seed_core_knowledge=False)
    knowledge.add_fact("naga", "fears", "suara_keras", "verified", "benchmark_lore")
    result = ReasoningEngine(knowledge).infer_dragon_bell()

    assert result["reasoning_type"] == "unknown"
    assert result["confidence_score"] == 0.0
    assert result["evidence"] == []


def test_v2_sqlite_save_restart_reload_preserves_facts_provenance_and_episode(tmp_path):
    database = tmp_path / "benchmark_v2.sqlite3"
    first = ILISCore(storage="sqlite", db_path=str(database))
    fact = first.knowledge_engine.add_fact(
        "pemain", "memiliki", "kunci", status="verified", source="benchmark"
    )
    session_id = first.create_session({"scenario": "sqlite_restart"})
    episode = first.context_engine.record_event(
        session_id,
        "Pemain menemukan kunci di ruang penyimpanan",
        event_type="discovery",
        entities=["pemain", "kunci"],
        attributes={"item": "key_01"},
    )
    first.close()  # simulate application shutdown / process restart

    second = ILISCore(storage="sqlite", db_path=str(database))
    restored_fact = second.knowledge_engine.fact_store.get(fact["id"])
    restored_provenance = second.knowledge_engine.get_provenance(fact["id"])
    restored_context = second.context_engine.get_context(session_id)

    assert restored_fact == fact
    assert restored_provenance == {
        "fact_id": fact["id"], "source": "benchmark", "status": "verified"
    }
    assert restored_context["episodic_memory"] == [episode]
    assert restored_context["session"]["metadata"]["scenario"] == "sqlite_restart"
    second.close()
