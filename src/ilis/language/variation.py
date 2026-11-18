"""Conservative lexical variation hints for Indonesian.

Mappings here are normalization hints, not universal equivalences. The original
surface form is always retained because forms such as 'gue', 'aku', and 'saya'
also carry register and social nuance.
"""

from __future__ import annotations

VARIATION_HINTS: dict[str, str] = {
    "gue": "saya",
    "gw": "saya",
    "gua": "saya",
    "lu": "kamu",
    "lo": "kamu",
    "elu": "kamu",
    "gak": "tidak",
    "ga": "tidak",
    "nggak": "tidak",
    "enggak": "tidak",
    "gk": "tidak",
    "kagak": "tidak",
    "udah": "sudah",
    "udh": "sudah",
    "aja": "saja",
    "doang": "saja",
    "cabut": "pergi",
    "prgi": "pergi",
    "mw": "mau",
}


def variation_hint(token: str) -> str | None:
    """Return a cautious canonical hint for a token, if one is known."""
    return VARIATION_HINTS.get(token.casefold())
