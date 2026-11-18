# Panduan Developer Multi-Turn ILIS V2.2

## Status

Multi-turn menggunakan SessionManager in-memory pada lapisan adapter. ILIS Core tidak menyimpan transcript. Semantic tetap 12 field, Reasoning tetap 6 key, dan SQLite Core tidak berubah.

## API ChatbotAdapter

```python
from ilis.interfaces import ILISCore, ChatbotAdapter, SessionManager

core = ILISCore()
sessions = SessionManager(max_turns=5)
chatbot = ChatbotAdapter(core, session_manager=sessions)

session_id = chatbot.create_session()
first = chatbot.respond("Apakah api bisa membakar kayu?", session_id)
second = chatbot.respond(
    "Lalu apakah api juga bisa membakar kertas?",
    session_id,
)
reset_result = chatbot.respond("reset percakapan", session_id)
```

Jika `session_id` tidak diberikan pada `respond`, adapter membuat sesi baru. Untuk integrasi yang sudah memiliki ID sendiri, adapter mengadopsi ID itu ke SessionManager. ID ini adalah ID percakapan adapter; aplikasi tetap bertanggung jawab mengelola autentikasi dan kepemilikannya.

## API SessionManager

- `create_session(session_id=None, metadata=None) -> str`
- `ensure_session(session_id, metadata=None) -> str`
- `get_session(session_id) -> ConversationSession | None`
- `add_turn(session_id, user_message, assistant_response, metadata=None)`
- `get_recent_turns(session_id) -> list[ConversationTurn]`
- `get_context_snapshot(session_id) -> dict`
- `reset_session(session_id) -> dict`
- `delete_session(session_id) -> bool`
- `close_session(session_id) -> None`

Riwayat dibatasi lima pasangan turn lengkap secara default. Pesan terbaru belum dimasukkan ke snapshot sebelum pemrosesan; pasangan baru disimpan setelah jawaban akhir tersedia.

## API Core

`ILISCore.analyze_text(text, context_snapshot=None)` menerima snapshot tambahan dan menghasilkan Semantic result dari teks saat ini. Snapshot tidak dimasukkan ke payload Semantic dan tidak disimpan oleh Core. Adapter meneruskan snapshot yang sama ke LanguageGenerator melalui parameter `context`.

## GameEngineAdapter

`GameEngineAdapter.create_session(metadata=None)` membuat ID percakapan adapter dan scope episodic internal yang terpisah. `handle_event(event, session_id=None, ..., conversation_session_id=None, context_snapshot=None)` menerima ID percakapan opsional. Untuk kompatibilitas, ID Core lama tetap diterima sebagai scope episodic; `conversation_session_id` dapat memisahkan transcript dari scope episode. Jangan menganggap Episodic Memory sebagai transcript dialog.

## Reset

Perintah persis `reset percakapan` atau `hapus riwayat` menghapus turn percakapan pada sesi aktif, mempertahankan session ID, dan tidak menghapus Knowledge, provenance, atau Episodic Memory.

## Batasan

- In-memory history hilang ketika proses berhenti.
- Persistent conversation storage belum diimplementasikan.
- SessionManager tidak menyediakan autentikasi/tenant ownership; host harus memvalidasi pemanggil sebelum memakai session ID.
- Context snapshot adalah konteks terbatas, bukan sumber fakta. Riwayat tidak boleh dianggap evidence terverifikasi.
- Tidak ada LLM atau panggilan model AI.
