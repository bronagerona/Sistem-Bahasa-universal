# PEMBARUAN DATA REFERENSI TAHAP 2 — RENCANA v1.1

**Lokasi:** `data/reference/tahap_02_kata_kalimat/PEMBARUAN_v1.1.md`  
**Branch:** `ilis-v2-development`  
**Status:** DAFTAR RENCANA TAMBAHAN — BELUM DITERAPKAN  
**Acuan:** `docs/FORMAT_DATASET.md`, `docs/DAFTAR_DASAR_TAHAP_02.md`, tiga JSON referensi Tahap 2, dan `tests/tahap_02_uji_verifikasi.md`

---

## 1. Tujuan dan Kondisi Saat Ini

Dokumen ini mencatat 11 kebutuhan tambahan yang akan menjadi panduan pembaruan data referensi Tahap 2 versi 1.1. Dokumen ini **bukan pengganti** JSON versi 1.0 dan tidak mengaktifkan atau mempromosikan data ke runtime.

Hasil verifikasi manual Tahap 2 saat ini:

| Status | Jumlah |
|---|---:|
| LULUS | 39 |
| GAGAL | 0 |
| BELUM DIDUKUNG | 11 |
| **Total** | **50** |

- Dukungan saat ini: **39/50 (78%)**.
- Tidak ditemukan kasus GAGAL pada hasil verifikasi yang dirujuk.
- Sebelas kebutuhan di bawah dicatat untuk ditangani pada pembaruan terpisah.
- Seluruh JSON Tahap 2 saat ini tetap menjadi versi 1.0 dan berstatus `referensi`.

## 2. Daftar Tambahan yang Direncanakan

### A. Morfologi — Prefiks, Sufiks, dan Konfiks

| No. | Contoh/Aturan yang perlu ditambahkan | Jenis | Sumber kebutuhan | Status |
|---:|---|---|---|---|
| 1 | `memukul` (pukul + meN-) | Prefiks meN-; contoh peluluhan bunyi awal p | T2-M-005 | Belum ada sebagai contoh eksplisit; tambahkan nanti |
| 2 | `berlari` (lari + ber-) | Prefiks ber-; contoh kegiatan | T2-M-008 | Belum tercantum; tambahkan nanti |
| 3 | `meluruskan` (lurus + me-…-kan) | Konfiks me-…-kan | T2-M-012 | Belum tercantum; tambahkan nanti |
| 4 | `bersampingan` (samping + ber-…-an) | Konfiks ber-…-an | T2-M-013 | Belum tercantum; tambahkan nanti |
| 5 | `tuliskan` (tulis + -kan) | Sufiks -kan | T2-M-016 | Belum tercantum; tambahkan nanti |
| 6 | `tulisan` (tulis + -an) | Sufiks -an; contoh bentuk hasil | T2-M-018 | Belum tercantum; tambahkan nanti |
| 7 | `penulis` (tulis + peN-) | Prefiks peN-; nomina pelaku | T2-M-020 | Belum tercantum sebagai contoh eksplisit; tambahkan nanti |

**Catatan morfologi:** Saat menambahkan contoh, pastikan analisis kata dasar, jenis imbuhan, perubahan bunyi, dan kelas/fungsi katanya tepat. Jangan menyamakan sekadar kemiripan bentuk dengan aturan morfologi yang sama.

### B. Makna dan Hubungan Kata

| No. | Pasangan/konsep yang perlu ditambahkan | Jenis hubungan | Sumber kebutuhan | Status |
|---:|---|---|---|---|
| 8 | `cepat — laju` | Sinonim; sertakan catatan bahwa kesepadanan bergantung konteks pemakaian | T2-X-001 | Belum tercantum; tambahkan nanti |
| 9 | `senang — gembira` | Sinonim/makna berdekatan; jelaskan nuansa pemakaian bila diperlukan | T2-X-002 | Belum tercantum sebagai pasangan eksplisit; tambahkan nanti |
| 10 | `masuk — keluar` | Antonim dalam konteks arah gerakan | T2-X-006 | Belum tercantum; tambahkan nanti |
| 11 | `jalan-jalan` | Reduplikasi yang dapat menyatakan kegiatan, bukan sekadar bentuk jamak | T2-X-007 | Penjelasan makna perlu diperjelas nanti |

**Catatan makna:** Hubungan sinonim tidak selalu berarti dua kata dapat saling menggantikan dalam semua kalimat. Antonim harus diberi konteks hubungan yang dimaksud. Makna reduplikasi perlu dijelaskan berdasarkan fungsi dan konteks, bukan hanya bentuk pengulangan.

## 3. Rencana Lokasi Pembaruan

Pembaruan berikutnya diarahkan ke file referensi yang sudah ada:

| File | Materi yang direncanakan |
|---|---|
| `aturan_morfologi.json` | Tujuh contoh/penjelasan morfologi pada Bagian A |
| `frasa_dan_makna.json` | Tiga pasangan hubungan kata dan satu penjelasan makna reduplikasi pada Bagian B |

Pemetaan ini merupakan rencana lokasi, bukan izin untuk mengubah file sekarang. Struktur dan nama field harus mengikuti `docs/FORMAT_DATASET.md` serta struktur JSON yang berlaku ketika pembaruan benar-benar dilakukan.

## 4. Prinsip Pembaruan Versi 1.1

Ketika pembaruan ini kelak disetujui dan dilaksanakan:

1. **Jangan menghapus atau menimpa entri versi 1.0.**
2. Hanya tambahkan contoh atau penjelasan yang tercantum dalam daftar ini, setelah isi dan analisisnya diperiksa.
3. Naikkan penanda versi data/format dari `1.0` menjadi `1.1` sesuai skema yang berlaku.
4. Catat tanggal penambahan di dalam metadata JSON atau pada setiap entri baru sesuai struktur skema yang ditetapkan.
5. Pertahankan sumber, status, tahap, dan metadata wajib lainnya sesuai `docs/FORMAT_DATASET.md`.
6. Jangan mengubah status `referensi` menjadi `aktif` hanya karena versi data diperbarui.
7. Jangan mengubah kode, loader, Semantic, Reasoning, KnowledgeEngine, konfigurasi, atau branch `main` sebagai bagian dari pembaruan data ini tanpa rencana dan persetujuan terpisah.

## 5. Verifikasi Setelah Pembaruan

Setelah 11 tambahan benar-benar masuk ke JSON versi 1.1:

1. Jalankan ulang **hanya 11 kasus yang tercantum pada daftar ini**.
2. Bandingkan setiap kasus langsung dengan JSON versi 1.1; jangan mengandalkan pengetahuan di luar sumber.
3. Catat hasil masing-masing kasus dan versi/blob sumber yang diperiksa.
4. Jangan mengubah kunci uji atau menyatakan lulus hanya untuk mengejar target.
5. Jika seluruh 11 kasus didukung dan lulus, hasil kumulatif menjadi **50/50 (100%)**, dengan asumsi 39 hasil LULUS sebelumnya tetap berlaku dan tidak ada perubahan yang merusaknya.
6. Jika ada kasus yang belum didukung atau analisisnya keliru, catat sebagai temuan dan minta evaluasi Dola. Jangan memaksakan kelulusan.

## 6. Batas Dokumen Ini

Dokumen ini hanya daftar rencana tambahan. Pada saat dokumen ini dibuat:

- [x] Mencatat 11 kebutuhan tambahan.
- [x] Memetakan kebutuhan ke kasus uji dan file referensi tujuan.
- [x] Menetapkan prinsip pembaruan dan verifikasi mendatang.
- [ ] Menambahkan entri ke JSON — **BELUM DILAKUKAN**.
- [ ] Mengubah versi JSON menjadi 1.1 — **BELUM DILAKUKAN**.
- [ ] Menjalankan ulang 11 kasus — **BELUM DILAKUKAN**.
- [ ] Mempromosikan data ke runtime — **TIDAK TERMASUK DALAM TUGAS INI**.

**Kesimpulan:** Daftar pembaruan Tahap 2 v1.1 telah direncanakan. Ketiga JSON versi 1.0 tidak boleh diubah berdasarkan dokumen ini saja. Semua tambahan menunggu tahap pelaksanaan dan evaluasi tersendiri.
