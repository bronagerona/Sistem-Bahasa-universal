"""Isolated end-to-end proof for Concept Engine KNOWN status.

All verified records below are test fixtures only. They are never added to
production ConceptStore seeds or KnowledgeEngine facts.
"""

from ilis.cognition import KnowledgeEngine
from ilis.cognition.reasoning_engine import ReasoningEngine
from ilis.concept_engine import (
    ConfidenceLevel,
    Concept,
    ConceptStore,
    InferenceEngine,
    Property,
    ProvenanceRef,
    Relation,
)
from ilis.generation import LanguageGenerator
from ilis.semantics.semantic_engine import SemanticEngine


REASONING_KEYS = {
    "conclusion",
    "confidence_score",
    "evidence",
    "reasoning_type",
    "reasons",
    "uncertainty",
}


def verified(item_id):
    return (
        ProvenanceRef(
            source_id=f"isolated-known-test:{item_id}",
            source="curated_test_fixture_only",
            verification_status="verified",
            note="Synthetic fixture for isolated pipeline verification; not production data.",
        ),
    )


def verified_api_wood_store():
    api = Concept(
        concept_id="fire",
        name="api",
        description="Fixture konsep api dengan data lengkap.",
        data_status=ConfidenceLevel.KNOWN,
        provenance=verified("fire"),
        relations=(
            Relation(
                relation_id="fire-can-burn-wood",
                subject_concept_id="fire",
                relation_type="can_burn",
                object_id="property:mudah_terbakar",
                confidence_level=ConfidenceLevel.KNOWN,
                provenance=verified("fire-can-burn-wood"),
            ),
        ),
    )
    wood = Concept(
        concept_id="wood",
        name="kayu",
        description="Fixture konsep kayu dengan data lengkap.",
        data_status=ConfidenceLevel.KNOWN,
        properties=(
            Property(
                property_id="wood-flammable",
                name="mudah_terbakar",
                description="Sifat kayu untuk fixture uji terisolasi.",
                confidence_level=ConfidenceLevel.KNOWN,
                provenance=verified("wood-flammable"),
            ),
        ),
        provenance=verified("wood"),
    )
    return ConceptStore((api, wood))


def semantic_question():
    text = "Apakah api bisa membakar kayu?"
    return SemanticEngine().analyze(
        {
            "contract_version": "1.0",
            "original_text": text,
            "ilve": {
                "normalized_text": text.casefold(),
                "tokens": ["apakah", "api", "bisa", "membakar", "kayu", "?"],
                "variation_hints": [],
            },
        }
    )


def test_known_status_runs_end_to_end_through_concept_engine_and_language_generator():
    # Disable all legacy seeded facts so KnowledgeEngine cannot intercept the
    # question. The KNOWN result must come from this test-only ConceptStore.
    reasoning_engine = ReasoningEngine(
        KnowledgeEngine(seed_core_knowledge=False),
        concept_store=verified_api_wood_store(),
    )
    semantic = semantic_question()

    reasoning = reasoning_engine.infer_semantic(semantic)
    generated = LanguageGenerator().generate(
        reasoning,
        semantic_result=semantic,
    )

    assert semantic["status"] == "supported"
    assert len(semantic["semantics"]) == 12
    assert set(reasoning) == REASONING_KEYS
    assert reasoning["reasoning_type"] == "concept_inference_known"
    # Existing V3-C confidence mapping is 0.72; keep the public API unchanged.
    assert reasoning["confidence_score"] == 0.72
    assert "Tahu Pasti" in reasoning["conclusion"]
    assert "concept:fire" in reasoning["evidence"]
    assert "concept:wood" in reasoning["evidence"]
    assert "relation:fire-can-burn-wood" in reasoning["evidence"]
    assert "property:wood-flammable" in reasoning["evidence"]

    assert generated["reasoning_type"] == "concept_inference_known"
    assert generated["confidence_score"] == 0.72
    assert generated["uncertainty_preserved"] is False
    assert generated["text"] == (
        "Ya, berdasarkan fakta yang tersedia, api bisa membakar kayu."
    )
    assert "dugaan" not in generated["text"].casefold()
