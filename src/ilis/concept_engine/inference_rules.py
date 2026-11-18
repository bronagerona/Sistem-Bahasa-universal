"""Deterministic, standalone inference rules for the ILIS V3-B milestone.

This module reads a static ConceptStore only. It does not call the legacy
KnowledgeEngine, ILIS Core, SQLite, or the V2.2 session layer.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from ilis.concept_engine.concept_store import (
    ConfidenceLevel,
    Concept,
    ConceptStore,
    Property,
    ProvenanceRef,
    Relation,
)


@dataclass(frozen=True, slots=True)
class InferenceResult:
    """Auditable result of one concept-level inference attempt."""

    status: ConfidenceLevel
    conclusion: str
    evidence: tuple[str, ...] = ()
    reasons: tuple[str, ...] = ()
    uncertainty: tuple[str, ...] = ()
    rule_id: str = "C-03"


class InferenceEngine:
    """Evaluate the C-01..C-04 rules against a read-only ConceptStore."""

    def __init__(self, concept_store: ConceptStore) -> None:
        if not isinstance(concept_store, ConceptStore):
            raise TypeError("concept_store must be a ConceptStore")
        self._store = concept_store

    def infer(
        self,
        subject: str,
        object: str,
        *,
        relation_type: str = "can_burn",
        required_property: str = "mudah_terbakar",
        conditions: Mapping[str, str] | None = None,
    ) -> InferenceResult:
        """Infer whether subject can interact with object through a named property.

        KNOWN requires a matching explicit relation, the object's matching
        property, complete KNOWN records, verified provenance on every record,
        and all declared conditions supplied exactly. A shared property alone
        can never establish a relation (C-04).
        """
        subject_concept = self._store.lookup(subject)
        object_concept = self._store.lookup(object)
        supplied_conditions = dict(conditions or {})

        if subject_concept is None and object_concept is None:
            return InferenceResult(
                status=ConfidenceLevel.UNKNOWN,
                conclusion="Data konsep atau relasi yang relevan belum tersedia.",
                reasons=("Tidak ada konsep subjek maupun objek di ConceptStore.",),
                uncertainty=("Kedua konsep tidak ditemukan.",),
                rule_id="C-03",
            )

        evidence: list[str] = []
        reasons: list[str] = []
        uncertainty: list[str] = []

        if subject_concept is not None:
            evidence.append(f"concept:{subject_concept.concept_id}")
        else:
            uncertainty.append(f"Konsep subjek '{subject}' tidak ditemukan.")

        if object_concept is not None:
            evidence.append(f"concept:{object_concept.concept_id}")
        else:
            uncertainty.append(f"Konsep objek '{object}' tidak ditemukan.")

        matching_properties: list[Property] = []
        if object_concept is not None:
            matching_properties = [
                prop for prop in object_concept.properties
                if self._same(prop.name, required_property)
                or self._same(prop.property_id, required_property)
            ]
            evidence.extend(f"property:{prop.property_id}" for prop in matching_properties)

        matching_relations: list[Relation] = []
        if subject_concept is not None:
            matching_relations = [
                relation
                for relation in subject_concept.relations
                if self._same(relation.relation_type, relation_type)
                and self._relation_targets_property(
                    relation, matching_properties, required_property
                )
            ]
            evidence.extend(f"relation:{rel.relation_id}" for rel in matching_relations)

        if not matching_properties and not matching_relations:
            return InferenceResult(
                status=ConfidenceLevel.UNKNOWN,
                conclusion="Belum ada data relevan yang cukup untuk menyimpulkan hubungan tersebut.",
                evidence=tuple(evidence),
                reasons=("Tidak ditemukan sifat objek atau relasi kemampuan yang cocok.",),
                uncertainty=tuple(uncertainty or ("Data konsep yang tersedia tidak mendukung aturan ini.",)),
                rule_id="C-03",
            )

        if not matching_properties:
            uncertainty.append(
                f"Objek belum memiliki sifat '{required_property}' yang tercatat."
            )
        if not matching_relations:
            uncertainty.append(
                f"Tidak ada relasi eksplisit '{relation_type}' yang menerima sifat '{required_property}'."
            )
            if matching_properties:
                reasons.append(
                    "Sifat objek saja tidak membuktikan kemampuan atau hubungan sebab-akibat (C-04)."
                )

        if subject_concept is not None and not self._record_is_fully_verified(subject_concept):
            uncertainty.append("Data konsep subjek belum lengkap atau provenance belum terverifikasi.")
        if object_concept is not None and not self._record_is_fully_verified(object_concept):
            uncertainty.append("Data konsep objek belum lengkap atau provenance belum terverifikasi.")

        property_is_known = any(self._record_is_fully_verified(p) for p in matching_properties)
        relation_is_known = any(self._record_is_fully_verified(r) for r in matching_relations)

        condition_complete = False
        condition_uncertainties: list[str] = []
        for relation in matching_relations:
            missing = self._missing_conditions(relation.conditions, supplied_conditions)
            if not missing:
                condition_complete = True
                break
            condition_uncertainties.extend(missing)
        if matching_relations and not condition_complete:
            uncertainty.extend(condition_uncertainties or [
                "Kondisi penerapan relasi belum dapat dipastikan."
            ])

        property_conditions_complete = False
        property_condition_uncertainties: list[str] = []
        for prop in matching_properties:
            missing = self._missing_conditions(prop.scope_conditions, supplied_conditions)
            if not missing:
                property_conditions_complete = True
                break
            property_condition_uncertainties.extend(missing)
        if matching_properties and not property_condition_complete:
            uncertainty.extend(property_condition_uncertainties)

        subject_verified = (
            subject_concept is not None
            and self._record_is_fully_verified(subject_concept)
        )
        object_verified = (
            object_concept is not None
            and self._record_is_fully_verified(object_concept)
        )

        if (
            subject_verified
            and object_verified
            and property_is_known
            and relation_is_known
            and condition_complete
            and property_condition_complete
            and matching_properties
            and matching_relations
        ):
            positive_relation = next(
                (rel for rel in matching_relations if rel.polarity == "positive"
                 and self._record_is_fully_verified(rel)
                 and not self._missing_conditions(rel.conditions, supplied_conditions)),
                None,
            )
            if positive_relation is not None:
                reasons.append(
                    "Sifat objek, relasi kemampuan yang secara eksplisit menerima sifat tersebut, "
                    "provenance, dan seluruh kondisi telah terverifikasi (C-01)."
                )
                return InferenceResult(
                    status=ConfidenceLevel.KNOWN,
                    conclusion=f"{subject_concept.name} dapat {self._verb_for(relation_type)} {object_concept.name}.",
                    evidence=tuple(evidence),
                    reasons=tuple(reasons),
                    uncertainty=(),
                    rule_id="C-01",
                )

        if not reasons:
            reasons.append(
                "Terdapat data yang relevan, tetapi satu atau lebih prasyarat C-01 belum terpenuhi (C-02)."
            )
        return InferenceResult(
            status=ConfidenceLevel.PARTIAL,
            conclusion="Ada indikasi yang relevan, tetapi hubungan tersebut belum dapat dipastikan.",
            evidence=tuple(evidence),
            reasons=tuple(reasons),
            uncertainty=tuple(dict.fromkeys(uncertainty or (
                "Verifikasi, relasi, atau kondisi wajib belum lengkap.",
            ))),
            rule_id="C-02",
        )

    @staticmethod
    def _same(left: str, right: str) -> bool:
        return " ".join(left.casefold().replace("-", "_").split()) == (
            " ".join(right.casefold().replace("-", "_").split())
        )

    @classmethod
    def _relation_targets_property(
        cls,
        relation: Relation,
        properties: tuple[Property, ...] | list[Property],
        required_property: str,
    ) -> bool:
        target = relation.object_id
        accepted_targets = {
            f"property:{required_property}",
            required_property,
        }
        for prop in properties:
            accepted_targets.update({
                f"property:{prop.name}",
                f"property:{prop.property_id}",
                prop.name,
                prop.property_id,
            })
        return any(cls._same(target, candidate) for candidate in accepted_targets)

    @staticmethod
    def _missing_conditions(
        required: tuple[tuple[str, str], ...],
        supplied: Mapping[str, str],
    ) -> tuple[str, ...]:
        return tuple(
            f"Kondisi '{key}={value}' belum dipenuhi atau tidak diberikan."
            for key, value in required
            if supplied.get(key) != value
        )

    @staticmethod
    def _record_is_fully_verified(record: Concept | Property | Relation) -> bool:
        if isinstance(record, Concept):
            status = record.data_status
        else:
            status = record.confidence_level
        provenance: tuple[ProvenanceRef, ...] = record.provenance
        return (
            status is ConfidenceLevel.KNOWN
            and bool(provenance)
            and all(ref.verification_status == "verified" for ref in provenance)
        )

    @staticmethod
    def _verb_for(relation_type: str) -> str:
        if relation_type == "can_burn":
            return "membakar"
        return relation_type.replace("_", " ")
