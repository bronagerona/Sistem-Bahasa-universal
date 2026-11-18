"""Minimal inspection pipeline for the ILIS language foundation."""

from __future__ import annotations

from ilis.language.tokenizer import tokenize
from ilis.language.variation import variation_hint


def inspect_text(text: str) -> dict[str, object]:
    """Return observable token and lexical-variation information.

    The output is deliberately not called a semantic interpretation: this first
    milestone detects token boundaries and a small set of lexical variants only.
    """
    tokens = tokenize(text)
    return {
        "input": text,
        "tokens": [
            {
                "surface": token,
                "variation_hint": variation_hint(token),
                "is_punctuation": len(token) == 1 and not token.isalnum(),
            }
            for token in tokens
        ],
        "limitations": [
            "Belum melakukan analisis sintaksis atau pemahaman semantik.",
            "Pemetaan variasi masih kecil dan berbasis aturan eksplisit.",
            "Belum melakukan koreksi typo secara kontekstual.",
        ],
    }
