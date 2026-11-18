"""Track learning candidates without silently verifying them."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


class HypothesisTracker:
    """Keep an auditable in-memory record of proposed hypotheses and review flags."""

    def __init__(self) -> None:
        self._items: dict[str, dict[str, Any]] = {}

    @staticmethod
    def _timestamp() -> str:
        return datetime.now(timezone.utc).isoformat()

    def track(
        self,
        *,
        origin: str,
        candidate: dict[str, str],
        fact: dict[str, Any] | None,
        status: str,
        conflict: bool,
        requires_confirmation: bool,
        source_ref: str | None = None,
        reason: str | None = None,
    ) -> dict[str, Any]:
        item = {
            "hypothesis_id": str(uuid4()),
            "origin": origin,
            "candidate": dict(candidate),
            "fact_id": fact.get("id") if fact else None,
            "knowledge_status": fact.get("status") if fact else None,
            "status": status,
            "conflict": conflict,
            "requires_confirmation": requires_confirmation,
            "source_ref": source_ref,
            "reason": reason,
            "created_at": self._timestamp(),
            "updated_at": self._timestamp(),
        }
        self._items[item["hypothesis_id"]] = item
        return dict(item)

    def get(self, hypothesis_id: str) -> dict[str, Any] | None:
        item = self._items.get(hypothesis_id)
        return dict(item) if item else None

    def all(self) -> list[dict[str, Any]]:
        return [dict(item) for item in self._items.values()]

    def update_review(
        self, hypothesis_id: str, *, status: str, knowledge_status: str | None
    ) -> dict[str, Any]:
        if hypothesis_id not in self._items:
            raise KeyError(f"unknown hypothesis_id: {hypothesis_id}")
        item = self._items[hypothesis_id]
        item["status"] = status
        item["knowledge_status"] = knowledge_status
        item["requires_confirmation"] = status == "pending_confirmation"
        item["updated_at"] = self._timestamp()
        return dict(item)
