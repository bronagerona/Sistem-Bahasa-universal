"""Deterministic persona response renderer for validated ILIS configurations.

The renderer decorates an existing Core answer with the configured identity.
It does not call or modify ILIS Core, Semantic, Reasoning, adapters, or storage.
"""
from __future__ import annotations

import re

from .profiles import (
    ILIS_IDENTITY_REPLY,
    MODE_A,
    MODE_B,
    MODE_C,
    PersonaConfig,
    PersonaMode,
    validate_persona_config,
)


_ILIS_MENTION_PATTERN = re.compile(r"\bILIS\b", re.IGNORECASE)


class PersonaRenderer:
    """Add the configured identity reply when the caller requests it."""

    def __init__(self, config: PersonaConfig) -> None:
        errors = validate_persona_config(config)
        if errors:
            raise ValueError("PersonaConfig tidak valid: " + " ".join(errors))
        self._config = config

    def render(self, raw_answer: str, *, include_identity: bool = True) -> str:
        """Return the configured identity + unchanged Core answer.

        Mode A can suppress its ILIS prefix for non-identity responses by
        passing ``include_identity=False``. Modes B and C retain their
        configured application/character identity behavior regardless of
        this Mode-A-specific option.

        For NPC mode, ILIS references in either the identity reply or raw
        answer are rejected unless the character explicitly allows them.
        """
        if not isinstance(raw_answer, str):
            raise TypeError("raw_answer harus berupa string.")
        if not isinstance(include_identity, bool):
            raise TypeError("include_identity harus berupa boolean.")

        mode = PersonaMode(self._config.mode)
        if mode == MODE_A:
            if not include_identity:
                return raw_answer
            identity_reply = ILIS_IDENTITY_REPLY
        elif mode == MODE_B:
            identity_reply = self._config.application.identity_reply
        elif mode == MODE_C:
            character = self._config.character
            identity_reply = character.identity_reply
            if (
                not character.allow_ilis_reference
                and (
                    _ILIS_MENTION_PATTERN.search(identity_reply)
                    or _ILIS_MENTION_PATTERN.search(raw_answer)
                )
            ):
                raise ValueError(
                    "Mode character tidak boleh menghasilkan teks yang "
                    "menyebut ILIS kecuali allow_ilis_reference=True."
                )
        else:
            raise ValueError("mode persona tidak didukung oleh renderer.")

        if not raw_answer:
            return identity_reply
        return f"{identity_reply}\n\n{raw_answer}"


__all__ = ["PersonaRenderer"]
