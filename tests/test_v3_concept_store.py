"""V3-A static ConceptStore tests and focused V2.2 regression checks."""

import pytest

from ilis.concept_engine import (
    ConfidenceLevel,
    ConceptStore,
    Property,
    ProvenanceRef,
    Relation,
)


@pytest.fixture
def store():
    return ConceptStore()


@pytest.mark.parametrize(
    ("identifier", "expected_id"),
    [
        ("fire", "fire"),
        ("WOOD", "wood"),
        (" paper ", "paper"),
        ("iron", "iron"),
        ("water", "water"),
        ("API", "fire"),
        ("kayu", "wood"),
        ("kertas", "paper"),
        ("besi", "iron"),
        ("air", "water"),
        ("nyala api", "fire"),
    ],
)
def test_lookup_by_id_canonical_name_and_alias(store, identifier, expected_id):
    concept = store.lookup(identifier)
    assert concept is not None
    assert concept.concept_id == expected_id


def test_lookup_methods_are_available_for_each_identifier_type(store):
    assert store.get_by_id("paper").name == "kertas"
    assert store.get_by_name("KERTAS").concept_id == "paper"
    assert store.get_by_alias("paper").concept_id == "paper"


def test_unknown_concept_returns_none(store):
    assert store.lookup("plasma-kuantum") is None
    assert store.get_by_id("not-registered") is None
    assert store.get_by_name("not-registered") is None
    assert store.get_by_alias("not-registered") is None


def test_seed_contains_exactly_the_five_initial_concepts(store):
    assert len(store) == 5
    assert {concept.name for concept in store.all()} == {
        "api", "kayu", "kertas", "besi", "air",
    }


def test_seed_properties_and_relations_are_structured_data(store):
    api = store.lookup("api")
    paper = store.lookup("kertas")

    assert any(item.name == "menghasilkan_panas" for item in api.properties)
    assert any(item.relation_type == "can_burn" for item in api.relations)
    assert any(item.name == "mudah_terbakar" for item in paper.properties)


def test_provenance_is_readable_for_concept_property_and_relation(store):
    api = store.lookup("api")
    paper = store.lookup("kertas")

    assert api.provenance
    assert api.provenance[0].source_id == "v3a-seed:fire"
    assert api.provenance[0].verification_status == "unverified"

    paper_property = next(p for p in paper.properties if p.name == "mudah_terbakar")
    assert paper_property.provenance[0].source == "ilis_v3_design_seed"

    burn_relation = next(r for r in api.relations if r.relation_type == "can_burn")
    assert burn_relation.provenance[0].source_id == (
        "v3a-seed:fire-can-burn-combustible-material"
    )


def test_seed_data_does_not_claim_unverified_facts_as_known(store):
    for concept in store.all():
        assert concept.data_status is ConfidenceLevel.PARTIAL
        for item in (*concept.properties, *concept.relations):
            assert item.confidence_level is ConfidenceLevel.PARTIAL
            assert all(
                ref.verification_status == "unverified"
                for ref in item.provenance
            )


def test_confidence_level_enum_exposes_the_three_design_values():
    assert {item.value for item in ConfidenceLevel} == {
        "KNOWN", "PARTIAL", "UNKNOWN",
    }


def test_provenance_rejects_missing_source_and_invalid_status():
    with pytest.raises(ValueError):
        ProvenanceRef(source_id="", source="manual")
    with pytest.raises(ValueError):
        ProvenanceRef(
            source_id="x", source="manual", verification_status="maybe"
        )


def test_property_and_relation_validate_confidence_and_required_fields():
    with pytest.raises(ValueError):
        Property(property_id="", name="x", description="desc")
    with pytest.raises(ValueError):
        Relation(
            relation_id="r", subject_concept_id="fire",
            relation_type="can_burn", object_id="paper", polarity="maybe",
        )


def test_duplicate_concept_id_or_alias_is_rejected(store):
    from ilis.concept_engine import Concept

    existing = store.lookup("api")
    duplicate_id = Concept(
        concept_id=existing.concept_id,
        name="api-lain",
        description="Duplikat ID",
    )
    with pytest.raises(ValueError, match="duplicate concept_id"):
        ConceptStore([existing, duplicate_id])


def test_semantic_and_reasoning_contracts_remain_unchanged():
    from ilis.interfaces import ILISCore

    result = ILISCore().analyze_text("Apakah api bisa membakar kayu?")
    assert len(result["semantics"]) == 12
    assert set(result["reasoning"]) == {
        "conclusion", "confidence_score", "evidence",
        "reasoning_type", "reasons", "uncertainty",
    }


def test_v2_2_multi_turn_same_session_still_works():
    from ilis.interfaces import ChatbotAdapter, ILISCore, SessionManager

    manager = SessionManager(max_turns=5)
    adapter = ChatbotAdapter(ILISCore(), session_manager=manager)
    session_id = adapter.create_session()

    first = adapter.respond("Apakah api bisa membakar kayu?", session_id)
    second = adapter.respond(
        "Lalu apakah api juga bisa membakar kertas?", session_id
    )

    assert first["metadata"]["session_id"] == session_id
    assert second["metadata"]["session_id"] == session_id
    assert second["metadata"]["context_turns_used"] == 1
    assert len(manager.get_recent_turns(session_id)) == 2
    assert second["reasoning_result"]["evidence"] == ["fact_3"]
