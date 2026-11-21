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

SQLite is imported only when `storage="sqlite"` is selected. It is part of
Python's standard library and has no third-party runtime dependency. Use a
separate database path per application/environment and close the core cleanly.

## Database path policy

- Empty paths, null bytes, existing directories, and paths containing a
  parent traversal component (`..`) are rejected.
- Relative paths are resolved from the process working directory.
- Absolute paths are accepted when explicitly configured by the application
  (for example, a managed application-data directory or test temporary folder).
- The special `:memory:` path is supported for temporary databases.
- The application is responsible for choosing a private directory and setting
  appropriate filesystem permissions.

## Sensitive data warning

SQLite stores facts, provenance source labels, session metadata, and episodic
event descriptions/entities/attributes as ordinary text or JSON. These values
are **not encrypted by ILIS**. Do not place passwords, access tokens, payment
details, private user messages, or other secrets in metadata, facts, event
descriptions, or episode attributes. Restrict filesystem access to the database
and its containing directory, define a retention/deletion policy, and consider
OS-level or database encryption when sensitive data must be retained. Deleting
an episode or session from application memory does not automatically erase
other copies or backups of the database.

## Schema and migrations

The `schema_version` table records the database schema version. Existing alpha
databases without this marker are recognized as schema version 1. Future schema
changes must add explicit sequential migrations and update the version only
after a successful migration. Databases with a newer unsupported schema version
are rejected rather than silently downgraded.

## Tables

- `schema_version`: current database schema version.
- `facts`: normalized subject-relation-object assertions and status.
- `provenance`: source and review status for each fact.
- `sessions`: session identity, timestamps, active state, and metadata.
- `episodic_memory`: event description, type, entities, attributes, and time.

## Tests

Run the full suite, including restart persistence tests:

```bash
python -m pytest
```
