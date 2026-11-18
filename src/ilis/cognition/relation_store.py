"""In-memory store for normalized relation names."""

from __future__ import annotations


class RelationStore:
    def __init__(self) -> None:
        self._relations: dict[str, str] = {}

    @staticmethod
    def _key(relation: str) -> str:
        if not isinstance(relation, str) or not relation.strip():
            raise ValueError("relation must be a non-empty string")
        return " ".join(relation.casefold().split())

    def add(self, relation: str) -> str:
        key = self._key(relation)
        self._relations.setdefault(key, key)
        return self._relations[key]

    def contains(self, relation: str) -> bool:
        return self._key(relation) in self._relations

    def all(self) -> list[str]:
        return sorted(self._relations.values())
