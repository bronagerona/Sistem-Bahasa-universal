# Learning Engine V1

## Tujuan dan batasan

Learning Engine V1 adalah komponen pembelajaran deterministik berbasis aturan. Tidak ada LLM, model AI, embedding model, atau layanan AI eksternal. Komponen ini mengubah masukan yang dapat direpresentasikan menjadi **hipotesis**, membandingkannya dengan KnowledgeEngine, dan mencatat konflik untuk ditinjau.

Learning Engine tidak membuktikan kebenaran. Status `verified` hanya dapat diberikan melalui pemanggilan eksplisit `confirm_hypothesis(..., confirmed_by=...)`, dan hipotesis yang sedang konflik tidak dapat diverifikasi sebelum konflik ditinjau.

## Alur

1. Terima hasil Semantic Engine melalui ContextEngine, atau episode dari Episodic Memory.
2. Bentuk kandidat hipotesis dengan sumber dan referensi asal.
3. Bandingkan subject + relation dengan fakta yang sudah ada.
4. Jika object berbeda, tandai konflik dan minta konfirmasi; KnowledgeEngine mengelola status konflik dan provenance.
5. Jika tidak konflik, simpan melalui KnowledgeEngine dengan status `hypothesis`.
6. Tidak ada promosi otomatis ke `verified`.

Laporan berisi `hipotesis_baru`, `konflik_ditemukan`, dan `aman`; `laporan` bernilai `hipotesis_baru`, `conflicting`, atau `tidak_dipelajari`.

## API

- `LearningEngine(knowledge_engine, context_engine=None, hypothesis_tracker=None)`
- `learn_from_semantics(semantic_result, source="semantic_engine")`
- `learn_from_context_message(session_id, speaker, text, source="context_semantic")`
- `learn_from_episode(session_id, episode_id, source="episodic_memory")`
- `get_hypotheses()`
- `confirm_hypothesis(hypothesis_id, confirmed_by=...)`

Untuk episode, atribut terstruktur `subject`, `relation`, dan `object` lebih disarankan. Jika tidak tersedia, episode dicatat sebagai relasi pengalaman (`experienced_event_<event_type>`) dengan deskripsi kejadian sebagai objek. Ini adalah catatan pengalaman, bukan klaim fakta terverifikasi.

Semantic Engine V1 belum mengenali pola kalimat "Besi tidak bisa dibakar". Karena itu `learn_from_context_message` menyediakan fallback aturan yang sangat terbatas untuk pola `<benda> [tidak] [bisa] dibakar`. Fallback hanya memetakan `can_burn=true/false`; ini bukan parser bahasa umum dan tidak mengubah Semantic Engine.

## Contoh integrasi Context + Knowledge

```python
from ilis.cognition import KnowledgeEngine
from ilis.cognition.context_engine import ContextEngine
from ilis.learning import LearningEngine

knowledge = KnowledgeEngine(seed_core_knowledge=False)
context = ContextEngine(knowledge)
learning = LearningEngine(knowledge, context)

session_id = context.create_session()
result = learning.learn_from_context_message(
    session_id, "player", "Besi tidak bisa dibakar"
)
print(result["laporan"])              # hipotesis_baru
print(result["fact"]["status"])       # hypothesis

# Peristiwa dari Episodic Memory:
episode = context.record_event(
    session_id,
    "Pintu terbuka setelah tuas ditarik",
    event_type="game_event",
    entities=["pintu", "tuas"],
    attributes={
        "subject": "pintu",
        "relation": "opened_after",
        "object": "tuas_ditarik",
    },
)
episode_result = learning.learn_from_episode(session_id, episode["episode_id"])

# Hanya perintah konfirmasi eksplisit yang dapat mempromosikan hipotesis:
# learning.confirm_hypothesis(result["hipotesis_baru"]["hypothesis_id"], confirmed_by="admin")
```

## Konflik dan provenance

KnowledgeEngine tetap menjadi pemilik FactStore dan ProvenanceStore. Saat kandidat bertentangan, KnowledgeEngine menandai fakta-fakta dalam kelompok subject+relation sebagai `conflicting`; LearningEngine tidak memilih pihak yang benar atau menghapus fakta. Hasil konflik harus ditinjau secara eksplisit. Konflik tidak dapat langsung dipromosikan menjadi verified.

## Pengujian

Jalankan:

```bash
python -m pip install -e ".[dev]"
python -m pytest
```

## Batasan V1

- Penyimpanan mengikuti KnowledgeEngine yang saat ini in-memory; restart proses menghilangkan data.
- Semantic ingestion hanya menerima hasil `supported` yang berupa assertion positif dengan subject, relation, dan object lengkap.
- Fallback bahasa hanya mencakup pola baku pembakaran yang didokumentasikan.
- Episodic memory tidak ditafsirkan secara bebas; gunakan atribut subject/relation/object agar pembentukan hipotesis terstruktur.
- Tidak ada verifikasi fakta otomatis, resolusi konflik otomatis, generalisasi bebas, atau LLM/model AI.
