"""Strict structural validators for the ILIS Semantic Engine contract 1.0."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ilis.semantics.constants import (
    ASPECTS,
    CONTRACT_VERSION,
    INTENTS,
    MODALITIES,
    NEGATIONS,
    REGISTERS,
    SEMANTIC_FIELDS,
    STATUSES,
)


class ContractValidationError(ValueError):
    """Raised when an input or output violates the ILIS contract."""


def validate_input(payload: Any) -> dict[str, Any]:
    """Validate and return a contract-1.0 ILVE + original-text input."""
    if not isinstance(payload, Mapping):
        raise ContractValidationError("input must be an object")
    if payload.get("contract_version") != CONTRACT_VERSION:
        raise ContractValidationError("contract_version must be '1.0'")
    original = payload.get("original_text")
    if not isinstance(original, str) or not original.strip():
        raise ContractValidationError("original_text must be a non-empty string")

    ilve = payload.get("ilve")
    if not isinstance(ilve, Mapping):
        raise ContractValidationError("ilve must be an object")
    if not isinstance(ilve.get("normalized_text"), str) or not ilve["normalized_text"].strip():
        raise ContractValidationError("ilve.normalized_text must be a non-empty string")
    tokens = ilve.get("tokens")
    if not isinstance(tokens, list) or not all(isinstance(token, str) for token in tokens):
        raise ContractValidationError("ilve.tokens must be an array of strings")
    hints = ilve.get("variation_hints")
    if not isinstance(hints, list):
        raise ContractValidationError("ilve.variation_hints must be an array")
    for index, hint in enumerate(hints):
        if not isinstance(hint, Mapping):
            raise ContractValidationError(f"variation_hints[{index}] must be an object")
        for field in ("surface", "normalized", "category"):
            if not isinstance(hint.get(field), str) or not hint[field]:
                raise ContractValidationError(
                    f"variation_hints[{index}].{field} must be a non-empty string"
                )
    # Copy containers so callers cannot mutate the returned input by alias.
    return {
        "contract_version": CONTRACT_VERSION,
        "original_text": original,
        "ilve": {
            "normalized_text": ilve["normalized_text"],
            "tokens": list(tokens),
            "variation_hints": [dict(hint) for hint in hints],
        },
    }


def validate_output(payload: Any) -> dict[str, Any]:
    """Validate output wrapper, all twelve semantic fields, and exact enums."""
    if not isinstance(payload, Mapping):
        raise ContractValidationError("output must be an object")
    if payload.get("contract_version") != CONTRACT_VERSION:
        raise ContractValidationError("output contract_version must be '1.0'")
    # The result must retain the exact source and validated ILVE payload.
    validate_input(
        {
            "contract_version": payload.get("contract_version"),
            "original_text": payload.get("original_text"),
            "ilve": payload.get("ilve"),
        }
    )
    status = payload.get("status")
    if status not in STATUSES:
        raise ContractValidationError(f"status must be one of {sorted(STATUSES)}")
    semantics = payload.get("semantics")
    if status == "unsupported":
        if semantics is not None:
            raise ContractValidationError("unsupported output must have semantics=null")
        return dict(payload)
    if not isinstance(semantics, Mapping):
        raise ContractValidationError("supported/low_confidence output needs semantics object")
    actual_fields = set(semantics)
    expected_fields = set(SEMANTIC_FIELDS)
    missing = sorted(expected_fields - actual_fields)
    extra = sorted(actual_fields - expected_fields)
    if missing or extra:
        details = []
        if missing:
            details.append(f"missing: {', '.join(missing)}")
        if extra:
            details.append(f"unexpected: {', '.join(extra)}")
        raise ContractValidationError(
            "semantics must contain exactly the twelve contract fields ("
            + "; ".join(details)
            + ")"
        )

    for field in SEMANTIC_FIELDS[:6]:
        value = semantics[field]
        if value is not None and (not isinstance(value, str) or not value.strip()):
            raise ContractValidationError(f"{field} must be a non-empty string or null")
    enum_fields = {
        "Aspect": ASPECTS,
        "Negation": NEGATIONS,
        "Modality": MODALITIES,
        "Intent": INTENTS,
        "Register": REGISTERS,
    }
    for field, allowed in enum_fields.items():
        if semantics[field] not in allowed:
            raise ContractValidationError(f"{field} must be one of {sorted(allowed)}")
    confidence = semantics["Confidence"]
    if isinstance(confidence, bool) or not isinstance(confidence, (int, float)):
        raise ContractValidationError("Confidence must be a number")
    if not 0.0 <= confidence <= 1.0:
        raise ContractValidationError("Confidence must be between 0.0 and 1.0")
    return dict(payload)
