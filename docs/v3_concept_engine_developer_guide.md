# ILIS V3 Concept Engine Developer Guide

**Status:** Implementasi V3-C — integrasi fallback pada ReasoningEngine.  
**Basis:** V2.2 + V3-A Static ConceptStore + V3-B Inference Rules.  
**Prinsip:** Deterministik, tanpa LLM, kompatibel dengan kontrak Semantic dan Reasoning yang ada.

## 1. Tujuan dan batas integrasi

V3-C menghubungkan \`InferenceEngine\` V3-B ke \`ReasoningEngine\` yang sudah dipakai \`ILISCore\`. Integrasi dilakukan pada jalur \`ReasoningEngine.infer_semantic()\`; \`ILISCore\` tetap membangun \`ReasoningEngine\` seperti sebelumnya.

Perubahan ini tidak:
- menambahkan atau mengubah 12 field Semantic;
- menambahkan atau mengubah enam key Reasoning;
- mengubah KnowledgeEngine, FactStore, ProvenanceStore, atau SQLite;
- mengubah SessionManager, transcript, context snapshot, Persona, atau Identity Intent;
- memindahkan penyimpanan konsep ke database.

## 2. Urutan eksekusi wajib

Urutan keputusan untuk pertanyaan semantik:

1. Validasi payload Semantic melalui \`validate_output\`.
2. Pertahankan penanganan intent, negasi, konteks follow-up, dan aturan khusus naga–lonceng yang sudah ada.
3. Cari fakta persis pada \`KnowledgeEngine.fact_store\` berdasarkan subject, relation, dan object.
4. Periksa konflik relasi yang relevan menggunakan mekanisme KnowledgeEngine lama.
5. Jika fakta persis ditemukan, gunakan hasil dan validasi/provenance lama. Concept Engine tidak boleh menimpa fakta tersebut.
6. Jika konflik relevan ditemukan, hentikan inferensi dengan hasil \`conflicting\` seperti perilaku lama.
7. Hanya jika tidak ada fakta persis dan tidak ada konflik yang menghalangi, jalankan fallback Concept Engine.
8. Pada tahap V3-C, fallback diaktifkan untuk relasi \`can_burn\` yang memiliki aturan sifat \`mudah_terbakar\` di Concept Engine.

\`\`\`text
Semantic (12 field)
       |
       v
ReasoningEngine.infer_semantic
       |
       v
KnowledgeEngine: exact subject + relation + object
       |
       +-- exact match --> validasi fakta/provenance lama --> hasil lama
       |
       +-- relevant conflict --> conflicting (jalur lama)
       |
       +-- no exact match, no blocking conflict
                         |
                         v
                InferenceEngine V3-B
                         |
                         v
                ConceptStore V3-A
                         |
                         v
              map to existing six keys
\`\`\`

Jangan memindahkan fallback ke depan lookup KnowledgeEngine. Jangan memakai transcript atau context snapshot sebagai bukti faktual.

## 3. Konstruksi dan injeksi

Secara default, \`ReasoningEngine\` membuat \`ConceptStore()\` statis dan \`InferenceEngine\` yang membacanya. Karena \`ILISCore\` sudah menginisialisasi \`ReasoningEngine\`, integrasi tersedia melalui Core tanpa mengubah alur konstruksi Core.

Untuk pengujian atau host yang memerlukan fixture statis khusus, \`ReasoningEngine\` menerima salah satu:
- \`concept_store=ConceptStore(...)\`; atau
- \`inference_engine=InferenceEngine(concept_store)\`.

Keduanya tidak boleh diberikan sekaligus. KnowledgeEngine tetap wajib diberikan dan tetap menjadi sumber fakta dengan prioritas pertama.

Contoh:

\`\`\`python
from ilis.cognition import KnowledgeEngine
from ilis.cognition.reasoning_engine import ReasoningEngine

# Tanpa seed agar fakta persis api -> kertas tidak ditemukan.
knowledge = KnowledgeEngine(seed_core_knowledge=False)
reasoning = ReasoningEngine(knowledge)
result = reasoning.infer_semantic(semantic_result)
\`\`\`

## 4. Pemetaan status V3 ke kontrak Reasoning

Output tetap tepat enam key:

| Status Concept Engine | conclusion | confidence_score* | reasoning_type |
|---|---|---:|---|
| \`KNOWN\` | Diawali label \`Tahu Pasti\` | 0.72 | \`concept_inference_known\` |
| \`PARTIAL\` | Diawali label \`Tahu Sebagian\` | 0.48 | \`concept_inference_partial\` |
| \`UNKNOWN\` | Diawali label \`Tidak Tahu\` | 0.0 | \`concept_inference_unknown\` |

\`evidence\` berisi ID konsep, sifat, relasi, dan provenance yang dikembalikan InferenceEngine. \`reasons\` mencatat bahwa fallback dijalankan setelah exact lookup tidak menemukan fakta serta alasan aturan. \`uncertainty\` memuat keterbatasan atau data yang belum tersedia.

*Angka tersebut adalah pemetaan heuristik kompatibilitas V3-C, bukan probabilitas terkalibrasi dan bukan key baru. Evaluasi kalibrasi angka memerlukan tahap terpisah.*

Key yang dipertahankan:
- \`conclusion\`
- \`confidence_score\`
- \`evidence\`
- \`reasoning_type\`
- \`reasons\`
- \`uncertainty\`

## 5. Skenario integrasi

### Fakta persis lama tersedia

Dengan seed KnowledgeEngine normal, fakta \`api --can_burn--> kertas\` tersedia. Hasil lama harus digunakan (misalnya evidence \`fact_3\` dan \`reasoning_type=verified_inference\`). Fallback tidak dijalankan.

### Fallback PARTIAL

Gunakan \`KnowledgeEngine(seed_core_knowledge=False)\` sehingga fakta persis tidak tersedia. ConceptStore V3-A memiliki data kandidat api/kertas tetapi provenance dan kondisi seed belum terverifikasi. Hasil yang diharapkan adalah \`PARTIAL\`, bukan klaim pasti.

### Fallback UNKNOWN

Dengan KnowledgeEngine tanpa seed dan objek yang tidak dikenal ConceptStore, tidak ada data konsep relevan yang cukup. Hasil yang diharapkan \`UNKNOWN\`.

### Fallback KNOWN

Untuk menguji pemetaan status KNOWN, gunakan fixture ConceptStore dengan konsep, sifat, relasi eksplisit, semua prasyarat, dan provenance berstatus verified. Fixture tidak mengubah seed produksi.

## 6. Batas kompatibilitas

- Semantic tetap 12 field.
- Reasoning tetap enam key.
- Exact fact dan konflik KnowledgeEngine tetap didahulukan.
- Aturan naga–lonceng tetap melalui jalur khusus lama.
- Snapshot multi-turn hanya membantu interpretasi Actor/Predicate; tidak menjadi evidence.
- Persona dan Identity Intent tetap pada adapter dan tidak dipindah ke ReasoningEngine.
- SQLite dan skema penyimpanan tidak berubah.
- Tidak ada LLM, jaringan, atau sumber fakta eksternal.

## 7. Pengujian

Jalankan:

\`\`\`bash
python -m pip install -e ".[dev]"
python -m pytest
\`\`\`

Tes V3-C meliputi:
- fallback \`api -> kertas\` ketika exact fact lama sengaja tidak tersedia;
- exact fact lama menang dan fallback tidak menggantikannya;
- pemetaan PARTIAL, UNKNOWN, dan KNOWN;
- integrasi melalui ReasoningEngine yang dibuat ILISCore;
- kontrak Semantic 12 field dan Reasoning enam key.

Suite regresi penuh tetap mencakup KnowledgeEngine, Reasoning lama, Semantic, adapter, persona, Identity Intent, dan Multi-turn V2.2.
