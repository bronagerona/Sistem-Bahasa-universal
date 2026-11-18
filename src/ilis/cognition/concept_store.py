"""In-memory store for normalized ILIS concepts."""

from __future__ import annotations


class ConceptStore:
    def __init__(self) -> None:
        self._concepts: dict[str, str] = {}

    @staticmethod
    def _key(concept: str) -> str:
        if not isinstance(concept, str) or not concept.strip():
            raise ValueError("concept must be a non-empty string")
        return " ".join(concept.casefold().split())

    def add(self, concept: str) -> str:
        key = self._key(concept)
        self._concepts.setdefault(key, key)
        return self._concepts[key]

    def contains(self, concept: str) -> bool:
        return self._key(concept) in self._concepts

    def get(self, concept: str) -> str | None:
        return self._concepts.get(self._key(concept))

    def all(self) -> list[str]:
        return sorted(self._concepts.values())
