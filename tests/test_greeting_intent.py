from ilis.interfaces import ILISCore
from ilis.semantics.constants import SEMANTIC_FIELDS


def test_halo_apa_kabar_is_recognized_as_supported_greeting():
    core = ILISCore()
    session_id = core.create_session()

    result = core.chatbot().respond("Halo, apa kabar?", session_id)

    assert result["semantic_result"]["status"] == "supported"
    assert set(result["semantic_result"]["semantics"]) == set(SEMANTIC_FIELDS)
    assert result["semantic_result"]["semantics"]["Predicate"] == "menyapa"
    assert result["semantic_result"]["semantics"]["Intent"] == "greeting"
    assert result["reasoning_result"]["reasoning_type"] == "greeting"
    assert result["generation"]["reasoning_type"] == "greeting"
    assert result["metadata"]["reasoning_type"] == "greeting"
    assert result["generation"]["meaning"] == {"kind": "greeting"}
    assert result["answer"] == (
        "Halo! Saya siap membantu. Bagaimana kabar Anda?"
    )
    assert "Saya ILIS, sistem kecerdasan bahasa." not in result["answer"]


def test_greeting_does_not_add_identity_prefix_and_keeps_six_reasoning_keys():
    core = ILISCore()
    session_id = core.create_session()

    result = core.chatbot().respond("Halo, apa kabar?", session_id)

    assert set(result["reasoning_result"]) == {
        "conclusion", "confidence_score", "evidence",
        "reasoning_type", "reasons", "uncertainty",
    }
    assert not result["answer"].startswith("Saya ILIS")
