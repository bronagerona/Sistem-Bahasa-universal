"""Deterministic concept, relation, fact, and provenance management."""

from __future__ import annotations

from typing import Any

from ilis.cognition.concept_store import ConceptStore
from ilis.cognition.fact_store import FactStore
from ilis.cognition.provenance_store import ProvenanceStore
from ilis.cognition.relation_store import RelationStore


FACT_STATUSES = frozenset({"verified", "hypothesis", "conflicting"})
# A source can burn multiple materials; these are cumulative, not exclusive facts.
MULTI_VALUED_RELATIONS = frozenset({"can_burn"})


class KnowledgeEngine:
    """Manage explicit knowledge triples and their provenance.

    storage_provider is optional. Without it, V1 behavior remains in-memory.
    """

    def __init__(
        self,
        seed_core_knowledge: bool = True,
        storage_provider: Any | None = None,
    ) -> None:
        self.storage_provider = storage_provider
        self.seed_core_knowledge = seed_core_knowledge
        self.concept_store = ConceptStore()
        self.relation_store = RelationStore()
        self.fact_store = FactStore()
        self.provenance = ProvenanceStore()

        if self.storage_provider is not None:
            for fact in self.storage_provider.load_facts():
                self.fact_store.load(fact)
                self.concept_store.add(fact["subject"])
                self.concept_store.add(fact["object"])
                self.relation_store.add(fact["relation"])
            for record in self.storage_provider.load_provenance():
                self.provenance.load(record)

        if seed_core_knowledge:
            # Seed each canonical fact independently so existing SQLite stores
            # receive newly added knowledge without duplicating prior records.
            core_facts = (
                ("api", "can_burn", "kayu"),
                ("rumah", "made_of", "kayu"),
                ("api", "can_burn", "kertas"),
            )
            existing = {
                (fact["subject"], fact["relation"], fact["object"])
                for fact in self.fact_store.all()
            }
            for subject, relation, object_ in core_facts:
                if (subject, relation, object_) not in existing:
                    self.add_fact(
                        subject, relation, object_,
                        status="verified", source="core_knowledge",
                    )

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
        provenance = self.provenance.record(fact["id"], fact["source"], fact["status"])
        self._persist_fact_and_provenance(fact, provenance)
        self._mark_conflicts(subject_key, relation_key)
        return self.fact_store.get(fact["id"])  # type: ignore[return-value]

    def _persist_fact_and_provenance(
        self, fact: dict[str, Any], record: dict[str, Any]
    ) -> None:
        if self.storage_provider is not None:
            atomic_save = getattr(self.storage_provider, "save_fact_with_provenance", None)
            if atomic_save is not None:
                atomic_save(fact, record)
            else:
                # Compatibility for third-party storage providers implementing
                # the older two-method protocol.
                self.storage_provider.save_fact(fact)
                self.storage_provider.save_provenance(record)

    def _persist_fact(self, fact: dict[str, Any]) -> None:
        if self.storage_provider is not None:
            self.storage_provider.save_fact(fact)

    def _persist_provenance(self, fact_id: str) -> None:
        if self.storage_provider is not None:
            record = self.provenance.get(fact_id)
            if record is not None:
                self.storage_provider.save_provenance(record)

    def search_facts(self, concept: str) -> list[dict[str, Any]]:
        normalized = " ".join(concept.casefold().split())
        return self.fact_store.find_by_concept(normalized)

    def detect_conflicts(self) -> list[list[dict[str, Any]]]:
        groups: dict[tuple[str, str], list[dict[str, Any]]] = {}
        for fact in self.fact_store.all():
            groups.setdefault((fact["subject"], fact["relation"]), []).append(fact)
        return [
            facts for (subject, relation), facts in groups.items()
            if len({fact["object"] for fact in facts}) > 1
            and not (
                relation in MULTI_VALUED_RELATIONS
                and all(
                    fact.get("status") == "verified"
                    and fact.get("source") == "core_knowledge"
                    for fact in facts
                )
            )
        ]

    def ingest_semantic_result(
        self, result: dict[str, Any], source: str = "semantic_engine"
    ) -> dict[str, Any]:
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

        fact = self.add_fact(subject, relation, object_, status="hypothesis", source=source)
        return {"accepted": True, "fact": fact, "reason": "stored_as_hypothesis_not_verified"}

    def get_provenance(self, fact_id: str) -> dict[str, Any] | None:
        return self.provenance.get(fact_id)

    def _mark_conflicts(self, subject: str, relation: str) -> None:
        matching = [
            fact for fact in self.fact_store.all()
            if fact["subject"] == subject and fact["relation"] == relation
        ]
        if relation in MULTI_VALUED_RELATIONS and all(
            fact.get("status") == "verified" and fact.get("source") == "core_knowledge"
            for fact in matching
        ):
            return
        if len({fact["object"] for fact in matching}) <= 1:
            return
        for fact in matching:
            self.fact_store.update_status(fact["id"], "conflicting")
            self.provenance.update_status(fact["id"], "conflicting")
            fact_record = self.fact_store.get(fact["id"])
            provenance_record = self.provenance.get(fact["id"])
            if fact_record is not None and provenance_record is not None:
                self._persist_fact_and_provenance(fact_record, provenance_record)
