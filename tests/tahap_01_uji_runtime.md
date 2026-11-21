# LAPORAN UJI RUNTIME TAHAP 1 — PEMETAAN 60 KASUS

**Branch pengujian:** `test/tahap-01-foundation-coverage`  
**Acuan:** `tests/tahap_01_uji_verifikasi.md`  
**Implementasi yang diuji:** `src/ilis/language/foundation.py`  
**Baseline implementasi:** merge PR #50 ke `ilis-v2-development`  
**Status:** pemetaan kemampuan runtime; bukan pengesahan Tahap 1 selesai

---

## 1. Tujuan dan batas

Laporan ini memisahkan dua hal yang sebelumnya mudah tercampur:

1. **Verifikasi referensi manual:** memeriksa apakah isi JSON dan aturan acuannya benar.
2. **Pengujian runtime:** memeriksa apakah API Python yang benar-benar tersedia dapat menjalankan kasus tersebut.

Status PASS pada pemeriksaan manual 60 kasus tidak otomatis berarti runtime telah menjalankan 60 kasus. API saat ini menyediakan pencarian bentuk kata persis (`lookup_word`), pemuatan aturan (`load_spelling_rules`), dan penyajian panduan ejaan (`inspect_spelling`). API belum menerima konteks kalimat untuk klasifikasi dan belum mendeteksi atau mengoreksi ejaan.

Status dalam laporan:
- **DIDUKUNG:** perilaku inti kasus dapat diperiksa langsung dengan API saat ini.
- **DIDUKUNG TERBATAS:** sebagian informasi tersedia, tetapi hasil yang diminta kasus belum dapat diputuskan sepenuhnya.
- **BELUM DIDUKUNG:** API saat ini belum memiliki kemampuan yang diperlukan.
- **TIDAK RELEVAN:** kasus berupa placeholder/batas konsep, bukan kata konkret yang perlu diklasifikasikan.

Tidak ada kasus yang diberi PASS runtime hanya karena referensinya tersedia.

## 2. Bagian A — Kelas kata (30 kasus)

| ID | Masukan | Status runtime | Alasan |
|---|---|---|---|
| T1-K-001 | buku | DIDUKUNG | Pencarian persis mengembalikan nomina |
| T1-K-002 | rumah | DIDUKUNG | Pencarian persis mengembalikan nomina |
| T1-K-003 | kucing | DIDUKUNG | Pencarian persis mengembalikan nomina |
| T1-K-004 | makan | DIDUKUNG | Pencarian persis mengembalikan verba |
| T1-K-005 | tidur | DIDUKUNG | Pencarian persis mengembalikan verba |
| T1-K-006 | tulis | DIDUKUNG | Pencarian persis mengembalikan verba |
| T1-K-007 | baik | DIDUKUNG | Pencarian persis mengembalikan adjektiva |
| T1-K-008 | dingin | DIDUKUNG | Pencarian persis mengembalikan adjektiva |
| T1-K-009 | tinggi | DIDUKUNG | Pencarian persis mengembalikan adjektiva |
| T1-K-010 | sering | DIDUKUNG | Pencarian persis mengembalikan adverbia |
| T1-K-011 | segera | DIDUKUNG | Pencarian persis mengembalikan adverbia |
| T1-K-012 | mungkin | DIDUKUNG | Pencarian persis mengembalikan adverbia |
| T1-K-013 | aku | DIDUKUNG | Pencarian persis mengembalikan pronomina |
| T1-K-014 | mereka | DIDUKUNG | Pencarian persis mengembalikan pronomina |
| T1-K-015 | siapa | DIDUKUNG | Pencarian persis mengembalikan pronomina |
| T1-K-016 | dua | DIDUKUNG | Pencarian persis mengembalikan numeralia |
| T1-K-017 | pertama | DIDUKUNG | Pencarian persis mengembalikan numeralia |
| T1-K-018 | di | DIDUKUNG TERBATAS | Kata terdaftar sebagai preposisi; API tidak memeriksa fungsi dalam kalimat |
| T1-K-019 | dari | DIDUKUNG | Pencarian persis mengembalikan preposisi |
| T1-K-020 | kepada | DIDUKUNG | Pencarian persis mengembalikan preposisi |
| T1-K-021 | karena | DIDUKUNG | Pencarian persis mengembalikan konjungsi |
| T1-K-022 | tetapi | DIDUKUNG | Pencarian persis mengembalikan konjungsi |
| T1-K-023 | aduh | DIDUKUNG | Pencarian persis mengembalikan interjeksi |
| T1-K-024 | halo | DIDUKUNG | Pencarian persis mengembalikan interjeksi |
| T1-K-025 | sang | DIDUKUNG | Pencarian persis mengembalikan artikula |
| T1-K-026 | para | DIDUKUNG | Pencarian persis mengembalikan artikula |
| T1-K-027 | -kah | DIDUKUNG | Bentuk berhubung tercatat sebagai partikel |
| T1-K-028 | dong | DIDUKUNG | Pencarian persis mengembalikan partikel |
| T1-K-029 | dekat (adjektiva) | DIDUKUNG TERBATAS | API mengembalikan dua kelas; belum menggunakan kalimat untuk memilih adjektiva |
| T1-K-030 | dekat (preposisi) | DIDUKUNG TERBATAS | API mengembalikan dua kelas; belum menggunakan kalimat untuk memilih preposisi |

**Rekap Bagian A:** 26 didukung langsung, 4 didukung terbatas. Tidak ada klaim bahwa kasus berkonteks telah diputuskan oleh runtime.

## 3. Bagian B — Ejaan dan penulisan (20 kasus)

Seluruh 20 kasus pada paket manual meminta sistem menghasilkan atau menilai bentuk ejaan yang benar dalam konteks kalimat. `inspect_spelling` saat ini hanya mengembalikan inventaris 12 aturan, menandai `reference_guidance_only`, mengembalikan `findings: []`, dan tidak mengubah masukan.

**Rekap Bagian B: 0 didukung sebagai pemeriksa/korektor runtime; 20 BELUM DIDUKUNG.**

Ini bukan 20 kegagalan algoritme yang sudah tersedia. Ini adalah kemampuan yang belum diimplementasikan. Karena itu, skor PASS/FAIL runtime tidak boleh diberikan untuk bagian ini.

## 4. Bagian C — Kasus khusus dan batas (10 kasus)

| ID | Masukan/tujuan | Status runtime | Alasan |
|---|---|---|---|
| T1-X-001 | lima belas | DIDUKUNG | Pencarian persis mengembalikan numeralia dan catatan bentuk majemuk |
| T1-X-002 | kah vs -kah | DIDUKUNG | `kah` unknown; `-kah` ditemukan sebagai partikel |
| T1-X-003 | placeholder kata tidak ada | TIDAK RELEVAN | Placeholder bukan token leksikal; prinsip unknown diuji melalui kasus masukan tak terdaftar |
| T1-X-004 | tiga puluh | DIDUKUNG | Pencarian persis mengembalikan numeralia dan catatan bentuk majemuk |
| T1-X-005 | -lah | DIDUKUNG | Bentuk terikat tercatat sebagai partikel |
| T1-X-006 | -tah | DIDUKUNG | Bentuk terikat tercatat sebagai partikel |
| T1-X-007 | dekat sebagai adjektiva dalam kalimat | DIDUKUNG TERBATAS | API hanya menyatakan dua kemungkinan kelas |
| T1-X-008 | dekat sebagai preposisi dalam kalimat | DIDUKUNG TERBATAS | API hanya menyatakan dua kemungkinan kelas |
| T1-X-009 | ditulis vs tulis | DIDUKUNG TERBATAS | `tulis` dan aturan awalan tersedia, tetapi API tidak menganalisis morfologi `ditulis` |
| T1-X-010 | para dan siswa | DIDUKUNG | `para` ditemukan; `siswa` unknown tanpa klaim bahwa kata itu bukan bahasa Indonesia |

**Rekap Bagian C:** 6 didukung langsung, 3 didukung terbatas, 1 tidak relevan.

## 5. Kesimpulan cakupan runtime

| Bagian | Total | Didukung langsung | Didukung terbatas | Belum didukung / tidak relevan |
|---|---:|---:|---:|---:|
| A — Kelas kata | 30 | 26 | 4 | 0 |
| B — Ejaan | 20 | 0 | 0 | 20 |
| C — Kasus khusus | 10 | 6 | 3 | 1 |
| **Total** | **60** | **32** | **7** | **21** |

Angka di atas adalah **pemetaan cakupan**, bukan skor akurasi runtime. Tidak tepat mengubahnya menjadi persentase kelulusan karena 20 kasus ejaan dan kasus kontekstual memerlukan kemampuan yang belum tersedia.

## 6. Celah kemampuan untuk pekerjaan berikutnya

1. **Klasifikasi kontekstual:** API perlu menerima kata beserta kalimat/contoh pemakaian, lalu mengembalikan kelas yang didukung konteks atau meminta konteks tambahan.
2. **Pemeriksaan ejaan berbasis aturan:** mulai dari aturan yang eksplisit dan deterministik dalam JSON; keluaran harus menunjukkan temuan, aturan pemicu, dan alasan. Jangan melakukan koreksi diam-diam.
3. **Pemetaan paket uji:** setelah kemampuan di atas tersedia, jalankan ulang kasus yang relevan dan simpan keluaran aktual secara verbatim.
4. **Batas referensi:** kata yang tidak ditemukan tetap `unknown`, bukan dinyatakan bukan bahasa Indonesia.

## 7. Batas perubahan dan status

- Laporan ini tidak mengubah kode produksi atau JSON referensi.
- Tidak ada integrasi ke Semantic, Reasoning, KnowledgeEngine, ChatbotAdapter, atau playground.
- Tidak ada promosi data dari `data/reference` ke `data/runtime`.
- Tidak ada perubahan ke `main`.
- PR ini hanya menambahkan pengujian dan dokumentasi cakupan.
- **Tahap 1 belum dinyatakan selesai.** Laporan ini adalah baseline untuk menentukan pekerjaan implementasi berikutnya.
