"""In-memory storage for subject-relation-object facts."""

from __future__ import annotations

from typing import Any


class FactStore:
    def __init__(self) -> None:
        self._facts: dict[str, dict[str, Any]] = {}
        self._next_id = 1

    def add(
        self, subject: str, relation: str, object_: str, status: str, source: str
    ) -> dict[str, Any]:
        fact_id = f"fact_{self._next_id}"
        self._next_id += 1
        fact = {
            "id": fact_id,
            "subject": subject,
            "relation": relation,
            "object": object_,
            "status": status,
            "source": source,
        }
        self._facts[fact_id] = fact
        return dict(fact)

    def get(self, fact_id: str) -> dict[str, Any] | None:
        fact = self._facts.get(fact_id)
        return dict(fact) if fact is not None else None

    def update_status(self, fact_id: str, status: str) -> None:
        self._facts[fact_id]["status"] = status

    def all(self) -> list[dict[str, Any]]:
        return [dict(fact) for fact in self._facts.values()]

    def find_by_concept(self, concept: str) -> list[dict[str, Any]]:
        key = " ".join(concept.casefold().split())
        return [
            dict(fact)
            for fact in self._facts.values()
            if fact["subject"] == key or fact["object"] == key
        ]
