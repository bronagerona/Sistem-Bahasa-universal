"""Regression tests for the isolated BL-ILIS-002 negation interpreter."""
import json
from pathlib import Path
import pytest
from ilis.experimental.negation_mapping import LABELS, legacy_mapping, map_negation

ROOT = Path(__file__).resolve().parents[1]
DIALOGUE_DIR = ROOT / "data" / "indonesian" / "dialogues"

@pytest.mark.parametrize(("text","source","expected"), [
 ("Saya membaca buku.",False,"none"),
 ("Saya tidak membaca buku.",False,"negative"),
 ("Saya belum membaca buku.",False,"not_yet"),
 ("Dia bukan kakak saya.",False,"identity_negative"),
 ("Jangan kirim berkas itu.",False,"prohibitive"),
 ("Pengunjung dilarang merokok.",False,"prohibitive"),
 ("Kamu tidak boleh menghapus berkas.",False,"prohibitive"),
 ("Saya tidak tidak setuju.",False,"ambiguous"),
 ("Saya belum tentu setuju.",False,"ambiguous"),
 ('Kata "tidak" terdiri dari empat huruf.',False,"none"),
 ("Saya tidak pernah merokok.",False,"negative"),
 ("Saya belum pernah ke sana.",False,"not_yet"),
 ("Rumah itu tanpa listrik.",False,"negative"),
 ("Bukan besok, melainkan lusa.",False,"negative"),
 ("Aku belum paham.",False,"not_yet"),
 ("Tidak, belum.",False,"ambiguous"),
])
def test_six_label_mapping(text, source, expected):
 result=map_negation(text,source)
 assert result["mapping_label"]==expected
 assert result["mapping_label"] in LABELS
 assert 0.0 <= result["confidence"] <= 1.0

def test_true_boolean_without_linguistic_cue_is_ambiguous():
 result=map_negation("Saya membaca buku.",True)
 assert result["mapping_label"]=="ambiguous"
 assert result["annotation_discrepancy"] is True

def test_false_boolean_with_clear_cue_follows_text_and_records_discrepancy():
 result=map_negation("Saya belum membaca buku.",False)
 assert result["mapping_label"]=="not_yet"
 assert result["annotation_discrepancy"] is True

def test_context_is_used_only_for_elliptical_belum():
 result=map_negation("Belum.",False,context=["Apakah berkas sudah kamu kirim?"])
 assert result["mapping_label"]=="not_yet"
 assert result["annotation_discrepancy"] is True

def test_invalid_inputs_are_rejected():
 with pytest.raises(ValueError): map_negation("  ",False)
 with pytest.raises(TypeError): map_negation("Tidak.",1)
 with pytest.raises(TypeError): map_negation("Tidak.",False,context="bukan list")

def test_legacy_baseline_is_reproducible():
 assert legacy_mapping(False,"Saya belum makan.")=="none"
 assert legacy_mapping(True,"Jangan masuk.")=="negative"
 assert legacy_mapping(True,"Bukan kakak saya.")=="identity_negative"

def test_all_205_dialogue_annotations_are_read_only_and_classified():
 paths=sorted(DIALOGUE_DIR.glob("batch_*.jsonl"))
 assert len(paths)==18
 before={path:path.read_bytes() for path in paths}
 total=0
 dialogue_count=0
 turn_count=0
 labels={label:0 for label in sorted(LABELS)}
 discrepancies=[]
 baseline_changes=[]
 for path in paths:
  for line in before[path].decode("utf-8").splitlines():
   if not line.strip(): continue
   dialogue=json.loads(line)
   dialogue_count+=1
   prior_turns=[]
   for turn in dialogue["turns"]:
    turn_count+=1
    annotation=turn.get("semantic_annotation",{})
    if "Negation" not in annotation: continue
    total+=1
    source=annotation["Negation"]
    assert type(source) is bool
    utterance=turn["utterance"]
    result=map_negation(utterance,source,context=prior_turns)
    labels[result["mapping_label"]]+=1
    if legacy_mapping(source,utterance)!=result["mapping_label"]:
     baseline_changes.append((dialogue["dialogue_id"],turn["turn_id"]))
    if result["annotation_discrepancy"]:
     discrepancies.append((dialogue["dialogue_id"],turn["turn_id"]))
    prior_turns.append(utterance)
 assert dialogue_count==88
 assert turn_count==205
 assert total==205
 assert sum(labels.values())==205
 assert all(label in LABELS for label in labels)
 assert {path:path.read_bytes() for path in paths}==before
 print({"annotations":total,"labels":labels,"baseline_changes":len(baseline_changes),"discrepancies":len(discrepancies)})
