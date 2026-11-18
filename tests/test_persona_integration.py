"""Adapter-level integration tests for the V2.1 Persona Layer."""

from ilis.interfaces import ILISCore
from ilis.interfaces.chatbot_adapter import ChatbotAdapter
from ilis.interfaces.game_adapter import GameEngineAdapter
from ilis.persona import (
    ApplicationProfile,
    CharacterProfile,
    MODE_B,
    MODE_C,
    PersonaConfig,
)


def test_chatbot_adapter_defaults_to_mode_a_ilis_identity():
    core = ILISCore()
    session_id = core.create_session()
    adapter = ChatbotAdapter(core)

    result = adapter.respond("Apakah api bisa membakar kayu?", session_id)

    assert result["answer"].startswith("Saya ILIS, sistem kecerdasan bahasa.\n\n")
    assert result["text"] == result["answer"]
    assert "kemungkinan" in result["generation"]["text"].casefold()
    assert result["generation"]["text"] != result["answer"]
    assert result["reasoning_result"]["reasoning_type"] == "verified_inference"


def test_game_adapter_supports_mode_b_application_identity():
    core = ILISCore()
    session_id = core.create_session()
    config = PersonaConfig(
        mode=MODE_B,
        application=ApplicationProfile(
            application_id="fantasy-game",
            display_name="Penjaga Dunia",
            role="narator permainan",
            identity_reply="Saya Penjaga Dunia, narator permainan ini.",
        ),
    )
    adapter = GameEngineAdapter(core, persona_config=config)

    result = adapter.handle_event("Naga takut lonceng", session_id, npc="narator")

    assert result["npc"] == "narator"
    assert result["dialogue"].startswith(
        "Saya Penjaga Dunia, narator permainan ini.\n\n"
    )
    assert result["answer"] == result["dialogue"]
    assert "naga takut pada lonceng" in result["generation"]["text"].casefold()


def test_game_adapter_mode_c_keeps_npc_dialogue_free_of_ilis_reference():
    core = ILISCore()
    session_id = core.create_session()
    config = PersonaConfig(
        mode=MODE_C,
        character=CharacterProfile(
            character_id="cave-guardian",
            display_name="Penjaga Gua",
            role="penjaga gua",
            identity_reply="Aku Penjaga Gua, pelindung tempat ini.",
        ),
    )
    adapter = GameEngineAdapter(core, persona_config=config)

    result = adapter.handle_event("Naga takut lonceng", session_id)

    assert result["dialogue"].startswith(
        "Aku Penjaga Gua, pelindung tempat ini.\n\n"
    )
    assert "ilis" not in result["dialogue"].casefold()
    assert "naga takut pada lonceng" in result["dialogue"].casefold()


def test_game_adapter_mode_c_allows_ilis_when_explicitly_part_of_lore():
    core = ILISCore()
    session_id = core.create_session()
    config = PersonaConfig(
        mode=MODE_C,
        character=CharacterProfile(
            character_id="archive-spirit",
            display_name="Roh Arsip",
            role="penjaga arsip",
            identity_reply="Aku Roh Arsip yang mengenal ILIS dalam kisah dunia ini.",
            allow_ilis_reference=True,
        ),
    )
    adapter = GameEngineAdapter(core, persona_config=config)

    result = adapter.handle_event("Naga takut lonceng", session_id)

    assert "ilis" in result["dialogue"].casefold()
    assert "naga takut pada lonceng" in result["dialogue"].casefold()
