"""SQLite persistence integration tests."""

import sqlite3

import pytest

from ilis.cognition.context_engine import ContextEngine
from ilis.cognition.knowledge_engine import KnowledgeEngine
from ilis.storage import SQLiteStorageProvider


def test_sqlite_persists_facts_provenance_and_episodes_after_reopen(tmp_path):
    database = tmp_path / "ilis_v2.db"
    provider = SQLiteStorageProvider(database)
    knowledge = KnowledgeEngine(seed_core_knowledge=False, storage_provider=provider)
    context = ContextEngine(knowledge, storage_provider=provider)

    fact = knowledge.add_fact(
        "pemain", "memiliki", "pedang", status="verified", source="game_seed"
    )
    session_id = context.create_session({"world": "demo"})
    episode = context.record_event(
        session_id, "Pemain mengambil pedang",
        event_type="inventory_event", entities=["pemain", "pedang"],
        attributes={"item_id": "sword_01"},
    )
    provider.close()

    reopened = SQLiteStorageProvider(database)
    restored_knowledge = KnowledgeEngine(
        seed_core_knowledge=False, storage_provider=reopened
    )
    restored_context = ContextEngine(
        restored_knowledge, storage_provider=reopened
    )

    assert restored_knowledge.fact_store.get(fact["id"]) == fact
    assert restored_knowledge.get_provenance(fact["id"]) == {
        "fact_id": fact["id"], "source": "game_seed", "status": "verified"
    }
    assert restored_context.get_context(session_id)["episodic_memory"] == [episode]
    reopened.close()


def test_sqlite_restores_core_seed_without_duplicate_records(tmp_path):
    database = tmp_path / "seed.db"
    first = SQLiteStorageProvider(database)
    KnowledgeEngine(storage_provider=first)
    first.close()

    second = SQLiteStorageProvider(database)
    restored = KnowledgeEngine(storage_provider=second)
    assert len(restored.fact_store.all()) == 2
    second.close()


def test_fact_and_provenance_save_rolls_back_atomically(tmp_path):
    provider = SQLiteStorageProvider(tmp_path / "rollback.db")
    provider._require_connection().execute(
        """CREATE TRIGGER reject_provenance BEFORE INSERT ON provenance
           BEGIN SELECT RAISE(ABORT, 'simulated provenance failure'); END"""
    )
    fact = {
        "id": "fact_rollback", "subject": "pemain", "relation": "memiliki",
        "object": "pedang", "status": "verified", "source": "test",
    }
    provenance = {
        "fact_id": "fact_rollback", "source": "test", "status": "verified",
    }

    with pytest.raises(sqlite3.IntegrityError, match="simulated provenance failure"):
        provider.save_fact_with_provenance(fact, provenance)

    assert provider._require_connection().execute(
        "SELECT id FROM facts WHERE id = ?", ("fact_rollback",)
    ).fetchone() is None
    assert provider.load_provenance() == []
    provider.close()


def test_sqlite_close_is_idempotent(tmp_path):
    provider = SQLiteStorageProvider(tmp_path / "close.db")
    provider.close()
    provider.close()
    with pytest.raises(RuntimeError, match="closed"):
        provider.load_facts()


@pytest.mark.parametrize("invalid_path", ["", "   ", "../outside.db", "folder/../outside.db"])
def test_sqlite_rejects_invalid_database_paths(invalid_path):
    with pytest.raises(ValueError, match="db_path"):
        SQLiteStorageProvider(invalid_path)


def test_sqlite_rejects_existing_directory_as_database_path(tmp_path):
    with pytest.raises(ValueError, match="database file"):
        SQLiteStorageProvider(tmp_path)


def test_sqlite_schema_version_is_initialized(tmp_path):
    provider = SQLiteStorageProvider(tmp_path / "schema.db")
    row = provider._require_connection().execute(
        "SELECT version FROM schema_version WHERE singleton_id = 1"
    ).fetchone()
    assert row["version"] == 1
    provider.close()
