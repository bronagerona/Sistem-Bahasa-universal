"""Generic, read-only loader and isolated A/B runner for Indonesian DRAFT batches 001-005."""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

from ilis.interfaces import ILISCore
from test2_sample5_injection_adapter import Sample5InjectionAdapter
from test2_playground_loader_sampel5 import CASES as REGRESSION_CASES, load_one

ROOT = Path(__file__).resolve().parents[1]
SOURCE_SHA = "80475e0f5e7c78c92a84109522777946dd9fb797"
BRANCH = "test-playground-batch001-005"
PILLARS = ("lexicon", "sentence_patterns", "dialogues", "knowledge", "evaluation")
REASONING_KEYS = {"conclusion", "confidence_score", "evidence", "reasoning_type", "reasons", "uncertainty"}
SEMANTIC_KEYS = {"Actor", "Predicate", "Patient/Object", "Intent", "Time", "Aspect", "Location", "Recipient", "Negation", "Modality", "Register", "Confidence"}


def read_batches():
    records = defaultdict(list)
    files = {}
    for pillar in PILLARS:
        for batch in range(1, 6):
            rel = f"{pillar}/batch_{batch:03d}.jsonl"
            path = ROOT / "data" / "indonesian" / rel
            rows = []
            with path.open(encoding="utf-8") as stream:
                for line_no, line in enumerate(stream, 1):
                    if not line.strip():
                        continue
                    row = json.loads(line)
                    row["_source_batch"] = batch
                    rid = next((row[k] for k in ("entry_id", "pattern_id", "dialogue_id", "fact_id", "evaluation_id") if k in row), None)
                    if not rid:
                        raise ValueError(f"{rel}:{line_no}: missing record ID")
                    status = row.get("verification_status", row.get("annotation_status"))
                    if status != "draft":
                        raise ValueError(f"{rid}: expected DRAFT, got {status!r}")
                    rows.append(row)
                    records[pillar].append(row)
            if not rows:
                raise ValueError(f"{rel}: empty batch")
            files[rel] = len(rows)
    return records, files


def normalize_dialogue_semantics(annotation):
    """Normalize dialogue schema to the runtime's 12-field Semantic contract."""
    value = dict(annotation or {})
    negation = value.get("Negation", False)
    if isinstance(negation, bool):
        # Dialogue annotations use bool; runtime uses typed string labels.
        negation = "negative" if negation else "none"
    elif negation is None:
        negation = "none"
    else:
        negation = str(negation)
    result = {
        "Actor": value.get("Actor"),
        "Predicate": value.get("Predicate"),
        "Patient/Object": value.get("Patient/Object"),
        "Intent": value.get("Intent") or "unknown",
        "Time": value.get("Time"),
        "Aspect": value.get("Aspect") or "unspecified",
        "Location": value.get("Location"),
        "Recipient": value.get("Recipient"),
        "Negation": negation,
        "Modality": value.get("Modality") or "none",
        "Register": value.get("Register") or "unknown",
        "Confidence": float(value.get("Confidence", 0.5)),
    }
    if set(result) != SEMANTIC_KEYS:
        raise AssertionError("Semantic normalization did not produce exactly 12 fields")
    return result


def build_cases(records):
    cases = {}
    # Dialogue turns provide the richest native Semantic annotations.
    for row in records["dialogues"]:
        for turn in row.get("turns", []):
            if turn.get("speaker") != "user":
                continue
            utterance = (turn.get("utterance") or "").strip()
            if utterance and utterance not in cases:
                cases[utterance] = {
                    "input": utterance, "batch": row["_source_batch"],
                    "pillar": "dialogues", "source_ids": [row["dialogue_id"]],
                    "draft_semantic": normalize_dialogue_semantics(turn.get("semantic_annotation")),
                    "draft_status": "DRAFT",
                }
    # Evaluation examples add explicit test prompts and linked target records.
    by_id = {row.get(k): row for p in records.values() for row in p
             for k in ("entry_id", "pattern_id", "dialogue_id", "fact_id") if row.get(k)}
    for row in records["evaluation"]:
        prompt = (row.get("input") or "").strip()
        if prompt and not prompt.lower().startswith("turn "):
            target = by_id.get(row.get("target_ref"))
            if prompt not in cases:
                cases[prompt] = {
                    "input": prompt, "batch": row["_source_batch"],
                    "pillar": "evaluation", "source_ids": [row["evaluation_id"], row.get("target_ref")],
                    "draft_semantic": None, "target_record": target, "draft_status": "DRAFT",
                }
    # Lexicon/pattern examples expand coverage when no dialogue/evaluation prompt exists.
    for pillar in ("lexicon", "sentence_patterns"):
        for row in records[pillar]:
            examples = row.get("positive_examples", [])
            if pillar == "lexicon":
                examples = examples or row.get("examples", [])
            for prompt in examples:
                prompt = (prompt or "").strip()
                if prompt and prompt not in cases:
                    rid = row.get("entry_id") or row.get("pattern_id")
                    cases[prompt] = {
                        "input": prompt, "batch": row["_source_batch"],
                        "pillar": pillar, "source_ids": [rid], "draft_semantic": None,
                        "target_record": row, "draft_status": "DRAFT",
                    }
    return list(cases.values())


def semantic_for_case(case):
    if case.get("draft_semantic"):
        return case["draft_semantic"]
    text = case["input"]
    record = case.get("target_record") or {}
    lower = text.casefold()
    neg = "not_yet" if re.search(r"\bbelum\b", lower) else "negative" if re.search(r"\b(tidak|bukan|jangan)\b", lower) else "none"
    intent = record.get("intent") or record.get("expected_behavior") or "assertion"
    if "?" in text:
        intent = "question"
    actor = next(iter(re.findall(r"\b[A-Z][a-zA-Z]+\b", text)), None)
    predicate = record.get("lemma") or record.get("name") or record.get("predicate")
    return {
        "Actor": actor, "Predicate": predicate, "Patient/Object": None,
        "Intent": str(intent)[:100], "Time": None, "Aspect": "unspecified",
        "Location": None, "Recipient": None, "Negation": neg,
        "Modality": "none", "Register": record.get("register", "unknown"),
        "Confidence": 0.55,
    }


class GenericBatchAdapter:
    """Per-instance adapter: exact prompts from loaded DRAFT records only."""
    def __init__(self, cases):
        self.by_text = {c["input"]: c for c in cases}
        self.knowledge = []

    def install(self, core):
        # Knowledge is retained only as in-memory hypotheses, never verified facts.
        for row in self.knowledge:
            core.knowledge_engine.add_fact(
                str(row.get("subject") or ""), str(row.get("predicate") or ""), str(row.get("object") or ""),
                status="hypothesis", source=f"dataset_draft:{row.get('fact_id')}",
            )
        original_analyze = core.analyze_text
        def analyze_text(text, *, context_snapshot=None):
            base = original_analyze(text, context_snapshot=context_snapshot)
            case = self.by_text.get(text)
            if not case:
                return base
            semantic = semantic_for_case(case)
            # The runtime validator receives a full, typed 12-key object.
            from ilis.semantics.contract_validator import validate_output
            result = dict(base)
            result["status"] = "supported"
            result["semantics"] = semantic
            validate_output(result)
            return result
        core.analyze_text = analyze_text

        original_reason = core.reasoning_engine.infer_semantic
        def infer_semantic(semantic, *, context_snapshot=None):
            base = original_reason(semantic, context_snapshot=context_snapshot)
            text = semantic.get("original_text", "")
            case = self.by_text.get(text)
            if not case:
                return base
            src = ", ".join(case["source_ids"])
            draft_fact = case.get("pillar") == "knowledge" or bool((case.get("target_record") or {}).get("fact_id"))
            return {
                "conclusion": f"Interpretasi sementara untuk input: {text}",
                "confidence_score": min(float((case.get("draft_semantic") or {}).get("Confidence", 0.55)), 0.75),
                "evidence": case["source_ids"],
                "reasoning_type": "draft_dataset_interpretation",
                "reasons": [f"Input dicocokkan dengan record DRAFT {src}.",
                            "Anotasi diperlakukan sebagai bahan uji, bukan gold label terverifikasi."],
                "uncertainty": (
                    "Record pengetahuan dan seluruh dataset masih DRAFT, belum diverifikasi; "
                    "kesimpulan ini hanya hipotesis dan tidak boleh diperlakukan sebagai fakta terverifikasi."
                    if draft_fact else
                    "Record dan anotasi masih DRAFT, belum diverifikasi; interpretasi dapat berubah setelah kurasi sumber."
                ),
            }
        core.reasoning_engine.infer_semantic = infer_semantic


def run_core(core, cases):
    bot = core.chatbot()
    out = []
    for case in cases:
        response = bot.respond(case["input"])
        out.append({
            "input": case["input"], "batch": case["batch"], "pillar": case["pillar"],
            "source_ids": case["source_ids"], "answer": response.get("answer"),
            "metadata": response.get("metadata"),
            "semantic_result": response.get("semantic_result"),
            "reasoning_result": response.get("reasoning_result"),
        })
    core.close()
    return out


def check_reasoning(results):
    failures = []
    for item in results:
        reasoning = item.get("reasoning_result") or {}
        if set(reasoning) != REASONING_KEYS:
            failures.append({"input": item["input"], "error": "reasoning_6_keys_incomplete", "keys": sorted(reasoning)})
        elif not isinstance(reasoning["confidence_score"], (int, float)):
            failures.append({"input": item["input"], "error": "confidence_not_numeric"})
        elif not reasoning["uncertainty"]:
            failures.append({"input": item["input"], "error": "uncertainty_empty"})
    return failures


def main():
    records, files = read_batches()
    cases = build_cases(records)
    if not cases:
        raise RuntimeError("No test cases generated from Batch 001-005")
    # Regression gate: original five Stage-A samples must remain byte-for-byte allowlisted
    # and preserve the six-key reasoning contract.
    old_bundle = {}
    for c in REGRESSION_CASES:
        for pillar, refs in c["records"].items():
            old_bundle.setdefault(pillar, [])
            for rel, key, rid in refs:
                old_bundle[pillar].append(load_one(rel, key, rid))
    regression_adapter = Sample5InjectionAdapter(old_bundle)
    regression_core = ILISCore()
    regression_adapter.install(regression_core)
    regression_results = run_core(regression_core, [
        {"input": c["input"], "batch": 0, "pillar": "stage_a_regression", "source_ids": [c["id"]]}
        for c in REGRESSION_CASES
    ])
    regression_errors = check_reasoning(regression_results)
    for item in regression_results:
        sem = item.get("semantic_result") or {}
        if sem.get("status") != "supported" or len(sem.get("semantics") or {}) != 12:
            regression_errors.append({"input": item["input"], "error": "stage_a_semantic_regression"})
    if regression_errors:
        raise AssertionError(f"Stage-A regression failed: {regression_errors}")

    # General loader A/B: Test 1 baseline vs Test 2 generic adapter with batches 001-005.
    baseline = run_core(ILISCore(), cases)
    adapter = GenericBatchAdapter(cases)
    adapter.knowledge = records["knowledge"]
    active_core = ILISCore()
    adapter.install(active_core)
    active = run_core(active_core, cases)
    reasoning_errors = check_reasoning(active)
    if reasoning_errors:
        raise AssertionError(f"Batch A/B Reasoning contract failed: {reasoning_errors}")

    batch_summary = {}
    for batch in range(1, 6):
        selected = [x for x in active if x["batch"] == batch]
        errs = [e for e in reasoning_errors if any(e["input"] == x["input"] for x in selected)]
        batch_summary[f"{batch:03d}"] = {
            "status": "LULUS" if selected and not errs else "GAGAL",
            "cases": len(selected), "reasoning_failures": len(errs),
            "note": "Status menilai loader, pemetaan dan kontrak Reasoning; bukan verifikasi kebenaran isi DRAFT.",
        }
    # Explicitly inspect bool-to-label conversion on all dialogue turn annotations.
    bool_negation = []
    for row in records["dialogues"]:
        for turn in row.get("turns", []):
            ann = turn.get("semantic_annotation") or {}
            if isinstance(ann.get("Negation"), bool):
                normalized = normalize_dialogue_semantics(ann)["Negation"]
                bool_negation.append({"dialogue_id": row["dialogue_id"], "turn_id": turn.get("turn_id"),
                                      "source_boolean": ann["Negation"], "runtime_label": normalized})

    comparison = []
    for before, after in zip(baseline, active):
        bs, ats = before.get("semantic_result") or {}, after.get("semantic_result") or {}
        br, ar = before.get("reasoning_result") or {}, after.get("reasoning_result") or {}
        comparison.append({
            "input": before["input"], "batch": before["batch"], "pillar": before["pillar"],
            "source_ids": before["source_ids"],
            "semantic_test1": bs.get("semantics"), "semantic_test2": ats.get("semantics"),
            "semantic_status": [bs.get("status"), ats.get("status")],
            "reasoning_test1": br, "reasoning_test2": ar,
        })

    report = {
        "title": "Tahap B — Generic loader A/B Batch 001-005",
        "source_branch": "ilis-v2-development", "source_sha": SOURCE_SHA,
        "experiment_branch": BRANCH, "created_at": datetime.now(timezone.utc).isoformat(),
        "read_only": True, "dataset_status": "ALL DRAFT",
        "files_per_pillar_batch": files,
        "records_per_pillar": {p: len(records[p]) for p in PILLARS},
        "total_records": sum(map(len, records.values())),
        "test_cases": len(cases),
        "stage_a_regression": {"status": "LULUS", "cases": len(regression_results),
                               "results": regression_results, "reasoning_failures": regression_errors},
        "dialogue_negation_normalization": {"count": len(bool_negation), "examples": bool_negation[:30],
                                            "rule": "bool true -> negative; bool false -> none"},
        "batch_status": batch_summary,
        "test1": {"mode": "ILIS murni; tanpa dataset adapter", "results": baseline},
        "test2": {"mode": "ILIS + loader umum Batch 001-005", "results": active},
        "semantic_reasoning_comparison": comparison,
        "errors_and_threats": [
            "Dataset seluruhnya DRAFT; output adapter adalah interpretasi eksperimen, bukan gold label.",
            "Negation boolean dialog dinormalisasi ke label runtime; pemetaan true=negative tidak membedakan jenis negasi.",
            "Kasus multi-turn evaluation yang berbentuk transcript tidak dieksekusi sebagai sesi percakapan; dihitung sebagai coverage limitation.",
            "Batch-level status hanya menilai loader dan kontrak output, bukan validitas linguistik/faktual.",
        ],
        "production_modified": False, "main_modified": False,
        "ilis_v2_development_modified": False, "jsonl_modified": False,
    }
    outdir = ROOT / "test-results"
    outdir.mkdir(exist_ok=True)
    (outdir / "test2-batch001-005-ab-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    log = [
        "TAHAP B — GENERIC LOADER + A/B TEST",
        f"SOURCE_SHA={SOURCE_SHA}", f"EXPERIMENT_BRANCH={BRANCH}",
        f"FILES_LOADED={len(files)}", f"RECORDS_LOADED={report['total_records']}",
        f"TEST_CASES={len(cases)}", "STAGE_A_REGRESSION=LULUS (5/5)",
        f"DIALOGUE_BOOLEAN_NEGATION_NORMALIZED={len(bool_negation)}",
        "TEST1=ILIS_BASELINE_NO_DATASET", "TEST2=GENERIC_BATCH_001_005_ADAPTER",
        *[f"BATCH_{b}_STATUS={v['status']} CASES={v['cases']}" for b, v in batch_summary.items()],
        f"REASONING_CONTRACT_FAILURES={len(reasoning_errors)}",
        "DRAFT_KNOWLEDGE_POLICY=ALL_KNOWLEDGE_HYPOTHESIS_ONLY",
        "JSONL_MODIFIED=NO", "PRODUCTION_MODIFIED=NO", "MAIN_MODIFIED=NO",
        "ILIS_V2_DEVELOPMENT_MODIFIED=NO",
    ]
    (outdir / "test2-batch001-005-proof.log").write_text("\n".join(log) + "\n", encoding="utf-8")
    print("\n".join(log))
    print("REPORT=test-results/test2-batch001-005-ab-report.json")
    print("PROOF_LOG=test-results/test2-batch001-005-proof.log")
    summary = __import__("os").environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as f:
            f.write("# Tahap B — Batch 001-005\n\n")
            f.write(f"- Loaded records: {report['total_records']} / {len(files)} files\n")
            f.write(f"- Test cases: {len(cases)}; Stage-A regression: PASS 5/5\n")
            f.write(f"- Dialogue boolean Negation normalized: {len(bool_negation)}\n\n")
            for batch, value in batch_summary.items():
                f.write(f"- Batch {batch}: **{value['status']}** ({value['cases']} cases)\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
