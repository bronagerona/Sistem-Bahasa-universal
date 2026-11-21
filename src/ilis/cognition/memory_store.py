"""In-memory Working Memory with optional persistent Episodic Memory."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def _required_text(value: str, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value.strip()


class MemoryStore:
    """Store session-scoped working memory and retained episodic records.

    With no provider this is the original V1 in-memory implementation. When a
    provider is supplied, sessions and episodes are restored and persisted;
    working conversation turns remain transient.
    """

    def __init__(self, storage_provider: Any | None = None) -> None:
        self.storage_provider = storage_provider
        self._sessions: dict[str, dict[str, Any]] = {}
        self._working: dict[str, list[dict[str, Any]]] = {}
        self._episodes: dict[str, list[dict[str, Any]]] = {}
        if storage_provider is not None:
            for session in storage_provider.load_sessions():
                self._sessions[session["session_id"]] = session
                self._working[session["session_id"]] = []
                self._episodes[session["session_id"]] = []
            for episode in storage_provider.load_episodes():
                self._episodes.setdefault(episode["session_id"], []).append(episode)

    def create_session(self, metadata: dict[str, Any] | None = None) -> dict[str, Any]:
        session_id = str(uuid4())
        session = {
            "session_id": session_id, "created_at": _timestamp(),
            "closed_at": None, "active": True, "metadata": dict(metadata or {}),
        }
        self._sessions[session_id] = session
        self._working[session_id] = []
        self._episodes[session_id] = []
        if self.storage_provider is not None:
            self.storage_provider.save_session(session)
        return dict(session)

    def get_session(self, session_id: str) -> dict[str, Any] | None:
        session = self._sessions.get(session_id)
        return dict(session) if session is not None else None

    def require_active_session(self, session_id: str) -> dict[str, Any]:
        session = self._sessions.get(session_id)
        if session is None:
            raise KeyError(f"unknown session_id: {session_id}")
        if not session["active"]:
            raise ValueError(f"session is closed: {session_id}")
        return session

    def close_session(self, session_id: str, clear_working: bool = True) -> dict[str, Any]:
        session = self._sessions.get(session_id)
        if session is None:
            raise KeyError(f"unknown session_id: {session_id}")
        if session["active"]:
            session["active"] = False
            session["closed_at"] = _timestamp()
            if self.storage_provider is not None:
                self.storage_provider.save_session(session)
        if clear_working:
            self._working[session_id].clear()
        return dict(session)

    def add_message(
        self, session_id: str, speaker: str, text: str,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        self.require_active_session(session_id)
        entry = {
            "message_id": str(uuid4()), "session_id": session_id,
            "speaker": _required_text(speaker, "speaker"),
            "text": _required_text(text, "text"), "timestamp": _timestamp(),
            "metadata": dict(metadata or {}),
        }
        self._working[session_id].append(entry)
        return dict(entry)

    def add_episode(
        self, session_id: str, description: str, *, event_type: str = "event",
        entities: list[str] | None = None,
        attributes: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        self.require_active_session(session_id)
        clean_entities = [_required_text(entity, "entity") for entity in (entities or [])]
        entry = {
            "episode_id": str(uuid4()), "session_id": session_id,
            "description": _required_text(description, "description"),
            "event_type": _required_text(event_type, "event_type"),
            "entities": clean_entities, "attributes": dict(attributes or {}),
            "timestamp": _timestamp(),
        }
        self._episodes[session_id].append(entry)
        if self.storage_provider is not None:
            self.storage_provider.save_episode(entry)
        return dict(entry)

    def get_working_memory(self, session_id: str) -> list[dict[str, Any]]:
        if session_id not in self._sessions:
            raise KeyError(f"unknown session_id: {session_id}")
        return [dict(item) for item in self._working[session_id]]

    def get_episodic_memory(self, session_id: str) -> list[dict[str, Any]]:
        if session_id not in self._sessions:
            raise KeyError(f"unknown session_id: {session_id}")
        return [dict(item) for item in self._episodes[session_id]]

    def clear_working_memory(self, session_id: str) -> None:
        if session_id not in self._sessions:
            raise KeyError(f"unknown session_id: {session_id}")
        self._working[session_id].clear()
