"""A small, explainable baseline tokenizer.

This is intentionally a first prototype, not a complete Indonesian tokenizer.
It preserves punctuation as separate tokens and does not discard the source text.
"""

from __future__ import annotations

import re

TOKEN_PATTERN = re.compile(r"[\w]+(?:['’][\w]+)*|[^\w\s]", re.UNICODE)


def tokenize(text: str) -> list[str]:
    """Split text into word-like tokens and punctuation."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return TOKEN_PATTERN.findall(text)
