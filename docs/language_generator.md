# Language Generator V1

## Tujuan

Language Generator V1 mengubah makna dan hasil inferensi menjadi kalimat Bahasa Indonesia yang disusun secara dinamis. Implementasi menggunakan komposisi semantik, aturan sintaksis sederhana, pilihan leksikal berdasarkan register, dan metadata ketidakpastian. Tidak menggunakan LLM, model AI, embedding, atau layanan eksternal.

## Input

- Objek hasil ReasoningEngine: `conclusion`, `reasoning_type`, `confidence_score`, `evidence`, dan `uncertainty`.
- Register eksplisit (`formal`, `informal`, `slang`) atau metadata `semantics.Register` dari Semantic Engine.
- Snapshot sesi ContextEngine, termasuk metadata sesi. Register eksplisit memiliki prioritas tertinggi; berikutnya metadata Semantic Engine, metadata sesi, lalu default formal.
- Opsional: representasi makna terstruktur melalui `reasoning_result["meaning"]`.

## API

```python
from ilis.cognition import KnowledgeEngine
from ilis.cognition.context_engine import ContextEngine
from ilis.cognition.reasoning_engine import ReasoningEngine
from ilis.generation import LanguageGenerator

knowledge = KnowledgeEngine()
context = ContextEngine(knowledge)
session_id = context.create_session(metadata={"register": "informal"})
context.add_message(session_id, "player", "Rumah itu dekat pohon.")

reasoning = ReasoningEngine(knowledge)
inference = reasoning.infer_burn_risk("api", "rumah")

generator = LanguageGenerator(context)
informal = generator.generate(inference, session_id=session_id)
formal = generator.generate(inference, register="formal")

print(informal["text"])
print(formal["text"])
```

Contoh keluaran:
- Informal: "Kayaknya rumah bisa kebakaran karena berbahan kayu dan terkena api lho."
- Formal: "Ada kemungkinan rumah akan terbakar karena terbuat dari kayu dan terpapar api."

## Penyusunan dinamis

Untuk aturan burn-risk V1, generator mengekstrak sumber, target, dan material dari kesimpulan ReasoningEngine (atau menerima `meaning` terstruktur). Komponen tersebut dirangkai dengan konstruksi sintaksis dan pilihan leksikal register. Objek, material, dan sumber yang berbeda menghasilkan kalimat berbeda; generator tidak hanya memilih satu jawaban utuh dari daftar template.

Register:
- `formal`: diksi baku dan konstruksi eksplisit.
- `informal`: diksi percakapan sehari-hari.
- `slang`: diksi santai/gaul terbatas.

## Ketidakpastian dan keselamatan makna

- Kesimpulan `verified_inference` dari ReasoningEngine tetap menyatakan kemungkinan, bukan kepastian.
- Kesimpulan `hypothetical_inference` juga mempertahankan bahasa kemungkinan.
- `unknown` diubah menjadi kalimat kekurangan informasi, bukan klaim positif.
- `conflicting` diubah menjadi pemberitahuan adanya informasi bertentangan, bukan memilih salah satu.
- Confidence dan evidence tetap dikembalikan untuk aplikasi pemanggil; confidence tidak ditafsirkan sebagai probabilitas terkalibrasi.

## Integrasi Semantic + Context + Reasoning

`LanguageGenerator.generate()` menerima hasil reasoning, semantic_result (opsional) untuk register, dan context snapshot atau session_id untuk metadata sesi. Generator hanya membaca snapshot dan tidak mengubah engine lama.

## Batasan V1

- Parser kesimpulan otomatis baru mengenali pola burn-risk dari ReasoningEngine V1; domain lain sebaiknya mengirim `meaning` terstruktur.
- Bahasa Indonesia dan variasi register masih memakai aturan eksplisit, belum mencakup seluruh variasi/typo.
- Context dipakai untuk metadata register dan referen eksplisit; generator tidak menyimpulkan fakta baru dari riwayat chat.
- Tidak ada LLM/model AI, pelatihan otomatis, atau layanan eksternal.

## Pengujian

```bash
python -m pip install -e ".[dev]"
python -m pytest
```

## Perluasan Language Generator V2

V2 mempertahankan kontrak hasil V1 dan menambahkan komposisi berdasarkan Intent Semantic Engine:

- **Pertanyaan (question)**: hasil reasoning didukung fakta dapat dirender sebagai jawaban. Contoh “Apakah api bisa membakar kayu?” menjadi “Ya, kemungkinan api bisa membakar kayu.” Jika reasoning berstatus unknown atau conflicting, generator tetap menghasilkan ketidakpastian/konflik, bukan jawaban positif.
- **Perintah (command)**: dirender sebagai respons pelaksanaan, bukan jawaban faktual. Contoh “Bunyikan lonceng” menjadi “Baik, lonceng akan dibunyikan.”
- **Naga + lonceng**: hasil aturan Reasoning V2 dirangkai dalam register formal, informal, atau slang dengan pilihan diksi berbeda.

| Register | Keluaran |
|---|---|
| Formal | Ada kemungkinan bahwa lonceng dapat menakuti naga karena menghasilkan suara keras yang ditakuti naga. |
| Informal | Kayaknya lonceng bisa bikin naga takut karena bunyinya keras lho. |
| Slang | Kayaknya lonceng bisa bikin naga ciut gara-gara suaranya kenceng deh. |

Ketidakpastian mempertimbangkan tipe inferensi, confidence score, dan catatan uncertainty. Penanda seperti “kemungkinan” atau “kayaknya” dipertahankan. Confidence tidak dianggap probabilitas terkalibrasi.

API generate() dan seluruh kunci hasil V1 tetap sama: text, register, meaning, reasoning_type, confidence_score, uncertainty_preserved, evidence, session_id. Semantic Engine, Reasoning Engine, dan Storage tidak dimodifikasi.