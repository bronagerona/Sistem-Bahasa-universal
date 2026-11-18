# SQLite Storage (ILIS V2)

ILIS V2 adds optional SQLite persistence for Knowledge Engine facts/provenance
and Context Engine Episodic Memory. The default remains the V1 in-memory mode.

## In-memory mode (default)

Existing applications need no changes:

```python
from ilis.interfaces import ILISCore

ilis = ILISCore()
# Existing V1 behavior: data lives in memory for this process.
```

## Enable SQLite

```python
from ilis.interfaces import ILISCore

ilis = ILISCore(storage="sqlite", db_path="./ilis_v2.db")
session_id = ilis.create_session({"world": "demo"})

ilis.knowledge_engine.add_fact(
    "pemain", "memiliki", "pedang",
    status="verified", source="game_seed",
)
ilis.context_engine.record_event(
    session_id,
    "Pemain mengambil pedang",
    event_type="inventory_event",
    entities=["pemain", "pedang"],
)

# On application shutdown:
ilis.close()
```

On the next launch, create ILISCore with the same `db_path`. Facts, their
provenance, session metadata, and episodic events are restored. Working
conversation turns are intentionally transient and are not persisted.

SQLite is part of Python's standard library; no third-party runtime dependency
is required. Use a separate database path per application/environment and
close the core cleanly during shutdown.

## Schema

- `facts`: normalized subject-relation-object assertions and status.
- `provenance`: source and review status for each fact.
- `sessions`: session identity, timestamps, active state, and metadata.
- `episodic_memory`: event description, type, entities, attributes, and time.

## Tests

Run the full suite, including restart persistence tests:

```bash
python -m pytest
```
