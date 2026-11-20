"""Deterministic concept, relation, fact, and provenance management."""

from __future__ import annotations

import json
from pathlib import Path
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

    def load_dataset_record(self, record: dict[str, Any]) -> dict[str, Any]:
        """Load one enrichment JSONL record without changing its source data.

        Dataset records use fact_id/predicate/verification_status, while the
        runtime store uses id/relation/status. Draft records remain unverified
        by mapping them to the engine's existing hypothesis status.
        """
        if not isinstance(record, dict):
            raise TypeError("dataset record must be a dictionary")

        fact_id = record.get("fact_id")
        subject = record.get("subject")
        relation = record.get("predicate")
        object_value = record.get("object")
        source = record.get("source")
        source_status = record.get("verification_status")

        if not isinstance(fact_id, str) or not fact_id.strip():
            raise ValueError("dataset record requires a non-empty fact_id")
        if self.fact_store.get(fact_id) is not None:
            raise ValueError(f"duplicate dataset fact_id: {fact_id}")
        if not isinstance(subject, str) or not subject.strip():
            raise ValueError(f"{fact_id}: subject must be a non-empty string")
        if not isinstance(relation, str) or not relation.strip():
            raise ValueError(f"{fact_id}: predicate must be a non-empty string")
        if not isinstance(source, str) or not source.strip():
            raise ValueError(f"{fact_id}: source must be a non-empty string")

        if isinstance(object_value, list):
            if not object_value or not all(
                isinstance(item, (str, int, float)) and not isinstance(item, bool)
                for item in object_value
            ):
                raise ValueError(f"{fact_id}: object list must contain scalar values")
            object_text = ", ".join(str(item) for item in object_value)
        elif isinstance(object_value, (str, int, float)) and not isinstance(object_value, bool):
            object_text = str(object_value)
        else:
            raise ValueError(f"{fact_id}: object must be a string, number, or scalar list")

        status_map = {
            "draft": "hypothesis",
            "verified": "verified",
            "hypothesis": "hypothesis",
            "conflicting": "conflicting",
        }
        if source_status not in status_map:
            raise ValueError(
                f"{fact_id}: unsupported verification_status {source_status!r}"
            )
        status = status_map[source_status]

        fact = {
            "id": fact_id,
            "subject": self.add_concept(subject),
            "relation": self.add_relation(relation),
            "object": self.add_concept(object_text),
            "status": status,
            "source": source.strip(),
            # Keep the original record, including qualifiers and review metadata.
            "dataset_record": dict(record),
        }
        self.fact_store.load(fact)
        self.provenance.load({
            "fact_id": fact_id,
            "source": source.strip(),
            "status": status,
        })
        return self.fact_store.get(fact_id)  # type: ignore[return-value]

    def load_jsonl_directory(self, directory: str | Path) -> int:
        """Load every batch_*.jsonl fact file in deterministic filename order."""
        dataset_dir = Path(directory)
        if not dataset_dir.is_dir():
            raise FileNotFoundError(f"Knowledge dataset directory not found: {dataset_dir}")

        files = sorted(dataset_dir.glob("batch_*.jsonl"))
        if not files:
            raise FileNotFoundError(f"No batch_*.jsonl files found in {dataset_dir}")

        loaded = 0
        for path in files:
            with path.open("r", encoding="utf-8") as stream:
                for line_number, line in enumerate(stream, start=1):
                    if not line.strip():
                        continue
                    try:
                        record = json.loads(line)
                    except json.JSONDecodeError as exc:
                        raise ValueError(
                            f"Invalid JSON in {path}:{line_number}: {exc.msg}"
                        ) from exc
                    try:
                        self.load_dataset_record(record)
                    except (TypeError, ValueError) as exc:
                        raise ValueError(
                            f"Invalid Knowledge record in {path}:{line_number}: {exc}"
                        ) from exc
                    loaded += 1
        return loaded

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
            and not all(
                "dataset_record" in fact and fact.get("status") == "hypothesis"
                for fact in facts
            )
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
