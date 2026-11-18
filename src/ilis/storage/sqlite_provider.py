"""SQLite persistence for ILIS facts, provenance, sessions, and episodes."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any


class SQLiteStorageProvider:
    """Small SQLite repository shared by KnowledgeEngine and MemoryStore.

    The provider owns one connection. Call close() when the application shuts
    down; reopening the provider on the same path restores persisted records.
    """

    def __init__(self, db_path: str | Path = "./ilis_v2.db") -> None:
        self.db_path = str(db_path)
        if self.db_path != ":memory:":
            Path(self.db_path).expanduser().resolve().parent.mkdir(
                parents=True, exist_ok=True
            )
        self._connection = sqlite3.connect(self.db_path)
        self._connection.row_factory = sqlite3.Row
        self._initialize_schema()

    def _initialize_schema(self) -> None:
        with self._connection:
            self._connection.executescript(
                """
                PRAGMA foreign_keys = ON;
                CREATE TABLE IF NOT EXISTS facts (
                    id TEXT PRIMARY KEY,
                    subject TEXT NOT NULL,
                    relation TEXT NOT NULL,
                    object TEXT NOT NULL,
                    status TEXT NOT NULL,
                    source TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS provenance (
                    fact_id TEXT PRIMARY KEY REFERENCES facts(id) ON DELETE CASCADE,
                    source TEXT NOT NULL,
                    status TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    created_at TEXT NOT NULL,
                    closed_at TEXT,
                    active INTEGER NOT NULL,
                    metadata_json TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS episodic_memory (
                    episode_id TEXT PRIMARY KEY,
                    session_id TEXT NOT NULL REFERENCES sessions(session_id),
                    description TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    entities_json TEXT NOT NULL,
                    attributes_json TEXT NOT NULL,
                    timestamp TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_facts_subject ON facts(subject);
                CREATE INDEX IF NOT EXISTS idx_facts_object ON facts(object);
                CREATE INDEX IF NOT EXISTS idx_episodes_session ON episodic_memory(session_id);
                """
            )

    def save_fact(self, fact: dict[str, Any]) -> None:
        with self._connection:
            self._connection.execute(
                """INSERT OR REPLACE INTO facts
                   (id, subject, relation, object, status, source)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (fact["id"], fact["subject"], fact["relation"], fact["object"],
                 fact["status"], fact["source"]),
            )

    def load_facts(self) -> list[dict[str, Any]]:
        rows = self._connection.execute(
            "SELECT id, subject, relation, object, status, source FROM facts ORDER BY rowid"
        ).fetchall()
        return [dict(row) for row in rows]

    def save_provenance(self, record: dict[str, Any]) -> None:
        with self._connection:
            self._connection.execute(
                """INSERT OR REPLACE INTO provenance (fact_id, source, status)
                   VALUES (?, ?, ?)""",
                (record["fact_id"], record["source"], record["status"]),
            )

    def update_provenance_status(self, fact_id: str, status: str) -> None:
        with self._connection:
            self._connection.execute(
                "UPDATE provenance SET status = ? WHERE fact_id = ?",
                (status, fact_id),
            )

    def load_provenance(self) -> list[dict[str, Any]]:
        rows = self._connection.execute(
            "SELECT fact_id, source, status FROM provenance ORDER BY rowid"
        ).fetchall()
        return [dict(row) for row in rows]

    def save_session(self, session: dict[str, Any]) -> None:
        with self._connection:
            self._connection.execute(
                """INSERT OR REPLACE INTO sessions
                   (session_id, created_at, closed_at, active, metadata_json)
                   VALUES (?, ?, ?, ?, ?)""",
                (session["session_id"], session["created_at"], session["closed_at"],
                 int(session["active"]), json.dumps(session.get("metadata", {}),
                 ensure_ascii=False)),
            )

    def load_sessions(self) -> list[dict[str, Any]]:
        rows = self._connection.execute(
            """SELECT session_id, created_at, closed_at, active, metadata_json
               FROM sessions ORDER BY rowid"""
        ).fetchall()
        return [{
            "session_id": row["session_id"],
            "created_at": row["created_at"],
            "closed_at": row["closed_at"],
            "active": bool(row["active"]),
            "metadata": json.loads(row["metadata_json"]),
        } for row in rows]

    def save_episode(self, episode: dict[str, Any]) -> None:
        with self._connection:
            self._connection.execute(
                """INSERT OR REPLACE INTO episodic_memory
                   (episode_id, session_id, description, event_type,
                    entities_json, attributes_json, timestamp)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (episode["episode_id"], episode["session_id"],
                 episode["description"], episode["event_type"],
                 json.dumps(episode.get("entities", []), ensure_ascii=False),
                 json.dumps(episode.get("attributes", {}), ensure_ascii=False),
                 episode["timestamp"]),
            )

    def load_episodes(self, session_id: str | None = None) -> list[dict[str, Any]]:
        if session_id is None:
            rows = self._connection.execute(
                """SELECT episode_id, session_id, description, event_type,
                   entities_json, attributes_json, timestamp
                   FROM episodic_memory ORDER BY rowid"""
            ).fetchall()
        else:
            rows = self._connection.execute(
                """SELECT episode_id, session_id, description, event_type,
                   entities_json, attributes_json, timestamp
                   FROM episodic_memory WHERE session_id = ? ORDER BY rowid""",
                (session_id,),
            ).fetchall()
        return [{
            "episode_id": row["episode_id"],
            "session_id": row["session_id"],
            "description": row["description"],
            "event_type": row["event_type"],
            "entities": json.loads(row["entities_json"]),
            "attributes": json.loads(row["attributes_json"]),
            "timestamp": row["timestamp"],
        } for row in rows]

    def close(self) -> None:
        """Commit pending work and close the underlying SQLite connection."""
        self._connection.commit()
        self._connection.close()

    def __enter__(self) -> "SQLiteStorageProvider":
        return self

    def __exit__(self, exc_type: Any, exc: Any, traceback: Any) -> None:
        if exc_type is None:
            self._connection.commit()
        self.close()
