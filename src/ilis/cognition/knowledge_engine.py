"""Deterministic concept, relation, fact, and provenance management.

This module stores claims and detects direct conflicts. It does not infer new
knowledge, reason over relations, verify sources, or call an AI/LLM service.
"""

from __future__ import annotations

from typing import Any

from ilis.cognition.concept_store import ConceptStore
from ilis.cognition.fact_store import FactStore
from ilis.cognition.provenance_store import ProvenanceStore
from ilis.cognition.relation_store import RelationStore


FACT_STATUSES = frozenset({"verified", "hypothesis", "conflicting"})


class KnowledgeEngine:
    """Manage explicit knowledge triples and their provenance."""

    def __init__(self, seed_core_knowledge: bool = True) -> None:
        self.concept_store = ConceptStore()
        self.relation_store = RelationStore()
        self.fact_store = FactStore()
        self.provenance = ProvenanceStore()
        if seed_core_knowledge:
            self.add_fact("api", "can_burn", "kayu", "verified", "core_knowledge")
            self.add_fact("rumah", "made_of", "kayu", "verified", "core_knowledge")

    def add_concept(self, concept: str) -> str:
        return self.concept_store.add(concept)

    def add_relation(self, relation: str) -> str:
        return self.relation_store.add(relation)

    def add_fact(
        self,
        subject: str,
        relation: str,
        object_: str,
        status: str = "hypothesis",
        source: str = "user_input",
    ) -> dict[str, Any]:
        """Store a fact and mark same-subject/relation disagreements as conflicting."""
        subject_key = self.add_concept(subject)
        relation_key = self.add_relation(relation)
        object_key = self.add_concept(object_)
        if status not in FACT_STATUSES:
            raise ValueError(f"status must be one of {sorted(FACT_STATUSES)}")
        if not isinstance(source, str) or not source.strip():
            raise ValueError("source must be a non-empty string")

        fact = self.fact_store.add(
            subject_key, relation_key, object_key, status, source.strip()
        )
        self.provenance.record(fact["id"], fact["source"], fact["status"])
        self._mark_conflicts(subject_key, relation_key)
        return self.fact_store.get(fact["id"])  # type: ignore[return-value]

    def search_facts(self, concept: str) -> list[dict[str, Any]]:
        """Find facts where concept appears as subject or object."""
        normalized = " ".join(concept.casefold().split())
        return self.fact_store.find_by_concept(normalized)

    def detect_conflicts(self) -> list[list[dict[str, Any]]]:
        """Return groups sharing subject/relation but asserting different objects."""
        groups: dict[tuple[str, str], list[dict[str, Any]]] = {}
        for fact in self.fact_store.all():
            groups.setdefault((fact["subject"], fact["relation"]), []).append(fact)
        conflicts = []
        for facts in groups.values():
            if len({fact["object"] for fact in facts}) > 1:
                conflicts.append(facts)
        return conflicts

    def ingest_semantic_result(
        self, result: dict[str, Any], source: str = "semantic_engine"
    ) -> dict[str, Any]:
        """Convert a supported, positive SVO assertion into a hypothesis fact.

        Semantic parsing confidence is not factual verification. Unsupported,
        incomplete, negated, or modal statements are not converted to triples.
        """
        if not isinstance(result, dict) or result.get("status") != "supported":
            return {"accepted": False, "fact": None, "reason": "semantic_result_not_supported"}
        semantics = result.get("semantics")
        if not isinstance(semantics, dict):
            return {"accepted": False, "fact": None, "reason": "missing_semantics"}
        if semantics.get("Intent") != "assertion":
            return {"accepted": False, "fact": None, "reason": "non_assertion"}
        if semantics.get("Negation", "none") != "none":
            return {"accepted": False, "fact": None, "reason": "negation_not_representable"}
        if semantics.get("Modality", "none") != "none":
            return {"accepted": False, "fact": None, "reason": "modality_not_representable"}

        subject = semantics.get("Actor")
        relation = semantics.get("Predicate")
        object_ = semantics.get("Patient/Object")
        if not all(isinstance(value, str) and value.strip() for value in (subject, relation, object_)):
            return {"accepted": False, "fact": None, "reason": "incomplete_subject_relation_object"}

        fact = self.add_fact(
            subject, relation, object_, status="hypothesis", source=source
        )
        return {
            "accepted": True,
            "fact": fact,
            "reason": "stored_as_hypothesis_not_verified",
        }

    def get_provenance(self, fact_id: str) -> dict[str, Any] | None:
        return self.provenance.get(fact_id)

    def _mark_conflicts(self, subject: str, relation: str) -> None:
        matching = [
            fact for fact in self.fact_store.all()
            if fact["subject"] == subject and fact["relation"] == relation
        ]
        if len({fact["object"] for fact in matching}) <= 1:
            return
        for fact in matching:
            self.fact_store.update_status(fact["id"], "conflicting")
            self.provenance.update_status(fact["id"], "conflicting")
