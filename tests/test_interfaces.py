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
    [
        ("formal", "Baik, saya sudah memahami pernyataanmu"),
        ("informal", "Oke, aku paham pernyataanmu"),
        ("slang", "Oke, nangkep pernyataanmu"),
    ],
)
def test_chatbot_api_touching_wooden_house_acknowledges_assertion(register, expected):
    core = ILISCore()
    session_id = core.create_session(metadata={"register": register})
    result = core.chatbot().respond("Api menyentuh rumah kayu", session_id)

    assert result["metadata"]["register"] == register
    assert result["generation"]["text"] == expected
    assert expected in result["answer"]
    assert result["semantic_result"]["status"] == "supported"
    assert result["semantic_result"]["semantics"]["Intent"] == "assertion"
    assert result["reasoning_result"]["reasoning_type"] == "assertion"
    assert "terbakar" not in result["answer"].casefold()
    assert "kebakaran" not in result["answer"].casefold()
    assert "kemungkinan" not in result["answer"].casefold()
    semantic_confidence = result["semantic_result"]["semantics"]["Confidence"]
    reasoning_base = core.reasoning_engine.infer_semantic(
        result["semantic_result"]
    )["confidence_score"]
    assert result["metadata"]["confidence_score"] == round(
        reasoning_base * semantic_confidence, 6
    )
    assert result["metadata"]["conflict_status"] == "clear"
    assert result["metadata"]["semantic_status"] == "supported"


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
    assert len(core.knowledge_engine.fact_store.all()) == core.knowledge_dataset_loaded + 3


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


def test_chatbot_runtime_exposes_bl_ilis_002_not_yet_mapping():
    core = ILISCore()
    result = core.chatbot().respond("Saya belum selesai")

    negation = result["metadata"]["negation"]
    assert negation["negation_type"] == "not_yet"
    assert negation["confidence"] == 0.86
    assert negation["evidence"]["detected_cues"] == ["belum"]
    assert "belum" in negation["evidence"]["reason"].casefold()


@pytest.mark.parametrize(
    ("message", "expected_label", "expected_semantic"),
    [
        ("Saya belum selesai", "not_yet", "not_yet"),
        ("Dia bukan dokter", "identity_negative", "identity_negative"),
        ("Jangan masuk", "prohibitive", "negative"),
        ("Kami datang tanpa mobil", "negative", "negative"),
    ],
)
def test_chatbot_runtime_maps_bl_ilis_002_into_semantic_negation(
    message, expected_label, expected_semantic
):
    core = ILISCore()
    result = core.chatbot().respond(message)

    assert result["metadata"]["negation"]["negation_type"] == expected_label
    assert result["metadata"]["negation"]["semantic_value"] == expected_semantic
    assert result["metadata"]["negation"]["applied_to_semantic"] is True
    assert result["semantic_result"]["semantics"]["Negation"] == expected_semantic
    assert len(result["semantic_result"]["semantics"]) == 12



def test_chatbot_uses_session_knowledge_for_mercury_multiturn_followups():
    core = ILISCore()
    chatbot = core.chatbot()
    session_id = chatbot.create_session()

    initial = chatbot.respond("Merkurius berotasi sekitar 58,6 hari.", session_id)
    assert initial["semantic_result"]["status"] == "supported"
    assert initial["semantic_result"]["semantics"]["Actor"] == "merkurius"
    assert initial["reasoning_result"]["reasoning_type"] == "assertion"

    solar_day = chatbot.respond(
        "Jadi satu hari Matahari di Merkurius juga 58,6 hari?", session_id
    )
    assert solar_day["reasoning_result"]["reasoning_type"] == "hypothetical_inference"
    assert solar_day["reasoning_result"]["evidence"] == ["fact-0033", "fact-0018"]
    assert "58,65 hari Bumi" in solar_day["answer"]
    assert "176 hari Bumi" in solar_day["answer"]
    assert "bukan bukti faktual" in " ".join(solar_day["reasoning_result"]["reasons"])
    assert len(solar_day["semantic_result"]["semantics"]) == 12
    assert len(solar_day["reasoning_result"]) == 6

    orbit = chatbot.respond("Bukankah orbitnya sekitar 88 hari?", session_id)
    assert orbit["reasoning_result"]["reasoning_type"] == "hypothetical_inference"
    assert orbit["reasoning_result"]["evidence"] == ["fact-0034"]
    assert "88 hari Bumi" in orbit["answer"]
    assert len(orbit["semantic_result"]["semantics"]) == 12
    assert len(orbit["reasoning_result"]) == 6

    assert core.knowledge_dataset_loaded == 90
    assert len(core.knowledge_engine.fact_store.all()) == 93


def test_chatbot_answers_supported_question_from_loaded_knowledge_dataset():
    core = ILISCore()
    result = core.chatbot().respond(
        "Apakah Merkurius memiliki periode rotasi sideris?"
    )

    assert result["metadata"]["semantic_status"] == "supported"
    assert result["reasoning_result"]["reasoning_type"] == "hypothetical_inference"
    assert result["reasoning_result"]["evidence"] == ["fact-0033"]
    assert "1.407,6 jam" in result["answer"]
    assert "bukan lama hari matahari" in result["answer"].casefold()
    assert result["metadata"]["confidence_score"] < 0.48
    assert len(result["semantic_result"]["semantics"]) == 12
    assert len(result["reasoning_result"]) == 6
