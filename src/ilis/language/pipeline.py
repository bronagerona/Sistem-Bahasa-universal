"""ILIS language pipeline: lexical inspection plus V1 semantic analysis."""

from __future__ import annotations

import re

from ilis.language.tokenizer import tokenize
from ilis.language.variation import variation_hint
from ilis.semantics.semantic_engine import SemanticEngine


def inspect_text(text: str) -> dict[str, object]:
    """Return observable token and lexical-variation information."""
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
            "Analisis semantik tersedia terpisah melalui analyze_semantics().",
            "Pemetaan variasi masih kecil dan berbasis aturan eksplisit.",
            "Belum melakukan koreksi typo secara kontekstual.",
        ],
    }


def analyze_semantics(text: str) -> dict[str, object]:
    """Run ILVE-style preprocessing and pass its contract payload to SemanticEngine.

    This adapter preserves the exact source text while converting the current
    inspect_text() representation into the stable Semantic Engine input contract.
    """
    inspection = inspect_text(text)
    token_items = inspection["tokens"]
    normalized_tokens: list[str] = []
    variation_hints: list[dict[str, str]] = []

    for item in token_items:
        surface = item["surface"]
        normalized = item["variation_hint"] or surface
        normalized_tokens.append(normalized)
        if item["variation_hint"] is not None:
            lowered = surface.casefold()
            category = "slang" if lowered in {
                "gue", "gw", "gua", "lu", "lo", "elu"
            } else "nonstandard"
            variation_hints.append(
                {
                    "surface": surface,
                    "normalized": normalized,
                    "category": category,
                }
            )

    normalized_text = " ".join(normalized_tokens)
    normalized_text = re.sub(r"\s+([.,!?;:])", r"\1", normalized_text)
    # A trailing response-style instruction is metadata for generation, not part
    # of the proposition. Preserve it when it is the entire user utterance so
    # the semantic engine can recognize it as a standalone command.
    standalone_style_command = re.fullmatch(
        r"(?:tolong\s+)?(?:jawab|jelaskan|uraikan|terangkan)\s+"
        r"(?:dengan\s+)?(?:sopan|singkat|ringkas|jelas|santai)[.!?]*",
        normalized_text, flags=re.IGNORECASE,
    )
    if not standalone_style_command:
        # Remove a leading style command when it introduces a question.
        # Example: "Tolong jawab dengan sopan, apakah naga takut lonceng?"
        normalized_text = re.sub(
            r"^(?:tolong\s+)?(?:jawab|jelaskan|uraikan|terangkan)\s+"
            r"(?:dengan\s+)?(?:sopan|singkat|ringkas|jelas|santai)"
            r"\s*[,;:]?\s*(?=(?:apakah|siapa|apa|mengapa|kenapa|"
            r"bagaimana|kapan|dimana|di\s+mana|mana)\b)",
            "", normalized_text, flags=re.IGNORECASE,
        ).strip()
        normalized_text = re.sub(
            r"\s+(?:tolong\s+)?(?:jawab|jelaskan|uraikan|terangkan)\s+"
            r"(?:dengan\s+)?(?:sopan|singkat|ringkas|jelas|santai)\s*[.!?]*$",
            "", normalized_text, flags=re.IGNORECASE,
        ).strip()
    payload = {
        "contract_version": "1.0",
        "original_text": text,
        "ilve": {
            "normalized_text": normalized_text,
            "tokens": normalized_tokens,
            "variation_hints": variation_hints,
        },
    }
    return SemanticEngine().analyze(payload)
