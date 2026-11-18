"""SQLite persistence integration tests."""

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
