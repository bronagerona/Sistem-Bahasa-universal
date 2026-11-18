"""Focused tests for ILIS V3-B deterministic inference rules (C-01..C-04)."""

import pytest

from ilis.concept_engine import (
    ConfidenceLevel,
    Concept,
    ConceptStore,
    InferenceEngine,
    Property,
    ProvenanceRef,
    Relation,
)


def verified(item_id):
    return (
        ProvenanceRef(
            source_id=f"test:{item_id}",
            source="curated_test_fixture",
            verification_status="verified",
        ),
    )


def make_verified_store(*, relation=True, relation_target="property:mudah_terbakar",
                        relation_conditions=(), property_conditions=()):
    actor = Concept(
        concept_id="fire",
        name="api",
        description="Konsep penguji yang telah dikurasi.",
        data_status=ConfidenceLevel.KNOWN,
        provenance=verified("fire"),
        relations=(
            Relation(
                relation_id="fire-can-burn",
                subject_concept_id="fire",
                relation_type="can_burn",
                object_id=relation_target,
                conditions=relation_conditions,
                confidence_level=ConfidenceLevel.KNOWN,
                provenance=verified("fire-can-burn"),
            ),
        ) if relation else (),
    )
    target = Concept(
        concept_id="paper",
        name="kertas",
        description="Konsep penguji yang telah dikurasi.",
        data_status=ConfidenceLevel.KNOWN,
        properties=(
            Property(
                property_id="paper-flammable",
                name="mudah_terbakar",
                description="Sifat penguji yang telah dikurasi.",
                scope_conditions=property_conditions,
                confidence_level=ConfidenceLevel.KNOWN,
                provenance=verified("paper-flammable"),
            ),
        ),
        provenance=verified("paper"),
    )
    return ConceptStore((actor, target))


def test_c01_known_requires_all_verified_prerequisites():
    result = InferenceEngine(make_verified_store()).infer("api", "kertas")

    assert result.status is ConfidenceLevel.KNOWN
    assert result.rule_id == "C-01"
    assert "dapat membakar" in result.conclusion
    assert "relation:fire-can-burn" in result.evidence
    assert "property:paper-flammable" in result.evidence
    assert not result.uncertainty


def test_c02_unverified_v3a_seed_is_only_partial():
    result = InferenceEngine(ConceptStore()).infer("api", "kertas")

    assert result.status is ConfidenceLevel.PARTIAL
    assert result.rule_id == "C-02"
    assert result.uncertainty


def test_c02_missing_relation_never_promotes_shared_property_to_known():
    result = InferenceEngine(
        make_verified_store(relation=False)
    ).infer("api", "kertas")

    assert result.status is ConfidenceLevel.PARTIAL
    assert result.rule_id == "C-02"
    assert any("saja tidak membuktikan" in reason for reason in result.reasons)
    assert "relation:fire-can-burn" not in result.evidence


def test_c04_shared_property_between_two_concepts_is_not_a_relation():
    shared = Property(
        property_id="combustible",
        name="mudah_terbakar",
        description="Sifat sama yang sengaja dibagikan pada dua konsep.",
        confidence_level=ConfidenceLevel.KNOWN,
        provenance=verified("shared-property"),
    )
    wood = Concept(
        concept_id="wood",
        name="kayu",
        description="Konsep kayu untuk pengujian C-04.",
        data_status=ConfidenceLevel.KNOWN,
        properties=(shared,),
        provenance=verified("wood"),
    )
    paper = Concept(
        concept_id="paper",
        name="kertas",
        description="Konsep kertas untuk pengujian C-04.",
        data_status=ConfidenceLevel.KNOWN,
        properties=(shared,),
        provenance=verified("paper"),
    )
    result = InferenceEngine(ConceptStore((wood, paper))).infer("kayu", "kertas")

    assert result.status is ConfidenceLevel.PARTIAL
    assert result.rule_id == "C-02"
    assert any("C-04" in reason for reason in result.reasons)
    assert "dapat membakar" not in result.conclusion


def test_c03_unknown_when_neither_concept_exists():
    result = InferenceEngine(ConceptStore()).infer("plasma-kuantum", "benda-x")

    assert result.status is ConfidenceLevel.UNKNOWN
    assert result.rule_id == "C-03"


def test_c02_relation_target_must_explicitly_match_required_property():
    result = InferenceEngine(
        make_verified_store(relation_target="property:material_organik")
    ).infer("api", "kertas")

    assert result.status is ConfidenceLevel.PARTIAL
    assert result.rule_id == "C-02"
    assert "relation:fire-can-burn" not in result.evidence


def test_c02_all_declared_conditions_must_be_supplied_exactly():
    store = make_verified_store(
        relation_conditions=(("temperature", "high"),),
        property_conditions=(("state", "dry"),),
    )
    engine = InferenceEngine(store)

    incomplete = engine.infer("api", "kertas")
    complete = engine.infer(
        "api",
        "kertas",
        conditions={"temperature": "high", "state": "dry"},
    )

    assert incomplete.status is ConfidenceLevel.PARTIAL
    assert complete.status is ConfidenceLevel.KNOWN
    assert complete.rule_id == "C-01"


def test_inference_result_exposes_only_defined_confidence_values():
    assert {level.value for level in ConfidenceLevel} == {
        "KNOWN", "PARTIAL", "UNKNOWN",
    }
