#!/usr/bin/env python3
"""Observational runner for ILIS Final-Test and custom Chatbot Playground prompts."""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ilis.interfaces import ILISCore

ROOT = Path(__file__).resolve().parents[1]
EVALUATION_DIR = ROOT / "data" / "indonesian" / "evaluation"
TURN_PATTERN = re.compile(r"Turn\s+\d+\s*:\s*(.*?)(?=Turn\s+\d+\s*:|$)", re.IGNORECASE | re.DOTALL)


def parse_turns(raw: str) -> list[str]:
    matches = [part.strip() for part in TURN_PATTERN.findall(raw)]
    return [part for part in matches if part] if matches else [raw.strip()]


def load_final_test_cases() -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    for path in sorted(EVALUATION_DIR.glob("batch_*.jsonl")):
        with path.open(encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                if not line.strip():
                    continue
                record = json.loads(line)
                if record.get("split") == "final_test":
                    raw_input = record.get("input", "")
                    cases.append({
                        "case_id": record.get("evaluation_id", f"{path.name}:{line_number}"),
                        "source_file": str(path.relative_to(ROOT)),
                        "group": record.get("group"),
                        "target_ref": record.get("target_ref"),
                        "input": raw_input,
                        "expected_behavior": record.get("expected_behavior", ""),
                        "verification_status": record.get("verification_status"),
                        "turns": parse_turns(raw_input),
                    })
    return cases


def load_custom_cases(raw: str) -> list[dict[str, Any]]:
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"custom_prompts_json bukan JSON valid: {exc}") from exc
    if not isinstance(payload, list) or not payload:
        raise ValueError("custom_prompts_json harus berupa array JSON yang tidak kosong.")
    if len(payload) > 25:
        raise ValueError("Maksimal 25 kasus custom per eksekusi.")
    cases = []
    for index, item in enumerate(payload, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"Kasus custom ke-{index} harus berupa objek.")
        case_id = str(item.get("id") or f"custom-{index:03d}")
        turns = item.get("turns")
        if not isinstance(turns, list) or not turns or len(turns) > 10:
            raise ValueError(f"{case_id}: turns harus berupa array 1–10 pesan.")
        clean_turns = []
        for turn in turns:
            if not isinstance(turn, str) or not turn.strip() or len(turn) > 5000:
                raise ValueError(f"{case_id}: setiap pesan harus 1–5000 karakter.")
            clean_turns.append(turn.strip())
        cases.append({
            "case_id": case_id,
            "source_file": "custom input",
            "group": "custom",
            "target_ref": None,
            "input": "\n".join(clean_turns),
            "expected_behavior": item.get("expected_behavior", ""),
            "verification_status": "custom",
            "turns": clean_turns,
        })
    return cases


def run_cases(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    results = []
    for case in cases:
        result = {**case, "execution_status": "EXECUTED", "turn_results": [], "execution_error": None}
        core = ILISCore()
        try:
            chatbot = core.chatbot()
            session_id = chatbot.create_session(metadata={
                "source": "ilis_final_test_playground", "case_id": case["case_id"]
            })
            result["session_id"] = session_id
            for turn_number, message in enumerate(case["turns"], start=1):
                try:
                    response = chatbot.respond(message, session_id)
                    result["turn_results"].append({
                        "turn": turn_number,
                        "user_message": message,
                        "answer": response.get("answer"),
                        "metadata": response.get("metadata"),
                        "semantic_result": response.get("semantic_result"),
                        "reasoning_result": response.get("reasoning_result"),
                        "generation": response.get("generation"),
                        "context_snapshot": response.get("context_snapshot"),
                    })
                except Exception as exc:
                    result["execution_status"] = "ERROR"
                    result["execution_error"] = f"Turn {turn_number}: {type(exc).__name__}: {exc}"
                    break
        except Exception as exc:
            result["execution_status"] = "ERROR"
            result["execution_error"] = f"{type(exc).__name__}: {exc}"
        finally:
            core.close()
        results.append(result)
        print(f"[{result['execution_status']}] {result['case_id']} ({len(result['turn_results'])}/{len(case['turns'])} turns)")
    return results


def build_report(results: list[dict[str, Any]], mode: str, commit: str) -> str:
    executed = sum(item["execution_status"] == "EXECUTED" for item in results)
    errors = len(results) - executed
    total_turns = sum(len(item["turn_results"]) for item in results)
    lines = [
        "# ILIS Chatbot Playground — Observational Run", "",
        f"- Mode: {mode}",
        f"- Timestamp (UTC): {datetime.now(timezone.utc).isoformat()}",
        f"- Checked-out commit: {commit or 'not supplied'}",
        f"- Cases: **{len(results)}**",
        f"- Cases executed without runtime exception: **{executed}**",
        f"- Cases with execution error: **{errors}**",
        f"- User turns processed: **{total_turns}**", "",
        "> This is an observational execution report, not a PASS/FAIL score. "
        "Expected behavior is shown for human comparison; it is not injected "
        "into ILIS and is not used to tune the system. Final-Test records remain DRAFT.", "",
    ]
    for item in results:
        lines.extend([
            "---", "", f"## {item['case_id']} — {item['execution_status']}", "",
            f"- Group: {item.get('group')}",
            f"- Target: {item.get('target_ref')}",
            f"- Source: {item.get('source_file')}",
            f"- Verification status: {item.get('verification_status')}", "",
            "**Expected behavior (reference only)**", "",
            item.get("expected_behavior") or "_Tidak disediakan._", "",
        ])
        if item.get("execution_error"):
            lines.extend(["**Execution error**", "", item["execution_error"], ""])
        for turn in item["turn_results"]:
            lines.extend([
                f"### Turn {turn['turn']}", "",
                "**Pesan pengguna**", "", turn["user_message"], "",
                "**Jawaban asli ILIS**", "", turn.get("answer") or "_Tidak ada jawaban._", "",
                "**Metadata**", "", json.dumps(turn.get("metadata"), ensure_ascii=False, indent=2, default=str), "",
                "**Semantic result**", "", json.dumps(turn.get("semantic_result"), ensure_ascii=False, indent=2, default=str), "",
                "**Reasoning result**", "", json.dumps(turn.get("reasoning_result"), ensure_ascii=False, indent=2, default=str), "",
            ])
    lines.extend([
        "---", "", "## Interpretasi", "",
        "Runner tidak menghitung PASS rate. Penilaian kesesuaian jawaban terhadap "
        "expected behavior dilakukan setelah membaca jawaban dan metadata asli. "
        "GitHub Actions berjalan pada runner jarak jauh, bukan staging lokal.", "",
    ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("final_test", "custom"), default="final_test")
    parser.add_argument("--custom-json", default="")
    args = parser.parse_args()
    if args.mode == "final_test":
        cases = load_final_test_cases()
        if len(cases) != 18:
            raise RuntimeError(f"Ditemukan {len(cases)} kasus Final-Test; diharapkan tepat 18.")
    else:
        cases = load_custom_cases(args.custom_json)

    results = run_cases(cases)
    output_dir = ROOT / "playground-results"
    output_dir.mkdir(exist_ok=True)
    (output_dir / "results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8"
    )
    import os
    report = build_report(results, args.mode, os.environ.get("GITHUB_SHA", ""))
    (output_dir / "report.md").write_text(report, encoding="utf-8")
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as handle:
            handle.write(report)
    return 1 if any(item["execution_status"] == "ERROR" for item in results) else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"PLAYGROUND ERROR: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise SystemExit(2)
