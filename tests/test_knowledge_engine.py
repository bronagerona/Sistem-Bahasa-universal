import pytest

from ilis.cognition import KnowledgeEngine


def test_core_knowledge_seed_contains_verified_api_kayu_kertas_and_rumah_facts():
    engine = KnowledgeEngine()

    facts = engine.fact_store.all()
    assert len(facts) == 3
    assert {
        (fact["subject"], fact["relation"], fact["object"], fact["status"], fact["source"])
        for fact in facts
    } == {
        ("api", "can_burn", "kayu", "verified", "core_knowledge"),
        ("rumah", "made_of", "kayu", "verified", "core_knowledge"),
        ("api", "can_burn", "kertas", "verified", "core_knowledge"),
    }
    paper_fact = next(f for f in facts if f["object"] == "kertas")
    assert engine.get_provenance(paper_fact["id"]) == {
        "fact_id": paper_fact["id"], "source": "core_knowledge", "status": "verified",
    }
    assert engine.concept_store.all() == ["api", "kayu", "kertas", "rumah"]
    assert engine.relation_store.all() == ["can_burn", "made_of"]


def test_add_concept_and_relation():
    engine = KnowledgeEngine(seed_core_knowledge=False)

    assert engine.add_concept(" Pohon ") == "pohon"
    assert engine.add_concept("POHON") == "pohon"
    assert engine.add_relation(" grows_on ") == "grows_on"
    assert engine.concept_store.contains("pohon")
    assert engine.relation_store.contains("GROWS_ON")


def test_add_fact_records_provenance():
    engine = KnowledgeEngine(seed_core_knowledge=False)

    fact = engine.add_fact("api", "can_burn", "kayu", source="manual_review")

    assert fact["subject"] == "api"
    assert fact["relation"] == "can_burn"
    assert fact["object"] == "kayu"
    assert fact["status"] == "hypothesis"
    assert fact["source"] == "manual_review"
    assert engine.get_provenance(fact["id"]) == {
        "fact_id": fact["id"],
        "source": "manual_review",
        "status": "hypothesis",
    }


def test_search_facts_by_subject_or_object():
    engine = KnowledgeEngine()

    assert len(engine.search_facts("api")) == 2
    assert len(engine.search_facts("kayu")) == 2
    assert len(engine.search_facts("kertas")) == 1
    assert len(engine.search_facts("rumah")) == 1
    assert engine.search_facts("tidak-ada") == []


def test_conflicting_objects_mark_all_related_facts_conflicting():
    engine = KnowledgeEngine(seed_core_knowledge=False)
    first = engine.add_fact("pohon", "made_of", "kayu", "verified", "core_knowledge")

    second = engine.add_fact("pohon", "made_of", "air", "hypothesis", "user_input")

    assert second["status"] == "conflicting"
    facts = engine.search_facts("api")
    assert {fact["status"] for fact in facts} == {"conflicting"}
    assert engine.get_provenance(first["id"])["status"] == "conflicting"
    assert engine.get_provenance(second["id"])["status"] == "conflicting"
    assert len(engine.detect_conflicts()) == 1


def test_can_burn_relation_accepts_multiple_verified_materials_without_conflict():
    engine = KnowledgeEngine()
    burn_facts = [fact for fact in engine.search_facts("api")]
    assert {fact["object"] for fact in burn_facts} == {"kayu", "kertas"}
    assert {fact["status"] for fact in burn_facts} == {"verified"}
    assert engine.detect_conflicts() == []


def test_semantic_engine_result_is_stored_as_hypothesis():
    engine = KnowledgeEngine(seed_core_knowledge=False)
    semantic_result = {
        "contract_version": "1.0",
        "status": "supported",
        "semantics": {
            "Actor": "saya",
            "Predicate": "makan",
            "Patient/Object": "nasi",
            "Recipient": None,
            "Location": None,
            "Time": None,
            "Aspect": "unspecified",
            "Negation": "none",
            "Modality": "none",
            "Intent": "assertion",
            "Register": "formal",
            "Confidence": 0.98,
        },
        "original_text": "Saya makan nasi.",
        "ilve": {},
    }

    ingested = engine.ingest_semantic_result(semantic_result)

    assert ingested["accepted"] is True
    assert ingested["fact"]["subject"] == "saya"
    assert ingested["fact"]["relation"] == "makan"
    assert ingested["fact"]["object"] == "nasi"
    assert ingested["fact"]["status"] == "hypothesis"
    assert ingested["fact"]["source"] == "semantic_engine"


@pytest.mark.parametrize(
    ("status", "negation", "modality", "expected_reason"),
    [
        ("unsupported", "none", "none", "semantic_result_not_supported"),
        ("supported", "negative", "none", "negation_not_representable"),
        ("supported", "none", "ability", "modality_not_representable"),
    ],
)
def test_semantic_ingestion_rejects_unsupported_claim_shapes(
    status, negation, modality, expected_reason
):
    engine = KnowledgeEngine(seed_core_knowledge=False)
    result = {
        "status": status,
        "semantics": {
            "Actor": "saya",
            "Predicate": "makan",
            "Patient/Object": "nasi",
            "Intent": "assertion",
            "Negation": negation,
            "Modality": modality,
        },
    }

    ingested = engine.ingest_semantic_result(result)

    assert ingested["accepted"] is False
    assert ingested["fact"] is None
    assert ingested["reason"] == expected_reason


def test_invalid_fact_status_and_empty_source_are_rejected():
    engine = KnowledgeEngine(seed_core_knowledge=False)

    with pytest.raises(ValueError):
        engine.add_fact("api", "can_burn", "kayu", status="guaranteed")
    with pytest.raises(ValueError):
        engine.add_fact("api", "can_burn", "kayu", source=" ")
