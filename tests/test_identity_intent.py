"""Deterministic identity-intent routing tests for ChatbotAdapter."""

import pytest

from ilis.interfaces import ILISCore
from ilis.interfaces.chatbot_adapter import ChatbotAdapter
from ilis.persona import (
    ApplicationProfile,
    CharacterProfile,
    MODE_B,
    MODE_C,
    PersonaConfig,
)


@pytest.mark.parametrize(
    "message",
    [
        "Siapa kamu?",
        "Apa yang bisa kamu lakukan?",
        "Apa kemampuanmu?",
        "Jelaskan kemampuanmu.",
    ],
)
def test_mode_a_routes_identity_keywords_to_static_persona_answer(message):
    core = ILISCore()
    session_id = core.create_session()
    adapter = ChatbotAdapter(core)

    result = adapter.respond(message, session_id)

    assert result["answer"].startswith(
        "Saya ILIS, sistem kecerdasan bahasa.\n\n"
    )
    assert "memahami pertanyaan berbahasa Indonesia" in result["answer"]
    assert "tanpa menggunakan model bahasa besar (LLM)" in result["answer"]
    assert result["metadata"]["response_type"] == "identity_intent"
    assert result["metadata"]["register"] == "formal"
    assert result["semantic_result"] is None
    assert result["reasoning_result"] is None
    assert result["generation"] is None


def test_run_15_combined_greeting_identity_and_capability_question():
    core = ILISCore()
    session_id = core.create_session()
    adapter = ChatbotAdapter(core)
    message = "Halo siapa kamu? Jelaskan apa yang bisa kamu lakukan"

    result = adapter.respond(message, session_id)

    assert result["answer"].startswith(
        "Saya ILIS, sistem kecerdasan bahasa.\n\n"
    )
    assert "memahami pertanyaan berbahasa Indonesia" in result["answer"]
    assert "menarik kesimpulan berdasarkan aturan" in result["answer"]
    assert result["metadata"]["response_type"] == "identity_intent"


@pytest.mark.parametrize(
    ("config", "expected_identity"),
    [
        (
            PersonaConfig(
                mode=MODE_B,
                application=ApplicationProfile(
                    application_id="host-app",
                    display_name="Arunika",
                    role="asisten aplikasi",
                    identity_reply="Saya Arunika, asisten aplikasi ini.",
                ),
            ),
            "Saya Arunika, asisten aplikasi ini.",
        ),
        (
            PersonaConfig(
                mode=MODE_C,
                character=CharacterProfile(
                    character_id="raka",
                    display_name="Raka",
                    role="penjaga gerbang",
                    identity_reply="Aku Raka, penjaga gerbang kerajaan.",
                ),
            ),
            "Aku Raka, penjaga gerbang kerajaan.",
        ),
    ],
)
def test_non_mode_a_identity_phrase_uses_normal_core_pipeline(
    config, expected_identity
):
    core = ILISCore()
    session_id = core.create_session()
    adapter = ChatbotAdapter(core, persona_config=config)

    result = adapter.respond("Halo siapa kamu?", session_id)

    assert result["answer"].startswith(expected_identity + "\n\n")
    assert result["metadata"].get("response_type") != "identity_intent"
    assert result["semantic_result"] is not None
    assert result["reasoning_result"] is not None
    assert result["generation"] is not None
