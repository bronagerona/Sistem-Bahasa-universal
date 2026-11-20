from pathlib import Path

from ilis.cognition import KnowledgeEngine
from ilis.interfaces import ILISCore


DATASET_DIR = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "indonesian"
    / "knowledge"
)


def test_dataset_record_maps_jsonl_fields_and_preserves_original_record():
    engine = KnowledgeEngine(seed_core_knowledge=False)
    record = {
        "fact_id": "fact-test-0001",
        "subject": "Mars",
        "predicate": "memiliki satelit",
        "object": ["Phobos", "Deimos"],
        "source": "NASA",
        "verification_status": "draft",
        "qualifiers": ["Dua satelit alami."],
    }

    fact = engine.load_dataset_record(record)

    assert fact["id"] == "fact-test-0001"
    assert fact["subject"] == "mars"
    assert fact["relation"] == "memiliki satelit"
    assert fact["object"] == "phobos, deimos"
    assert fact["status"] == "hypothesis"
    assert fact["source"] == "NASA"
    assert fact["dataset_record"] == record
    assert engine.get_provenance("fact-test-0001") == {
        "fact_id": "fact-test-0001",
        "source": "NASA",
        "status": "hypothesis",
    }


def test_dataset_loader_reads_all_18_batches_without_loading_sample_jsonl():
    engine = KnowledgeEngine(seed_core_knowledge=False)

    loaded = engine.load_jsonl_directory(DATASET_DIR)

    assert loaded == 90
    assert len(engine.fact_store.all()) == 90
    assert len(engine.provenance.all()) == 90
    assert engine.fact_store.get("fact-0003")["object"] == "4"
    assert engine.fact_store.get("fact-0003")["dataset_record"]["object"] == 4
    assert engine.fact_store.get("fact-0031")["object"] == "phobos, deimos"
    assert engine.fact_store.get("fact-0031")["dataset_record"]["object"] == [
        "Phobos",
        "Deimos",
    ]


def test_ilis_core_loads_knowledge_dataset_and_keeps_three_core_facts():
    core = ILISCore()

    assert core.knowledge_dataset_loaded == 90
    facts = core.knowledge_engine.fact_store.all()
    assert len(facts) == 93

    core_facts = {
        (fact["subject"], fact["relation"], fact["object"], fact["status"], fact["source"])
        for fact in facts
        if fact["source"] == "core_knowledge"
    }
    assert core_facts == {
        ("api", "can_burn", "kayu", "verified", "core_knowledge"),
        ("rumah", "made_of", "kayu", "verified", "core_knowledge"),
        ("api", "can_burn", "kertas", "verified", "core_knowledge"),
    }

    rotation = core.knowledge_engine.fact_store.get("fact-0033")
    orbit = core.knowledge_engine.fact_store.get("fact-0034")
    assert rotation["subject"] == "merkurius"
    assert rotation["relation"] == "memiliki periode rotasi sideris sekitar"
    assert rotation["status"] == "hypothesis"
    assert orbit["relation"] == "memiliki periode orbit mengelilingi matahari sekitar"
    assert orbit["status"] == "hypothesis"
    assert rotation["dataset_record"]["verification_status"] == "draft"


def test_ilis_core_loads_dataset_when_core_seeding_is_disabled():
    core = ILISCore(seed_core_knowledge=False)

    assert core.knowledge_dataset_loaded == 90
    assert len(core.knowledge_engine.fact_store.all()) == 90
    assert not any(
        fact["source"] == "core_knowledge"
        for fact in core.knowledge_engine.fact_store.all()
    )


def test_unverified_dataset_variants_do_not_create_global_conflict():
    engine = KnowledgeEngine(seed_core_knowledge=False)
    engine.load_jsonl_directory(DATASET_DIR)

    # fact-0008 and fact-0038 express the same "Matahari merupakan ..."
    # statement with different wording. Both source records are still drafts.
    assert engine.detect_conflicts() == []
