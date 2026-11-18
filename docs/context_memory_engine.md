# Context & Memory Engine V1

## Tujuan

Context Engine melacak sesi, pembicara, riwayat percakapan, kejadian, dan
referensi pengetahuan jangka panjang. Implementasi deterministik ini tidak
menggunakan LLM, model AI, machine learning, atau layanan eksternal.

## Tiga jenis memori

1. **Working Memory** menyimpan giliran percakapan untuk sesi aktif. Secara
   default, isinya dihapus ketika sesi ditutup.
2. **Long-Term Memory** bukan salinan database baru. Context Engine menunjuk
   langsung ke instance `KnowledgeEngine`, yang menyimpan konsep, relasi,
   fakta, dan provenance.
3. **Episodic Memory** menyimpan catatan kejadian per sesi. Catatan ini tetap
   tersedia setelah sesi ditutup secara default.

Semua penyimpanan pada V1 berbasis memori proses (in-memory), bukan database
persisten. Data hilang ketika proses aplikasi berhenti.

## Contoh integrasi lengkap

```python
from ilis.cognition import KnowledgeEngine
from ilis.cognition.context_engine import ContextEngine
from ilis.cognition.reasoning_engine import ReasoningEngine

knowledge = KnowledgeEngine()
context_engine = ContextEngine(knowledge)
reasoner = ReasoningEngine(knowledge)

session_id = context_engine.create_session(
    {"mode": "game", "scene": "village"}
)

context_engine.add_message(
    session_id, "game_system", "Api menyentuh rumah kayu."
)
context_engine.record_event(
    session_id,
    "Api menyentuh rumah kayu",
    event_type="environment_event",
    entities=["api", "rumah", "kayu"],
    attributes={"source": "api", "target": "rumah"},
)

session_context = context_engine.get_context(session_id)
result = context_engine.reason_from_context(
    session_id, "api", "rumah", reasoner
)
print(session_context)
print(result["inference"])

context_engine.close_session(session_id)
```

Dengan fakta inti Knowledge Engine:

- `api can_burn kayu` (verified)
- `rumah made_of kayu` (verified)

Reasoning Engine menghasilkan kesimpulan bahwa api yang menyambar rumah
berbahan kayu **berpotensi** menyebabkan rumah terbakar. Hasil ini merupakan
inferensi berbasis aturan, bukan kepastian. Event dari Episodic Memory
disertakan pada hasil `reason_from_context` sebagai konteks pemicu; event
tidak otomatis diubah menjadi fakta pengetahuan.

## API utama

- `create_session(metadata=None) -> session_id`: membuat sesi dengan UUID unik.
- `close_session(session_id, clear_working=True)`: menutup sesi dan menghapus
  Working Memory secara default.
- `add_message(session_id, speaker, text, metadata=None)`: menyimpan giliran
  percakapan dan identitas pembicara.
- `process_message(..., ingest_semantics=False)`: menyimpan pesan dan
  menjalankan adapter Semantic Engine. Ingest ke Knowledge Engine bersifat
  opt-in; jika diterima, klaim disimpan sebagai hypothesis oleh Knowledge Engine.
- `record_event(session_id, description, ...)`: menyimpan kejadian episodik.
- `get_context(session_id)`: mengembalikan ID/status sesi, peserta,
  conversation history, episodic memory, serta snapshot konsep/relasi/fakta
  beserta provenance dari Knowledge Engine.
- `reason_from_context(session_id, source, target, reasoning_engine=None)`:
  mengirim permintaan inferensi ke Reasoning Engine dan mengembalikan hasil
  bersama snapshot konteks sesi.

## Batasan V1

- MemoryStore in-memory dan tidak menyediakan persistence lintas restart.
- Working Memory tidak memiliki batas token atau kebijakan pemangkasan otomatis.
- Episodic Memory menyimpan deskripsi dan metadata yang diberikan pemanggil;
  belum mengekstrak event secara otomatis dari kalimat.
- Context Engine tidak menyimpulkan fakta dari event. Pengubahan pesan menjadi
  hipotesis hanya dilakukan bila `process_message(..., ingest_semantics=True)`
  dipilih secara eksplisit dan Semantic Engine menerima input.
- Reasoning Engine tetap memakai fakta Knowledge Engine sesuai aturan yang
  sudah ada; konteks episodik disertakan untuk transparansi, bukan dianggap
  sebagai premis faktual baru.

## Pengujian

```bash
python -m pip install -e ".[dev]"
python -m pytest
```
