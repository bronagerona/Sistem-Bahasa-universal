"""SQLite persistence for ILIS facts, provenance, sessions, and episodes."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any


SCHEMA_VERSION = 1


def _normalize_db_path(db_path: str | Path) -> str:
    """Validate and normalize a trusted application database path.

    Relative paths may not contain parent-directory traversal. Absolute paths
    are accepted as explicit deployment configuration (for example pytest's
    temporary directory). The special ':memory:' database remains supported.
    """
    if not isinstance(db_path, (str, Path)):
        raise TypeError("db_path must be a string or pathlib.Path")
    raw_path = str(db_path)
    if not raw_path.strip():
        raise ValueError("db_path must not be empty")
    if "\x00" in raw_path:
        raise ValueError("db_path must not contain null bytes")
    if raw_path == ":memory:":
        return raw_path

    # Reject traversal on both POSIX and Windows-style separators.
    components = raw_path.replace("\\", "/").split("/")
    if ".." in components:
        raise ValueError("db_path must not contain parent-directory traversal ('..')")

    path = Path(raw_path).expanduser()
    if path.exists() and path.is_dir():
        raise ValueError("db_path must identify a database file, not a directory")
    return str(path.resolve())


class SQLiteStorageProvider:
    """SQLite repository shared by KnowledgeEngine and MemoryStore.

    Relative paths are resolved from the current working directory and may not
    traverse to parent directories. Absolute paths are accepted only when
    explicitly supplied by the application. Call close() at shutdown.
    """

    def __init__(self, db_path: str | Path = "./ilis_v2.db") -> None:
        self.db_path = _normalize_db_path(db_path)
        self._closed = False
        self._connection: sqlite3.Connection | None = None
        try:
            if self.db_path != ":memory:":
                Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
            self._connection = sqlite3.connect(self.db_path)
            self._connection.row_factory = sqlite3.Row
            self._initialize_schema()
        except Exception as exc:
            if self._connection is not None:
                try:
                    self._connection.close()
                finally:
                    self._connection = None
                    self._closed = True
            if isinstance(exc, (OSError, sqlite3.Error)):
                raise RuntimeError(
                    f"Unable to initialize ILIS SQLite database at {self.db_path!r}: {exc}"
                ) from exc
            raise

    def _require_connection(self) -> sqlite3.Connection:
        if self._closed or self._connection is None:
            raise RuntimeError("SQLiteStorageProvider is closed")
        return self._connection

    def _initialize_schema(self) -> None:
        connection = self._require_connection()
        with connection:
            connection.executescript(
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
                CREATE TABLE IF NOT EXISTS schema_version (
                    singleton_id INTEGER PRIMARY KEY CHECK (singleton_id = 1),
                    version INTEGER NOT NULL
                );
                """
            )

        # Existing databases without this table are treated as the original
        # alpha schema (version 1); future schema changes must add migrations.
        with connection:
            row = connection.execute(
                "SELECT version FROM schema_version WHERE singleton_id = 1"
            ).fetchone()
            if row is None:
                connection.execute(
                    "INSERT INTO schema_version (singleton_id, version) VALUES (1, ?)",
                    (SCHEMA_VERSION,),
                )
            elif row["version"] > SCHEMA_VERSION:
                raise RuntimeError(
                    f"Database schema version {row['version']} is newer than "
                    f"supported version {SCHEMA_VERSION}"
                )
            elif row["version"] < SCHEMA_VERSION:
                self._migrate_schema(row["version"], connection)

    def _migrate_schema(self, current_version: int, connection: sqlite3.Connection) -> None:
        """Apply sequential schema upgrades; version 1 is the alpha baseline."""
        version = current_version
        with connection:
            while version < SCHEMA_VERSION:
                if version == 0:
                    # Version 0 represents a legacy database without a version
                    # marker; its existing alpha tables already match v1.
                    version = 1
                    connection.execute(
                        "UPDATE schema_version SET version = ? WHERE singleton_id = 1",
                        (version,),
                    )
                else:
                    raise RuntimeError(
                        f"No migration path from database schema version {version}"
                    )

    def save_fact(self, fact: dict[str, Any]) -> None:
        connection = self._require_connection()
        with connection:
            connection.execute(
                """INSERT OR REPLACE INTO facts
                   (id, subject, relation, object, status, source)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (fact["id"], fact["subject"], fact["relation"], fact["object"],
                 fact["status"], fact["source"]),
            )

    def save_fact_with_provenance(
        self, fact: dict[str, Any], record: dict[str, Any]
    ) -> None:
        """Persist a fact and its provenance atomically."""
        connection = self._require_connection()
        with connection:
            connection.execute(
                """INSERT OR REPLACE INTO facts
                   (id, subject, relation, object, status, source)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (fact["id"], fact["subject"], fact["relation"], fact["object"],
                 fact["status"], fact["source"]),
            )
            connection.execute(
                """INSERT OR REPLACE INTO provenance (fact_id, source, status)
                   VALUES (?, ?, ?)""",
                (record["fact_id"], record["source"], record["status"]),
            )

    def load_facts(self) -> list[dict[str, Any]]:
        rows = self._require_connection().execute(
            "SELECT id, subject, relation, object, status, source FROM facts ORDER BY rowid"
        ).fetchall()
        return [dict(row) for row in rows]

    def save_provenance(self, record: dict[str, Any]) -> None:
        connection = self._require_connection()
        with connection:
            connection.execute(
                """INSERT OR REPLACE INTO provenance (fact_id, source, status)
                   VALUES (?, ?, ?)""",
                (record["fact_id"], record["source"], record["status"]),
            )

    def update_provenance_status(self, fact_id: str, status: str) -> None:
        connection = self._require_connection()
        with connection:
            connection.execute(
                "UPDATE provenance SET status = ? WHERE fact_id = ?",
                (status, fact_id),
            )

    def load_provenance(self) -> list[dict[str, Any]]:
        rows = self._require_connection().execute(
            "SELECT fact_id, source, status FROM provenance ORDER BY rowid"
        ).fetchall()
        return [dict(row) for row in rows]

    def save_session(self, session: dict[str, Any]) -> None:
        connection = self._require_connection()
        with connection:
            connection.execute(
                """INSERT OR REPLACE INTO sessions
                   (session_id, created_at, closed_at, active, metadata_json)
                   VALUES (?, ?, ?, ?, ?)""",
                (session["session_id"], session["created_at"], session["closed_at"],
                 int(session["active"]), json.dumps(session.get("metadata", {}),
                 ensure_ascii=False)),
            )

    def load_sessions(self) -> list[dict[str, Any]]:
        rows = self._require_connection().execute(
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
        connection = self._require_connection()
        with connection:
            connection.execute(
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
        connection = self._require_connection()
        if session_id is None:
            rows = connection.execute(
                """SELECT episode_id, session_id, description, event_type,
                   entities_json, attributes_json, timestamp
                   FROM episodic_memory ORDER BY rowid"""
            ).fetchall()
        else:
            rows = connection.execute(
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
        """Commit pending work and close the connection; safe to repeat."""
        if self._closed:
            return
        connection = self._connection
        self._closed = True
        self._connection = None
        if connection is not None:
            try:
                connection.commit()
            finally:
                connection.close()

    def __enter__(self) -> "SQLiteStorageProvider":
        self._require_connection()
        return self

    def __exit__(self, exc_type: Any, exc: Any, traceback: Any) -> None:
        connection = self._require_connection()
        try:
            if exc_type is None:
                connection.commit()
            else:
                connection.rollback()
        finally:
            self.close()
