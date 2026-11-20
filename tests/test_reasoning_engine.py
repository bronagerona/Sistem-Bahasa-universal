import pytest

from ilis.cognition import KnowledgeEngine
from ilis.cognition.reasoning_engine import ReasoningEngine


def test_verified_api_kayu_rumah_inference_is_possible_not_certain():
    knowledge = KnowledgeEngine()
    reasoning = ReasoningEngine(knowledge)

    result = reasoning.infer_burn_risk("api", "rumah")

    assert result["reasoning_type"] == "verified_inference"
    assert result["confidence_score"] == 0.72
    assert len(result["evidence"]) == 2
    assert "berpotensi" in result["conclusion"]
    assert "bukan kepastian" in result["uncertainty"]
    assert all(
        "can_burn" in reason or "made_of" in reason or "Aturan" in reason
        for reason in result["reasons"]
    )


def test_hypothesis_premise_produces_hypothetical_inference():
    knowledge = KnowledgeEngine(seed_core_knowledge=False)
    knowledge.add_fact("api", "can_burn", "kayu", "verified", "core_knowledge")
    knowledge.add_fact("rumah", "made_of", "kayu", "hypothesis", "user_input")

    result = ReasoningEngine(knowledge).infer("api", "rumah")

    assert result["reasoning_type"] == "hypothetical_inference"
    assert result["confidence_score"] == 0.48
    assert len(result["evidence"]) == 2
    assert "hipotesis" in result["uncertainty"]


def test_relevant_knowledge_conflict_blocks_inference():
    knowledge = KnowledgeEngine(seed_core_knowledge=False)
    knowledge.add_fact("api", "can_burn", "kayu", "verified", "core_knowledge")
    knowledge.add_fact("rumah", "made_of", "kayu", "verified", "core_knowledge")
    knowledge.add_fact("rumah", "made_of", "bata", "hypothesis", "user_input")

    result = ReasoningEngine(knowledge).infer_burn_risk("api", "rumah")

    assert result["reasoning_type"] == "conflicting"
    assert result["confidence_score"] == 0.0
    assert result["evidence"]
    assert "bertentangan" in result["conclusion"]


def test_missing_premise_returns_unknown_and_no_evidence():
    knowledge = KnowledgeEngine(seed_core_knowledge=False)
    knowledge.add_fact("api", "can_burn", "kayu", "verified", "core_knowledge")

    result = ReasoningEngine(knowledge).infer_burn_risk("api", "rumah")

    assert result["reasoning_type"] == "unknown"
    assert result["confidence_score"] == 0.0
    assert result["evidence"] == []
    assert "Belum cukup data" in result["conclusion"]


def test_missing_provenance_returns_unknown():
    knowledge = KnowledgeEngine()
    knowledge.provenance._records.pop("fact_1")

    result = ReasoningEngine(knowledge).infer_burn_risk("api", "rumah")

    assert result["reasoning_type"] == "unknown"
    assert result["confidence_score"] == 0.0
    assert result["evidence"] == ["fact_1", "fact_2"]


def test_fact_and_provenance_status_mismatch_is_conflicting():
    knowledge = KnowledgeEngine()
    knowledge.provenance.update_status("fact_1", "hypothesis")

    result = ReasoningEngine(knowledge).infer_burn_risk("api", "rumah")

    assert result["reasoning_type"] == "conflicting"
    assert result["confidence_score"] == 0.0


def test_unrelated_conflict_does_not_block_requested_inference():
    knowledge = KnowledgeEngine()
    knowledge.add_fact("air", "made_of", "oksigen", "verified", "source_a")
    knowledge.add_fact("air", "made_of", "hidrogen", "hypothesis", "source_b")

    result = ReasoningEngine(knowledge).infer_burn_risk("api", "rumah")

    assert result["reasoning_type"] == "verified_inference"


def test_engine_requires_knowledge_engine_instance():
    with pytest.raises(TypeError):
        ReasoningEngine(object())


@pytest.mark.parametrize(("source", "target"), [("", "rumah"), ("api", " ")])
def test_empty_query_concepts_are_rejected(source, target):
    reasoning = ReasoningEngine(KnowledgeEngine())
    with pytest.raises(ValueError):
        reasoning.infer_burn_risk(source, target)



def test_v2_dragon_bell_rule_uses_two_premises_and_keeps_evidence():
    knowledge = KnowledgeEngine(seed_core_knowledge=False)
    knowledge.add_fact("naga", "fears", "suara_keras", "verified", "game_lore")
    knowledge.add_fact("lonceng", "produces", "suara_keras", "verified", "game_lore")

    result = ReasoningEngine(knowledge).infer_dragon_bell()

    assert result["reasoning_type"] == "verified_inference"
    assert result["confidence_score"] == 0.72
    assert len(result["evidence"]) == 2
    assert "menakuti naga" in result["conclusion"]


def test_v2_dragon_bell_rule_returns_unknown_without_both_premises():
    knowledge = KnowledgeEngine(seed_core_knowledge=False)
    knowledge.add_fact("naga", "fears", "suara_keras", "verified", "game_lore")
    result = ReasoningEngine(knowledge).infer_dragon_bell()
    assert result["reasoning_type"] == "unknown"
    assert result["evidence"] == []


def test_v2_semantic_question_is_answered_from_matching_knowledge_fact():
    from ilis.semantics.semantic_engine import SemanticEngine

    sentence = "Apakah api bisa membakar kayu?"
    words = ["apakah", "api", "bisa", "membakar", "kayu"]
    semantic = SemanticEngine().analyze({
        "contract_version": "1.0",
        "original_text": sentence,
        "ilve": {"normalized_text": "apakah api bisa membakar kayu?",
                 "tokens": words + ["?"], "variation_hints": []},
    })
    result = ReasoningEngine(KnowledgeEngine()).infer_semantic(semantic)
    assert result["reasoning_type"] == "verified_inference"
    assert result["confidence_score"] == 0.72
    assert result["evidence"]


def test_v2_semantic_intents_are_distinguished():
    from ilis.semantics.semantic_engine import SemanticEngine

    engine = SemanticEngine()
    reasoner = ReasoningEngine(KnowledgeEngine())
    payload = lambda text, tokens: {
        "contract_version": "1.0", "original_text": text,
        "ilve": {"normalized_text": text.casefold(), "tokens": tokens,
                 "variation_hints": []},
    }
    command = engine.analyze(payload("Bunyikan lonceng", ["bunyikan", "lonceng"]))
    assertion = engine.analyze(payload("Saya makan nasi.", ["saya", "makan", "nasi", "."]))
    assert reasoner.infer_semantic(command)["reasoning_type"] == "command"
    assert reasoner.infer_semantic(assertion)["reasoning_type"] == "assertion"


def test_dataset_fact_retrieval_matches_subject_and_relation_cues():
    from pathlib import Path

    from ilis.interfaces import ILISCore

    core = ILISCore()
    semantic = core.analyze_text("Apakah Merkurius memiliki periode rotasi sideris?")
    assert semantic["status"] == "supported"
    assert semantic["semantics"]["Actor"] == "merkurius"
    assert semantic["semantics"]["Predicate"] == "memiliki"
    assert semantic["semantics"]["Patient/Object"] == "periode rotasi sideris"

    result = core.reasoning_engine.infer_semantic(semantic)

    assert result["reasoning_type"] == "hypothetical_inference"
    assert result["confidence_score"] == 0.48
    assert result["evidence"] == ["fact-0033"]
    assert "1.407,6 jam" in result["conclusion"]
    assert "bukan lama hari Matahari" in result["conclusion"]
    assert any("verification" not in reason and "sumber:" in reason for reason in result["reasons"])


def test_dataset_fact_retrieval_supports_rotation_question_without_object():
    from ilis.interfaces import ILISCore

    core = ILISCore()
    semantic = core.analyze_text("Berapa lama Merkurius berotasi?")
    assert semantic["status"] == "supported"
    assert semantic["semantics"]["Intent"] == "question"
    assert semantic["semantics"]["Actor"] == "merkurius"
    assert semantic["semantics"]["Predicate"] == "berotasi"
    assert semantic["semantics"]["Patient/Object"] is None

    result = core.reasoning_engine.infer_semantic(semantic)
    assert result["evidence"] == ["fact-0033"]
    assert "58,65 hari Bumi" in result["conclusion"]


def test_dataset_fact_retrieval_does_not_choose_between_multiple_candidates():
    from ilis.cognition import KnowledgeEngine
    from ilis.cognition.reasoning_engine import ReasoningEngine

    knowledge = KnowledgeEngine(seed_core_knowledge=False)
    knowledge.load_dataset_record({
        "fact_id": "fact-9001", "subject": "Merkurius",
        "predicate": "memiliki periode rotasi sideris sekitar",
        "object": "58,65 hari", "source": "source A",
        "verification_status": "draft",
    })
    knowledge.load_dataset_record({
        "fact_id": "fact-9002", "subject": "Merkurius",
        "predicate": "memiliki periode rotasi sideris sekitar",
        "object": "59 hari", "source": "source B",
        "verification_status": "draft",
    })
    semantic = {
        "contract_version": "1.0", "status": "supported",
        "semantics": {
            "Actor": "merkurius", "Predicate": "memiliki",
            "Patient/Object": "periode rotasi sideris", "Recipient": None,
            "Location": None, "Time": None, "Aspect": "unspecified",
            "Negation": "none", "Modality": "none", "Intent": "question",
            "Register": "formal", "Confidence": 0.9,
        },
        "original_text": "Apakah Merkurius memiliki periode rotasi sideris?",
        "ilve": {"normalized_text": "apakah merkurius memiliki periode rotasi sideris",
                 "tokens": [], "variation_hints": []},
    }
    result = ReasoningEngine(knowledge).infer_semantic(semantic)
    assert result["reasoning_type"] == "unknown"
    assert result["evidence"] == []
    assert "lebih dari satu fakta kandidat" in result["conclusion"]
