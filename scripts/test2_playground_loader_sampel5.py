"""Isolated five-sample dataset loader and Playground evaluator."""
from __future__ import annotations
import json, os
from pathlib import Path
from datetime import datetime, timezone
from ilis.interfaces import ILISCore
from ilis.language.pipeline import analyze_semantics

ROOT = Path(__file__).resolve().parents[1]
SOURCE_SHA = "80475e0f5e7c78c92a84109522777946dd9fb797"
CASES = [
 {"id":"T2-01","label":"Negasi temporal: belum","input":"Aku belum membaca buku itu.","records":{"lexicon":[("lexicon/batch_010.jsonl","entry_id","lex-0048")],"sentence_patterns":[("sentence_patterns/batch_010.jsonl","pattern_id","pat-0048")],"dialogues":[("dialogues/batch_010.jsonl","dialogue_id","dlg-0046")]}},
 {"id":"T2-02","label":"Penyangkalan identitas: bukan","input":"Orang yang menelepon tadi bukan kakakku.","records":{"lexicon":[("lexicon/batch_010.jsonl","entry_id","lex-0049")],"sentence_patterns":[("sentence_patterns/batch_010.jsonl","pattern_id","pat-0049")],"dialogues":[("dialogues/batch_010.jsonl","dialogue_id","dlg-0047")]}},
 {"id":"T2-03","label":"Larangan: jangan","input":"Jangan kirim berkas itu dulu.","records":{"lexicon":[("lexicon/batch_010.jsonl","entry_id","lex-0051")],"sentence_patterns":[("sentence_patterns/batch_010.jsonl","pattern_id","pat-0051")],"dialogues":[("dialogues/batch_010.jsonl","dialogue_id","dlg-0049")]}},
 {"id":"T2-04","label":"Polisemi awalan ter-","input":"Ia terjatuh saat menuruni tangga.","records":{"lexicon":[("lexicon/batch_018.jsonl","entry_id","lex-0091")],"sentence_patterns":[("sentence_patterns/batch_018.jsonl","pattern_id","pat-0091")]}},
 {"id":"T2-05","label":"Fakta pengetahuan: satuan astronomi","input":"Berapa meter nilai satu satuan astronomi (au) menurut definisi IAU?","records":{"knowledge":[("knowledge/batch_010.jsonl","fact_id","fact-0048")]}},
]

def load_one(rel, key, wanted):
    path=ROOT/"data"/"indonesian"/rel
    found=[]
    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                row=json.loads(line)
                if row.get(key)==wanted: found.append(row)
    if len(found)!=1: raise ValueError(f"Expected one {wanted} in {rel}, got {len(found)}")
    row=found[0]
    if not (row.get("verification_status")=="draft" or row.get("annotation_status")=="draft"):
        raise ValueError(f"{wanted} is not DRAFT; refusing to load")
    return row

def main():
    report={"title":"TEST 2 - PLAYGROUND ONLY (NOT PRODUCTION)","source_branch":"ilis-v2-development","source_sha":SOURCE_SHA,"harness_branch":"test-playground-loader-sampel5","created_at":datetime.now(timezone.utc).isoformat(),"dataset_integration":"HARNESS ONLY; NOT INJECTED INTO ILIS RUNTIME","cases":[]}
    logs=[]
    print("=== TEST 2 DATASET LOADER: PLAYGROUND ONLY / NOT PRODUCTION ===")
    print(f"SOURCE_SHA={SOURCE_SHA}")
    print("MODE=READ_ONLY_SELECTED_DRAFT_RECORDS")
    print("RUNTIME_INJECTION=DISABLED")
    total=0
    for case in CASES:
        loaded={}
        for pillar, refs in case["records"].items():
            loaded[pillar]=[]
            for rel,key,rid in refs:
                row=load_one(rel,key,rid); loaded[pillar].append(row); total+=1
                line=f"LOADER_OK case={case['id']} pillar={pillar} id={rid} status=DRAFT file=data/indonesian/{rel}"
                print(line); logs.append(line)
        print(f"SAMPLE_LOADED case={case['id']} label={case['label']} record_count={sum(map(len,loaded.values()))}")
        sem=analyze_semantics(case["input"])
        core=ILISCore()
        sid=core.create_session(metadata={"source":"test_playground_loader_sampel5","dataset_mode":"harness_only"})
        try: result=core.chatbot().respond(case["input"],sid)
        finally: core.close()
        item={"id":case["id"],"label":case["label"],"input":case["input"],"loaded_record_ids":{p:[r.get("entry_id") or r.get("pattern_id") or r.get("dialogue_id") or r.get("fact_id") for r in rows] for p,rows in loaded.items()},"all_loaded_records_draft":True,"semantic_12_field_output":sem,"chatbot_answer":result.get("answer"),"chatbot_metadata":result.get("metadata"),"reasoning_6_keys":"NOT EXPOSED AS COMPLETE SIX-KEY OBJECT","dataset_runtime_effect":"NOT TESTED; LOADER IS OUTSIDE ILIS RUNTIME"}
        report["cases"].append(item)
        print(f"ILIS_ANSWER case={case['id']}: {item['chatbot_answer']}")
        print("SEMANTIC_OUTPUT="+json.dumps(sem,ensure_ascii=False))
        print("REASONING_6_KEYS=NOT_FULLY_EXPOSED")
        print("RUNTIME_DATASET_INJECTION=NO")
    report.update({"loaded_case_count":len(report["cases"]),"loaded_record_count":total,"loader_result":"PASS" if len(report["cases"])==5 else "FAIL","dataset_records_remain_draft":True,"production_modified":False})
    out=ROOT/"test-results"; out.mkdir(exist_ok=True)
    rp=out/"test2-sampel5-report.json"; rp.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    lp=out/"test2-loader-proof.log"
    lp.write_text("\n".join(["TEST 2 - PLAYGROUND ONLY (NOT PRODUCTION)",f"SOURCE_SHA={SOURCE_SHA}",f"LOADER_RESULT={report['loader_result']}",f"LOADED_CASES={len(report['cases'])}",f"LOADED_RECORDS={total}",*logs,"DATASET_STATUS=DRAFT","RUNTIME_INJECTION=DISABLED","PRODUCTION_MODIFIED=NO"])+"\n",encoding="utf-8")
    print(f"LOADER_RESULT={report['loader_result']}")
    print(f"LOADED_CASES={len(report['cases'])}")
    print(f"LOADED_RECORDS={total}")
    print(f"PROOF_LOG={lp}")
    print(f"REPORT_JSON={rp}")
    summary=os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary,"a",encoding="utf-8") as f:
            f.write("# TEST 2 — PLAYGROUND ONLY (NOT PRODUCTION)\n\n")
            f.write(f"- Source SHA: {SOURCE_SHA}\n- Loaded cases: {len(report['cases'])}/5\n- Loaded DRAFT records: {total}\n- Dataset injected into ILIS runtime: No\n- Production modified: No\n\n")
            for x in report["cases"]: f.write(f"## {x['id']} — {x['label']}\n\nInput: {x['input']}\n\nAnswer: {x['chatbot_answer']}\n\n")
    return 0 if report["loader_result"]=="PASS" else 1

if __name__=="__main__": raise SystemExit(main())
