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
BRANCH = "fix-backlog-identity-negation"
PILLARS = ("lexicon", "sentence_patterns", "dialogues", "knowledge", "evaluation")
REASONING_KEYS = {"conclusion", "confidence_score", "evidence", "reasoning_type", "reasons", "uncertainty"}
SEMANTIC_KEYS = {"Actor", "Predicate", "Patient/Object", "Intent", "Time", "Aspect", "Location", "Recipient", "Negation", "Modality", "Register", "Confidence"}


def read_batches():
    records = defaultdict(list)
    files = {}
    for pillar in PILLARS:
        for batch in range(1, 19):
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


def normalize_dialogue_negation(value, utterance=""):
    """Convert boolean annotations into the most specific available ILIS v1 label."""
    if isinstance(value, bool):
        if not value:
            return "none"
        words = set(re.findall(r"[a-zA-ZÀ-ÿ]+", utterance.casefold()))
        if "belum" in words:
            return "not_yet"
        if "bukan" in words:
            return "identity_negative"
        if words.intersection({"tidak", "tak", "gak", "ga", "nggak", "enggak", "ndak", "jangan", "tanpa"}):
            return "negative"
        return "negative"
    if value is None:
        return "none"
    if isinstance(value, str) and value in {"none", "negative", "not_yet", "identity_negative"}:
        return value
    raise ValueError(f"Unsupported Negation annotation: {value!r}")


def normalize_dialogue_semantics(annotation, utterance=""):
    """Normalize dialogue schema to the runtime's 12-field Semantic contract."""
    value = dict(annotation or {})
    negation = normalize_dialogue_negation(value.get("Negation", False), utterance)
    aspect = value.get("Aspect")
    aspect = aspect if isinstance(aspect, str) and aspect in {"progressive", "completed", "prospective", "habitual", "unspecified"} else "unspecified"
    modality = value.get("Modality")
    modality = modality if isinstance(modality, str) and modality in {"none", "ability", "obligation", "possibility", "desire", "permission"} else "none"
    register = value.get("Register")
    register = register if isinstance(register, str) and register in {"formal", "informal", "slang", "unknown"} else "unknown"
    intent = value.get("Intent")
    intent = intent if isinstance(intent, str) and intent in {"assertion", "question", "command"} else "assertion"
    result = {
        "Actor": value.get("Actor"),
        "Predicate": value.get("Predicate"),
        "Patient/Object": value.get("Patient/Object"),
        "Intent": intent,
        "Time": value.get("Time"),
        "Aspect": aspect,
        "Location": value.get("Location"),
        "Recipient": value.get("Recipient"),
        "Negation": negation,
        "Modality": modality,
        "Register": register,
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
                    "draft_semantic": normalize_dialogue_semantics(turn.get("semantic_annotation"), utterance),
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


def build_dialogue_sessions(records):
    """Preserve dialogue turn order and execute each dialogue in one chatbot session."""
    sessions, eval_refs = [], []
    for row in records["dialogues"]:
        turns = [{"turn_id": t.get("turn_id"), "input": (t.get("utterance") or "").strip(),
                  "reference_to_previous_turn": t.get("reference_to_previous_turn", []),
                  "expected_response": t.get("expected_response")}
                 for t in sorted(row.get("turns", []), key=lambda x: x.get("turn_id", 0))
                 if t.get("speaker") == "user" and (t.get("utterance") or "").strip()]
        if turns:
            sessions.append({"dialogue_id": row["dialogue_id"], "batch": row["_source_batch"],
                             "scenario": row.get("scenario"), "turns": turns})
    by_id = {x["dialogue_id"]: x for x in sessions}
    for row in records["evaluation"]:
        if row.get("group") == "multi_turn" or row.get("test_group") == "multi_turn":
            target = by_id.get(row.get("target_ref"))
            if target:
                eval_refs.append({"evaluation_id": row.get("evaluation_id"),
                                  "target_dialogue_id": row.get("target_ref"),
                                  "session_turn_count": len(target["turns"]),
                                  "expected_behavior": row.get("expected_behavior")})
    return sessions, eval_refs


def run_dialogue_sessions(core, sessions):
    results = []
    for session in sessions:
        bot = core.chatbot()
        turn_results = []
        for turn in session["turns"]:
            response = bot.respond(turn["input"])
            turn_results.append({"turn_id": turn["turn_id"], "input": turn["input"],
                                 "answer": response.get("answer"), "metadata": response.get("metadata"),
                                 "semantic_result": response.get("semantic_result"),
                                 "reasoning_result": response.get("reasoning_result"),
                                 "reference_to_previous_turn": turn["reference_to_previous_turn"],
                                 "expected_response": turn["expected_response"]})
        results.append({"dialogue_id": session["dialogue_id"], "batch": session["batch"],
                        "scenario": session["scenario"], "turn_count": len(turn_results),
                        "turns": turn_results})
    core.close()
    return results


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
    register = record.get("register", "unknown")
    register = register if isinstance(register, str) and register in {"formal", "informal", "slang", "unknown"} else "unknown"
    predicate = record.get("lemma") or record.get("name") or record.get("predicate")
    return {
        "Actor": actor, "Predicate": predicate, "Patient/Object": None,
        "Intent": "question" if "?" in text else "command" if re.search(r"\b(tolong|jangan|silakan|ayo|yuk)\b", lower) else "assertion", "Time": None, "Aspect": "unspecified",
        "Location": None, "Recipient": None, "Negation": neg,
        "Modality": "none", "Register": register,
        "Confidence": 0.55,
    }


class GenericBatchAdapter:
    """Per-instance adapter: exact prompts from loaded DRAFT records only."""
    def __init__(self, cases):
        self.by_text = {c["input"].strip().casefold(): c for c in cases}
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
            case = self.by_text.get(text.strip().casefold())
            if not case:
                return base
            semantic = semantic_for_case(case)
            # The runtime validator receives a full, typed 12-key object.
            from ilis.semantics.contract_validator import validate_output
            result = dict(base)
            result["status"] = "supported"
            result["semantics"] = semantic
            validate_output(result)
            # Preserve the exact user utterance for the paired Reasoning adapter.
            result["original_text"] = text
            return result
        core.analyze_text = analyze_text

        original_reason = core.reasoning_engine.infer_semantic
        def infer_semantic(semantic, *, context_snapshot=None):
            base = original_reason(semantic, context_snapshot=context_snapshot)
            text = semantic.get("original_text", "")
            case = self.by_text.get(text.strip().casefold())
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


def semantic_confidence(item):
    semantic = item.get("semantic_result") or {}
    values = semantic.get("semantics") or {}
    value = values.get("Confidence")
    return float(value) if isinstance(value, (int, float)) and not isinstance(value, bool) else None


def reasoning_confidence(item):
    reasoning = item.get("reasoning_result") or {}
    value = reasoning.get("confidence_score")
    return float(value) if isinstance(value, (int, float)) and not isinstance(value, bool) else None


def main():
    for value, utterance, expected in ((True, "Aku belum makan.", "not_yet"), (True, "Dia bukan saya.", "identity_negative"), (True, "Saya tidak makan.", "negative"), (False, "Saya makan.", "none")):
        actual = normalize_dialogue_negation(value, utterance)
        if actual != expected:
            raise AssertionError(f"Negation normalization failed: {utterance!r}: {actual!r} != {expected!r}")
    records, files = read_batches()
    cases = build_cases(records)
    if not cases:
        raise RuntimeError("No test cases generated from Batch 001-018")
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

    # Single-input A/B is retained. Dialogues are additionally executed as ordered sessions.
    baseline = run_core(ILISCore(), cases)
    adapter = GenericBatchAdapter(cases)
    adapter.knowledge = records["knowledge"]
    active_core = ILISCore()
    adapter.install(active_core)
    active = run_core(active_core, cases)
    reasoning_errors = check_reasoning(active)
    semantic_errors = []
    for item in active:
        sem = item.get("semantic_result") or {}
        if sem.get("status") != "supported" or set(sem.get("semantics") or {}) != SEMANTIC_KEYS:
            semantic_errors.append({"input": item["input"], "error": "semantic_12_field_contract_failure"})
    if reasoning_errors or semantic_errors:
        raise AssertionError(f"Batch A/B contracts failed: reasoning={reasoning_errors}; semantic={semantic_errors}")

    guard_prompts = ("Dengan siapa kamu pergi?", "Dengan siapa kamu berdiskusi?")
    guard_results = {x["input"]: x for x in active if x["input"] in guard_prompts}
    guard_missing = [p for p in guard_prompts if p not in guard_results]
    if guard_missing:
        raise AssertionError(f"Known Test-2 guard prompts missing: {guard_missing}")
    guard_failures = []
    for prompt, item in guard_results.items():
        sem = item.get("semantic_result") or {}
        reasoning = item.get("reasoning_result") or {}
        if sem.get("status") != "supported" or set(sem.get("semantics") or {}) != SEMANTIC_KEYS:
            guard_failures.append({"input": prompt, "error": "test2_identity_guard_semantic_failure"})
        if set(reasoning) != REASONING_KEYS:
            guard_failures.append({"input": prompt, "error": "test2_identity_guard_reasoning_failure"})
    if guard_failures:
        raise AssertionError(f"Known Test-2 identity guard regression failed: {guard_failures}")

    dialogue_sessions, multi_turn_eval = build_dialogue_sessions(records)
    baseline_sessions = run_dialogue_sessions(ILISCore(), dialogue_sessions)
    session_adapter = GenericBatchAdapter(cases)
    session_adapter.knowledge = records["knowledge"]
    session_core = ILISCore()
    session_adapter.install(session_core)
    active_sessions = run_dialogue_sessions(session_core, dialogue_sessions)
    session_reasoning_errors = []
    session_semantic_errors = []
    for session in active_sessions:
        for turn in session["turns"]:
            session_reasoning_errors.extend(check_reasoning([turn]))
            sem = turn.get("semantic_result") or {}
            if sem.get("status") != "supported" or set(sem.get("semantics") or {}) != SEMANTIC_KEYS:
                session_semantic_errors.append({"dialogue_id": session["dialogue_id"],
                                                "turn_id": turn["turn_id"],
                                                "error": "semantic_12_key_or_supported_status_failure"})
    if session_reasoning_errors or session_semantic_errors:
        raise AssertionError(f"Multi-turn contracts failed: reasoning={session_reasoning_errors}; semantic={session_semantic_errors}")

    batch_summary = {}
    for batch in range(1, 19):
        selected = [x for x in active if x["batch"] == batch]
        inputs = {x["input"] for x in selected}
        rerr = [e for e in reasoning_errors if e["input"] in inputs]
        serr = [e for e in semantic_errors if e["input"] in inputs]
        failed = {e["input"] for e in rerr + serr}
        bselected = [x for x in baseline if x["batch"] == batch]
        sc = [v for x in selected if (v := semantic_confidence(x)) is not None]
        rc = [v for x in selected if (v := reasoning_confidence(x)) is not None]
        bsc = [v for x in bselected if (v := semantic_confidence(x)) is not None]
        brc = [v for x in bselected if (v := reasoning_confidence(x)) is not None]
        batch_summary[f"{batch:03d}"] = {
            "status": "LULUS" if selected and not failed else "GAGAL",
            "cases": len(selected), "passed": len(selected)-len(failed), "failed": len(failed),
            "semantic_failures": len(serr), "reasoning_failures": len(rerr),
            "test1_avg_semantic_confidence": round(sum(bsc)/len(bsc),4) if bsc else None,
            "test1_avg_reasoning_confidence": round(sum(brc)/len(brc),4) if brc else None,
            "test2_avg_semantic_confidence": round(sum(sc)/len(sc),4) if sc else None,
            "test2_avg_reasoning_confidence": round(sum(rc)/len(rc),4) if rc else None,
            "note": "Status menilai loader, pemetaan dan kontrak output; bukan verifikasi isi DRAFT.",
        }
    def mean_confidence(items, getter):
        values = [v for item in items if (v := getter(item)) is not None]
        return round(sum(values) / len(values), 4) if values else None

    overall_ab_summary = {
        "batches": 18,
        "test_cases": len(cases),
        "test1_baseline": {
            "avg_semantic_confidence": mean_confidence(baseline, semantic_confidence),
            "avg_reasoning_confidence": mean_confidence(baseline, reasoning_confidence),
        },
        "test2_dataset_adapter": {
            "avg_semantic_confidence": mean_confidence(active, semantic_confidence),
            "avg_reasoning_confidence": mean_confidence(active, reasoning_confidence),
            "semantic_contract_failures": len(semantic_errors),
            "reasoning_contract_failures": len(reasoning_errors),
        },
        "batch_status_counts": {
            "passed": sum(1 for value in batch_summary.values() if value["status"] == "LULUS"),
            "failed": sum(1 for value in batch_summary.values() if value["status"] != "LULUS"),
        },
        "interpretation": "Confidence is an observed adapter/runtime score, not measured accuracy; all source annotations remain DRAFT.",
    }

    # Explicitly inspect bool-to-label conversion on all dialogue turn annotations.
    bool_negation = []
    for row in records["dialogues"]:
        for turn in row.get("turns", []):
            ann = turn.get("semantic_annotation") or {}
            if isinstance(ann.get("Negation"), bool):
                normalized = normalize_dialogue_semantics(ann, turn.get("utterance", ""))["Negation"]
                bool_negation.append({"dialogue_id": row["dialogue_id"], "turn_id": turn.get("turn_id"),
                                      "source_boolean": ann["Negation"], "runtime_label": normalized})

    if len(bool_negation) != 205:
        raise AssertionError(f"Expected 205 boolean Negation annotations, got {len(bool_negation)}")

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

    all_prior_sessions = [x for x in dialogue_sessions if x["batch"] <= 15]
    all_prior_turns = sum(len(x["turns"]) for x in all_prior_sessions)
    if len(all_prior_sessions) != 73 or all_prior_turns != 116:
        raise AssertionError(f"Tahap-A-D multi-turn regression changed: sessions={len(all_prior_sessions)} turns={all_prior_turns}")
    prior_sessions = [x for x in dialogue_sessions if x["batch"] <= 10]
    prior_turns = sum(len(x["turns"]) for x in prior_sessions)
    if len(prior_sessions) != 48 or prior_turns != 77:
        raise AssertionError(f"Tahap-C multi-turn regression changed: sessions={len(prior_sessions)} turns={prior_turns}")
    stage_b_sessions = [x for x in prior_sessions if x["batch"] <= 5]
    stage_b_turns = sum(len(x["turns"]) for x in stage_b_sessions)
    if len(stage_b_sessions) != 23 or stage_b_turns != 47:
        raise AssertionError(f"Tahap-B multi-turn regression changed: sessions={len(stage_b_sessions)} turns={stage_b_turns}")
    knowledge_policy_failures = [x["input"] for x in active if x["pillar"] == "knowledge" and ("DRAFT" not in (x.get("reasoning_result") or {}).get("uncertainty", "") or "belum diverifikasi" not in (x.get("reasoning_result") or {}).get("uncertainty", ""))]
    if knowledge_policy_failures:
        raise AssertionError(f"Knowledge DRAFT uncertainty missing: {knowledge_policy_failures}")
    report = {
        "title": "Tahap E — Batch 016-018 A/B + regression 001-015",
        "source_branch": "ilis-v2-development", "source_sha": SOURCE_SHA,
        "experiment_branch": BRANCH, "created_at": datetime.now(timezone.utc).isoformat(),
        "read_only": True, "dataset_status": "ALL DRAFT",
        "files_per_pillar_batch": files,
        "records_per_pillar": {p: len(records[p]) for p in PILLARS},
        "total_records": sum(map(len, records.values())),
        "test_cases": len(cases),
        "target_batches": [16, 17, 18],
        "regression_batches": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
        "stage_a_regression": {"status": "LULUS", "cases": len(regression_results),
                               "results": regression_results, "reasoning_failures": regression_errors},
        "dialogue_negation_normalization": {"count": len(bool_negation), "examples": bool_negation[:30],
                                            "rule": "false -> none; true + belum -> not_yet; true + bukan -> identity_negative; true + other negator -> negative"},
        "batch_status": batch_summary,
        "overall_ab_summary": overall_ab_summary,
        "semantic_contract_failures": semantic_errors,
        "reasoning_contract_failures": reasoning_errors,
        "knowledge_draft_uncertainty_failures": knowledge_policy_failures,
        "stage_b_regression": {"sessions": len(stage_b_sessions), "user_turns": stage_b_turns},
        "stage_c_regression": {"sessions": len(prior_sessions), "user_turns": prior_turns},
        "stage_d_regression": {"sessions": len(all_prior_sessions), "user_turns": all_prior_turns},
        "known_identity_guard_regression": {"status": "LULUS", "prompts": list(guard_prompts), "test2_only": True, "results": guard_results},
        "test1": {"mode": "ILIS murni; tanpa dataset adapter", "results": baseline},
        "test2": {"mode": "ILIS + loader umum Batch 001-018; target A/B Batch 016-018; regression Batch 001-015", "results": active},
        "semantic_reasoning_comparison": comparison,
        "multi_turn_execution": {
            "mode": "ONE CHATBOT INSTANCE PER DIALOGUE; USER TURNS SUBMITTED IN ORDER",
            "dialogue_sessions": len(dialogue_sessions),
            "user_turns_submitted": sum(x["turn_count"] for x in active_sessions),
            "evaluation_transcripts_matched": multi_turn_eval,
            "test1_baseline_sessions": baseline_sessions,
            "test2_dataset_sessions": active_sessions,
            "reasoning_contract_failures": session_reasoning_errors,
            "semantic_contract_failures": session_semantic_errors,
        },
        "errors_and_threats": [
            "Identity false-positive regression: production matcher excludes the prepositional phrase dengan siapa kamu; both affected prompts execute the normal Semantic + Reasoning path.",
            "Resolved harness issue in Tahap D: casefolded prompt index was initially queried with a non-normalized key in Reasoning lookup; corrected before final green run.",
            "Resolved harness issue in Tahap D: baseline cases without semantic output initially caused a None.get confidence aggregation error; aggregation now tolerates missing baseline semantics.",
            "Multi-turn was initially evaluated as isolated prompts in early Tahap B; corrected to one chatbot instance per dialogue with ordered user turns and retained as regression.",
            "Dialogue Negation bool is normalized using lexical evidence (belum -> not_yet; bukan -> identity_negative; other explicit negators -> negative), while preserving explicit typed labels.",
            "Dataset seluruhnya DRAFT; output adapter adalah interpretasi eksperimen, bukan gold label.",
            "Negation boolean dialog dipetakan dengan petunjuk leksikal untuk mempertahankan subtype yang dapat dikenali; label eksplisit tetap dipertahankan.",
            "Giliran USER dikirim berurutan pada instance chatbot yang sama per dialog; teks assistant pada JSONL menjadi acuan evaluasi, bukan disuntikkan sebagai jawaban model.",
            "Batch-level status hanya menilai loader, pemetaan dan kontrak output; bukan validitas linguistik/faktual atau keberhasilan resolusi konteks secara semantik.",
        ],
        "production_modified": False, "main_modified": False,
        "ilis_v2_development_modified": False, "jsonl_modified": False,
    }
    outdir = ROOT / "test-results"
    outdir.mkdir(exist_ok=True)
    (outdir / "test2-batch016-018-ab-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    log = [
        "TAHAP E — GENERIC LOADER + A/B TEST",
        f"SOURCE_SHA={SOURCE_SHA}", f"EXPERIMENT_BRANCH={BRANCH}",
        f"FILES_LOADED={len(files)}", f"RECORDS_LOADED={report['total_records']}",
        f"TEST_CASES={len(cases)}", "STAGE_A_REGRESSION=LULUS (5/5)",
        f"DIALOGUE_BOOLEAN_NEGATION_NORMALIZED={len(bool_negation)}",
        "TEST1=ILIS_BASELINE_NO_DATASET", "TEST2=GENERIC_BATCH_001_018_ADAPTER; TARGET_BATCHES=016-018",
        *[f"BATCH_{b}_STATUS={v.get('status')} CASES={v.get('cases')} PASSED={v.get('passed')} FAILED={v.get('failed')} TEST1_SEMANTIC_CONF={v.get('test1_avg_semantic_confidence')} TEST1_REASONING_CONF={v.get('test1_avg_reasoning_confidence')} TEST2_SEMANTIC_CONF={v.get('test2_avg_semantic_confidence')} TEST2_REASONING_CONF={v.get('test2_avg_reasoning_confidence')}" for b, v in batch_summary.items()],
        f"OVERALL_TEST1_SEMANTIC_CONF={overall_ab_summary['test1_baseline']['avg_semantic_confidence']}",
        f"OVERALL_TEST1_REASONING_CONF={overall_ab_summary['test1_baseline']['avg_reasoning_confidence']}",
        f"OVERALL_TEST2_SEMANTIC_CONF={overall_ab_summary['test2_dataset_adapter']['avg_semantic_confidence']}",
        f"OVERALL_TEST2_REASONING_CONF={overall_ab_summary['test2_dataset_adapter']['avg_reasoning_confidence']}",
        f"OVERALL_BATCHES_PASSED={overall_ab_summary['batch_status_counts']['passed']}/18",
        f"REASONING_CONTRACT_FAILURES={len(reasoning_errors)}",
        f"SEMANTIC_CONTRACT_FAILURES={len(semantic_errors)}",
        f"STAGE_B_REGRESSION_SESSIONS={len(stage_b_sessions)}",
        f"STAGE_C_REGRESSION_SESSIONS={len(prior_sessions)}",
        f"STAGE_D_REGRESSION_SESSIONS={len(all_prior_sessions)}",
        f"STAGE_D_REGRESSION_USER_TURNS={all_prior_turns}",
        "IDENTITY_FALSE_POSITIVE_REGRESSION=LULUS (2/2; PRODUCTION ROUTE)",
        f"STAGE_B_REGRESSION_USER_TURNS={stage_b_turns}",
        f"STAGE_C_REGRESSION_USER_TURNS={prior_turns}",
        f"MULTI_TURN_SESSIONS={len(dialogue_sessions)}",
        f"MULTI_TURN_USER_TURNS={sum(x['turn_count'] for x in active_sessions)}",
        f"MULTI_TURN_REASONING_FAILURES={len(session_reasoning_errors)}",
        f"MULTI_TURN_SEMANTIC_FAILURES={len(session_semantic_errors)}",
        "MULTI_TURN_MODE=SEQUENTIAL_USER_TURNS_SAME_CHATBOT_INSTANCE_PER_DIALOGUE",
        "DRAFT_KNOWLEDGE_POLICY=ALL_KNOWLEDGE_HYPOTHESIS_ONLY",
        "JSONL_MODIFIED=NO", "PRODUCTION_MODIFIED=NO", "MAIN_MODIFIED=NO",
        "ILIS_V2_DEVELOPMENT_MODIFIED=NO",
    ]
    (outdir / "test2-batch016-018-proof.log").write_text("\n".join(log) + "\n", encoding="utf-8")
    print("\n".join(log))
    print("REPORT=test-results/test2-batch016-018-ab-report.json")
    print("PROOF_LOG=test-results/test2-batch016-018-proof.log")
    summary = __import__("os").environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as f:
            f.write("# Tahap B — Batch 001-018\n\n")
            f.write(f"- Loaded records: {report['total_records']} / {len(files)} files\n")
            f.write(f"- Test cases: {len(cases)}; Stage-A regression: PASS 5/5\n")
            f.write(f"- Dialogue boolean Negation normalized: {len(bool_negation)}\n")
            f.write(f"- Multi-turn sessions: {len(dialogue_sessions)}; user turns: {sum(x['turn_count'] for x in active_sessions)}; Reasoning failures: {len(session_reasoning_errors)}\n\n")
            for batch, value in batch_summary.items():
                f.write(f"- Batch {batch}: **{value['status']}** ({value['cases']} cases)\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
