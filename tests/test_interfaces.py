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


@pytest.mark.parametrize(
    "message",
    ["Halo", "Hai", "Hi", "Hello", "Apa kabar", "Halo apa kabar"],
)
def test_chatbot_synchronizes_greeting_intent_across_runtime_layers(message):
    core = ILISCore()
    result = core.chatbot().respond(message)

    assert result["semantic_result"]["status"] == "supported"
    assert result["semantic_result"]["semantics"]["Intent"] == "greeting"
    assert result["reasoning_result"]["reasoning_type"] == "greeting"
    assert result["generation"]["reasoning_type"] == "greeting"
    assert result["metadata"]["reasoning_type"] == "greeting"
    assert result["generation"]["meaning"]["kind"] == "greeting"
    assert len(result["semantic_result"]["semantics"]) == 12
    assert len(result["reasoning_result"]) == 6


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
    assert "58,65 hari bumi" in solar_day["answer"].casefold()
    assert "176 hari bumi" in solar_day["answer"].casefold()
    assert "bukan bukti faktual" in " ".join(solar_day["reasoning_result"]["reasons"])
    assert len(solar_day["semantic_result"]["semantics"]) == 12
    assert len(solar_day["reasoning_result"]) == 6

    orbit = chatbot.respond("Bukankah orbitnya sekitar 88 hari?", session_id)
    assert orbit["reasoning_result"]["reasoning_type"] == "hypothetical_inference"
    assert orbit["reasoning_result"]["evidence"] == ["fact-0034"]
    assert "88 hari bumi" in orbit["answer"].casefold()
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


def test_chatbot_confidence_propagates_through_reasoning_generation_and_metadata():
    core = ILISCore()
    result = core.chatbot().respond(
        "Apakah Merkurius memiliki periode rotasi sideris?"
    )

    semantic_confidence = result["semantic_result"]["semantics"]["Confidence"]
    assert semantic_confidence == 0.9

    # The reasoning source remains 0.48 for a draft/hypothesis fact.
    # The adapter applies the existing semantic-confidence multiplier once.
    expected_final = round(0.48 * semantic_confidence, 6)
    assert expected_final == 0.432
    assert result["reasoning_result"]["confidence_score"] == expected_final
    assert result["generation"]["confidence_score"] == expected_final
    assert result["metadata"]["confidence_score"] == expected_final


def test_chatbot_does_not_invent_confidence_when_reasoning_has_no_assessment():
    core = ILISCore()
    result = core.chatbot().respond(
        "Apakah Merkurius memiliki warna ungu?"
    )

    assert result["semantic_result"]["status"] == "supported"
    assert result["semantic_result"]["semantics"]["Confidence"] == 0.9
    assert result["reasoning_result"]["reasoning_type"] == "unknown"
    assert result["reasoning_result"]["confidence_score"] == 0.0
    assert result["generation"]["confidence_score"] == 0.0
    assert result["metadata"]["confidence_score"] == 0.0


def test_chatbot_recovers_previous_topic_after_explicit_topic_switch():
    core = ILISCore()
    chatbot = core.chatbot()
    session_id = chatbot.create_session()

    first = chatbot.respond("Aku sedang mencari buku sejarah.", session_id)
    first_topic = first["context_snapshot"]["topic_context"]["active_topic"]
    assert first_topic["label"] == "buku sejarah"
    assert first["context_snapshot"]["topic_context"]["resolution"]["status"] == "initial_topic"

    second = chatbot.respond(
        "Ngomong-ngomong, apa fungsi akar tumbuhan?", session_id
    )
    second_context = second["context_snapshot"]["topic_context"]
    assert second_context["resolution"]["status"] == "new_topic"
    assert second_context["active_topic"]["label"] == "akar tumbuhan"
    assert len(second_context["topic_history"]) == 2

    third = chatbot.respond(
        "Kembali ke buku tadi, aku butuh untuk tugas sekolah.", session_id
    )
    topic_context = third["context_snapshot"]["topic_context"]
    assert topic_context["resolution"]["status"] == "returned_to_previous"
    assert topic_context["active_topic"]["topic_id"] == first_topic["topic_id"]
    assert len(topic_context["topic_history"]) == 2
    assert third["metadata"]["reasoning_type"] == "topic_recovery"
    assert third["metadata"]["confidence_score"] == 0.0
    assert third["semantic_result"]["status"] == "low_confidence"
    assert "buku sejarah" in third["answer"].casefold()
    assert "tugas sekolah" in third["answer"].casefold()
    assert len(third["semantic_result"]["semantics"]) == 12
    assert len(third["reasoning_result"]) == 6
    assert third["reasoning_result"]["evidence"] == []


def test_chatbot_does_not_switch_topic_on_ambiguous_return_reference():
    from ilis.interfaces.session_manager import SessionManager

    manager = SessionManager()
    session_id = manager.create_session()
    manager.update_topic_context(session_id, "Aku sedang mencari buku sejarah.")
    manager.add_turn(session_id, "Aku sedang mencari buku sejarah.", "Baik.")
    manager.update_topic_context(session_id, "Ngomong-ngomong, apa fungsi akar tumbuhan?")
    manager.add_turn(session_id, "Ngomong-ngomong, apa fungsi akar tumbuhan?", "Baik.")

    before = manager.get_topic_context(session_id)["active_topic"]["topic_id"]
    result = manager.update_topic_context(session_id, "Kembali ke hal tadi, ya.")
    after = manager.get_topic_context(session_id)["active_topic"]["topic_id"]

    assert result["resolution"]["status"] == "ambiguous_reference"
    assert after == before
    assert len(result["topic_history"]) == 2


def test_topic_history_keeps_prior_topics_beyond_bounded_transcript():
    from ilis.interfaces.session_manager import SessionManager

    manager = SessionManager(max_turns=1)
    session_id = manager.create_session()

    first_message = "Aku sedang mencari buku sejarah."
    first = manager.update_topic_context(session_id, first_message)
    first_topic_id = first["active_topic"]["topic_id"]
    manager.add_turn(session_id, first_message, "Baik.")

    deeper_message = "Siapa penulis buku sejarah itu?"
    deeper = manager.update_topic_context(session_id, deeper_message)
    assert deeper["resolution"]["status"] == "same_topic_deepened"
    assert deeper["active_topic"]["topic_id"] == first_topic_id
    manager.add_turn(session_id, deeper_message, "Saya belum tahu.")

    switch_message = "Ngomong-ngomong, apa fungsi akar tumbuhan?"
    switched = manager.update_topic_context(session_id, switch_message)
    assert switched["resolution"]["status"] == "new_topic"
    second_topic_id = switched["active_topic"]["topic_id"]
    manager.add_turn(session_id, switch_message, "Baik.")

    assert len(manager.get_recent_turns(session_id)) == 1
    assert len(manager.get_topic_context(session_id)["topic_history"]) == 2

    returned = manager.update_topic_context(
        session_id, "Kembali ke buku sejarah tadi, ya."
    )
    assert returned["resolution"]["status"] == "returned_to_previous"
    assert returned["active_topic"]["topic_id"] == first_topic_id
    assert returned["active_topic"]["topic_id"] != second_topic_id


@pytest.mark.parametrize(
    ("message", "fact_id", "expected_value", "expected_phrase"),
    [
        (
            "Apa rotasi sideris Merkurius?",
            "fact-0033",
            "1.407,6 jam (≈ 58,65 hari Bumi)",
            "bukan lama hari Matahari",
        ),
        (
            "Berapa hari Merkurius mengelilingi Matahari?",
            "fact-0034",
            "88 hari Bumi",
            "berbeda dari periode rotasi",
        ),
    ],
)
def test_chatbot_answers_direct_mercury_dataset_questions_without_changing_contracts(
    message, fact_id, expected_value, expected_phrase,
):
    core = ILISCore()
    result = core.chatbot().respond(message)

    assert result["reasoning_result"]["reasoning_type"] == "hypothetical_inference"
    assert result["reasoning_result"]["evidence"] == [fact_id]
    assert expected_value in result["reasoning_result"]["conclusion"]
    assert expected_value in result["answer"]
    assert expected_phrase.casefold() in result["answer"].casefold()
    assert result["semantic_result"]["status"] == "low_confidence"
    assert len(result["semantic_result"]["semantics"]) == 12
    assert set(result["reasoning_result"]) == {
        "conclusion", "confidence_score", "evidence",
        "reasoning_type", "reasons", "uncertainty",
    }
    assert result["reasoning_result"]["confidence_score"] == 0.12
    assert result["generation"]["confidence_score"] == 0.12
    assert result["metadata"]["confidence_score"] == 0.12
    assert result["metadata"]["reasoning_type"] == "hypothetical_inference"


def test_chatbot_does_not_answer_direct_dataset_question_without_matching_fact():
    core = ILISCore()
    result = core.chatbot().respond("Apa rotasi sideris Venus?")

    assert result["reasoning_result"]["reasoning_type"] == "unknown"
    assert result["reasoning_result"]["evidence"] == []
    assert result["reasoning_result"]["confidence_score"] == 0.0
    assert "belum cukup informasi" in result["answer"].casefold()


def test_chatbot_keeps_hypothesis_opening_for_existing_supported_dataset_question():
    core = ILISCore()
    result = core.chatbot().respond(
        "Apakah Merkurius memiliki periode rotasi sideris?"
    )

    assert result["reasoning_result"]["evidence"] == ["fact-0033"]
    assert result["reasoning_result"]["reasoning_type"] == "hypothetical_inference"
    assert result["answer"].startswith("Ada kemungkinan bahwa ")
    assert "1.407,6 jam (≈ 58,65 hari Bumi)" in result["answer"]
    assert result["metadata"]["confidence_score"] == 0.432
