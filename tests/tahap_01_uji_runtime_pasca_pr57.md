# LAPORAN UJI RUNTIME TAHAP 1 — PEMBARUAN PASCA-PR #54 DAN #57

**Acuan branch:** `ilis-v2-development` setelah merge PR #57  
**Baseline kode:** `81029fbeca166fd06b4251e8c1e08ff89d1728c5`  
**Tujuan:** memperbarui peta cakupan runtime setelah implementasi EJA-04 dan classifier terbatas `dekat`.  
**Status:** laporan cakupan dan rencana verifikasi; bukan pengesahan Tahap 1 selesai.

---

## 1. Batas pengujian

Laporan ini membedakan tiga lapisan:

1. **Verifikasi referensi manual:** memeriksa isi JSON dan kunci 60 kasus. Hasil historisnya 60/60, tetapi tidak menjalankan API.
2. **Uji unit runtime fondasi:** memanggil fungsi Python `lookup_word()`, `inspect_spelling()`, dan `classify_word_in_context()` secara langsung melalui tes otomatis.
3. **Uji chatbot/playground:** menguji perilaku ILIS melalui percakapan. Ini belum dilakukan oleh rangkaian uji fondasi ini.

Keberhasilan tes unit tidak boleh disebut sebagai bukti bahwa kemampuan baru sudah terintegrasi ke chatbot atau mampu menangani semua variasi bahasa Indonesia.

## 2. Kemampuan runtime yang benar-benar tersedia

| API | Kemampuan yang diuji | Batas |
|---|---|---|
| `lookup_word(word)` | Pencarian bentuk kata persis pada referensi; status `found`, `ambiguous`, atau `unknown` | Tidak menganalisis fungsi kata dalam kalimat dan tidak melakukan stemming/morfologi |
| `inspect_spelling(text)` | Pemeriksaan parsial EJA-04 untuk nama hari/bulan pada pola tanggal eksplisit | Tidak memeriksa 11 aturan ejaan lain; tidak menulis ulang teks |
| `classify_word_in_context(text, target_span)` | Disambiguasi kata `dekat` untuk dua pola struktural yang disetujui | Bukan classifier umum; wajib menerima span token eksplisit; pola lain tetap `needs_context` |

Semua fungsi membaca file referensi secara langsung. Tes read-only memastikan byte JSON tidak berubah akibat operasi baca.

## 3. Pemetaan ulang Bagian A — 30 kasus kelas kata

- **T1-K-001 sampai T1-K-028:** tetap dapat diperiksa melalui pencarian persis `lookup_word()`. Tes cakupan memeriksa seluruh 152 entri referensi dan keberadaan seluruh 11 kelas kata.
- **T1-K-029 — “Rumah itu dekat.”:** kini diuji melalui classifier dan diharapkan `classified: adjektiva`.
- **T1-K-030 — “Mereka duduk dekat rumah.”:** kini diuji secara eksplisit sebagai regresi dari paket 60 kasus. Pola pronomina + verba + `dekat` + nomina cocok dengan pola terbatas yang disetujui; hasil diharapkan `classified: preposisi`.

Catatan: dua kasus kontekstual tersebut hanya membuktikan dua contoh/pola yang disetujui. Hasil ini tidak membuktikan bahwa classifier mampu menentukan kelas kata semua kata atau semua konstruksi yang memakai `dekat`.

## 4. Pemetaan ulang Bagian B — 20 kasus ejaan

Pemeriksa ejaan sekarang memiliki cakupan nyata untuk EJA-04 saja.

Tes EJA-04 memuat 16 kalimat kandidat dengan 20 temuan token:
- **10 `issue`:** kapitalisasi nama hari/bulan salah pada pola tanggal yang dikenali.
- **4 `no_issue`:** kapitalisasi benar pada pola tanggal yang dikenali.
- **6 `needs_context`:** nama hari/bulan muncul tanpa pola tanggal yang cukup jelas.

Angka tersebut adalah distribusi status temuan pada paket EJA-04, bukan skor akurasi untuk 20 kasus ejaan lama.

**Status 20 kasus ejaan lama:** belum dapat dinyatakan lulus sebagai tugas pemeriksaan ejaan lengkap. Sebagian besar meminta kemampuan yang masih ditunda, seperti kapitalisasi awal kalimat, nama orang/tempat, pemisahan kata depan, awalan `di-`, tanda baca, atau sapaan/kekerabatan. EJA-04 hanya boleh memberi temuan pada pola tanggal eksplisit; kata hari/bulan di luar pola tersebut dapat menghasilkan `needs_context`, bukan koreksi yang dipaksakan.

Batas penting:
- Tidak ada `corrected_text` atau penulisan ulang.
- `Awas?` tetap persis; tanda tanya tidak diubah menjadi tanda seru.
- Bentuk numerik seperti `05/10/2026` belum menjadi pola yang diperiksa.
- EJA-01–03 dan EJA-05–12 tetap ditunda.

## 5. Pemetaan ulang Bagian C — 10 kasus khusus

| Kasus | Status runtime saat ini |
|---|---|
| T1-X-001 `lima belas` | Dapat diperiksa sebagai bentuk yang tercantum melalui lookup persis; bukan analisis numeralia dalam kalimat |
| T1-X-002 `kah` vs `-kah` | Lookup dapat membedakan bentuk bebas yang tidak ditemukan dari bentuk terikat yang terdaftar |
| T1-X-003 placeholder kata tidak ada | Tetap kasus batas konsep; bukan token leksikal konkret |
| T1-X-004 `tiga puluh` | Dapat diperiksa melalui lookup persis sesuai entri referensi |
| T1-X-005 `-lah` | Dapat diperiksa melalui lookup persis |
| T1-X-006 `-tah` | Dapat diperiksa melalui lookup persis |
| T1-X-007 “Rumah itu dekat.” | Didukung oleh pola adjektiva terbatas |
| T1-X-008 “Duduk dekat rumah.” | Belum didukung pola yang disetujui; harus tetap `needs_context` |
| T1-X-009 `ditulis` | Bentuk tidak ditemukan sebagai entri dasar; API tidak melakukan analisis morfologi |
| T1-X-010 `para siswa` | `para` dapat ditemukan; `siswa` tetap `unknown` dalam referensi ini |

`unknown` berarti belum tercantum dalam referensi Tahap 1, bukan berarti kata tersebut bukan bahasa Indonesia.

## 6. Gerbang keselamatan dan regresi

Rangkaian tes saat ini mencakup:
- 16 kasus spesifikasi disambiguasi `dekat`;
- dua kasus kontekstual asli T1-K-029 dan T1-K-030 sebagai regresi;
- target berulang dengan span eksplisit;
- span salah/parsial, offset Unicode, emoji, dan variasi kapitalisasi;
- token tidak dikenal dan kata terdaftar di luar cakupan classifier;
- 16 kasus EJA-04 dan kasus keselamatan lintas aturan;
- pembacaan ulang referensi dan pemeriksaan bahwa JSON tidak dimodifikasi.

Kasus yang belum didukung atau ambigu harus mempertahankan status konservatif. Status `needs_context` bukan kegagalan jika memang bukti yang tersedia belum cukup.

## 7. Kesimpulan dan tindak lanjut

1. Fondasi pencarian kata tetap terbatas pada pencarian bentuk persis.
2. EJA-04 sudah memiliki pemeriksaan parsial yang dapat diuji, tetapi 11 aturan lain belum diimplementasikan.
3. Disambiguasi kontekstual kini dapat menangani dua pola untuk `dekat`; bukan classifier umum.
4. Kasus T1-K-029 dan T1-K-030 perlu tetap menjadi regresi wajib.
5. Tahap berikutnya adalah meninjau keluaran uji dan kesesuaian kunci, bukan langsung memperluas cakupan kata atau aturan.
6. Integrasi ke Semantic 12, Reasoning 6, ChatbotAdapter, KnowledgeEngine, dan playground tetap di luar cakupan dan memerlukan rancangan serta persetujuan terpisah.

**Status Tahap 1: BELUM SELESAI.** Laporan ini memperbarui peta kemampuan runtime dan tidak mengesahkan promosi JSON referensi ke runtime.
