from ilis.generation import LanguageGenerator


def _semantic_question():
    from ilis.semantics.semantic_engine import SemanticEngine

    payload = {
        "contract_version": "1.0",
        "original_text": "Apakah api bisa membakar besi?",
        "ilve": {
            "normalized_text": "apakah api bisa membakar besi?",
            "tokens": ["apakah", "api", "bisa", "membakar", "besi", "?"],
            "variation_hints": [],
        },
    }
    return SemanticEngine().analyze(payload)


def _concept_result(reasoning_type, confidence, conclusion):
    return {
        "conclusion": conclusion,
        "confidence_score": confidence,
        "reasoning_type": reasoning_type,
        "evidence": [],
        "uncertainty": "Status Concept Engine.",
    }


def test_concept_inference_unknown_returns_standard_unknown_answer():
    result = LanguageGenerator().generate(
        _concept_result(
            "concept_inference_unknown",
            0.0,
            "Tidak Tahu: belum ada informasi memadai tentang api dan besi.",
        ),
        semantic_result=_semantic_question(),
    )

    assert result["text"] == (
        "Belum cukup informasi untuk memastikan jawaban atas pertanyaanmu."
    )
    assert result["reasoning_type"] == "concept_inference_unknown"
    assert result["confidence_score"] == 0.0
    assert result["uncertainty_preserved"] is True


def test_concept_inference_partial_includes_explicit_warning():
    result = LanguageGenerator().generate(
        _concept_result(
            "concept_inference_partial",
            0.48,
            "Tahu Sebagian: informasi tentang api dan besi belum lengkap.",
        ),
        semantic_result=_semantic_question(),
    )

    assert result["text"].startswith("Ya, kemungkinan api bisa membakar besi.")
    assert result["text"].endswith(
        "Informasi belum lengkap, ini hanya dugaan."
    )
    assert result["reasoning_type"] == "concept_inference_partial"
    assert result["confidence_score"] == 0.48
    assert result["uncertainty_preserved"] is True


def test_concept_inference_known_generates_normal_verified_answer():
    result = LanguageGenerator().generate(
        _concept_result(
            "concept_inference_known",
            0.72,
            "Tahu Pasti: hubungan dan properti didukung data terverifikasi.",
        ),
        semantic_result=_semantic_question(),
    )

    assert result["text"] == "Ya, berdasarkan fakta yang tersedia, api bisa membakar besi."
    assert "dugaan" not in result["text"].casefold()
    assert result["reasoning_type"] == "concept_inference_known"
    assert result["confidence_score"] == 0.72
    assert result["uncertainty_preserved"] is False


def test_concept_reasoning_metadata_stays_synchronized_with_answer():
    generator = LanguageGenerator()
    semantic = _semantic_question()
    cases = [
        ("concept_inference_known", 0.72, "Ya, berdasarkan fakta yang tersedia, api bisa membakar besi."),
        ("concept_inference_partial", 0.48, "Informasi belum lengkap, ini hanya dugaan."),
        ("concept_inference_unknown", 0.0, "Belum cukup informasi untuk memastikan jawaban atas pertanyaanmu."),
    ]

    for reasoning_type, confidence, expected_text in cases:
        result = generator.generate(
            _concept_result(reasoning_type, confidence, "Status Concept Engine."),
            semantic_result=semantic,
        )
        assert result["reasoning_type"] == reasoning_type
        assert result["confidence_score"] == confidence
        assert expected_text.casefold() in result["text"].casefold()


def test_legacy_verified_inference_rendering_remains_unchanged():
    reasoning = {
        "conclusion": "Ya, berdasarkan fakta yang tersimpan, api dapat membakar kayu.",
        "confidence_score": 0.72,
        "reasoning_type": "verified_inference",
        "evidence": ["fact_1"],
        "uncertainty": "Kesimpulan berbasis aturan.",
    }
    result = LanguageGenerator().generate(
        reasoning,
        semantic_result=_semantic_question(),
    )

    assert result["text"] == "Ya, kemungkinan api bisa membakar besi."
    assert result["reasoning_type"] == "verified_inference"


def test_legacy_unknown_rendering_remains_unchanged():
    reasoning = {
        "conclusion": "Belum cukup data untuk menentukan apakah rumah dapat terbakar.",
        "confidence_score": 0.0,
        "reasoning_type": "unknown",
        "evidence": [],
        "uncertainty": "Data tidak tersedia bukan berarti mustahil.",
    }
    result = LanguageGenerator().generate(reasoning)

    assert result["text"] == "Belum cukup informasi untuk memastikan apakah rumah dapat terjadi."
    assert result["reasoning_type"] == "unknown"
