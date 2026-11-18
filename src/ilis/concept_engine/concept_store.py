"""Static, deterministic concept data for the ILIS V3-A milestone.

This module is deliberately standalone: it does not import or modify the
legacy KnowledgeEngine, ILIS Core, SQLite, or the V2.2 session layer.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable


class ConfidenceLevel(str, Enum):
    """Evidence completeness labels shared by the planned V3 inference layer."""

    KNOWN = "KNOWN"
    PARTIAL = "PARTIAL"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True, slots=True)
class ProvenanceRef:
    """Traceable origin and verification state for a seeded data item."""

    source_id: str
    source: str
    verification_status: str = "unverified"
    note: str = ""

    def __post_init__(self) -> None:
        if not self.source_id.strip():
            raise ValueError("source_id must be a non-empty string")
        if not self.source.strip():
            raise ValueError("source must be a non-empty string")
        if self.verification_status not in {"verified", "unverified"}:
            raise ValueError(
                "verification_status must be 'verified' or 'unverified'"
            )


@dataclass(frozen=True, slots=True)
class Property:
    """A named property attached to a concept, with explicit provenance."""

    property_id: str
    name: str
    description: str
    value_type: str = "boolean"
    scope_conditions: tuple[tuple[str, str], ...] = ()
    confidence_level: ConfidenceLevel = ConfidenceLevel.PARTIAL
    provenance: tuple[ProvenanceRef, ...] = ()

    def __post_init__(self) -> None:
        if not self.property_id.strip() or not self.name.strip():
            raise ValueError("property_id and name must be non-empty")
        if not self.description.strip():
            raise ValueError("description must be a non-empty string")
        if not isinstance(self.confidence_level, ConfidenceLevel):
            raise TypeError("confidence_level must be a ConfidenceLevel")
        object.__setattr__(self, "scope_conditions", tuple(self.scope_conditions))
        object.__setattr__(self, "provenance", tuple(self.provenance))


@dataclass(frozen=True, slots=True)
class Relation:
    """An explicit relation between a concept and another concept/property."""

    relation_id: str
    subject_concept_id: str
    relation_type: str
    object_id: str
    conditions: tuple[tuple[str, str], ...] = ()
    polarity: str = "positive"
    confidence_level: ConfidenceLevel = ConfidenceLevel.PARTIAL
    provenance: tuple[ProvenanceRef, ...] = ()

    def __post_init__(self) -> None:
        for field_name in (
            "relation_id",
            "subject_concept_id",
            "relation_type",
            "object_id",
        ):
            if not getattr(self, field_name).strip():
                raise ValueError(f"{field_name} must be a non-empty string")
        if self.polarity not in {"positive", "negative"}:
            raise ValueError("polarity must be 'positive' or 'negative'")
        if not isinstance(self.confidence_level, ConfidenceLevel):
            raise TypeError("confidence_level must be a ConfidenceLevel")
        object.__setattr__(self, "conditions", tuple(self.conditions))
        object.__setattr__(self, "provenance", tuple(self.provenance))


@dataclass(frozen=True, slots=True)
class Concept:
    """Canonical concept record and its directly attached static data."""

    concept_id: str
    name: str
    description: str
    parent_categories: tuple[str, ...] = ()
    aliases: tuple[str, ...] = ()
    data_status: ConfidenceLevel = ConfidenceLevel.PARTIAL
    properties: tuple[Property, ...] = ()
    relations: tuple[Relation, ...] = ()
    provenance: tuple[ProvenanceRef, ...] = ()

    def __post_init__(self) -> None:
        for field_name in ("concept_id", "name", "description"):
            if not getattr(self, field_name).strip():
                raise ValueError(f"{field_name} must be a non-empty string")
        if not isinstance(self.data_status, ConfidenceLevel):
            raise TypeError("data_status must be a ConfidenceLevel")
        object.__setattr__(self, "parent_categories", tuple(self.parent_categories))
        object.__setattr__(self, "aliases", tuple(self.aliases))
        object.__setattr__(self, "properties", tuple(self.properties))
        object.__setattr__(self, "relations", tuple(self.relations))
        object.__setattr__(self, "provenance", tuple(self.provenance))


def _seed_provenance(item_id: str, note: str) -> tuple[ProvenanceRef, ...]:
    # These are design-seed records, not claims of externally verified facts.
    # Keep them unverified until a source is reviewed and recorded explicitly.
    return (
        ProvenanceRef(
            source_id=f"v3a-seed:{item_id}",
            source="ilis_v3_design_seed",
            verification_status="unverified",
            note=note,
        ),
    )


def _build_seed_concepts() -> tuple[Concept, ...]:
    api = Concept(
        concept_id="fire",
        name="api",
        description="Fenomena panas yang dapat berkaitan dengan proses pembakaran.",
        parent_categories=("fenomena",),
        aliases=("nyala api",),
        data_status=ConfidenceLevel.PARTIAL,
        properties=(
            Property(
                property_id="fire-produces-heat",
                name="menghasilkan_panas",
                description="Dicatat sebagai sifat awal dalam seed desain.",
                confidence_level=ConfidenceLevel.PARTIAL,
                provenance=_seed_provenance("fire-produces-heat", "Perlu verifikasi sumber."),
            ),
            Property(
                property_id="fire-burns-combustible-material",
                name="dapat_membakar_material_mudah_terbakar",
                description="Kandidat kemampuan; bukan aturan inferensi pada tahap V3-A.",
                confidence_level=ConfidenceLevel.PARTIAL,
                provenance=_seed_provenance("fire-burns-combustible-material", "Perlu verifikasi sumber dan kondisi."),
            ),
        ),
        relations=(
            Relation(
                relation_id="fire-can-burn-combustible-material",
                subject_concept_id="fire",
                relation_type="can_burn",
                object_id="property:material-mudah-terbakar",
                conditions=(("condition", "seluruh kondisi pembakaran harus diketahui"),),
                confidence_level=ConfidenceLevel.PARTIAL,
                provenance=_seed_provenance("fire-can-burn-combustible-material", "Relasi kandidat; belum diverifikasi."),
            ),
        ),
        provenance=_seed_provenance("fire", "Konsep seed awal; perlu kurasi."),
    )
    kayu = Concept(
        concept_id="wood",
        name="kayu",
        description="Material yang umumnya berasal dari jaringan tumbuhan.",
        parent_categories=("material", "material_organik"),
        aliases=("wood",),
        data_status=ConfidenceLevel.PARTIAL,
        properties=(
            Property(
                property_id="wood-organic-material",
                name="material_organik",
                description="Kategori sifat awal dalam seed desain.",
                confidence_level=ConfidenceLevel.PARTIAL,
                provenance=_seed_provenance("wood-organic-material", "Perlu verifikasi sumber."),
            ),
        ),
        provenance=_seed_provenance("wood", "Konsep seed awal; perlu kurasi."),
    )
    kertas = Concept(
        concept_id="paper",
        name="kertas",
        description="Material lembaran yang umumnya berbasis serat selulosa.",
        parent_categories=("material", "material_selulosa"),
        aliases=("paper",),
        data_status=ConfidenceLevel.PARTIAL,
        properties=(
            Property(
                property_id="paper-cellulose-based",
                name="berbasis_serat_selulosa",
                description="Deskripsi umum dalam seed desain.",
                confidence_level=ConfidenceLevel.PARTIAL,
                provenance=_seed_provenance("paper-cellulose-based", "Perlu verifikasi sumber."),
            ),
            Property(
                property_id="paper-flammable",
                name="mudah_terbakar",
                description="Kandidat sifat; kondisi dan sumber perlu diverifikasi.",
                confidence_level=ConfidenceLevel.PARTIAL,
                provenance=_seed_provenance("paper-flammable", "Perlu verifikasi sumber dan kondisi."),
            ),
        ),
        provenance=_seed_provenance("paper", "Konsep seed awal; perlu kurasi."),
    )
    besi = Concept(
        concept_id="iron",
        name="besi",
        description="Unsur logam.",
        parent_categories=("unsur", "logam"),
        aliases=("iron",),
        data_status=ConfidenceLevel.PARTIAL,
        properties=(
            Property(
                property_id="iron-metal",
                name="bersifat_logam",
                description="Kategori sifat awal dalam seed desain.",
                confidence_level=ConfidenceLevel.PARTIAL,
                provenance=_seed_provenance("iron-metal", "Perlu verifikasi sumber."),
            ),
        ),
        provenance=_seed_provenance("iron", "Konsep seed awal; perlu kurasi."),
    )
    air = Concept(
        concept_id="water",
        name="air",
        description="Zat yang dikenal dalam bentuk cair pada kondisi lingkungan umum.",
        parent_categories=("zat", "cairan"),
        aliases=("water",),
        data_status=ConfidenceLevel.PARTIAL,
        properties=(
            Property(
                property_id="water-liquid-at-ambient",
                name="cair_pada_kondisi_lingkungan_umum",
                description="Pernyataan dibatasi pada kondisi lingkungan umum.",
                scope_conditions=(("kondisi", "lingkungan umum"),),
                confidence_level=ConfidenceLevel.PARTIAL,
                provenance=_seed_provenance("water-liquid-at-ambient", "Perlu verifikasi sumber dan rentang kondisi."),
            ),
        ),
        provenance=_seed_provenance("water", "Konsep seed awal; perlu kurasi."),
    )
    return api, kayu, kertas, besi, air


class ConceptStore:
    """Read-only in-memory store with deterministic ID/name/alias lookup."""

    def __init__(self, concepts: Iterable[Concept] | None = None) -> None:
        records = tuple(_build_seed_concepts() if concepts is None else concepts)
        self._by_id: dict[str, Concept] = {}
        self._by_name: dict[str, Concept] = {}
        self._by_alias: dict[str, Concept] = {}

        for concept in records:
            if not isinstance(concept, Concept):
                raise TypeError("ConceptStore accepts only Concept instances")
            concept_id = self._normalize(concept.concept_id)
            name = self._normalize(concept.name)
            if concept_id in self._by_id:
                raise ValueError(f"duplicate concept_id: {concept.concept_id}")
            if name in self._by_name:
                raise ValueError(f"duplicate concept name: {concept.name}")
            self._by_id[concept_id] = concept
            self._by_name[name] = concept

        for concept in records:
            for alias in concept.aliases:
                normalized_alias = self._normalize(alias)
                if not normalized_alias:
                    raise ValueError("aliases must be non-empty strings")
                existing = self._by_alias.get(normalized_alias)
                if existing is not None and existing != concept:
                    raise ValueError(f"duplicate concept alias: {alias}")
                named = self._by_name.get(normalized_alias)
                if named is not None and named != concept:
                    raise ValueError(f"alias conflicts with canonical name: {alias}")
                self._by_alias[normalized_alias] = concept

    @staticmethod
    def _normalize(value: str) -> str:
        if not isinstance(value, str):
            raise TypeError("concept lookup value must be a string")
        return " ".join(value.casefold().split())

    def get_by_id(self, concept_id: str) -> Concept | None:
        """Return a concept by stable concept_id, or None when absent."""
        return self._by_id.get(self._normalize(concept_id))

    def get_by_name(self, name: str) -> Concept | None:
        """Return a concept by canonical name, ignoring case and extra spaces."""
        return self._by_name.get(self._normalize(name))

    def get_by_alias(self, alias: str) -> Concept | None:
        """Return a concept by an explicitly registered alias."""
        return self._by_alias.get(self._normalize(alias))

    def lookup(self, identifier: str) -> Concept | None:
        """Resolve concept_id first, then canonical name, then registered alias."""
        normalized = self._normalize(identifier)
        return (
            self._by_id.get(normalized)
            or self._by_name.get(normalized)
            or self._by_alias.get(normalized)
        )

    def all(self) -> tuple[Concept, ...]:
        """Return all concepts in their stable seed/insertion order."""
        return tuple(self._by_id.values())

    def __len__(self) -> int:
        return len(self._by_id)
