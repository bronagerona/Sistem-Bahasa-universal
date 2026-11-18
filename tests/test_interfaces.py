import pytest

from ilis.interfaces import ILISCore


def test_core_initializes_all_engines_and_adapters():
    core = ILISCore()
    assert core.semantic_engine is not None
    assert core.knowledge_engine is not None
    assert core.reasoning_engine is not None
    assert core.context_engine is not None
    assert core.learning_engine is not None
    assert core.language_generator is not None
    assert core.chatbot() is not None
    assert core.game() is not None


@pytest.mark.parametrize(
    ("register", "expected"),
    [("formal", "Ada kemungkinan"), ("informal", "Kayaknya"), ("slang", "Kayaknya")],
)
def test_chatbot_api_touching_wooden_house_uses_register(register, expected):
    core = ILISCore()
    session_id = core.create_session(metadata={"register": register})
    result = core.chatbot().respond("Api menyentuh rumah kayu", session_id)

    assert expected in result["answer"]
    assert result["metadata"]["register"] == register
    assert result["metadata"]["confidence_score"] == 0.72
    assert result["metadata"]["conflict_status"] == "clear"
    assert result["metadata"]["semantic_status"] in {"unsupported", "low_confidence"}


def test_chatbot_explicit_register_overrides_session_register():
    core = ILISCore()
    session_id = core.create_session(metadata={"register": "formal"})
    result = core.chatbot().respond(
        "Api menyentuh rumah kayu", session_id, register="slang"
    )
    assert result["metadata"]["register"] == "slang"


def test_game_adapter_records_dragon_fears_bell_and_generates_npc_conclusion():
    core = ILISCore()
    session_id = core.create_session(metadata={"register": "informal"})
    result = core.game().handle_event(
        "Naga takut lonceng", session_id, entities=["naga", "lonceng"]
    )

    assert result["episode"]["description"] == "Naga takut lonceng"
    assert result["metadata"]["episode_id"] == result["episode"]["episode_id"]
    assert "naga takut pada lonceng" in result["dialogue"].casefold()
    assert result["metadata"]["reasoning_type"] == "hypothetical_inference"
    assert result["metadata"]["confidence_score"] == 0.48
    assert len(core.context_engine.get_context(session_id)["episodic_memory"]) == 1
    assert core.knowledge_engine.fact_store.all() == [
        core.knowledge_engine.fact_store.all()[0],
        core.knowledge_engine.fact_store.all()[1],
    ]


def test_game_adapter_uses_reasoning_engine_for_supported_burn_event():
    core = ILISCore()
    session_id = core.create_session()
    result = core.game().handle_event("Api menyentuh rumah kayu", session_id)
    assert result["metadata"]["reasoning_type"] == "verified_inference"
    assert "kemungkinan" in result["dialogue"].casefold()


def test_unknown_game_event_is_stored_but_not_overinterpreted():
    core = ILISCore()
    session_id = core.create_session()
    result = core.game().handle_event("Pemain membuka gerbang kuno", session_id)
    assert result["episode"]["description"] == "Pemain membuka gerbang kuno"
    assert result["metadata"]["reasoning_type"] == "unknown"
    assert "Belum cukup informasi" in result["dialogue"]


def test_invalid_session_and_empty_inputs_are_rejected():
    core = ILISCore()
    session_id = core.create_session()
    with pytest.raises(ValueError):
        core.chatbot().respond("", session_id)
    with pytest.raises(ValueError):
        core.game().handle_event("   ", session_id)
    with pytest.raises(KeyError):
        core.chatbot().respond("Api menyentuh rumah kayu", "missing")
