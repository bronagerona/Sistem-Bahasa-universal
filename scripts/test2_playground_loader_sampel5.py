"""Run a reproducible A/B comparison for exactly five DRAFT dataset samples."""
from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime, timezone
from ilis.interfaces import ILISCore
from test2_sample5_injection_adapter import Sample5InjectionAdapter

ROOT = Path(__file__).resolve().parents[1]
SOURCE_SHA = "80475e0f5e7c78c92a84109522777946dd9fb797"
CASES = [
 {"id":"T2-01","label":"Negasi temporal: belum","input":"Aku belum membaca buku itu.","records":{"lexicon":[("lexicon/batch_010.jsonl","entry_id","lex-0048")],"sentence_patterns":[("sentence_patterns/batch_010.jsonl","pattern_id","pat-0048")],"dialogues":[("dialogues/batch_010.jsonl","dialogue_id","dlg-0046")]}},
 {"id":"T2-02","label":"Penyangkalan identitas: bukan","input":"Orang yang menelepon tadi bukan kakakku.","records":{"lexicon":[("lexicon/batch_010.jsonl","entry_id","lex-0049")],"sentence_patterns":[("sentence_patterns/batch_010.jsonl","pattern_id","pat-0049")],"dialogues":[("dialogues/batch_010.jsonl","dialogue_id","dlg-0047")]}},
 {"id":"T2-03","label":"Larangan: jangan","input":"Jangan kirim berkas itu dulu.","records":{"lexicon":[("lexicon/batch_010.jsonl","entry_id","lex-0051")],"sentence_patterns":[("sentence_patterns/batch_010.jsonl","pattern_id","pat-0051")],"dialogues":[("dialogues/batch_010.jsonl","dialogue_id","dlg-0049")]}},
 {"id":"T2-04","label":"Polisemi awalan ter-","input":"Ia terjatuh saat menuruni tangga.","records":{"lexicon":[("lexicon/batch_018.jsonl","entry_id","lex-0091")],"sentence_patterns":[("sentence_patterns/batch_018.jsonl","pattern_id","pat-0091")]}},
 {"id":"T2-05","label":"Fakta pengetahuan: satuan astronomi","input":"Berapa meter nilai satu satuan astronomi (au) menurut definisi IAU?","records":{"knowledge":[("knowledge/batch_010.jsonl","fact_id","fact-0048")]}},
]


def load_one(rel: str, key: str, wanted: str) -> dict:
    path = ROOT / "data" / "indonesian" / rel
    found = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                row = json.loads(line)
                if row.get(key) == wanted:
                    found.append(row)
    if len(found) != 1:
        raise ValueError(f"Expected exactly one {wanted} in {rel}; found {len(found)}")
    row = found[0]
    if not (row.get("verification_status") == "draft" or row.get("annotation_status") == "draft"):
        raise ValueError(f"{wanted} is not DRAFT; refusing to load")
    return row


def run_core(core: ILISCore, cases: list[dict]) -> list[dict]:
    bot = core.chatbot()
    results = []
    for case in cases:
        response = bot.respond(case["input"])
        results.append({
            "id": case["id"], "input": case["input"],
            "answer": response.get("answer"),
            "metadata": response.get("metadata"),
            "semantic_result": response.get("semantic_result"),
            "reasoning_result": response.get("reasoning_result"),
        })
    core.close()
    return results


def main() -> int:
    print("=== TEST 2 A/B: FIVE-SAMPLE ISOLATED DATASET INJECTION ===")
    print(f"SOURCE_SHA={SOURCE_SHA}")
    loaded = {case["id"]: {} for case in CASES}
    proof_lines = []
    count = 0
    for case in CASES:
        for pillar, refs in case["records"].items():
            loaded[case["id"]][pillar] = []
            for rel, key, record_id in refs:
                row = load_one(rel, key, record_id)
                loaded[case["id"]][pillar].append(row)
                count += 1
                line = f"LOADER_OK case={case['id']} pillar={pillar} id={record_id} status=DRAFT"
                print(line)
                proof_lines.append(line)
        print(f"SAMPLE_BUNDLE_OK case={case['id']}")

    if len(loaded) != 5 or count != 12:
        raise RuntimeError(f"Expected 5 sample bundles / 12 records; got {len(loaded)} / {count}")

    # A/B condition 1: clean ILIS instance, no dataset adapter and no dataset facts.
    baseline = run_core(ILISCore(), CASES)

    # A/B condition 2: a separate ILIS instance with an allowlisted adapter.
    # The adapter receives only the twelve records loaded above.
    adapter = Sample5InjectionAdapter({
        case_id: {pillar: rows for pillar, rows in pillars.items()}
        for case_id, pillars in loaded.items()
    })
    injected_core = ILISCore()
    adapter.install(injected_core)
    injected = run_core(injected_core, CASES)

    comparison = []
    for before, after in zip(baseline, injected):
        bsem = before.get("semantic_result") or {}
        asem = after.get("semantic_result") or {}
        breason = before.get("reasoning_result") or {}
        areason = after.get("reasoning_result") or {}
        comparison.append({
            "id": before["id"], "input": before["input"],
            "test1_without_dataset": before,
            "test2_dataset_active": after,
            "semantic_status_changed": [bsem.get("status"), asem.get("status")],
            "semantic_confidence_changed": [
                (bsem.get("semantics") or {}).get("Confidence"),
                (asem.get("semantics") or {}).get("Confidence"),
            ],
            "reasoning_type_changed": [
                breason.get("reasoning_type"), areason.get("reasoning_type")
            ],
            "reasoning_confidence_changed": [
                breason.get("confidence_score"), areason.get("confidence_score")
            ],
        })

    report = {
        "title": "ILIS Test 1 vs Test 2 — isolated five-sample A/B",
        "source_branch": "ilis-v2-development",
        "source_sha": SOURCE_SHA,
        "experiment_branch": "test-playground-loader-sampel5",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "dataset_records_loaded": count,
        "dataset_status": "ALL DRAFT; READ-ONLY",
        "test1": {"mode": "BASELINE; NO DATASET ADAPTER", "results": baseline},
        "test2": {
            "mode": "ISOLATED SAMPLE5 ADAPTER ACTIVE",
            "adapter_scope": "EXACTLY FIVE ALLOWLISTED INPUTS",
            "draft_knowledge_policy": "fact-0048 inserted into in-memory KnowledgeEngine as hypothesis, never verified",
            "results": injected,
        },
        "comparison": comparison,
        "production_modified": False,
        "source_branches_modified": False,
        "jsonl_modified": False,
    }
    out = ROOT / "test-results"
    out.mkdir(exist_ok=True)
    (out / "test2-sampel5-ab-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    log = [
        "TEST 2 A/B — ISOLATED PLAYGROUND ONLY",
        f"SOURCE_SHA={SOURCE_SHA}",
        "EXPERIMENT_BRANCH=test-playground-loader-sampel5",
        "TEST1_DATASET_ADAPTER=DISABLED",
        "TEST2_DATASET_ADAPTER=ENABLED_FOR_EXACTLY_5_INPUTS",
        "LOADER_RESULT=PASS",
        "LOADED_CASES=5",
        f"LOADED_RECORDS={count}",
        *proof_lines,
        "DRAFT_FACT_POLICY=fact-0048 -> in-memory hypothesis only",
        "JSONL_MODIFIED=NO",
        "PRODUCTION_MODIFIED=NO",
        "MAIN_MODIFIED=NO",
        "ILIS_V2_DEVELOPMENT_MODIFIED=NO",
    ]
    (out / "test2-sampel5-ab-proof.log").write_text("\n".join(log) + "\n", encoding="utf-8")
    print("\n".join(log))
    print("A_B_REPORT=test-results/test2-sampel5-ab-report.json")
    print("PROOF_LOG=test-results/test2-sampel5-ab-proof.log")
    summary = __import__("os").environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as handle:
            handle.write("# Test 1 vs Test 2 — five-sample A/B\n\n")
            handle.write(f"- Loaded DRAFT records: {count}/12\n- Test 1: adapter disabled\n- Test 2: adapter enabled for exactly five allowlisted inputs\n- Draft fact-0048: in-memory hypothesis only\n- JSONL / production / main / development branch modified: no\n\n")
            for item in comparison:
                handle.write(f"## {item['id']}\n\n")
                handle.write(f"- Semantic status: {item['semantic_status_changed']}\n")
                handle.write(f"- Semantic confidence: {item['semantic_confidence_changed']}\n")
                handle.write(f"- Reasoning type: {item['reasoning_type_changed']}\n")
                handle.write(f"- Reasoning confidence: {item['reasoning_confidence_changed']}\n\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
