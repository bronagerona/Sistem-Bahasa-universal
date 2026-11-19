"""V3-C integration tests: legacy exact facts first, Concept Engine fallback second."""

from ilis.cognition import KnowledgeEngine
from ilis.cognition.reasoning_engine import ReasoningEngine
from ilis.concept_engine import (
    ConfidenceLevel,
    Concept,
    ConceptStore,
    Property,
    ProvenanceRef,
    Relation,
)
from ilis.interfaces import ILISCore
from ilis.semantics.semantic_engine import SemanticEngine


REASONING_KEYS = {
    "conclusion",
    "confidence_score",
    "evidence",
    "reasoning_type",
    "reasons",
    "uncertainty",
}


def semantic_question(actor="api", predicate="membakar", patient="kertas"):
    text = f"Apakah {actor} bisa {predicate} {patient}?"
    tokens = ["apakah", actor, "bisa", predicate, patient, "?"]
    return SemanticEngine().analyze({
        "contract_version": "1.0",
        "original_text": text,
        "ilve": {
            "normalized_text": text.casefold(),
            "tokens": tokens,
            "variation_hints": [],
        },
    })


def verified(item_id):
    return (
        ProvenanceRef(
            source_id=f"test:{item_id}",
            source="curated_test_fixture",
            verification_status="verified",
        ),
    )


def verified_concept_store():
    api = Concept(
        concept_id="fire",
        name="api",
        description="Konsep api untuk fixture integrasi.",
        data_status=ConfidenceLevel.KNOWN,
        provenance=verified("fire"),
        relations=(
            Relation(
                relation_id="fire-can-burn",
                subject_concept_id="fire",
                relation_type="can_burn",
                object_id="property:mudah_terbakar",
                confidence_level=ConfidenceLevel.KNOWN,
                provenance=verified("fire-can-burn"),
            ),
        ),
    )
    paper = Concept(
        concept_id="paper",
        name="kertas",
        description="Konsep kertas untuk fixture integrasi.",
        data_status=ConfidenceLevel.KNOWN,
        properties=(
            Property(
                property_id="paper-flammable",
                name="mudah_terbakar",
                description="Sifat kertas terverifikasi untuk fixture.",
                confidence_level=ConfidenceLevel.KNOWN,
                provenance=verified("paper-flammable"),
            ),
        ),
        provenance=verified("paper"),
    )
    return ConceptStore((api, paper))


def test_v3c_fallback_api_to_paper_when_legacy_exact_fact_is_absent():
    # seed_core_knowledge=False intentionally removes all legacy exact facts.
    knowledge = KnowledgeEngine(seed_core_knowledge=False)
    reasoning = ReasoningEngine(knowledge)

    result = reasoning.infer_semantic(semantic_question())

    assert set(result) == REASONING_KEYS
    assert result["reasoning_type"] == "concept_inference_partial"
    assert result["confidence_score"] == 0.48
    assert "Tahu Sebagian" in result["conclusion"]
    assert any(item == "property:paper-flammable" for item in result["evidence"])
    assert any("fallback Concept Engine V3" in reason for reason in result["reasons"])


def test_v3c_legacy_exact_fact_wins_and_fallback_does_not_replace_it():
    # The normal KnowledgeEngine seed includes the exact api-can_burn-kertas fact.
    knowledge = KnowledgeEngine()
    reasoning = ReasoningEngine(knowledge)

    result = reasoning.infer_semantic(semantic_question())

    assert set(result) == REASONING_KEYS
    assert result["reasoning_type"] == "verified_inference"
    assert result["evidence"] == ["fact_3"]
    assert "Tahu Sebagian" not in result["conclusion"]
    assert not any("fallback Concept Engine V3" in reason for reason in result["reasons"])


def test_v3c_partial_status_maps_to_existing_reasoning_fields():
    reasoning = ReasoningEngine(KnowledgeEngine(seed_core_knowledge=False))

    result = reasoning.infer_semantic(semantic_question(patient="kertas"))

    assert result["reasoning_type"] == "concept_inference_partial"
    assert 0.0 < result["confidence_score"] < 1.0
    assert result["evidence"]
    assert result["uncertainty"]


def test_v3c_unknown_status_maps_to_existing_reasoning_fields():
    reasoning = ReasoningEngine(KnowledgeEngine(seed_core_knowledge=False))

    result = reasoning.infer_semantic(
        semantic_question(patient="plasma-kuantum")
    )

    assert set(result) == REASONING_KEYS
    assert result["reasoning_type"] == "concept_inference_unknown"
    assert result["confidence_score"] == 0.0
    assert "Tidak Tahu" in result["conclusion"]
    assert result["uncertainty"]


def test_v3c_known_status_maps_without_adding_reasoning_keys():
    reasoning = ReasoningEngine(
        KnowledgeEngine(seed_core_knowledge=False),
        concept_store=verified_concept_store(),
    )

    result = reasoning.infer_semantic(semantic_question())

    assert set(result) == REASONING_KEYS
    assert result["reasoning_type"] == "concept_inference_known"
    assert result["confidence_score"] == 0.72
    assert "Tahu Pasti" in result["conclusion"]
    assert "relation:fire-can-burn" in result["evidence"]


def test_ilis_core_wires_v3_fallback_without_changing_semantic_contract():
    core = ILISCore(seed_core_knowledge=False)
    semantic = core.analyze_text("Apakah api bisa membakar kertas?")
    result = core.reasoning_engine.infer_semantic(semantic)

    assert len(semantic["semantics"]) == 12
    assert set(result) == REASONING_KEYS
    assert result["reasoning_type"] == "concept_inference_partial"
