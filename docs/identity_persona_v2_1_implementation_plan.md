# Rencana Implementasi Identity & Persona Layer ILIS V2.1

**Status:** Desain dan rencana implementasi; belum ada kode Persona Layer yang diterapkan.  
**Basis:** `ilis-v2-development` setelah PR #3 digabung.  
**Batas wajib:** Semantic tetap 12 field; Reasoning tetap 6 key; tidak mengubah kode inti Semantic Engine atau Reasoning Engine.

## 1. Tujuan dan keputusan arsitektur

Identity & Persona Layer memisahkan mesin bahasa dari identitas yang tampil kepada pengguna. Satu ILIS Core dapat dipakai oleh beberapa aplikasi dan karakter game tanpa membuat Core mengaku sebagai aplikasi atau karakter tersebut.

Keputusan yang mengikat:

1. Konfigurasi persona dimiliki aplikasi dan dibaca pada lapisan adapter/entry point (misalnya `ChatbotAdapter` atau `GameEngineAdapter`), bukan disimpan sebagai konfigurasi di `ILISCore`.
2. Core tetap memproses bahasa, konteks, pengetahuan, reasoning, dan menghasilkan teks jawaban melalui generator yang ada.
3. Persona Layer menerima teks jawaban dari Core serta konfigurasi identitas dari adapter. Lapisan ini menambahkan atau memilih respons identitas/perkenalan dan melakukan rendering persona secara terbatas.
4. Persona Layer tidak mengubah fakta, evidence, confidence, reasoning type, atau status ketidakpastian. Ia juga tidak boleh mengklaim aksi aplikasi/game telah berhasil tanpa konfirmasi adapter/integrasi.
5. Semantic contract (12 field), Reasoning contract (6 key), SQLite provider, dan kode inti Semantic/Reasoning tidak diubah dalam implementasi V2.1.
6. Tidak ada LLM/model AI. Pemilihan identitas dan respons identitas menggunakan aturan deterministik.

## 2. Tiga mode identitas

### Mode A — Chatbot ILIS

- `mode = chatbot_ilis`
- Identitas yang terlihat: **“Saya ILIS, sistem kecerdasan bahasa.”**
- Character Identity tidak digunakan.
- Untuk pertanyaan identitas seperti “Siapa kamu?”, “Kamu siapa?”, atau “Apa nama kamu?”, Persona Layer memberi jawaban identitas ILIS.
- Pada perkenalan awal, adapter boleh meminta Persona Layer menambahkan perkenalan satu kali per sesi. Jangan mengulang perkenalan pada setiap balasan.

### Mode B — Application Identity

- `mode = application`
- Identitas yang terlihat adalah nama/peran aplikasi, bukan ILIS.
- Contoh: “Saya asisten layanan Toko Arunika. Ada yang bisa saya bantu?”
- Profil aplikasi minimal memiliki `application_id`, `display_name`, `role`, `identity_reply`, dan register default.
- Jika nama/peran aplikasi tidak tersedia, gunakan fallback generik yang dikonfigurasi aplikasi. Jangan menebak nama merek atau mengaku sebagai ILIS.

### Mode C — Character Identity (NPC Game)

- `mode = character`
- Identitas yang terlihat adalah karakter aktif di dalam game.
- Contoh: “Aku penjaga gerbang Kerajaan Arunika.”
- NPC tidak menyebut ILIS kepada pemain, kecuali hal tersebut memang bagian eksplisit dari lore yang diberikan game.
- Profil karakter minimal memiliki `character_id`, `display_name`, `role`, `identity_reply`, register/gaya bicara, dan batas pengetahuan/lore.
- Jika karakter tidak tersedia, gunakan fallback NPC yang ditentukan game; jangan mengarang nama, latar, atau lore.

## 3. Alur arsitektur yang diusulkan

```text
Pengguna / Pemain
       |
       v
Application Entry Point / Adapter
  - membaca konfigurasi aplikasi
  - memilih mode A / B / C
  - memilih profil aplikasi / karakter aktif
       |
       +------------------------------+
       |                              |
       v                              v
   ILIS Core                    Persona Layer
   - proses bahasa              - menerima answer_text dari Core
   - konteks & reasoning        - mendeteksi pertanyaan identitas
   - hasilkan teks              - memilih identity_reply dari profil
       |                        - menambah perkenalan bila diminta
       +------------+-----------+ - render persona tanpa mengubah fakta
                    |
                    v
           Respons ke pengguna
```

Untuk permintaan biasa, adapter menjalankan Core dan meneruskan hanya teks hasil generator sebagai input konten ke Persona Layer. Metadata Core tetap dipertahankan apa adanya pada respons adapter. Untuk pertanyaan identitas, Persona Layer memilih jawaban identitas berdasarkan profil aktif; ia tidak meminta Semantic/Reasoning Engine mempelajari identitas aplikasi atau karakter.

**Pemisahan tanggung jawab:**

- `ILISCore`: tidak menerima `persona_config`, `application_identity`, atau `character_identity`; tidak memilih identitas.
- `ChatbotAdapter`: membaca konfigurasi Mode A/B dari aplikasi, memanggil Core, lalu memanggil Persona Layer.
- `GameEngineAdapter`: membaca konfigurasi Mode C dan karakter aktif dari game, memanggil Core untuk interpretasi event/dialog, lalu memanggil Persona Layer.
- `PersonaLayer`: fungsi deterministik dan stateless sejauh mungkin; tidak memiliki koneksi database dan tidak menyimpan konfigurasi global.
- Aplikasi/game: sumber kebenaran profil, karakter aktif, lore, dan konfirmasi aksi.

## 4. Kontrak konfigurasi konseptual

Contoh bentuk konfigurasi (skema final ditetapkan saat implementasi):

```python
PersonaConfig(
    mode="chatbot_ilis",  # chatbot_ilis | application | character
    application=ApplicationProfile(
        application_id="ilis-chatbot",
        display_name="ILIS",
        role="sistem kecerdasan bahasa",
        identity_reply="Saya ILIS, sistem kecerdasan bahasa.",
        default_register="formal",
    ),
    character=None,
)
```

Mode B mengisi `application` dengan profil aplikasi milik integrator. Mode C mengisi `application` sebagai konteks game dan `character` dengan karakter aktif. Validasi harus menolak mode yang tidak dikenal, profil wajib yang kosong, register di luar `formal|informal|slang`, dan konfigurasi karakter yang tidak lengkap. Jangan menyimpan konfigurasi persona di SQLite Core pada tahap ini; aplikasi menjadi pemilik konfigurasi dan dapat menyimpannya sendiri.

## 5. Aturan rendering dan prioritas

Urutan prioritas yang disarankan:

1. Konfigurasi identitas aktif dari aplikasi/game.
2. Respons identitas khusus jika input merupakan pertanyaan identitas.
3. Instruksi gaya eksplisit dari pengguna (misalnya “jawab dengan sopan” atau “jawab dengan santai”).
4. Register default profil aplikasi/karakter.
5. Fallback formal yang aman.

Persona boleh mengubah sapaan, pilihan kata, sudut pandang orang pertama, dan pembungkus dialog. Persona tidak boleh:
- menambahkan fakta/lore yang tidak ada di profil atau konteks;
- mengubah kesimpulan, evidence, confidence, atau ketidakpastian Core;
- mengubah jawaban “belum diketahui” menjadi klaim pasti;
- mengubah instruksi sopan/santai yang sudah didukung PR #3;
- mengklaim transaksi, pintu, serangan, atau aksi game telah berhasil tanpa hasil konfirmasi dari aplikasi/game.

Perkenalan otomatis harus eksplisit dikendalikan adapter (misalnya `introduce_on_session_start`) dan ditandai per sesi di lapisan aplikasi. Jangan memakai SQLite Core untuk menyimpan status perkenalan persona kecuali kelak ada kebutuhan produk terpisah.

## 6. Daftar file rencana perubahan

### File kode yang direncanakan

| File | Rencana |
|---|---|
| `src/ilis/persona/__init__.py` | Mengekspor API Persona Layer. |
| `src/ilis/persona/profiles.py` | Tipe/validasi `PersonaConfig`, `ApplicationProfile`, dan `CharacterProfile`. |
| `src/ilis/persona/renderer.py` | Deteksi pertanyaan identitas, pemilihan identity reply, perkenalan, dan rendering persona deterministik. |
| `src/ilis/interfaces/chatbot_adapter.py` | Menerima konfigurasi dari aplikasi; memilih Mode A/B; meneruskan teks Core ke Persona Layer; menjaga metadata dan register instruksi. |
| `src/ilis/interfaces/game_adapter.py` | Menerima profil game/karakter aktif untuk Mode C; memastikan dialog NPC tidak membocorkan identitas ILIS. |

### File tes yang direncanakan

| File | Rencana |
|---|---|
| `tests/test_persona_layer.py` | Tes unit profil, validasi, identitas, fallback, rendering, dan larangan mengubah makna/ketidakpastian. |
| `tests/test_interfaces.py` | Tes integrasi adapter untuk Mode A/B/C dan kompatibilitas pemanggilan lama tanpa konfigurasi persona eksplisit. |
| `tests/test_e2e_chatbot.py` | Tes end-to-end pertanyaan identitas, instruksi sopan/santai, dan respons biasa. |
| `tests/test_sqlite_persist.py` | Tes regresi bahwa konfigurasi persona tidak mengubah skema, persistensi, atau lifecycle SQLite Core. |

### Dokumentasi yang direncanakan

| File | Rencana |
|---|---|
| `docs/persona_identity_layer.md` | Perbarui arsitektur konseptual dengan kontrak adapter, tiga mode final, dan batas Core/Persona. |
| `docs/testing_guide_v2_beta.md` | Tambahkan skenario uji Persona Layer setelah fitur benar-benar diimplementasikan. |

Tidak direncanakan mengubah `src/ilis/semantics/semantic_engine.py`, `src/ilis/semantics/contract_validator.py`, `src/ilis/cognition/reasoning_engine.py`, `src/ilis/interfaces/ilis_core.py`, atau `src/ilis/storage/sqlite_provider.py`. `LanguageGenerator` dan `SentenceBuilder` juga tidak perlu diubah pada rancangan awal; Persona Layer bekerja setelah teks Core tersedia.

## 7. Test case dan kriteria penerimaan

### Mode A — Chatbot ILIS

| ID | Input / kondisi | Hasil yang diharapkan |
|---|---|---|
| A-01 | “Siapa kamu?” | Jawaban menyebut “Saya ILIS, sistem kecerdasan bahasa.” |
| A-02 | “Kamu siapa?” | Identitas ILIS tetap terjawab. |
| A-03 | Sesi baru dengan perkenalan diaktifkan | Perkenalan muncul satu kali. |
| A-04 | Balasan kedua pada sesi yang sama | Tidak mengulang perkenalan otomatis. |
| A-05 | Pertanyaan pengetahuan biasa | Jawaban Core dipertahankan; tidak menambahkan klaim identitas yang tidak perlu. |
| A-06 | Profil chatbot hilang/tidak valid | Fallback aman atau error validasi yang jelas; tidak diam-diam memakai identitas aplikasi lain. |

### Mode B — Application Identity

| ID | Input / kondisi | Hasil yang diharapkan |
|---|---|---|
| B-01 | Profil aplikasi “Toko Arunika”; “Siapa kamu?” | Memperkenalkan diri sebagai asisten Toko Arunika. |
| B-02 | Profil aplikasi layanan bank; “Kamu siapa?” | Menggunakan nama/peran aplikasi yang dikonfigurasi; tidak menyebut ILIS. |
| B-03 | Pertanyaan biasa | Isi faktual Core tetap sama; hanya gaya/sapaan yang boleh disesuaikan. |
| B-04 | Dua aplikasi memakai Core dan session berbeda | Identitas aplikasi tidak tertukar/bocor. |
| B-05 | Nama aplikasi kosong | Validasi/fallback generik; tidak mengarang nama aplikasi. |
| B-06 | Instruksi “jawab dengan santai” | Register informal tetap diterapkan pada respons aplikasi. |

### Mode C — Character Identity (NPC Game)

| ID | Input / kondisi | Hasil yang diharapkan |
|---|---|---|
| C-01 | NPC penjaga gerbang; “Siapa kamu?” | Menjawab sebagai penjaga gerbang sesuai profil. |
| C-02 | NPC horor; “Kamu siapa?” | Jawaban in-character sesuai teks/profil yang disediakan. |
| C-03 | NPC kasir simulasi; “Siapa kamu?” | Memperkenalkan diri sebagai kasir/pemilik toko sesuai profil. |
| C-04 | Profil lore tidak memuat suatu fakta | NPC tidak mengarang fakta tersebut; ketidakpastian dipertahankan. |
| C-05 | Dua NPC bergantian memakai Core yang sama | Nama, gaya, dan identity reply tidak tertukar. |
| C-06 | Pertanyaan identitas pada NPC | Tidak menyebut ILIS kecuali lore eksplisit menyatakannya. |
| C-07 | Event aksi game belum dikonfirmasi | NPC tidak mengaku aksi berhasil. |
| C-08 | Karakter aktif tidak tersedia | Fallback dari aplikasi game; tidak mewarisi karakter sesi sebelumnya. |

### Tes kontrak dan regresi lintas-mode

- R-01: Semantic result tetap tepat 12 field; tidak ada field persona baru di payload Semantic.
- R-02: Reasoning result tetap tepat 6 key; tidak ada key persona baru.
- R-03: Instruksi “Jawab dengan sopan” tetap memilih formal dan mempertahankan pembuka sopan PR #3.
- R-04: Instruksi “Jawab dengan santai” tetap memilih informal.
- R-05: Instruksi gaya di depan dan belakang pertanyaan tetap berfungsi.
- R-06: Confidence, evidence, reasoning_type, dan uncertainty sebelum/sesudah Persona Layer identik.
- R-07: SQLite memory/knowledge/episodic persistence tetap lulus; konfigurasi persona tidak masuk ke tabel atau skema Core.
- R-08: Session/karakter/aplikasi terisolasi, termasuk setelah close/recreate session.
- R-09: API adapter lama tanpa konfigurasi persona eksplisit tetap kompatibel melalui default yang terdokumentasi.
- R-10: Tidak ada dependency atau pemanggilan LLM/model AI.

## 8. Risiko regresi dan mitigasi

| Area | Risiko | Mitigasi / tes |
|---|---|---|
| SQLite | Profil atau status perkenalan tanpa sengaja disimpan ke storage Core; perubahan lifecycle session. | Persona config tetap milik adapter; jangan ubah provider/schema; jalankan seluruh tes SQLite dan R-07/R-08. |
| PR #3: sopan/santai | Renderer menimpa register eksplisit atau menghapus pembuka sopan. | Urutan prioritas instruksi eksplisit di atas default persona; tes R-03 sampai R-05. |
| Semantic contract | Menambah field identity/persona ke hasil Semantic. | Jangan ubah Semantic Engine/validator; tes exact field set R-01. |
| Reasoning contract | Menambah key persona atau mengubah reasoning type/confidence. | Persona hanya menerima teks dan konfigurasi; tes R-02/R-06. |
| Kebocoran identitas | NPC menyebut ILIS atau aplikasi A menjawab sebagai aplikasi B. | Profil eksplisit per adapter/sesi; tes B-04, C-05, C-06, C-08. |
| Halusinasi persona | NPC menambah lore atau mengaku melakukan aksi yang belum terjadi. | Gunakan hanya profil/context yang diberikan; tes C-04 dan C-07. |
| Kompatibilitas API | Perubahan constructor/response adapter mematahkan integrator lama. | Parameter persona opsional dengan default terdokumentasi; pertahankan bentuk response adapter; tes R-09. |
| Perkenalan berulang | Salam/perkenalan muncul di setiap balasan. | Status perkenalan dikelola adapter per sesi, bukan Core; tes A-03/A-04. |

## 9. Tahapan implementasi yang disarankan

1. **Tahap 1 — Kontrak dan profil:** definisikan tipe profil, validasi, default, dan prioritas register.
2. **Tahap 2 — Persona renderer:** implementasi deteksi pertanyaan identitas, identity reply, fallback, dan rendering tanpa mutasi metadata Core.
3. **Tahap 3 — Chatbot adapter:** integrasikan Mode A dan B; pertahankan API lama dan alur instruksi PR #3.
4. **Tahap 4 — Game adapter:** integrasikan Mode C, pergantian karakter, lore boundary, dan action acknowledgement.
5. **Tahap 5 — Tes regresi:** jalankan seluruh suite termasuk SQLite, kontrak Semantic/Reasoning, dan pengujian Playground.
6. **Tahap 6 — Dokumentasi dan review:** perbarui arsitektur/panduan uji, buka PR ke `ilis-v2-development`, jangan merge ke `main` langsung.

## 10. Pesan commit untuk implementasi kode nanti

```text
feat(v2.1): implementasikan Identity & Persona Layer untuk chatbot, aplikasi, dan NPC
```

Commit dokumentasi ini tidak mengimplementasikan kode Persona Layer. Semua file kode di atas tetap berupa rencana sampai tugas implementasi disetujui.

## 11. Batas perubahan yang tidak boleh dilanggar

- Tidak mengubah Semantic Engine atau kontrak 12 field.
- Tidak mengubah Reasoning Engine atau kontrak 6 key.
- Tidak menaruh konfigurasi persona di `ILISCore`.
- Tidak menambah LLM/model AI.
- Tidak mengubah skema SQLite untuk menyimpan persona.
- Tidak membiarkan Persona Layer mengubah fakta, confidence, evidence, reasoning type, atau uncertainty dari Core.
