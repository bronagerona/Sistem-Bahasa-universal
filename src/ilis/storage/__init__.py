"""Optional persistence backends for ILIS.

SQLite is imported on demand so the default in-memory core does not require it.
"""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ilis.storage.sqlite_provider import SQLiteStorageProvider


def __getattr__(name: str) -> Any:
    if name == "SQLiteStorageProvider":
        from ilis.storage.sqlite_provider import SQLiteStorageProvider
        return SQLiteStorageProvider
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = ["SQLiteStorageProvider"]
