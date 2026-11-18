"""Multi-turn adapter session tests plus V2.1 regression coverage."""

import pytest

from ilis.interfaces import (
    ILISCore, ChatbotAdapter, GameEngineAdapter, SessionManager,
)
from ilis.persona import (
    ApplicationProfile, CharacterProfile, PersonaConfig, MODE_B, MODE_C,
)


@pytest.fixture
def setup_chatbot():
    core = ILISCore()
    manager = SessionManager(max_turns=5)
    adapter = ChatbotAdapter(core, session_manager=manager)
    session_id = adapter.create_session()
    return core, manager, adapter, session_id


# ---------------------------------------------------------------------------
# 14 positive multi-turn tests
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("turn_count", range(1, 15))
def test_multi_turn_store_accepts_complete_turns_and_builds_bounded_snapshot(turn_count):
    manager = SessionManager(max_turns=5)
    sid = manager.create_session()
    for index in range(turn_count):
        manager.add_turn(sid, f"Pertanyaan {index}", f"Jawaban {index}")
    snapshot = manager.get_context_snapshot(sid)
    expected = min(turn_count, 5)
    assert len(snapshot["turns"]) == expected
    assert snapshot["turns"][-1]["user_message"] == f"Pertanyaan {turn_count - 1}"
    assert snapshot["turns"][-1]["assistant_response"] == f"Jawaban {turn_count - 1}"


def test_multi_turn_example_fire_wood_then_paper_uses_same_session(setup_chatbot):
    core, manager, adapter, sid = setup_chatbot
    first = adapter.respond("Apakah api bisa membakar kayu?", sid)
    second = adapter.respond("Lalu apakah api juga bisa membakar kertas?", sid)
    assert first["generation"]["text"].startswith("Ya,")
    assert second["generation"]["text"].startswith("Ya,")
    assert second["reasoning_result"]["reasoning_type"] == "verified_inference"
    assert second["reasoning_result"]["evidence"]
    assert any("pertanyaan lanjutan" in reason for reason in second["reasoning_result"]["reasons"])
    assert second["metadata"]["session_id"] == sid
    assert second["metadata"]["context_turns_used"] == 1
    assert second["context_snapshot"]["turns"][0]["user_message"] == "Apakah api bisa membakar kayu?"
    assert second["semantic_result"]["semantics"]["Patient/Object"] == "kertas"
    assert len(manager.get_recent_turns(sid)) == 2


def test_multi_turn_new_session_has_no_previous_context():
    adapter = ChatbotAdapter(ILISCore())
    first_sid = adapter.create_session()
    adapter.respond("Apakah api bisa membakar kayu?", first_sid)
    second_sid = adapter.create_session()
    result = adapter.respond("Lalu apakah api juga bisa membakar kertas?", second_sid)
    assert result["metadata"]["context_turns_used"] == 0
    assert not any("pertanyaan lanjutan" in reason for reason in result["reasoning_result"]["reasons"])


def test_multi_turn_context_snapshot_is_passed_to_core_without_semantic_mutation(setup_chatbot):
    core, manager, adapter, sid = setup_chatbot
    adapter.respond("Apakah api bisa membakar kayu?", sid)
    snapshot = manager.get_context_snapshot(sid)
    result = core.analyze_text("Apakah api bisa membakar kertas?", context_snapshot=snapshot)
    assert len(result["semantics"]) == 12
    assert "turns" not in result["semantics"]


def test_multi_turn_session_manager_adopts_external_session_id():
    manager = SessionManager()
    assert manager.ensure_session("host-session-1") == "host-session-1"
    assert manager.get_session("host-session-1").active


def test_multi_turn_session_metadata_can_supply_default_register():
    core = ILISCore()
    manager = SessionManager()
    sid = manager.create_session(metadata={"register": "informal"})
    adapter = ChatbotAdapter(core, session_manager=manager)
    result = adapter.respond("Apakah api bisa membakar kayu?", sid)
    assert result["metadata"]["register"] == "informal"


def test_multi_turn_identity_intent_is_saved_as_completed_turn(setup_chatbot):
    core, manager, adapter, sid = setup_chatbot
    result = adapter.respond("Lu siapa?", sid)
    assert result["metadata"]["response_type"] == "identity_intent"
    assert manager.get_recent_turns(sid)[0].assistant_response == result["answer"]


def test_multi_turn_game_adapter_stores_dialogue_separately_from_episode():
    core = ILISCore()
    core_sid = core.create_session()
    manager = SessionManager()
    game = GameEngineAdapter(core, session_manager=manager)
    result = game.handle_event("naga takut lonceng", core_sid, npc="Naga")
    turns = manager.get_recent_turns(core_sid)
    assert len(turns) == 1
    assert turns[0].user_message == "naga takut lonceng"
    assert result["episode"]["episode_id"] == result["metadata"]["episode_id"]
    assert result["metadata"]["context_turns_used"] == 0


def test_multi_turn_game_adapter_accepts_distinct_conversation_session_id():
    core = ILISCore()
    core_sid = core.create_session()
    manager = SessionManager()
    game = GameEngineAdapter(core, session_manager=manager)
    result = game.handle_event(
        "naga takut lonceng", core_sid, conversation_session_id="player-npc-1"
    )
    assert result["metadata"]["session_id"] == "player-npc-1"
    assert manager.get_session("player-npc-1") is not None


def test_multi_turn_game_adapter_can_create_session_without_supplied_id():
    core = ILISCore()
    manager = SessionManager()
    game = GameEngineAdapter(core, session_manager=manager)
    first = game.handle_event("naga takut lonceng")
    sid = first["metadata"]["session_id"]
    second = game.handle_event("api menyentuh rumah kayu", sid)
    assert second["metadata"]["session_id"] == sid
    assert second["metadata"]["context_turns_used"] == 1
    assert len(manager.get_recent_turns(sid)) == 2


def test_multi_turn_game_second_turn_receives_first_turn_snapshot():
    core = ILISCore()
    core_sid = core.create_session()
    manager = SessionManager()
    game = GameEngineAdapter(core, session_manager=manager)
    game.handle_event("naga takut lonceng", core_sid)
    second = game.handle_event("api menyentuh rumah kayu", core_sid)
    assert second["metadata"]["context_turns_used"] == 1
    assert second["conversation_context"]["turns"][0]["user_message"] == "naga takut lonceng"


def test_multi_turn_turn_sequence_remains_monotonic_after_history_trimming():
    manager = SessionManager(max_turns=2)
    sid = manager.create_session()
    for index in range(4):
        manager.add_turn(sid, f"q{index}", f"a{index}")
    turns = manager.get_recent_turns(sid)
    assert [turn.sequence for turn in turns] == [3, 4]


def test_multi_turn_snapshot_is_a_fresh_detached_structure():
    manager = SessionManager()
    sid = manager.create_session()
    manager.add_turn(sid, "q", "a")
    snapshot = manager.get_context_snapshot(sid)
    snapshot["turns"].clear()
    assert len(manager.get_context_snapshot(sid)["turns"]) == 1


def test_multi_turn_invalid_snapshot_type_is_rejected(setup_chatbot):
    _, _, adapter, sid = setup_chatbot
    with pytest.raises(TypeError):
        adapter.respond("Apakah api bisa membakar kayu?", sid, context_snapshot="bad")


# ---------------------------------------------------------------------------
# 8 reset/session lifecycle tests
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "command",
    [
        "reset percakapan", "Reset Percakapan!", "hapus riwayat",
        "hapus riwayat percakapan", "RESET PERCAKAPAN",
        "hapus riwayat.", "reset percakapan?", "Hapus Riwayat Percakapan",
    ],
)
def test_reset_commands_clear_only_active_session(command, setup_chatbot):
    _, manager, adapter, sid = setup_chatbot
    other = adapter.create_session()
    adapter.respond("Apakah api bisa membakar kayu?", sid)
    manager.add_turn(other, "q lain", "a lain")
    result = adapter.respond(command, sid)
    assert result["metadata"]["response_type"] == "session_reset"
    assert manager.get_context_snapshot(sid)["turns"] == []
    assert len(manager.get_recent_turns(other)) == 1


def test_reset_preserves_session_id_and_allows_new_turn(setup_chatbot):
    _, manager, adapter, sid = setup_chatbot
    adapter.respond("Apakah api bisa membakar kayu?", sid)
    adapter.respond("reset percakapan", sid)
    result = adapter.respond("Apakah api bisa membakar kertas?", sid)
    assert result["metadata"]["session_id"] == sid
    assert result["metadata"]["context_turns_used"] == 0
    assert len(manager.get_recent_turns(sid)) == 1
    assert result["reasoning_result"]["reasoning_type"] == "verified_inference"
    assert result["reasoning_result"]["evidence"]


def test_reset_does_not_delete_core_episodic_memory():
    core = ILISCore()
    core_sid = core.create_session()
    core.context_engine.record_event(core_sid, "naga takut lonceng")
    manager = SessionManager()
    adapter = ChatbotAdapter(core, session_manager=manager)
    adapter.respond("Apakah api bisa membakar kayu?", core_sid)
    adapter.respond("hapus riwayat", core_sid)
    assert len(core.context_engine.get_context(core_sid)["episodic_memory"]) == 1


def test_reset_does_not_delete_knowledge_facts(setup_chatbot):
    core, _, adapter, sid = setup_chatbot
    before = core.knowledge_engine.fact_store.all()
    adapter.respond("Apakah api bisa membakar kayu?", sid)
    adapter.respond("reset percakapan", sid)
    assert core.knowledge_engine.fact_store.all() == before


def test_reset_does_not_treat_ordinary_question_as_command(setup_chatbot):
    _, manager, adapter, sid = setup_chatbot
    result = adapter.respond("Bagaimana cara melakukan reset percakapan?", sid)
    assert result["metadata"].get("response_type") != "session_reset"
    assert len(manager.get_recent_turns(sid)) == 1


def test_reset_unknown_session_is_not_silently_created():
    manager = SessionManager()
    with pytest.raises(KeyError):
        manager.reset_session("missing")


def test_delete_session_removes_only_requested_session():
    manager = SessionManager()
    first = manager.create_session()
    second = manager.create_session()
    assert manager.delete_session(first) is True
    assert manager.get_session(first) is None
    assert manager.get_session(second) is not None


# ---------------------------------------------------------------------------
# 15 V2.1 regression tests: persona, identity, register, contracts, storage
# ---------------------------------------------------------------------------

def test_regression_semantic_contract_has_exactly_twelve_fields(setup_chatbot):
    _, _, adapter, sid = setup_chatbot
    result = adapter.respond("Apakah api bisa membakar kayu?", sid)
    assert len(result["semantic_result"]["semantics"]) == 12


def test_regression_reasoning_contract_has_exactly_six_keys(setup_chatbot):
    _, _, adapter, sid = setup_chatbot
    result = adapter.respond("Apakah api bisa membakar kayu?", sid)
    assert set(result["reasoning_result"]) == {
        "conclusion", "confidence_score", "evidence",
        "reasoning_type", "reasons", "uncertainty",
    }


def test_regression_mode_a_identity_intent_remains_static(setup_chatbot):
    _, _, adapter, sid = setup_chatbot
    result = adapter.respond("Lu siapa?", sid)
    assert result["metadata"]["response_type"] == "identity_intent"
    assert result["answer"].startswith("Saya ILIS, sistem kecerdasan bahasa.")


def test_regression_mode_a_identity_variation_lo_still_routes(setup_chatbot):
    _, _, adapter, sid = setup_chatbot
    result = adapter.respond("Kemampuan lo apa aja?", sid)
    assert result["metadata"]["response_type"] == "identity_intent"


def test_regression_mode_a_identity_variation_km_still_routes(setup_chatbot):
    _, _, adapter, sid = setup_chatbot
    result = adapter.respond("Eh km bisa ngapain?", sid)
    assert result["metadata"]["response_type"] == "identity_intent"


def test_regression_mode_b_keeps_application_identity():
    core = ILISCore()
    config = PersonaConfig(
        mode=MODE_B,
        application=ApplicationProfile(
            application_id="host", display_name="Arunika", role="asisten aplikasi",
            identity_reply="Saya Arunika, asisten aplikasi ini.",
        ),
    )
    manager = SessionManager()
    sid = manager.create_session()
    result = ChatbotAdapter(core, persona_config=config, session_manager=manager).respond(
        "Halo siapa kamu?", sid
    )
    assert result["answer"].startswith("Saya Arunika, asisten aplikasi ini.")


def test_regression_mode_c_keeps_character_identity():
    core = ILISCore()
    config = PersonaConfig(
        mode=MODE_C,
        character=CharacterProfile(
            character_id="raka", display_name="Raka", role="penjaga gerbang",
            identity_reply="Aku Raka, penjaga gerbang kerajaan.",
        ),
    )
    manager = SessionManager()
    sid = manager.create_session()
    result = ChatbotAdapter(core, persona_config=config, session_manager=manager).respond(
        "Halo siapa kamu?", sid
    )
    assert result["answer"].startswith("Aku Raka, penjaga gerbang kerajaan.")


def test_regression_explicit_polite_instruction_remains_formal(setup_chatbot):
    _, _, adapter, sid = setup_chatbot
    result = adapter.respond("Tolong jawab dengan sopan, apakah api bisa membakar kayu?", sid)
    assert result["metadata"]["register"] == "formal"
    assert "Dengan senang hati," in result["answer"]


def test_regression_explicit_casual_instruction_remains_informal(setup_chatbot):
    _, _, adapter, sid = setup_chatbot
    result = adapter.respond("Jawab dengan santai, apakah api bisa membakar kayu?", sid)
    assert result["metadata"]["register"] == "informal"


def test_regression_latest_style_instruction_overrides_session_default(setup_chatbot):
    _, manager, adapter, sid = setup_chatbot
    manager.require_session(sid).metadata["register"] = "formal"
    result = adapter.respond("Jawab dengan santai, apakah api bisa membakar kayu?", sid)
    assert result["metadata"]["register"] == "informal"


def test_regression_identity_intent_does_not_run_semantic_or_reasoning(setup_chatbot):
    _, _, adapter, sid = setup_chatbot
    result = adapter.respond("Siapa kamu?", sid)
    assert result["semantic_result"] is None
    assert result["reasoning_result"] is None
    assert result["generation"] is None


def test_regression_core_analyze_text_does_not_retain_context_state():
    core = ILISCore()
    snapshot = {"session_id": "s1", "turns": [{"user_message": "lama"}]}
    core.analyze_text("Apakah api bisa membakar kayu?", context_snapshot=snapshot)
    assert not hasattr(core, "conversation_history")
    assert not hasattr(core, "session_manager")


def test_regression_sqlite_schema_has_no_conversation_tables(tmp_path):
    core = ILISCore(storage="sqlite", db_path=str(tmp_path / "ilis.sqlite"))
    try:
        rows = core.storage_provider._connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
        names = {row[0] for row in rows}
        assert "conversation_turns" not in names
        assert "conversation_sessions" not in names
    finally:
        core.close()


def test_regression_sqlite_knowledge_and_episodic_storage_still_works(tmp_path):
    path = str(tmp_path / "ilis.sqlite")
    core = ILISCore(storage="sqlite", db_path=path)
    sid = core.create_session()
    core.context_engine.record_event(sid, "naga takut lonceng")
    core.close()
    restored = ILISCore(storage="sqlite", db_path=path)
    try:
        assert restored.context_engine.get_context(sid)["episodic_memory"]
        assert restored.knowledge_engine.fact_store.all()
    finally:
        restored.close()


def test_regression_no_llm_dependency_is_introduced():
    from pathlib import Path
    project = Path(__file__).resolve().parents[1]
    config = (project / "pyproject.toml").read_text(encoding="utf-8").casefold()
    assert "openai" not in config
    assert "transformers" not in config
    assert "langchain" not in config
