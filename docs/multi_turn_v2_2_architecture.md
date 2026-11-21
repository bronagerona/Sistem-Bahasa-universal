# Arsitektur Multi-Turn Percakapan ILIS V2.2

**Status:** Dokumen desain; belum ada implementasi kode.  
**Basis desain:** `ilis-v2-development` (V2.1 Persona, Identity Intent Tahap E–G, instruksi register PR #3, dan SQLite).  
**Target:** Menambahkan konteks percakapan lintas giliran tanpa LLM dan tanpa mengubah kontrak Semantic/Reasoning.  
**Batas perubahan untuk tugas ini:** Hanya dokumen ini. Tidak ada file kode yang diubah.

---

## 1. Tujuan dan prinsip yang mengikat

Multi-turn memungkinkan ILIS menghubungkan pesan terbaru dengan percakapan sebelumnya. Contoh:

1. Pengguna: “Apakah api bisa membakar kayu?”
2. ILIS: menjawab berdasarkan fakta dan aturan yang tersedia.
3. Pengguna: “Lalu apakah api juga bisa membakar kertas?”
4. ILIS: memahami bahwa pertanyaan kedua merupakan lanjutan topik sebelumnya, sambil tetap menilai fakta untuk objek “kertas” secara mandiri.

Prinsip desain:

1. **Adapter owns conversation state.** `ChatbotAdapter` dan `GameEngineAdapter` memiliki atau menerima `ConversationSessionStore`; hanya lapisan ini yang menyimpan pesan pengguna/pemain dan jawaban chatbot/NPC.
2. **Core stateless terhadap riwayat dialog.** ILIS Core menerima snapshot konteks per permintaan, menggunakannya selama pemrosesan, lalu membuang referensi tersebut. Core tidak membuat, menyimpan, memperbarui, atau mencari riwayat percakapan.
3. **Semantic tetap 12 field.** Konteks tidak disisipkan ke objek `semantics`, wrapper Semantic, atau payload input Semantic. Kontrak tetap seperti `docs/semantic_contract.md`.
4. **Reasoning tetap 6 key.** Konteks tidak menambah key ke hasil Reasoning: `conclusion`, `confidence_score`, `evidence`, `reasoning_type`, `reasons`, `uncertainty`.
5. **Penyimpanan terpisah.** SQLite Core yang sudah ada dipakai untuk Knowledge/fakta, provenance, dan Episodic Memory. Riwayat dialog multi-turn memiliki store dan lifecycle terpisah. Sesi percakapan persisten, bila dipilih, menggunakan backend/store terpisah dan tidak menambah tabel percakapan ke provider SQLite Core yang ada.
6. **Deterministik, tanpa LLM.** Pemilihan konteks, reset, batas riwayat, dan resolusi rujukan menggunakan aturan eksplisit.
7. **Kompatibilitas V2.1.** Persona Mode A/B/C, Identity Intent Tahap E–G, dan instruksi sopan/santai PR #3 tetap menjadi tanggung jawab dan urutan prioritas yang telah ada; multi-turn tidak boleh mengambil alih rute khusus tersebut.

### 1.1 Klarifikasi kondisi kode saat ini

Pada basis kode yang diperiksa:

- `ChatbotAdapter.respond()` memanggil `core.context_engine.process_message()`, sehingga pesan chat masuk ke Working Memory milik `ContextEngine`.
- `ILISCore` memiliki `ContextEngine`; `ContextEngine` mengelola session, Working Memory, dan Episodic Memory.
- `MemoryStore` saat ini menyimpan pesan Working Memory di memori proses. Jika provider SQLite dipakai, metadata session dan Episodic Memory dipersistenkan; pesan Working Memory tidak dipulihkan setelah restart.
- `GameEngineAdapter` merekam event ke Episodic Memory dan mengambil konteks dari `ContextEngine`.
- `LanguageGenerator.generate()` sudah menerima parameter `context` terpisah, tetapi parameter `session_id` akan meminta generator mengambil konteks langsung dari `ContextEngine`.

Karena itu, implementasi V2.2 kelak perlu memutus ketergantungan riwayat dialog dari `ContextEngine`/Core secara bertahap. Jangan menganggap pemindahan riwayat sudah selesai hanya dengan menambah parameter konteks. Fungsi episodic game dan penyimpanan pengetahuan yang sudah ada tetap harus dipertahankan. `sessions` yang ada di provider lama adalah metadata session internal untuk fitur Context/Episodic; tabel tersebut bukan penyimpanan transcript multi-turn yang diusulkan.

---

## 2. Arsitektur dan diagram alur penuh

### 2.1 Alur normal satu giliran

```text
Pengguna / Pemain
       |
       v
ChatbotAdapter / GameEngineAdapter
       |
       +--> validasi session_id dan status sesi
       |
       +--> deteksi perintah reset (sebelum memanggil Core)
       |
       +--> ConversationSessionStore.get_recent_turns(session_id)
       |        |
       |        +--> maksimal 5 pasangan giliran lengkap
       |
       +--> bentuk ConversationContext snapshot (immutable)
       |
       v
ILISCore.process_text(text, conversation_context=...)
       |
       +--> Context Resolver deterministik (bila diperlukan)
       |       - membaca snapshot saja
       |       - mengenali kesinambungan/rujukan yang didukung
       |       - tidak menulis balik ke session store
       |
       +--> Semantic Engine (input teks saat ini; kontrak tetap)
       |
       +--> Reasoning Engine (aturan + Knowledge; konteks hanya input tambahan)
       |
       +--> Language Generator (menerima konteks sebagai parameter terpisah)
       |
       v
Hasil Core (Semantic 12 field + Reasoning 6 key tetap utuh)
       |
       v
Adapter menerapkan Persona / Identity / register sesuai aturan V2.1
       |
       +--> hasil akhir dikirim ke pengguna/pemain
       |
       +--> ConversationSessionStore.append_turn(
                 user_message, assistant_response
            )
       |
       v
Session tersimpan untuk giliran berikutnya
```

**Urutan penyimpanan:** Ambil snapshot sebelum giliran baru ditambahkan. Simpan pasangan pesan pengguna dan jawaban akhir setelah jawaban berhasil dibentuk. Dengan begitu, konteks untuk suatu permintaan hanya berisi giliran sebelumnya, tidak menduplikasi pesan saat ini.

Jika pemrosesan gagal sebelum jawaban tersedia, jangan menyimpan pasangan percakapan setengah jadi. Error teknis boleh dicatat pada log aplikasi terpisah, bukan sebagai jawaban ILIS dalam riwayat.

### 2.2 Batas tanggung jawab

| Komponen | Tanggung jawab | Yang tidak boleh dilakukan |
|---|---|---|
| ChatbotAdapter | Mengelola session chat, mengambil/menyimpan turn, reset, Persona Mode A/B, meneruskan snapshot | Menyimpan riwayat di objek Core |
| GameEngineAdapter | Mengelola session dialog pemain/NPC, menyimpan pertukaran dialog, tetap merekam event game sebagai episode | Mengubah episode menjadi transcript atau mencampur session antar-NPC |
| ConversationSessionStore | CRUD session dan pasangan turn; membatasi riwayat; isolasi session | Menjalankan Semantic/Reasoning atau mengubah fakta |
| ILISCore | Memproses satu permintaan dengan input eksplisit; memakai konteks hanya selama pemanggilan | Menyimpan session, transcript, atau state turn |
| Context Resolver | Menghasilkan petunjuk konteks deterministik dari pesan saat ini dan snapshot | Mengarang informasi yang tidak terdapat pada teks/riwayat |
| Semantic Engine | Menganalisis teks saat ini sesuai kontrak yang ada | Menerima field riwayat baru di payload Semantic |
| Reasoning Engine | Menarik kesimpulan berbasis aturan, fakta, evidence, dan petunjuk konteks yang didukung | Mengubah enam key output atau menganggap riwayat sebagai fakta terverifikasi |
| PersonaRenderer | Merender jawaban sesuai Mode A/B/C | Mengubah hasil fakta, confidence, evidence, atau uncertainty |
| SQLite Core provider | Knowledge, provenance, dan Episodic Memory | Menjadi tempat penyimpanan transcript multi-turn |

### 2.3 Perilaku contoh api–kayu–kertas

- Turn 1 disimpan sebagai pasangan lengkap pengguna/ILIS.
- Turn 2 mengambil Turn 1 sebagai konteks, lalu memproses teks “Lalu apakah api juga bisa membakar kertas?”.
- Konteks dapat memberi petunjuk bahwa “juga” menghubungkan pertanyaan ini dengan topik api dan pembakaran.
- Semantic tetap menganalisis teks Turn 2 sebagaimana adanya dan menghasilkan struktur 12 field yang sama.
- Reasoning tetap memeriksa fakta/aturan untuk api dan kertas. Fakta bahwa kayu dibahas pada Turn 1 tidak membuktikan bahwa kertas dapat terbakar.
- Jika pengetahuan untuk kertas tidak tersedia, ILIS harus mempertahankan hasil `unknown`/ketidakpastian; konteks percakapan tidak boleh menggantikan evidence.

---

## 3. Model data dan batas riwayat

### 3.1 Identitas session

Setiap percakapan mempunyai `session_id` unik (UUID). ID dibuat oleh Adapter/SessionStore, bukan oleh Semantic Engine atau Reasoning Engine.

Satu session memiliki:
- `session_id`: UUID unik.
- `created_at`, `updated_at`.
- `status`: `active` atau `closed`.
- `adapter_type`: `chatbot` atau `game`.
- `persona_mode`: Mode A/B/C atau nilai konfigurasi adapter yang relevan.
- `metadata`: metadata non-sensitif yang diperlukan integrasi; bukan tempat menyimpan transcript.

Session antar pengguna, aplikasi, game, dan karakter harus terisolasi. Jangan menggunakan satu session global untuk semua pengguna.

### 3.2 Bentuk pasangan turn

Satu turn adalah satu pertukaran lengkap:

```json
{
  "turn_id": "uuid",
  "session_id": "uuid",
  "sequence": 1,
  "user_message": "Apakah api bisa membakar kayu?",
  "assistant_response": "Jawaban ILIS yang dikirim kepada pengguna.",
  "created_at": "timestamp",
  "metadata": {
    "persona_mode": "chatbot_ilis",
    "register": "formal"
  }
}
```

Field metadata opsional dan tidak menjadi bagian dari Semantic/Reasoning. Jangan menyimpan seluruh objek hasil Semantic/Reasoning kecuali ada kebutuhan audit yang disetujui terpisah. Default riwayat hanya menyimpan teks input pengguna/pemain dan teks jawaban akhir yang benar-benar dikirim.

### 3.3 Snapshot konteks untuk Core

Nama tipe konseptual: `ConversationContext`. Snapshot bersifat read-only/immutable dan hanya hidup selama satu pemanggilan Core.

```json
{
  "context_version": "1.0",
  "session_id": "uuid",
  "max_turns": 5,
  "turns": [
    {
      "sequence": 1,
      "user_message": "Apakah api bisa membakar kayu?",
      "assistant_response": "..."
    }
  ]
}
```

Aturan:
- `turns` diurutkan dari paling lama ke paling baru.
- Maksimum **5 pasangan turn lengkap** secara default; konfigurasi dapat diturunkan oleh aplikasi, tetapi tidak boleh tanpa batas.
- Tidak mengirim pesan saat ini di dalam `turns`; pesan saat ini dikirim sebagai argumen teks terpisah.
- Jangan mengirim session lain, metadata privat, token, kredensial, atau data yang tidak relevan.
- Jika tidak ada riwayat, kirim `null` atau snapshot dengan `turns: []`; keduanya harus memiliki perilaku setara.
- Snapshot dibuat ulang dari SessionStore untuk setiap giliran. Core tidak menyimpan cache percakapan.
- Batas lima turn berarti lima pertukaran pengguna–asisten, bukan lima pesan individual.

---

## 4. Spesifikasi API parameter konteks

API berikut adalah rancangan target, bukan API yang sudah tersedia.

### 4.1 API pemrosesan Core

Usulan entry point aditif:

```python
core.process_text(
    text: str,
    *,
    conversation_context: ConversationContext | None = None,
    register: str | None = None,
    polite: bool = False,
) -> CoreResponse
```

Ketentuan:
1. `text` adalah pesan saat ini.
2. `conversation_context` adalah parameter tambahan terpisah, bukan bagian dari Semantic payload.
3. Semantic tetap menerima teks saat ini dan menghasilkan wrapper serta 12 field yang sama.
4. Reasoning tetap menghasilkan tepat enam key yang sudah ditetapkan.
5. Context Resolver boleh menghasilkan petunjuk sementara untuk resolusi rujukan/kelanjutan. Petunjuk itu menjadi argumen lokal ke tahap pemrosesan berikutnya, bukan field Semantic baru.
6. Generator menerima snapshot melalui parameter `context` yang sudah tersedia atau API setara; jalur ini tidak boleh memakai `session_id` untuk mengambil riwayat dari Core.
7. Pemanggilan yang sama dengan input dan snapshot yang sama harus menghasilkan keluaran yang sama, selama Knowledge dan konfigurasi generator tidak berubah.
8. Setelah return, Core tidak mempertahankan referensi snapshot sebagai state session.

### 4.2 Bentuk respons

Respons tetap menggunakan bentuk adapter/Core yang kompatibel. `semantic_result` dan `reasoning_result` tidak memperoleh field baru. Metadata adapter boleh memuat `session_id` dan `response_type` karena keduanya berada di luar kontrak Semantic/Reasoning.

### 4.3 Kompatibilitas pemanggilan lama

- API adapter lama harus tetap berfungsi selama masa transisi.
- `session_id` tetap dapat diterima oleh adapter sebagai identitas session, tetapi tidak boleh menjadi alasan Core membaca transcript.
- Peralihan dari `ContextEngine.process_message()` untuk menyimpan chat ke ConversationSessionStore harus diuji terpisah.
- Jika diperlukan `episodic_session_id` internal untuk mengaitkan event game dengan Episodic Memory yang lama, ID itu harus dikelola sebagai detail integrasi adapter dan tidak disamakan diam-diam dengan transcript session. Pemetaan harus eksplisit serta tidak membocorkan riwayat dialog ke Core.

---

## 5. Dukungan Mode A, B, dan C

| Mode | Identitas jawaban | Pemilik session | Multi-turn |
|---|---|---|---|
| A — Chatbot ILIS | ILIS | ChatbotAdapter | Ya |
| B — Aplikasi | Identitas aplikasi/host | ChatbotAdapter atau adapter aplikasi | Ya |
| C — NPC Game | Karakter aktif | GameEngineAdapter / host game | Ya |

Aturan lintas mode:
- Riwayat hanya milik session aktif; dua aplikasi atau dua NPC tidak boleh berbagi riwayat kecuali host secara eksplisit membuat ruang percakapan bersama.
- Pergantian NPC membuat konteks karakter baru atau memakai session karakter yang memang dipilih host. Jangan otomatis mewariskan konteks NPC sebelumnya.
- Persona tetap diterapkan setelah hasil Core, seperti alur V2.1.
- Riwayat menyimpan jawaban akhir setelah PersonaRenderer, sebab itulah jawaban yang benar-benar diterima pengguna/pemain.
- Instruksi eksplisit “jawab dengan sopan”/“jawab dengan santai” tetap diproses oleh aturan PR #3. Register instruksi saat ini lebih tinggi prioritasnya daripada register default persona. Konteks lama tidak boleh mengalahkan instruksi gaya terbaru.

### 5.1 Prioritas rute adapter

Urutan pemeriksaan yang disarankan:

1. Validasi session dan hak aksesnya.
2. Deteksi perintah reset.
3. Deteksi Identity Intent yang sudah didukung; pertahankan aturan Mode A/B/C Tahap E–G.
4. Untuk pesan biasa, ambil snapshot konteks dan panggil Core.
5. Terapkan PersonaRenderer dan register.
6. Simpan pasangan turn lengkap.

Identity Intent tetap rute adapter yang sudah ada. Multi-turn tidak boleh membuat pertanyaan “Lu siapa?” atau variasinya dipaksa ke Context Resolver/Core. Untuk rute identity khusus, jawaban tetap disimpan sebagai jawaban assistant agar percakapan berikutnya memiliki transcript yang konsisten, kecuali kebijakan produk memilih mengecualikan rute tersebut secara eksplisit.

---

## 6. Reset sesi percakapan

### 6.1 Pemicu

Deteksi deterministik setelah normalisasi huruf/spasi terhadap perintah yang jelas, minimal:
- “reset percakapan”
- “hapus riwayat”
- “hapus riwayat percakapan”
- “mulai percakapan baru”

Daftar variasi bahasa dapat diperluas melalui tes. Jangan menganggap kalimat yang sekadar membahas kata “reset” sebagai perintah reset; gunakan pencocokan frasa/perintah yang tegas.

### 6.2 Perilaku reset

Sediakan API eksplisit:

```python
adapter.reset_session(session_id) -> ResetResult
```

Saat perintah reset diterima:
1. Validasi bahwa session aktif dan dimiliki pemanggil.
2. Hapus seluruh pasangan turn percakapan dari ConversationSessionStore untuk session tersebut.
3. Pertahankan `session_id` aktif agar pengguna dapat langsung melanjutkan.
4. Kembalikan konfirmasi deterministik melalui persona aktif, misalnya “Riwayat percakapan sesi ini sudah direset. Kita mulai dari awal, ya.”
5. Tandai metadata respons sebagai `response_type: session_reset` di lapisan adapter.
6. Jangan jalankan Semantic/Reasoning untuk teks perintah reset.
7. Jangan menghapus Knowledge, provenance, fakta, atau Episodic Memory.
8. Jangan menghapus session milik pengguna lain atau session lain.
9. Setelah reset, permintaan berikutnya menerima `turns: []`; tidak boleh ada konteks lama yang muncul lagi.

Reset percakapan berbeda dari menutup/menghapus session permanen dan berbeda dari penghapusan memori episodik. Operasi penutupan session menjadi API lifecycle terpisah.

---

## 7. Sesi sementara dan sesi persisten

| Aspek | Sementara (in-memory) | Persisten (jangka panjang) |
|---|---|---|
| Backend | Store di memori proses milik adapter | Store terpisah yang durable; dapat memakai SQLite terpisah |
| Umur data | Hilang saat proses berhenti/restart | Bertahan setelah restart sampai dihapus/retensi berakhir |
| Isolasi | Kunci berdasarkan session_id | Kunci berdasarkan session_id dan pemilik/tenant |
| Pemulihan | Tidak ada | Load ulang session aktif dan turn yang diperlukan |
| Batas riwayat | Maksimum 5 turn | Maksimum 5 turn yang dikirim ke Core; retensi arsip dapat diatur terpisah |
| Reset | Hapus daftar turn pada session | Hapus turn terkait session secara transaksional |
| Kegunaan | Demo, chatbot sementara, game satu sesi | Chatbot layanan, kampanye game panjang, sesi lintas restart |

Keputusan:
- **Default awal:** in-memory agar sederhana, aman, dan tidak mengubah SQLite Core.
- **Opsi persisten:** implementasi backend SessionStore tersendiri, idealnya database/file terpisah dari database Knowledge/Episodic Memory.
- Jangan menambahkan tabel transcript ke `SQLiteStorageProvider` Core yang sudah ada.
- Jika backend persisten menggunakan SQLite, wajib memiliki file/provider, lifecycle, migrasi, dan tes sendiri. Nama tabel dapat berupa `conversation_sessions` dan `conversation_turns`; jangan memakai tabel `sessions` internal provider lama.
- Kebijakan retensi, enkripsi, penghapusan, dan kepemilikan data perlu ditetapkan sebelum sesi persisten dipakai pada produk nyata.

---

## 8. Daftar file implementasi yang direncanakan

**Tidak satu pun file berikut diubah pada tugas desain ini.** Daftar adalah rencana implementasi setelah desain disetujui.

### 8.1 File baru

| File | Tanggung jawab |
|---|---|
| `src/ilis/session/__init__.py` | Ekspor model dan interface session. |
| `src/ilis/session/models.py` | Model `ConversationTurn`, `ConversationSession`, `ConversationContext`, dan hasil reset. |
| `src/ilis/session/store.py` | Interface/protocol `ConversationSessionStore` dan implementasi in-memory. |
| `src/ilis/session/sqlite_store.py` | Opsional: implementasi persistent store terpisah dari SQLite Core provider. |
| `src/ilis/session/context_resolver.py` | Resolusi konteks/rujukan deterministik dari teks saat ini dan snapshot riwayat; tidak menyimpan state. |

### 8.2 File yang direncanakan untuk dimodifikasi

| File | Rencana perubahan | Batas wajib |
|---|---|---|
| `src/ilis/interfaces/chatbot_adapter.py` | Inject SessionStore; ambil/simpan turn; reset; kirim snapshot; tetap mengatur Mode A/B dan Identity Intent. | Jangan ubah Semantic/Reasoning contract atau Persona Layer. |
| `src/ilis/interfaces/game_adapter.py` | Inject SessionStore; simpan pertukaran pemain/NPC; kirim konteks dialog; pertahankan pencatatan event episodik. | Pisahkan transcript dari Episodic Memory; isolasi karakter/session. |
| `src/ilis/interfaces/ilis_core.py` | Tambah entry point pemrosesan satu permintaan yang menerima snapshot konteks sebagai parameter opsional. | Tidak memiliki session store, transcript, atau state percakapan. |
| `src/ilis/cognition/context_engine.py` | Tegaskan batas fungsi: event/Episodic Memory tetap tersedia; jalur percakapan tidak lagi menjadi penyimpanan transcript adapter. | Jangan menghapus fitur episodic yang dipakai GameAdapter. |
| `src/ilis/cognition/memory_store.py` | Pisahkan tanggung jawab working chat history dari session/episode internal; pertahankan kompatibilitas episodic dan migrasi yang diperlukan. | Jangan memindahkan transcript ke SQLite Core. |
| `src/ilis/generation/language_generator.py` | Pastikan snapshot `context` dapat dipakai tanpa lookup berdasarkan `session_id`. | Pertahankan pemilihan register, polite, uncertainty, dan output yang ada. |

### 8.3 File tes baru / yang diperbarui

| File | Cakupan |
|---|---|
| `tests/test_multi_turn_context.py` | Snapshot konteks, batas 5 turn, resolusi rujukan, urutan turn, determinisme. |
| `tests/test_conversation_session_store.py` | CRUD session, isolasi, in-memory, persistent store, reset, restart. |
| `tests/test_multi_turn_chatbot_adapter.py` | Multi-turn Mode A/B, reset, penyimpanan pasangan turn, Identity Intent. |
| `tests/test_multi_turn_game_adapter.py` | Multi-turn Mode C, isolasi NPC, pencatatan episodic tetap berfungsi. |
| `tests/test_multi_turn_regression_v21.py` | Kontrak Semantic/Reasoning, Persona, Identity Intent, instruksi register, SQLite Knowledge/Episodic. |

Dokumentasi implementasi berikutnya dapat memperbarui panduan pengujian V2.2 setelah kode benar-benar tersedia. Tugas desain ini hanya membuat file arsitektur yang ditentukan.

---

## 9. Test case dan kriteria penerimaan

### 9.1 Tes positif multi-turn

| ID | Skenario | Hasil yang diharapkan |
|---|---|---|
| MT-01 | Turn 1 api–kayu, Turn 2 “Lalu apakah api juga bisa membakar kertas?” | Snapshot berisi Turn 1; sistem mengenali hubungan lanjutan tanpa menganggap fakta kayu berlaku untuk kertas. |
| MT-02 | “Dia siapa?” setelah nama karakter disebut pada turn sebelumnya | Rujukan hanya diresolusikan bila antecedent jelas dan unik; jika ambigu, ILIS meminta klarifikasi/tidak menebak. |
| MT-03 | “Bagaimana dengan yang tadi?” setelah satu topik jelas | Konteks sebelumnya digunakan secara deterministik. |
| MT-04 | Lima turn tersimpan | Snapshot berisi maksimal lima pasangan terbaru dalam urutan kronologis. |
| MT-05 | Enam turn tersimpan | Snapshot hanya memuat lima pasangan paling baru; turn lama tidak ikut dikirim ke Core. |
| MT-06 | Session A dan B berjalan bersamaan | Riwayat tidak tercampur. |
| MT-07 | Mode A dua giliran | Jawaban tetap beridentitas ILIS dan konteks berlanjut. |
| MT-08 | Mode B dua giliran | Jawaban tetap beridentitas aplikasi yang benar dan konteks terisolasi. |
| MT-09 | Mode C dua giliran dengan NPC sama | Dialog NPC memanfaatkan riwayat NPC/session tersebut. |
| MT-10 | Pergantian NPC | Konteks NPC sebelumnya tidak bocor ke NPC baru. |
| MT-11 | In-memory store | Riwayat tersedia selama proses berjalan dan hilang setelah restart. |
| MT-12 | Persistent store | Riwayat yang belum kedaluwarsa dapat dipulihkan setelah restart. |
| MT-13 | Input dan snapshot identik | Hasil pemrosesan deterministik identik selama Knowledge/configuration tidak berubah. |
| MT-14 | Tidak ada riwayat | Sistem berperilaku seperti pemrosesan single-turn V2.1. |

### 9.2 Tes reset

| ID | Skenario | Hasil yang diharapkan |
|---|---|---|
| RS-01 | “reset percakapan” | Turn percakapan session aktif terhapus dan konfirmasi reset diberikan. |
| RS-02 | “hapus riwayat” | Hasil sama dengan RS-01. |
| RS-03 | Pesan setelah reset merujuk “yang tadi” | Riwayat lama tidak tersedia; sistem tidak mengarang konteks. |
| RS-04 | Reset Session A | Session B tetap utuh. |
| RS-05 | Reset pada persistent store | Turn session terhapus secara durable, termasuk setelah restart. |
| RS-06 | Reset percakapan saat ada Episodic Memory | Episode game, Knowledge, dan provenance tetap utuh. |
| RS-07 | Session tidak dikenal/tidak dimiliki pemanggil | Reset ditolak dengan error aman; tidak menghapus data lain. |
| RS-08 | Frasa “cara kerja reset percakapan” sebagai pertanyaan | Tidak dianggap perintah reset bila tidak cocok dengan pola perintah tegas. |

### 9.3 Tes regresi V2.1 — wajib lulus

| ID | Area | Hasil yang diharapkan |
|---|---|---|
| REG-01 | Semantic | Tepat 12 field; tidak ada field konteks/riwayat tambahan. |
| REG-02 | Reasoning | Tepat 6 key; nama dan tipe perilaku tetap. |
| REG-03 | Persona Mode A | Chatbot tetap mengidentifikasi diri sebagai ILIS. |
| REG-04 | Persona Mode B | Aplikasi tetap menggunakan identitas host, bukan ILIS. |
| REG-05 | Persona Mode C | NPC tetap menggunakan identitas karakter; tidak membocorkan ILIS. |
| REG-06 | Identity Intent Tahap E–G | Frasa identitas formal/santai yang telah didukung tetap masuk rute adapter yang benar, termasuk variasi “lo/lu” dan “km”. |
| REG-07 | Instruksi PR #3 | “Jawab dengan sopan” tetap formal; “jawab dengan santai” tetap informal. |
| REG-08 | Prioritas instruksi | Instruksi gaya pada turn saat ini mengalahkan register default persona dan tidak ditimpa konteks lama. |
| REG-09 | SQLite Knowledge | Fakta dan provenance tetap dapat dimuat/disimpan seperti sebelumnya. |
| REG-10 | SQLite Episodic | Event game tetap direkam dan dibaca setelah restart sesuai konfigurasi storage. |
| REG-11 | Pemisahan storage | Transcript percakapan tidak ditulis ke tabel/provider SQLite Core. |
| REG-12 | Stateless Core | Setelah pemanggilan selesai, Core tidak menyimpan transcript atau session history. |
| REG-13 | Single-turn | Seluruh skenario single-turn V2.1 tetap lulus. |
| REG-14 | Persona metadata | Persona tidak mengubah confidence, evidence, reasoning_type, atau uncertainty. |
| REG-15 | Tanpa LLM | Tidak ada dependency, API, atau fallback ke LLM/model AI. |

Kriteria penerimaan rilis: seluruh tes baru dan seluruh suite regresi V2.1 lulus pada CI. Uji manual Playground mencakup minimal satu rangkaian dua turn, satu reset, satu Mode B/C bila konfigurasi Playground mendukungnya, serta verifikasi metadata dan isolasi session.

---

## 10. Risiko regresi dan mitigasi

| Area | Risiko | Mitigasi |
|---|---|---|
| Semantic 12 field | Riwayat dimasukkan ke payload Semantic atau menambah field semantik. | Snapshot hanya parameter tambahan Core; uji exact field set REG-01. |
| Reasoning 6 key | Konteks menyebabkan key baru atau mengubah arti confidence/evidence. | Pertahankan schema enam key; riwayat bukan evidence faktual; REG-02/REG-14. |
| Stateless Core | Core menyimpan cache/history atau membaca session dari ContextEngine. | Snapshot immutable per pemanggilan; adapter store sebagai satu-satunya transcript owner; REG-12. |
| Persona Mode A/B/C | Konteks lintas persona membuat identitas salah atau bocor. | Isolasi session berdasarkan host/persona/karakter; REG-03 sampai REG-05. |
| Identity Intent E–G | Frasa identitas dianggap pertanyaan lanjutan biasa. | Rute identity tetap diperiksa di adapter sesuai urutan V2.1; REG-06. |
| Instruksi sopan/santai | Register dari turn lama mengalahkan instruksi terbaru. | Instruksi eksplisit saat ini menjadi prioritas; konteks hanya fallback; REG-07/REG-08. |
| SQLite Knowledge/Episodic | Reset atau pemisahan session menghapus fakta/episode. | Store transcript terpisah; reset tidak menyentuh Core storage; REG-09/REG-10/RS-06. |
| Session legacy | ID session adapter tidak cocok dengan foreign key session episodic lama. | Rancang pemetaan eksplisit antara conversation session dan episodic scope; jangan memakai ID secara implisit. |
| Batas konteks | Riwayat terlalu panjang, urutan salah, atau pasangan terpotong. | Simpan pasangan atomik, ambil lima turn terbaru; MT-04/MT-05. |
| Salah rujuk | Kata “dia/itu/tadi” punya beberapa antecedent. | Resolver harus abstain/meminta klarifikasi jika ambigu; jangan menebak. |
| Persistent privacy | Riwayat pengguna tersimpan terlalu lama atau tercampur tenant. | Ownership, retensi, penghapusan, dan isolasi wajib ditentukan sebelum mengaktifkan persistent mode. |
| Game event vs dialog | Transcript NPC tercampur dengan episodic event atau mengubah makna event. | Dua store dan dua model data; episode tetap dicatat oleh jalur episodic. |

---

## 11. Tahapan implementasi yang direkomendasikan

1. **Tahap A — Model dan kontrak session:** model turn/session/context, store interface, batas 5 turn, dan isolasi.
2. **Tahap B — In-memory store:** implementasi dan tes tanpa menyentuh SQLite Core.
3. **Tahap C — Core stateless entry point:** terima snapshot per pemanggilan; pastikan tidak ada lookup transcript dari Core.
4. **Tahap D — ChatbotAdapter:** integrasi Mode A/B, reset, Identity Intent, instruksi register, dan simpan jawaban akhir.
5. **Tahap E — GameEngineAdapter:** integrasi Mode C; pisahkan transcript dialog dari Episodic Memory dan pertahankan pencatatan event.
6. **Tahap F — Persistent session store opsional:** database/provider terpisah dengan kebijakan retensi dan migrasi tersendiri.
7. **Tahap G — Regresi dan Playground:** seluruh tes V2.1 + multi-turn, lalu uji manual dua turn dan reset.

Setiap tahap harus melalui CI sebelum tahap berikutnya. Jangan menggabungkan refactor storage besar sekaligus dengan perubahan Semantic/Reasoning.

---

## 12. Checklist review desain untuk tim

### Arsitektur
- [ ] Riwayat percakapan hanya dimiliki ChatbotAdapter/GameEngineAdapter melalui SessionStore.
- [ ] Core hanya menerima snapshot konteks untuk satu pemanggilan dan tidak menyimpan state dialog.
- [ ] Context Resolver deterministik dan dapat abstain ketika rujukan ambigu.
- [ ] Semantic payload tetap sama; tidak ada field riwayat.
- [ ] Reasoning result tetap enam key.

### Session dan storage
- [ ] Setiap session memiliki UUID unik dan ownership/isolasi yang jelas.
- [ ] Riwayat disimpan sebagai pasangan user/pemain dan assistant/NPC.
- [ ] Maksimal lima pasangan turn dikirim ke Core.
- [ ] Pesan saat ini tidak diduplikasi dalam snapshot.
- [ ] In-memory dan persistent store memiliki interface yang sama.
- [ ] Persistent store terpisah dari SQLite Core provider.
- [ ] Reset hanya menghapus transcript session aktif, bukan Knowledge/Episodic Memory.

### Integrasi V2.1
- [ ] Mode A, B, dan C tetap mempertahankan identitas masing-masing.
- [ ] Identity Intent Tahap E–G tetap dideteksi sebelum alur multi-turn biasa.
- [ ] Instruksi sopan/santai saat ini mengalahkan default register dan konteks lama.
- [ ] Persona hanya merender teks; tidak mengubah makna atau metadata reasoning.
- [ ] Game event tetap dicatat sebagai Episodic Memory secara terpisah dari dialog.

### Pengujian dan rilis
- [ ] Semua tes positif multi-turn lulus.
- [ ] Semua tes reset dan isolasi session lulus.
- [ ] Seluruh tes regresi V2.1 lulus.
- [ ] Single-turn tetap berperilaku sama.
- [ ] Tidak ada dependency atau pemanggilan LLM.
- [ ] CI dan Playground membuktikan alur dua turn serta reset.

---

## 13. Keputusan yang harus disetujui sebelum implementasi

1. Apakah batas default lima turn diterima sebagai lima pasangan lengkap user–assistant?
2. Apakah persistent session menjadi fitur opsional setelah in-memory stabil?
3. Apakah jawaban Identity Intent dan reset disimpan sebagai turn assistant dalam transcript? Rekomendasi desain: ya, agar riwayat mencerminkan apa yang benar-benar dilihat pengguna.
4. Untuk GameAdapter, apakah session mengikuti pemain, NPC, atau kombinasi pemain+NPC? Rekomendasi: host game menentukan conversation scope secara eksplisit; jangan berbagi konteks antar-NPC secara default.
5. Bagaimana kebijakan retensi dan penghapusan transcript persisten ditetapkan sebelum penggunaan produksi?

**Rekomendasi:** setujui pemisahan adapter-owned transcript terlebih dahulu, implementasikan in-memory, dan jangan aktifkan persistent conversation store sebelum isolasi serta kebijakan retensi ditinjau.

---

## 14. Pesan commit

```text
docs(v2.2): arsitektur desain multi-turn percakapan
```

**Cakupan commit yang diizinkan untuk tugas ini:** hanya `docs/multi_turn_v2_2_architecture.md`. Tidak ada perubahan kode, kontrak, database, atau tes pada commit desain ini.
