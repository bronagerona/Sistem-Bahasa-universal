"""Persona identity profiles and deterministic configuration validation.

This module only describes and validates profiles. It does not render responses,
read application settings, access ILIS Core, or persist persona data.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import re
from typing import Optional, Tuple


class PersonaMode(str, Enum):
    """Supported identity modes for an application integration."""

    CHATBOT_ILIS = "chatbot_ilis"
    APPLICATION = "application"
    CHARACTER = "character"


# Public aliases used by application configuration (Mode A, B, and C).
MODE_A = PersonaMode.CHATBOT_ILIS
MODE_B = PersonaMode.APPLICATION
MODE_C = PersonaMode.CHARACTER

SUPPORTED_REGISTERS = frozenset({"formal", "informal", "slang"})
ILIS_MENTION_PATTERN = re.compile(r"\bILIS\b", re.IGNORECASE)
ILIS_IDENTITY_REPLY = "Saya ILIS, sistem kecerdasan bahasa."


@dataclass(frozen=True)
class ApplicationProfile:
    """Identity owned by a host application (Mode A or Mode B)."""

    application_id: str
    display_name: str
    role: str
    identity_reply: str
    default_register: str = "formal"


@dataclass(frozen=True)
class CharacterProfile:
    """Identity and lore boundaries for one active game character (Mode C)."""

    character_id: str
    display_name: str
    role: str
    identity_reply: str
    default_register: str = "formal"
    lore_boundaries: Tuple[str, ...] = ()
    # Only set this when the game explicitly makes ILIS part of its lore.
    allow_ilis_reference: bool = False


@dataclass(frozen=True)
class PersonaConfig:
    """Validated-at-boundary persona configuration supplied by an adapter."""

    mode: PersonaMode
    application: Optional[ApplicationProfile] = None
    character: Optional[CharacterProfile] = None

    @classmethod
    def chatbot_ilis(cls) -> "PersonaConfig":
        """Build the canonical Mode A configuration."""
        return cls(
            mode=MODE_A,
            application=ApplicationProfile(
                application_id="ilis-chatbot",
                display_name="ILIS",
                role="sistem kecerdasan bahasa",
                identity_reply=ILIS_IDENTITY_REPLY,
                default_register="formal",
            ),
        )


def _required_text(value: object, field_name: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{field_name} wajib berupa teks yang tidak kosong.")


def _validate_register(value: object, field_name: str, errors: list[str]) -> None:
    if value not in SUPPORTED_REGISTERS:
        allowed = ", ".join(sorted(SUPPORTED_REGISTERS))
        errors.append(f"{field_name} harus salah satu dari: {allowed}.")


def validate_persona_config(config: object) -> list[str]:
    """Return validation errors; an empty list means the config is valid.

    Validation is intentionally side-effect free and does not modify the
    Semantic or Reasoning payloads, adapters, Core, or SQLite storage.
    """
    if not isinstance(config, PersonaConfig):
        return ["config harus berupa PersonaConfig."]

    errors: list[str] = []
    try:
        mode = PersonaMode(config.mode)
    except (TypeError, ValueError):
        return ["mode persona tidak dikenal."]

    app = config.application
    character = config.character

    if mode in (MODE_A, MODE_B):
        if app is None:
            errors.append("profil application wajib diisi untuk mode ini.")
        elif not isinstance(app, ApplicationProfile):
            errors.append("application harus berupa ApplicationProfile.")
        else:
            for field_name in ("application_id", "display_name", "role", "identity_reply"):
                _required_text(getattr(app, field_name), f"application.{field_name}", errors)
            _validate_register(app.default_register, "application.default_register", errors)

        if character is not None:
            errors.append("character harus None untuk mode chatbot/application.")

        if mode == MODE_A and isinstance(app, ApplicationProfile):
            if app.display_name.strip().casefold() != "ilis":
                errors.append("mode chatbot_ilis harus menggunakan display_name 'ILIS'.")
            normalized_reply = " ".join(app.identity_reply.casefold().split())
            if "ilis" not in normalized_reply or "sistem kecerdasan bahasa" not in normalized_reply:
                errors.append(
                    "identity_reply mode chatbot_ilis harus memperkenalkan ILIS "
                    "sebagai sistem kecerdasan bahasa."
                )

    elif mode == MODE_C:
        if not isinstance(character, CharacterProfile):
            errors.append("profil character wajib berupa CharacterProfile untuk mode character.")
        else:
            for field_name in ("character_id", "display_name", "role", "identity_reply"):
                _required_text(getattr(character, field_name), f"character.{field_name}", errors)
            _validate_register(character.default_register, "character.default_register", errors)
            if not isinstance(character.lore_boundaries, tuple):
                errors.append("character.lore_boundaries harus berupa tuple teks.")
            elif any(not isinstance(item, str) or not item.strip() for item in character.lore_boundaries):
                errors.append("setiap character.lore_boundaries harus berupa teks yang tidak kosong.")
            if not isinstance(character.allow_ilis_reference, bool):
                errors.append("character.allow_ilis_reference harus berupa boolean.")
            elif (
                not character.allow_ilis_reference
                and isinstance(character.identity_reply, str)
                and ILIS_MENTION_PATTERN.search(character.identity_reply)
            ):
                errors.append(
                    "identity_reply NPC tidak boleh menyebut ILIS kecuali "
                    "allow_ilis_reference=True karena bagian eksplisit dari lore."
                )

        if app is not None and not isinstance(app, ApplicationProfile):
            errors.append("application pada mode character harus berupa ApplicationProfile atau None.")

    return errors


__all__ = [
    "ApplicationProfile",
    "CharacterProfile",
    "PersonaConfig",
    "PersonaMode",
    "MODE_A",
    "MODE_B",
    "MODE_C",
    "SUPPORTED_REGISTERS",
    "ILIS_IDENTITY_REPLY",
    "validate_persona_config",
]
