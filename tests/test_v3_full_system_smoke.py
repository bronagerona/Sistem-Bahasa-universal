"""V3 full-system smoke tests across the V2.2 and V3 integration layers.

These tests exercise existing production wiring only. KNOWN fixture data remains
isolated in the test process; no production seed or persistence is modified.
"""

from ilis.interfaces import ChatbotAdapter, GameEngineAdapter, ILISCore
from ilis.persona import (
    ApplicationProfile,
    CharacterProfile,
    MODE_B,
    MODE_C,
    PersonaConfig,
)

SEMANTIC_FIELDS = {
    "Actor", "Predicate", "Patient/Object", "Intent", "Time", "Aspect",
    "Location", "Recipient", "Negation", "Modality", "Register", "Confidence",
}
REASONING_KEYS = {
    "conclusion", "confidence_score", "evidence",
    "reasoning_type", "reasons", "uncertainty",
}


def test_smoke_legacy_exact_fact_has_priority_through_chatbot_pipeline():
    core = ILISCore()
    adapter = ChatbotAdapter(core)
    session_id = adapter.create_session()

    result = adapter.respond("Apakah api bisa membakar kertas?", session_id)

    assert result["semantic_result"]["status"] == "supported"
    assert set(result["semantic_result"]["semantics"]) == SEMANTIC_FIELDS
    assert set(result["reasoning_result"]) == REASONING_KEYS
    assert result["reasoning_result"]["reasoning_type"] == "verified_inference"
    assert result["reasoning_result"]["evidence"] == ["fact_3"]
    assert result["generation"]["reasoning_type"] == "verified_inference"
    assert result["metadata"]["session_id"] == session_id
    assert result["answer"].startswith("Saya ILIS, sistem kecerdasan bahasa.")


def test_smoke_concept_partial_and_unknown_reach_language_generator():
    partial_core = ILISCore(seed_core_knowledge=False)
    partial_adapter = ChatbotAdapter(partial_core)
    partial_session = partial_adapter.create_session()
    partial = partial_adapter.respond(
        "Apakah api bisa membakar paper?", partial_session
    )

    assert partial["reasoning_result"]["reasoning_type"] == "concept_inference_partial"
    assert partial["generation"]["reasoning_type"] == "concept_inference_partial"
    assert partial["generation"]["uncertainty_preserved"] is True
    assert partial["generation"]["text"].endswith(
        "Informasi belum lengkap, ini hanya dugaan."
    )

    unknown_core = ILISCore(seed_core_knowledge=False)
    unknown_adapter = ChatbotAdapter(unknown_core)
    unknown_session = unknown_adapter.create_session()
    unknown = unknown_adapter.respond(
        "Apakah api bisa membakar besi?", unknown_session
    )

    assert unknown["reasoning_result"]["reasoning_type"] == "concept_inference_unknown"
    assert unknown["generation"]["reasoning_type"] == "concept_inference_unknown"
    assert unknown["generation"]["text"] == (
        "Belum cukup informasi untuk memastikan jawaban atas pertanyaanmu."
    )


def test_smoke_multi_turn_identity_and_reset_keep_one_session():
    core = ILISCore()
    adapter = ChatbotAdapter(core)
    session_id = adapter.create_session()

    first = adapter.respond("Apakah api bisa membakar kayu?", session_id)
    second = adapter.respond(
        "Lalu apakah api juga bisa membakar kertas?", session_id
    )
    identity = adapter.respond("Lu siapa?", session_id)

    assert first["metadata"]["session_id"] == session_id
    assert second["metadata"]["session_id"] == session_id
    assert second["metadata"]["context_turns_used"] == 1
    assert second["reasoning_result"]["evidence"] == ["fact_3"]
    assert identity["metadata"]["response_type"] == "identity_intent"
    assert len(adapter.session_manager.get_recent_turns(session_id)) == 3

    reset = adapter.respond("reset percakapan", session_id)
    assert reset["metadata"]["response_type"] == "session_reset"
    assert reset["metadata"]["session_id"] == session_id
    assert adapter.session_manager.get_context_snapshot(session_id)["turns"] == []


def test_smoke_style_instruction_reaches_generation_without_leaking():
    core = ILISCore()
    adapter = ChatbotAdapter(core)
    session_id = adapter.create_session()

    formal = adapter.respond(
        "Apakah api bisa membakar kayu? Jawab dengan sopan.", session_id
    )
    informal = adapter.respond(
        "Apakah api bisa membakar kayu? Jawab dengan santai.", session_id
    )

    assert formal["metadata"]["register"] == "formal"
    assert formal["generation"]["text"].startswith("Dengan senang hati,")
    assert informal["metadata"]["register"] == "informal"
    assert informal["generation"]["text"].startswith("Iya, kayaknya")
    assert "jawab dengan" not in formal["answer"].casefold()
    assert "jawab dengan" not in informal["answer"].casefold()


def test_smoke_game_adapter_preserves_application_and_npc_personas():
    application = PersonaConfig(
        mode=MODE_B,
        application=ApplicationProfile(
            application_id="smoke-game",
            display_name="Penjaga Dunia",
            role="narator permainan",
            identity_reply="Saya Penjaga Dunia, narator permainan ini.",
        ),
    )
    app_adapter = GameEngineAdapter(ILISCore(), persona_config=application)
    app_session = app_adapter.create_session()
    app_result = app_adapter.handle_event(
        "naga takut lonceng", app_session, npc="narator"
    )

    assert app_result["dialogue"].startswith(
        "Saya Penjaga Dunia, narator permainan ini."
    )
    assert app_result["metadata"]["session_id"] == app_session
    assert app_result["episode"]["episode_id"] == app_result["metadata"]["episode_id"]

    character = PersonaConfig(
        mode=MODE_C,
        character=CharacterProfile(
            character_id="smoke-guardian",
            display_name="Penjaga Gua",
            role="penjaga gua",
            identity_reply="Aku Penjaga Gua, pelindung tempat ini.",
        ),
    )
    npc_adapter = GameEngineAdapter(ILISCore(), persona_config=character)
    npc_session = npc_adapter.create_session()
    npc_result = npc_adapter.handle_event(
        "naga takut lonceng", npc_session, npc="Penjaga Gua"
    )

    assert npc_result["dialogue"].startswith(
        "Aku Penjaga Gua, pelindung tempat ini."
    )
    assert "ilis" not in npc_result["dialogue"].casefold()
    assert npc_result["metadata"]["session_id"] == npc_session
