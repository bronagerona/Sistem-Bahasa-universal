"""Adapter-owned in-memory conversation sessions; independent of Core memory."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class ConversationTurn:
    """One complete user/assistant exchange."""

    turn_id: str
    session_id: str
    sequence: int
    user_message: str
    assistant_response: str
    created_at: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ConversationSession:
    """Adapter-owned conversation lifecycle and turn history."""

    session_id: str
    created_at: str
    updated_at: str
    active: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)
    turns: list[ConversationTurn] = field(default_factory=list)


class SessionManager:
    """Manage bounded in-memory conversation history outside ILIS Core.

    The manager never accesses ContextEngine, Knowledge, Episodic Memory, or
    SQLite. Existing host-generated IDs can be adopted with ensure_session().
    """

    def __init__(self, *, max_turns: int = 5) -> None:
        if not isinstance(max_turns, int) or isinstance(max_turns, bool) or max_turns < 1:
            raise ValueError("max_turns must be a positive integer")
        self.max_turns = max_turns
        self._sessions: dict[str, ConversationSession] = {}

    def create_session(
        self, session_id: str | None = None, *,
        metadata: dict[str, Any] | None = None,
    ) -> str:
        identifier = session_id or str(uuid4())
        if not isinstance(identifier, str) or not identifier.strip():
            raise ValueError("session_id must be a non-empty string")
        if identifier in self._sessions:
            raise ValueError(f"session already exists: {identifier}")
        now = _now()
        self._sessions[identifier] = ConversationSession(
            session_id=identifier, created_at=now, updated_at=now,
            metadata=dict(metadata or {}),
        )
        return identifier

    def ensure_session(
        self, session_id: str, *, metadata: dict[str, Any] | None = None,
    ) -> str:
        """Adopt a caller-provided ID or validate an existing active session."""
        if not isinstance(session_id, str) or not session_id.strip():
            raise ValueError("session_id must be a non-empty string")
        session = self._sessions.get(session_id)
        if session is None:
            return self.create_session(session_id, metadata=metadata)
        if not session.active:
            raise ValueError(f"session is closed: {session_id}")
        return session_id

    def get_session(self, session_id: str) -> ConversationSession | None:
        return self._sessions.get(session_id)

    def require_session(self, session_id: str) -> ConversationSession:
        session = self._sessions.get(session_id)
        if session is None:
            raise KeyError(f"unknown session_id: {session_id}")
        if not session.active:
            raise ValueError(f"session is closed: {session_id}")
        return session

    def add_turn(
        self, session_id: str, user_message: str, assistant_response: str,
        *, metadata: dict[str, Any] | None = None,
    ) -> ConversationTurn:
        session = self.require_session(session_id)
        if not isinstance(user_message, str) or not user_message.strip():
            raise ValueError("user_message must be a non-empty string")
        if not isinstance(assistant_response, str) or not assistant_response.strip():
            raise ValueError("assistant_response must be a non-empty string")
        turn = ConversationTurn(
            turn_id=str(uuid4()), session_id=session_id,
            sequence=(session.turns[-1].sequence + 1 if session.turns else 1),
            user_message=user_message.strip(),
            assistant_response=assistant_response.strip(),
            created_at=_now(), metadata=dict(metadata or {}),
        )
        session.turns.append(turn)
        session.updated_at = turn.created_at
        if len(session.turns) > self.max_turns:
            del session.turns[:-self.max_turns]
        return turn

    def get_recent_turns(self, session_id: str) -> list[ConversationTurn]:
        return list(self.require_session(session_id).turns[-self.max_turns:])

    def get_context_snapshot(self, session_id: str) -> dict[str, Any]:
        session = self.require_session(session_id)
        return {
            "context_version": "1.0",
            "session_id": session_id,
            "max_turns": self.max_turns,
            "turns": [
                {
                    "sequence": turn.sequence,
                    "user_message": turn.user_message,
                    "assistant_response": turn.assistant_response,
                }
                for turn in session.turns[-self.max_turns:]
            ],
        }

    def reset_session(self, session_id: str) -> dict[str, Any]:
        session = self.require_session(session_id)
        deleted = len(session.turns)
        session.turns.clear()
        session.updated_at = _now()
        return {"session_id": session_id, "deleted_turns": deleted, "reset": True}

    def delete_session(self, session_id: str) -> bool:
        if session_id not in self._sessions:
            return False
        del self._sessions[session_id]
        return True

    def close_session(self, session_id: str) -> None:
        session = self.require_session(session_id)
        session.active = False
        session.updated_at = _now()

    def __len__(self) -> int:
        return len(self._sessions)
