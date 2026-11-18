"""Separate provenance records for facts and their review status."""

from __future__ import annotations

from typing import Any


class ProvenanceStore:
    def __init__(self) -> None:
        self._records: dict[str, dict[str, Any]] = {}

    def record(self, fact_id: str, source: str, status: str) -> dict[str, Any]:
        entry = {"fact_id": fact_id, "source": source, "status": status}
        self._records[fact_id] = entry
        return dict(entry)

    def update_status(self, fact_id: str, status: str) -> None:
        self._records[fact_id]["status"] = status

    def get(self, fact_id: str) -> dict[str, Any] | None:
        entry = self._records.get(fact_id)
        return dict(entry) if entry is not None else None

    def all(self) -> list[dict[str, Any]]:
        return [dict(entry) for entry in self._records.values()]
