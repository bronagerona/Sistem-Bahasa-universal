"""Adapter-owned in-memory conversation sessions; independent of Core memory."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


_TOPIC_STOPWORDS = {
    "aku", "saya", "kamu", "dia", "kami", "kita", "mereka", "nya", "ini", "itu",
    "tadi", "tersebut", "yang", "dan", "atau", "di", "ke", "dari", "untuk",
    "pada", "dengan", "dalam", "sedang", "lagi", "sudah", "belum", "akan",
    "apa", "siapa", "bagaimana", "mengapa", "apakah", "ngomong", "omong",
    "fungsi", "tentang", "mengenai", "mencari", "cari", "butuh", "perlu",
    "ingin", "mau", "adalah", "yaitu", "jadi", "maka", "juga", "saja",
    "sebuah", "suatu", "beberapa", "lebih", "paling", "bisa", "dapat",
    "tolong", "dong", "ya", "nih", "kan", "kok", "deh", "pun",
}
_TOPIC_RETURN = re.compile(
    r"^\s*(?:kembali|balik)\s+(?:lagi\s+)?(?:ke\s+topik|ke\s+pembahasan|ke)\s+(?P<reference>[^,;.!?]+)",
    re.IGNORECASE,
)
_TOPIC_SHIFT = re.compile(
    r"\b(?:ngomong[- ]ngomong|omong[- ]omong|beralih\s+ke|ganti\s+topik|topik\s+lain)\b",
    re.IGNORECASE,
)


def _topic_tokens(text: str) -> list[str]:
    """Extract conservative lexical anchors; this is not semantic parsing."""
    tokens = re.findall(r"[a-zA-ZÀ-ÿ0-9]+", text.casefold())
    return list(dict.fromkeys(
        token for token in tokens
        if len(token) > 2 and token not in _TOPIC_STOPWORDS and not token.isdigit()
    ))


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
    topic_history: list[dict[str, Any]] = field(default_factory=list)
    active_topic_id: str | None = None
    topic_resolution: dict[str, Any] = field(default_factory=dict)


class SessionManager:
    """Manage bounded in-memory conversation history outside ILIS Core.

    The manager never accesses ContextEngine, Knowledge, Episodic Memory, or
    SQLite. Existing host-generated IDs can be adopted with ensure_session().
    Topic history is kept separately from the bounded transcript so a topic
    can be revisited even after it is no longer active.
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

    def update_topic_context(self, session_id: str, user_message: str) -> dict[str, Any]:
        """Track topic changes and conservatively resolve explicit return references.

        Topic anchors are lexical hints only. They never become Semantic fields,
        Knowledge facts, or evidence for factual conclusions.
        """
        session = self.require_session(session_id)
        if not isinstance(user_message, str) or not user_message.strip():
            raise ValueError("user_message must be a non-empty string")
        sequence = session.turns[-1].sequence + 1 if session.turns else 1
        return_match = _TOPIC_RETURN.match(user_message)
        if return_match:
            reference_tokens = _topic_tokens(return_match.group("reference"))
            ranked: list[tuple[int, dict[str, Any]]] = []
            for topic in session.topic_history:
                overlap = set(reference_tokens).intersection(topic.get("anchors", []))
                if overlap:
                    ranked.append((len(overlap), topic))
            if ranked:
                best_score = max(score for score, _ in ranked)
                best = [topic for score, topic in ranked if score == best_score]
                if len(best) == 1:
                    topic = best[0]
                    session.active_topic_id = topic["topic_id"]
                    topic["last_mentioned_sequence"] = sequence
                    topic["mention_count"] = int(topic.get("mention_count", 1)) + 1
                    session.topic_resolution = {
                        "status": "returned_to_previous",
                        "topic_id": topic["topic_id"],
                        "topic": topic["label"],
                        "matched_anchors": sorted(
                            set(reference_tokens).intersection(topic.get("anchors", []))
                        ),
                        "explicit_reference": True,
                    }
                    return self.get_topic_context(session_id)

            session.topic_resolution = {
                "status": "ambiguous_reference",
                "topic_id": None,
                "topic": None,
                "matched_anchors": [],
                "explicit_reference": True,
            }
            return self.get_topic_context(session_id)

        anchors = _topic_tokens(user_message)
        active = next(
            (topic for topic in session.topic_history
             if topic["topic_id"] == session.active_topic_id),
            None,
        )
        overlap = (
            set(anchors).intersection(active.get("anchors", []))
            if active is not None else set()
        )
        explicit_shift = bool(_TOPIC_SHIFT.search(user_message))

        if anchors and (
            active is None
            or (explicit_shift and not overlap)
            or (not overlap and len(anchors) >= 2)
        ):
            topic_id = f"topic-{sequence}"
            topic = {
                "topic_id": topic_id,
                "label": " ".join(anchors[:3]),
                "anchors": list(anchors),
                "first_sequence": sequence,
                "last_mentioned_sequence": sequence,
                "mention_count": 1,
            }
            session.topic_history.append(topic)
            session.active_topic_id = topic_id
            status = "new_topic" if active is not None else "initial_topic"
            session.topic_resolution = {
                "status": status, "topic_id": topic_id,
                "topic": topic["label"], "matched_anchors": [],
                "explicit_reference": False,
            }
        elif active is not None and overlap:
            active["last_mentioned_sequence"] = sequence
            active["mention_count"] = int(active.get("mention_count", 1)) + 1
            session.topic_resolution = {
                "status": "same_topic_deepened",
                "topic_id": active["topic_id"],
                "topic": active["label"],
                "matched_anchors": sorted(overlap),
                "explicit_reference": False,
            }
        else:
            session.topic_resolution = {
                "status": "topic_uncertain",
                "topic_id": session.active_topic_id,
                "topic": active.get("label") if active else None,
                "matched_anchors": [],
                "explicit_reference": False,
            }
        return self.get_topic_context(session_id)

    def get_topic_context(self, session_id: str) -> dict[str, Any]:
        session = self.require_session(session_id)
        active = next(
            (topic for topic in session.topic_history
             if topic["topic_id"] == session.active_topic_id),
            None,
        )
        return {
            "active_topic": dict(active) if active else None,
            "topic_history": [dict(topic) for topic in session.topic_history],
            "resolution": dict(session.topic_resolution),
        }

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
                    "semantic_result": turn.metadata.get("semantic_result"),
                }
                for turn in session.turns[-self.max_turns:]
            ],
            "topic_context": self.get_topic_context(session_id),
        }

    def reset_session(self, session_id: str) -> dict[str, Any]:
        session = self.require_session(session_id)
        deleted = len(session.turns)
        session.turns.clear()
        session.topic_history.clear()
        session.active_topic_id = None
        session.topic_resolution = {}
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
