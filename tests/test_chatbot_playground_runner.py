from __future__ import annotations

import importlib.util
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "run_chatbot_playground.py"
SPEC = importlib.util.spec_from_file_location("ilis_chatbot_playground_runner", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)


def test_parse_turns_preserves_multi_turn_order():
    raw = "Turn 1: Halo.\nTurn 2: Apa kabar?\nTurn 3: Baik."
    assert RUNNER.parse_turns(raw) == ["Halo.", "Apa kabar?", "Baik."]


def test_parse_turns_keeps_single_prompt_intact():
    assert RUNNER.parse_turns("Halo, apa kabar?") == ["Halo, apa kabar?"]


def test_custom_cases_accept_ordered_turns():
    cases = RUNNER.load_custom_cases(
        '[{"id":"manual-01","turns":["Halo.","Apa kabar?"]}]'
    )
    assert len(cases) == 1
    assert cases[0]["case_id"] == "manual-01"
    assert cases[0]["turns"] == ["Halo.", "Apa kabar?"]


def test_final_test_inventory_is_exactly_18_without_mutation():
    cases = RUNNER.load_final_test_cases()
    assert len(cases) == 18
    assert all(case["verification_status"] == "draft" for case in cases)
