# ILIS Fase 2 — Concept & Knowledge Engine V1

## Batas kemampuan

Knowledge Engine V1 menggunakan penyimpanan in-memory dan aturan deterministik.
Tidak ada LLM, model AI, inferensi relasi, penalaran, pemeriksaan kebenaran
otomatis, atau pembelajaran mandiri. Konflik yang dideteksi hanya konflik
langsung: fakta dengan `subject` dan `relation` sama tetapi `object` berbeda.

Empat penyimpanan terpisah:

1. `concept_store`: konsep unik, misalnya `api`, `kayu`, `rumah`.
2. `relation_store`: nama relasi, misalnya `can_burn`, `made_of`.
3. `fact_store`: triple fakta beserta `subject`, `relation`, `object`,
   `status`, dan `source`.
4. `provenance`: catatan sumber dan status per ID fakta.

Status fakta yang tersedia: `verified`, `hypothesis`, dan `conflicting`.
Status `verified` adalah label yang diberikan secara eksplisit; sistem tidak
memverifikasi kebenaran fakta dengan sendirinya. Fakta yang ditambahkan tanpa
status eksplisit dimulai sebagai `hypothesis`.

## Data bawaan

Saat dibuat dengan `KnowledgeEngine()`, dua fakta inti dimuat:

| Subject | Relation | Object | Status | Source |
|---|---|---|---|---|
| api | can_burn | kayu | verified | core_knowledge |
| rumah | made_of | kayu | verified | core_knowledge |

Gunakan `KnowledgeEngine(seed_core_knowledge=False)` untuk penyimpanan kosong.

## Contoh penggunaan

```python
from ilis.cognition import KnowledgeEngine

knowledge = KnowledgeEngine()

knowledge.add_concept("besi")
knowledge.add_relation("made_of")
fact = knowledge.add_fact(
    "pedang", "made_of", "besi",
    status="hypothesis",
    source="user_observation",
)

print(knowledge.search_facts("besi"))
print(knowledge.get_provenance(fact["id"]))
print(knowledge.detect_conflicts())
```

## Mengirim hasil Semantic Engine

Hasil Semantic Engine dapat diteruskan langsung. Hanya hasil berstatus
`supported` dengan bentuk pernyataan positif S-R-O (subject-relation-object)
yang disimpan. Hasil tersebut selalu menjadi `hypothesis`, bukan `verified`,
karena confidence Semantic Engine mengukur keyakinan parsing, bukan kebenaran
fakta. Kalimat negatif, modal, tidak lengkap, atau unsupported tidak dipaksakan
menjadi fakta positif.

```python
from ilis.language.pipeline import analyze_semantics
from ilis.cognition import KnowledgeEngine

semantic_result = analyze_semantics("Saya makan nasi.")
knowledge = KnowledgeEngine()
ingested = knowledge.ingest_semantic_result(semantic_result)

print(ingested)
# Fact: saya --makan--> nasi; status=hypothesis; source=semantic_engine
```

Pemetaan ini menyimpan isi pernyataan sebagai klaim hipotetis. Ia tidak berarti
bahwa sistem menyimpulkan atau membuktikan bahwa peristiwa tersebut benar-benar
terjadi. Semantic Engine V1 juga memiliki cakupan pola bahasa yang terbatas;
jika hasilnya `low_confidence` atau `unsupported`, Knowledge Engine tidak
membuat fakta.

## Conflict handling

Dua fakta dianggap konflik jika `subject` dan `relation` sama, tetapi
`object` berbeda. Semua fakta dalam kelompok tersebut dan status provenance
masing-masing ditandai `conflicting`. Ini adalah deteksi perbedaan klaim
langsung, bukan resolusi konflik atau penentuan fakta mana yang benar.
