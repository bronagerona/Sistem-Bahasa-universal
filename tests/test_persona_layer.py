"""Unit tests for persona profiles and configuration validation only."""

import pytest

from ilis.persona import (
    ILIS_IDENTITY_REPLY,
    MODE_A,
    MODE_B,
    MODE_C,
    ApplicationProfile,
    CharacterProfile,
    PersonaConfig,
    PersonaRenderer,
    PersonaMode,
    validate_persona_config,
)


def app_profile(**overrides):
    values = {
        "application_id": "arunika-app",
        "display_name": "Toko Arunika",
        "role": "asisten layanan toko",
        "identity_reply": "Saya asisten layanan Toko Arunika.",
        "default_register": "formal",
    }
    values.update(overrides)
    return ApplicationProfile(**values)


def npc_profile(**overrides):
    values = {
        "character_id": "gate-keeper",
        "display_name": "Raka",
        "role": "penjaga gerbang",
        "identity_reply": "Aku Raka, penjaga gerbang kerajaan.",
        "default_register": "informal",
        "lore_boundaries": ("Tidak mengetahui isi istana.",),
    }
    values.update(overrides)
    return CharacterProfile(**values)


def test_mode_constants_map_to_expected_modes():
    assert MODE_A is PersonaMode.CHATBOT_ILIS
    assert MODE_B is PersonaMode.APPLICATION
    assert MODE_C is PersonaMode.CHARACTER


def test_mode_a_factory_builds_canonical_ilis_identity():
    config = PersonaConfig.chatbot_ilis()

    assert config.mode == MODE_A
    assert config.application.identity_reply == ILIS_IDENTITY_REPLY
    assert config.character is None
    assert validate_persona_config(config) == []


def test_mode_a_rejects_non_ilis_display_name():
    config = PersonaConfig(
        mode=MODE_A,
        application=app_profile(display_name="Asisten Lain"),
    )

    errors = validate_persona_config(config)

    assert any("display_name 'ILIS'" in error for error in errors)


def test_mode_a_requires_canonical_ilis_identity_description():
    config = PersonaConfig(
        mode=MODE_A,
        application=app_profile(
            display_name="ILIS",
            identity_reply="Saya asisten virtual.",
        ),
    )

    errors = validate_persona_config(config)

    assert any("sistem kecerdasan bahasa" in error for error in errors)


def test_mode_b_accepts_complete_application_profile():
    config = PersonaConfig(mode=MODE_B, application=app_profile())

    assert validate_persona_config(config) == []


@pytest.mark.parametrize(
    "field,value",
    [
        ("application_id", ""),
        ("display_name", "   "),
        ("role", ""),
        ("identity_reply", ""),
    ],
)
def test_mode_b_rejects_missing_required_application_fields(field, value):
    config = PersonaConfig(mode=MODE_B, application=app_profile(**{field: value}))

    errors = validate_persona_config(config)

    assert any(f"application.{field}" in error for error in errors)


@pytest.mark.parametrize("register", ["unknown", "", None, "casual"])
def test_application_profile_rejects_unsupported_register(register):
    config = PersonaConfig(
        mode=MODE_B,
        application=app_profile(default_register=register),
    )

    errors = validate_persona_config(config)

    assert any("application.default_register" in error for error in errors)


def test_mode_b_rejects_character_profile():
    config = PersonaConfig(
        mode=MODE_B,
        application=app_profile(),
        character=npc_profile(),
    )

    assert any("character harus None" in error for error in validate_persona_config(config))


def test_mode_c_accepts_complete_npc_profile_without_ilis_reference():
    config = PersonaConfig(mode=MODE_C, character=npc_profile())

    assert validate_persona_config(config) == []


@pytest.mark.parametrize(
    "field,value",
    [
        ("character_id", ""),
        ("display_name", " "),
        ("role", ""),
        ("identity_reply", ""),
    ],
)
def test_mode_c_rejects_missing_required_character_fields(field, value):
    config = PersonaConfig(mode=MODE_C, character=npc_profile(**{field: value}))

    errors = validate_persona_config(config)

    assert any(f"character.{field}" in error for error in errors)


@pytest.mark.parametrize("register", ["unknown", "", None, "santai"])
def test_character_profile_rejects_unsupported_register(register):
    config = PersonaConfig(
        mode=MODE_C,
        character=npc_profile(default_register=register),
    )

    errors = validate_persona_config(config)

    assert any("character.default_register" in error for error in errors)


def test_mode_c_rejects_npc_identity_reply_that_mentions_ilis():
    config = PersonaConfig(
        mode=MODE_C,
        character=npc_profile(identity_reply="Aku ILIS, penjaga gerbang."),
    )

    errors = validate_persona_config(config)

    assert any("NPC tidak boleh menyebut ILIS" in error for error in errors)


def test_mode_c_allows_ilis_reference_only_when_explicit_lore_flag_is_true():
    config = PersonaConfig(
        mode=MODE_C,
        character=npc_profile(
            identity_reply="Dalam legenda, ILIS adalah nama artefak kuno.",
            allow_ilis_reference=True,
        ),
    )

    assert validate_persona_config(config) == []


def test_mode_c_rejects_non_tuple_lore_boundaries():
    config = PersonaConfig(
        mode=MODE_C,
        character=npc_profile(lore_boundaries=["Tidak tahu isi istana"]),
    )

    assert any("lore_boundaries harus berupa tuple" in error for error in validate_persona_config(config))


def test_mode_c_rejects_empty_lore_boundary_items():
    config = PersonaConfig(
        mode=MODE_C,
        character=npc_profile(lore_boundaries=("   ",)),
    )

    assert any("setiap character.lore_boundaries" in error for error in validate_persona_config(config))


def test_mode_c_rejects_non_boolean_ilis_lore_flag():
    config = PersonaConfig(
        mode=MODE_C,
        character=npc_profile(allow_ilis_reference="yes"),
    )

    assert any("allow_ilis_reference harus berupa boolean" in error for error in validate_persona_config(config))


def test_mode_c_rejects_wrong_character_profile_type():
    config = PersonaConfig(mode=MODE_C, character=app_profile())

    assert any("CharacterProfile" in error for error in validate_persona_config(config))


def test_mode_a_and_b_require_application_profile():
    assert validate_persona_config(PersonaConfig(mode=MODE_A)) != []
    assert validate_persona_config(PersonaConfig(mode=MODE_B)) != []


def test_unknown_mode_is_rejected():
    config = PersonaConfig(mode="unsupported-mode")

    assert any("mode persona tidak dikenal" in error for error in validate_persona_config(config))


def test_non_persona_config_is_rejected():
    assert validate_persona_config({"mode": "character"}) == [
        "config harus berupa PersonaConfig."
    ]


def test_profiles_are_immutable():
    profile = app_profile()

    with pytest.raises((AttributeError, TypeError)):
        profile.display_name = "Nama Baru"



# Stage B: deterministic identity rendering (no adapter/Core integration).


def test_renderer_mode_a_uses_canonical_ilis_identity_reply():
    renderer = PersonaRenderer(PersonaConfig.chatbot_ilis())

    assert renderer.render("Halo!") == f"{ILIS_IDENTITY_REPLY}\n\nHalo!"


def test_renderer_mode_b_prefixes_application_identity_reply():
    config = PersonaConfig(mode=MODE_B, application=app_profile())
    renderer = PersonaRenderer(config)

    assert renderer.render("Ada yang bisa saya bantu?") == (
        "Saya asisten layanan Toko Arunika.\n\n"
        "Ada yang bisa saya bantu?"
    )


def test_renderer_mode_c_prefixes_npc_identity_without_mentioning_ilis():
    renderer = PersonaRenderer(PersonaConfig(mode=MODE_C, character=npc_profile()))

    result = renderer.render("Gerbang kerajaan ada di sebelah utara.")

    assert result == (
        "Aku Raka, penjaga gerbang kerajaan.\n\n"
        "Gerbang kerajaan ada di sebelah utara."
    )
    assert "ILIS" not in result


def test_renderer_mode_c_rejects_ilis_mention_in_raw_answer_without_lore_flag():
    renderer = PersonaRenderer(PersonaConfig(mode=MODE_C, character=npc_profile()))

    with pytest.raises(ValueError, match="allow_ilis_reference=True"):
        renderer.render("Aku pernah mendengar nama ILIS.")


def test_renderer_mode_c_allows_ilis_mention_when_explicit_lore_flag_is_true():
    config = PersonaConfig(
        mode=MODE_C,
        character=npc_profile(
            identity_reply="Dalam legenda, ILIS adalah nama artefak kuno.",
            allow_ilis_reference=True,
        ),
    )
    renderer = PersonaRenderer(config)

    result = renderer.render("Legenda itu menyebut ILIS sebagai artefak.")

    assert "ILIS" in result


def test_renderer_rejects_invalid_persona_config():
    with pytest.raises(ValueError, match="PersonaConfig tidak valid"):
        PersonaRenderer(PersonaConfig(mode=MODE_B))


def test_renderer_rejects_non_string_core_answer():
    renderer = PersonaRenderer(PersonaConfig.chatbot_ilis())

    with pytest.raises(TypeError, match="raw_answer harus berupa string"):
        renderer.render(None)


def test_renderer_returns_identity_reply_when_core_answer_is_empty():
    renderer = PersonaRenderer(PersonaConfig.chatbot_ilis())

    assert renderer.render("") == ILIS_IDENTITY_REPLY


def test_renderer_preserves_raw_core_answer_text_exactly():
    renderer = PersonaRenderer(PersonaConfig.chatbot_ilis())
    raw_answer = "  Jawaban inti tetap apa adanya.  "

    result = renderer.render(raw_answer)

    assert result.endswith(raw_answer)
