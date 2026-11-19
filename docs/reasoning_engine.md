# Reasoning Engine V1

## Tujuan dan batasan

Reasoning Engine V1 adalah mesin inferensi deterministik berbasis aturan atas
triple dari `KnowledgeEngine`. Implementasi ini tidak menggunakan LLM, model
AI, layanan eksternal, machine learning, atau probabilistic model.

V1 hanya menyediakan satu aturan inferensi risiko kebakaran. Ini bukan mesin
penalaran umum, simulasi fisika, penentu kebenaran fakta, atau prediksi kejadian
dunia nyata.

## Integrasi

```python
from ilis.cognition import KnowledgeEngine
from ilis.cognition.reasoning_engine import ReasoningEngine

knowledge = KnowledgeEngine()  # memuat fakta inti V1
reasoner = ReasoningEngine(knowledge)

result = reasoner.infer_burn_risk("api", "rumah")
print(result)
```

Knowledge Engine menyediakan concept store, relation store, fact store, dan
provenance. Reasoning Engine membaca data tersebut tanpa mengubah Semantic
Engine maupun Knowledge Engine.

## Aturan inferensi V1

Aturan `material_burn_risk_v1` mencocokkan dua premis:

1. `source --can_burn--> material`
2. `target --made_of--> material`

Kedua triple harus menunjuk material yang sama. Jika cocok, sistem menghasilkan
kesimpulan bahwa sumber berpotensi menyebabkan target terbakar.

Contoh fakta inti:

- `api can_burn kayu` — verified
- `rumah made_of kayu` — verified

Kesimpulan: `api yang menyambar rumah berbahan kayu berpotensi menyebabkan
rumah terbakar`.

Kesimpulan ini bukan kepastian. Intensitas dan durasi api, kadar air,
perlakuan bahan, kondisi bangunan, dan faktor lingkungan dapat mengubah hasil
nyata. V1 tidak memiliki data untuk mengevaluasi faktor-faktor tersebut.

## Status penalaran

| reasoning_type | Makna |
| --- | --- |
| `verified_inference` | Semua premis tersedia, provenance cocok, dan berstatus verified. Kesimpulan tetap hasil aturan, bukan fakta terverifikasi langsung. |
| `hypothetical_inference` | Premis lengkap, tetapi setidaknya satu berstatus hypothesis. |
| `conflicting` | Ada konflik relevan, status fact/provenance tidak cocok, atau premis conflicting. Inferensi dihentikan. |
| `unknown` | Premis atau provenance tidak tersedia. Tidak menarik kesimpulan. |

Fakta verified adalah klaim sumber yang tersimpan sebagai verified.
Kesimpulan berbasis aturan adalah hasil penerapan aturan terhadap fakta-fakta
tersebut. Keduanya tidak boleh disamakan.

## Bentuk hasil

Setiap pemanggilan mengembalikan:

- `conclusion`: teks kesimpulan atau status data.
- `confidence_score`: skor heuristik 0.0–1.0, bukan probabilitas terkalibrasi.
- `evidence`: daftar ID fakta pendukung dari Knowledge Engine.
- `reasoning_type`: salah satu dari empat status di atas.
- `reasons`: langkah dan alasan aturan yang diterapkan.
- `uncertainty`: keterbatasan dan catatan ketidakpastian.

Skor V1 bersifat tetap dan transparan: 0.72 untuk dua premis verified,
0.48 jika ada premis hypothesis, dan 0.0 untuk conflicting/unknown.
Skor tersebut bukan peluang kebakaran di dunia nyata.

## Pemeriksaan konflik

Sebelum menerapkan aturan, Reasoning Engine memanggil
`KnowledgeEngine.detect_conflicts()`. Konflik yang menyentuh konsep query
atau relasi aturan V1 akan menghentikan inferensi. Konflik yang tidak terkait
dengan query tidak menghalangi inferensi tersebut.

Status fakta dan catatan provenance juga harus konsisten. Provenance yang
hilang menghasilkan `unknown`; ketidaksesuaian status menghasilkan
`conflicting`.

## Contoh hasil

Dengan dua fakta inti bawaan, hasil utamanya memiliki bentuk:

```python
{
    "conclusion": "api yang menyambar rumah berbahan kayu berpotensi menyebabkan rumah terbakar.",
    "confidence_score": 0.72,
    "evidence": ["fact_1", "fact_2"],
    "reasoning_type": "verified_inference",
    "reasons": [...],
    "uncertainty": "Ini adalah kesimpulan berbasis aturan, bukan kepastian. ..."
}
```

ID fakta mengikuti urutan penambahan fakta pada instance Knowledge Engine,
sehingga contoh ID di atas berlaku untuk instance baru dengan seed bawaan.

## Pengujian

Jalankan seluruh suite proyek:

```bash
python -m pip install -e ".[dev]"
python -m pytest
```

Tes mencakup inferensi verified, hipotesis, konflik relevan, data tidak
tersedia, provenance hilang/tidak konsisten, konflik yang tidak relevan,
dan validasi input.


## Perluasan Reasoning Engine V2

V2 menambahkan aturan deterministik `dragon_bell_fear_v2` dengan dua premis:

1. `naga --fears--> suara_keras`
2. `lonceng --produces--> suara_keras`

Jika kedua fakta tersedia, status fakta dan provenance konsisten, dan tidak ada
konflik, sistem menyimpulkan bahwa lonceng dapat menakuti naga. Kedua ID fakta
disimpan pada `evidence`. Skor 0.72 digunakan untuk premis verified dan 0.48
jika ada premis hypothesis; nilai ini skor heuristik, bukan probabilitas.

### Pertanyaan dari Semantic Engine

Gunakan `ReasoningEngine.infer_semantic(hasil_semantic)` untuk menerima hasil
`SemanticEngine.analyze()`. Untuk pertanyaan sederhana dengan pola subjek-
predikat-objek, relasi `membakar`/ `bakar` dipetakan ke fakta `can_burn`.
Contoh `Apakah api bisa membakar kayu?` dijawab dari fakta
`api --can_burn--> kayu`, beserta confidence score dan ID evidence.

Intent `question`, `command`, dan `assertion` dibedakan. Perintah dan
pernyataan tidak diperlakukan sebagai pertanyaan. Pertanyaan yang belum
tercakup, negasi yang belum memiliki aturan khusus, fakta hilang, dan
provenance yang tidak lengkap menghasilkan status `unknown`; konflik tetap
menghasilkan `conflicting`.

Nilai `reasoning_type` tambahan yang dapat dikembalikan oleh
`infer_semantic()` untuk input non-pertanyaan adalah:

- `command`: Semantic Engine memvalidasi Intent sebagai `command`; input dikenali
  sebagai perintah dan tidak dijalankan sebagai pertanyaan.
- `assertion`: Semantic Engine memvalidasi Intent sebagai `assertion`; input
  dikenali sebagai pernyataan dan tidak dijawab sebagai pertanyaan.

Kedua nilai ini hanya memperluas enum `reasoning_type` pada jalur
`infer_semantic()`. Bentuk hasil Reasoning tetap enam key yang sama. Konsumen
yang memakai enum tertutup harus menerima `command` dan `assertion` selain
status inferensi yang sudah didokumentasikan di atas.

### Kompatibilitas

Bentuk hasil tidak berubah: `conclusion`, `confidence_score`, `evidence`,
`reasoning_type`, `reasons`, dan `uncertainty`. Aturan risiko kebakaran
V1 dan API `infer_burn_risk()`/`infer()` tetap dipertahankan. Semantic Engine
dan Storage tidak dimodifikasi.


## Integrasi Concept Engine V3-C

Mulai V3-C, `ReasoningEngine.infer_semantic()` menggunakan Concept Engine sebagai
fallback terbatas setelah lookup fakta persis KnowledgeEngine lama tidak
menemukan kecocokan. Fakta persis dan konflik relevan dari KnowledgeEngine
tetap diproses dengan perilaku lama dan tidak boleh ditimpa oleh inferensi
konsep. Aturan khusus naga–lonceng juga tetap menggunakan jalur lama.

Urutan fallback:

1. Cari fakta persis berdasarkan subject, relation, dan object pada FactStore.
2. Jika ditemukan, validasi fakta/provenance dan kembalikan hasil lama.
3. Jika konflik relevan ditemukan, hentikan inferensi seperti sebelumnya.
4. Jika tidak ada fakta persis dan tidak ada konflik penghalang, jalankan
   InferenceEngine V3-B dengan ConceptStore statis V3-A.
5. Petakan status ke enam key Reasoning yang sudah ada.

Pemetaan status fallback:
- `KNOWN` → `concept_inference_known`, label Tahu Pasti, skor heuristik 0.72.
- `PARTIAL` → `concept_inference_partial`, label Tahu Sebagian, skor heuristik 0.48.
- `UNKNOWN` → `concept_inference_unknown`, label Tidak Tahu, skor 0.0.

Tidak ada key baru. Kontrak Semantic tetap 12 field dan kontrak Reasoning
tetap `conclusion`, `confidence_score`, `evidence`, `reasoning_type`,
`reasons`, dan `uncertainty`. Skor di atas merupakan pemetaan kompatibilitas,
bukan probabilitas terkalibrasi.

Implementasi dan contoh pengujian lebih lengkap tersedia di
`docs/v3_concept_engine_developer_guide.md`. Integrasi tidak mengubah
KnowledgeEngine, SQLite, SessionManager, Persona, atau Identity Intent.
