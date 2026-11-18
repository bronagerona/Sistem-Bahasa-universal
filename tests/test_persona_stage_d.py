"""Stage D behavioral regression tests for the V2.1 Persona Layer."""

from ilis.interfaces import ILISCore
from ilis.interfaces.chatbot_adapter import ChatbotAdapter
from ilis.interfaces.game_adapter import GameEngineAdapter
from ilis.persona import (
    ApplicationProfile,
    CharacterProfile,
    MODE_B,
    MODE_C,
    PersonaConfig,
    PersonaRenderer,
)


def _application_config():
    return PersonaConfig(
        mode=MODE_B,
        application=ApplicationProfile(
            application_id="arunika",
            display_name="Arunika",
            role="asisten aplikasi",
            identity_reply="Saya Arunika, asisten aplikasi ini.",
            default_register="formal",
        ),
    )


def _character_config():
    return PersonaConfig(
        mode=MODE_C,
        character=CharacterProfile(
            character_id="raka",
            display_name="Raka",
            role="penjaga gerbang",
            identity_reply="Aku Raka, penjaga gerbang kerajaan.",
            default_register="informal",
        ),
    )


def test_chatbot_mode_a_keeps_ilis_identity_across_multiple_turns():
    core = ILISCore()
    session_id = core.create_session()
    adapter = ChatbotAdapter(core)

    first = adapter.respond("Apakah api bisa membakar kayu?", session_id)
    second = adapter.respond("Apakah naga takut lonceng?", session_id)

    expected = "Saya ILIS, sistem kecerdasan bahasa.\n\n"
    assert first["answer"].startswith(expected)
    assert second["answer"].startswith(expected)


def test_chatbot_can_use_host_application_identity():
    core = ILISCore()
    session_id = core.create_session()
    adapter = ChatbotAdapter(core, persona_config=_application_config())

    result = adapter.respond("Apakah api bisa membakar kayu?", session_id)

    assert result["answer"].startswith("Saya Arunika, asisten aplikasi ini.\n\n")
    assert "Saya ILIS" not in result["answer"]


def test_game_mode_c_speaks_as_the_configured_npc():
    core = ILISCore()
    session_id = core.create_session()
    adapter = GameEngineAdapter(core, persona_config=_character_config())

    result = adapter.handle_event("naga takut lonceng", session_id, npc="raka")

    assert result["npc"] == "raka"
    assert result["dialogue"].startswith("Aku Raka, penjaga gerbang kerajaan.\n\n")
    assert "ilis" not in result["dialogue"].casefold()


def test_game_adapter_without_persona_preserves_legacy_generation_text():
    core = ILISCore()
    session_id = core.create_session()
    adapter = GameEngineAdapter(core)

    result = adapter.handle_event("naga takut lonceng", session_id)

    assert result["dialogue"] == result["generation"]["text"]
    assert result["answer"] == result["generation"]["text"]


def test_polite_instruction_survives_ilis_persona_rendering():
    core = ILISCore()
    session_id = core.create_session()
    adapter = ChatbotAdapter(core)

    result = adapter.respond(
        "Apakah api bisa membakar kayu? Jawab dengan sopan.", session_id
    )

    assert result["metadata"]["register"] == "formal"
    assert result["generation"]["text"].startswith("Dengan senang hati,")
    assert result["answer"].startswith("Saya ILIS, sistem kecerdasan bahasa.\n\n")
    assert "Dengan senang hati," in result["answer"]


def test_casual_instruction_survives_application_persona_rendering():
    core = ILISCore()
    session_id = core.create_session()
    adapter = ChatbotAdapter(core, persona_config=_application_config())

    result = adapter.respond(
        "Apakah api bisa membakar kayu? Jawab dengan santai.", session_id
    )

    assert result["metadata"]["register"] == "informal"
    assert result["generation"]["text"].startswith("Iya, kayaknya")
    assert result["answer"].startswith("Saya Arunika, asisten aplikasi ini.\n\n")
    assert "Iya, kayaknya" in result["answer"]


def test_persona_choice_does_not_change_semantic_reasoning_or_generation():
    question = "Apakah api bisa membakar kayu?"

    core_ilis = ILISCore()
    session_ilis = core_ilis.create_session()
    result_ilis = ChatbotAdapter(core_ilis).respond(question, session_ilis)

    core_app = ILISCore()
    session_app = core_app.create_session()
    result_app = ChatbotAdapter(
        core_app, persona_config=_application_config()
    ).respond(question, session_app)

    assert result_ilis["semantic_result"] == result_app["semantic_result"]
    assert result_ilis["reasoning_result"] == result_app["reasoning_result"]
    assert result_ilis["generation"] == result_app["generation"]
    assert result_ilis["answer"] != result_app["answer"]


def test_renderer_preserves_raw_generator_text_as_an_exact_suffix():
    raw_text = "  Kesimpulan inti tidak boleh diubah.  "
    renderer = PersonaRenderer(_character_config())

    rendered = renderer.render(raw_text)

    assert rendered == "Aku Raka, penjaga gerbang kerajaan.\n\n" + raw_text
    assert rendered.endswith(raw_text)
