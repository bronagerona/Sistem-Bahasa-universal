import pytest

from ilis.cognition import KnowledgeEngine
from ilis.cognition.context_engine import ContextEngine
from ilis.cognition.reasoning_engine import ReasoningEngine
from ilis.generation import LanguageGenerator


def _reasoning_result():
    return ReasoningEngine(KnowledgeEngine()).infer_burn_risk("api", "rumah")


def test_burn_risk_generates_distinct_formal_and_informal_indonesian():
    generator = LanguageGenerator()
    result = _reasoning_result()

    formal = generator.generate(result, register="formal")
    informal = generator.generate(result, register="informal")

    assert formal["text"] == "Ada kemungkinan rumah akan terbakar karena terbuat dari kayu dan terpapar api."
    assert informal["text"] == "Kayaknya rumah bisa kebakaran karena berbahan kayu dan terkena api lho."
    assert formal["text"] != informal["text"]
    assert formal["uncertainty_preserved"] is True
    assert "berpotensi" in result["conclusion"]


def test_semantic_register_metadata_is_used_when_register_not_explicit():
    generator = LanguageGenerator()
    semantic_result = {"status": "supported", "semantics": {"Register": "slang"}}

    result = generator.generate(_reasoning_result(), semantic_result=semantic_result)

    assert result["register"] == "slang"
    assert "deh" in result["text"]


def test_explicit_register_overrides_semantic_metadata():
    generator = LanguageGenerator()
    semantic_result = {"status": "supported", "semantics": {"Register": "slang"}}

    result = generator.generate(
        _reasoning_result(), register="formal", semantic_result=semantic_result
    )

    assert result["register"] == "formal"


def test_context_session_register_and_context_snapshot_are_used():
    knowledge = KnowledgeEngine()
    context = ContextEngine(knowledge)
    session = context.create_session(metadata={"register": "informal"})
    context.add_message(session, "player", "Kita perlu cek rumah itu.")
    result = LanguageGenerator(context).generate(
        _reasoning_result(), session_id=session
    )

    assert result["register"] == "informal"
    assert result["session_id"] == session


def test_unknown_and_conflicting_results_are_not_rendered_as_facts():
    generator = LanguageGenerator()
    unknown = generator.generate({
        "conclusion": "Belum cukup data untuk menentukan apakah rumah dapat terbakar.",
        "reasoning_type": "unknown",
        "confidence_score": 0.0,
        "uncertainty": "Data tidak tersedia bukan berarti mustahil.",
        "evidence": [],
    })
    conflict = generator.generate({
        "conclusion": "Data tentang kemungkinan rumah terbakar memiliki fakta yang saling bertentangan.",
        "reasoning_type": "conflicting",
        "confidence_score": 0.0,
        "uncertainty": "Tinjau konflik dahulu.",
        "evidence": ["fact_1"],
    })

    assert "Belum cukup informasi" in unknown["text"]
    assert "bertentangan" in conflict["text"]


def test_structured_meaning_can_be_generated_without_reasoning_conclusion_parser():
    result = LanguageGenerator().generate({
        "meaning": {"kind": "burn_risk", "source": "api", "target": "gedung", "material": "bambu"},
        "reasoning_type": "hypothetical_inference",
        "confidence_score": 0.48,
        "uncertainty": "Masih hipotesis.",
        "evidence": ["f1", "f2"],
    }, register="formal")

    assert "gedung" in result["text"]
    assert "bambu" in result["text"]
    assert "kemungkinan" in result["text"]


def test_invalid_inputs_and_register_are_rejected():
    generator = LanguageGenerator()
    with pytest.raises(TypeError):
        generator.generate("not a reasoning object")
    with pytest.raises(ValueError):
        generator.generate(_reasoning_result(), register="regional")
    with pytest.raises(ValueError):
        LanguageGenerator().generate(_reasoning_result(), session_id="missing")


def _semantic_payload(text, tokens):
    return {"contract_version": "1.0", "original_text": text,
            "ilve": {"normalized_text": text.casefold(), "tokens": tokens, "variation_hints": []}}


def test_question_answer_generation_uses_reasoning_confidence():
    from ilis.semantics.semantic_engine import SemanticEngine
    semantic = SemanticEngine().analyze(_semantic_payload("Apakah api bisa membakar kayu?",
        ["apakah", "api", "bisa", "membakar", "kayu", "?"]))
    reasoning = {"conclusion": "Ya, berdasarkan fakta yang tersimpan, api dapat membakar kayu.",
        "confidence_score": 0.72, "reasoning_type": "verified_inference",
        "evidence": ["fact_1"], "uncertainty": "Kesimpulan berbasis aturan."}
    result = LanguageGenerator().generate(reasoning, semantic_result=semantic, register="formal")
    assert result["text"] == "Ya, kemungkinan api bisa membakar kayu."
    assert result["uncertainty_preserved"] is True
    assert result["confidence_score"] == 0.72


def test_command_intent_generates_acknowledgement_not_an_answer():
    from ilis.semantics.semantic_engine import SemanticEngine
    semantic = SemanticEngine().analyze(_semantic_payload("Bunyikan lonceng", ["bunyikan", "lonceng"]))
    reasoning = {"conclusion": "Input dikenali sebagai perintah, bukan pertanyaan yang perlu dijawab.",
        "confidence_score": 0.0, "reasoning_type": "command", "evidence": [], "uncertainty": "Gunakan pertanyaan eksplisit."}
    result = LanguageGenerator().generate(reasoning, semantic_result=semantic)
    assert result["text"] == "Baik, lonceng akan dibunyikan."


def test_dragon_bell_has_formal_informal_and_slang_variants():
    reasoning = {"conclusion": "Lonceng dapat menakuti naga karena menghasilkan suara keras yang ditakuti naga.",
        "confidence_score": 0.72, "reasoning_type": "verified_inference",
        "evidence": ["fact_1", "fact_2"], "uncertainty": "Kesimpulan bergantung pada fakta."}
    generator = LanguageGenerator()
    outputs = [generator.generate(reasoning, register=register) for register in ("formal", "informal", "slang")]
    assert all("naga" in item["text"].casefold() for item in outputs)
    assert len({item["text"] for item in outputs}) == 3
    assert all(item["uncertainty_preserved"] for item in outputs)

def test_explicit_polite_generation_adds_polite_formal_opening():
    from ilis.semantics.semantic_engine import SemanticEngine
    semantic = SemanticEngine().analyze(_semantic_payload(
        "Apakah api bisa membakar kayu?", ["apakah", "api", "bisa", "membakar", "kayu", "?"]
    ))
    reasoning = {
        "conclusion": "Ya, berdasarkan fakta yang tersimpan, api dapat membakar kayu.",
        "confidence_score": 0.72,
        "reasoning_type": "verified_inference",
        "evidence": ["fact_1"],
        "uncertainty": "Kesimpulan berbasis aturan.",
    }

    result = LanguageGenerator().generate(
        reasoning, semantic_result=semantic, register="formal", polite=True
    )

    assert result["register"] == "formal"
    assert result["text"].startswith("Dengan senang hati,")
