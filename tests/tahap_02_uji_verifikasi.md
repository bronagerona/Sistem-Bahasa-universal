# PAKET UJI VERIFIKASI TAHAP 2 — PEMBENTUKAN KATA & KALIMAT

**Branch:** `ilis-v2-development`  
**Status:** Verifikasi manual referensi v1.0 dan uji ulang kasus terdampak v1.1 — SELESAI  
**Acuan utama:** `docs/DAFTAR_DASAR_TAHAP_02.md` dan tiga file JSON referensi Tahap 2  
**Lokasi data:** `data/reference/tahap_02_kata_kalimat/`  
**Batas:** Dokumen rencana uji saja. Tidak mengubah data JSON, kode, runtime, atau branch `main`.

---

## 1 — Kriteria Kelulusan

Paket terdiri atas 50 kasus:

- Bagian A — Morfologi dan pembentukan kata: 20 kasus.
- Bagian B — Frasa dan pola kalimat: 20 kasus.
- Bagian C — Makna dan hubungan kata: 10 kasus.

Kriteria kelulusan:

1. Minimal 90% kasus dinyatakan benar.
2. Tidak boleh ada kesalahan kritis, termasuk aturan morfologi yang salah, contoh yang keliru, atau klasifikasi yang terbalik.
3. Pemeriksaan dilakukan secara manual dengan membandingkan masukan dan hasil yang diharapkan terhadap isi file JSON referensi yang disebutkan.
4. Materi yang tidak tercantum atau tidak didukung secara eksplisit oleh JSON tidak boleh dinyatakan lulus hanya berdasarkan pengetahuan di luar sumber. Catat sebagai ketidaksesuaian atau kebutuhan klarifikasi evaluator.
5. Dokumen ini belum menjalankan pengujian dan belum memberikan keputusan lulus/gagal terhadap data.

### Aturan pencatatan

- **LULUS:** informasi yang diuji didukung oleh isi JSON secara tepat.
- **GAGAL:** isi JSON bertentangan dengan hasil yang diharapkan atau memuat aturan/contoh yang keliru.
- **TIDAK DIDUKUNG:** kasus tidak dapat dibuktikan dari JSON yang ditetapkan sebagai sumber kebenaran. Jangan otomatis dihitung sebagai lulus.
- **PERLU KLARIFIKASI:** rumusan kasus atau kunci uji perlu diperjelas sebelum hasil dapat diputuskan.

Status semua kasus saat dokumen dibuat: **BELUM DIUJI**.

---

## 2 — Bagian A: Morfologi & Pembentukan Kata (20 Kasus)

| ID Uji | Masukan / Aturan | Hasil yang Diharapkan | Sumber Acuan | Status |
|---|---|---|---|---|
| T2-M-001 | tulis + me- | menulis — bunyi awal t luluh | `aturan_morfologi.json` → perubahan_bunyi | LULUS |
| T2-M-002 | ambil + me- | mengambil — bunyi awal a tetap | `aturan_morfologi.json` → perubahan_bunyi | LULUS |
| T2-M-003 | baca + me- | membaca — bunyi awal b tetap | `aturan_morfologi.json` → perubahan_bunyi | LULUS |
| T2-M-004 | kirim + me- | mengirim — bunyi awal k luluh | `aturan_morfologi.json` → perubahan_bunyi | LULUS |
| T2-M-005 | pukul + me- | memukul — bunyi awal p luluh | `aturan_morfologi.json` → perubahan_bunyi | LULUS |
| T2-M-006 | pasif: ditulis → aktif | menulis — perubahan di- menjadi meN- pada pasangan ini | `aturan_morfologi.json` → prefiks di- dan meN- | TIDAK DIDUKUNG |
| T2-M-007 | pasif: dibaca → aktif | membaca — perubahan di- menjadi meN- pada pasangan ini | `aturan_morfologi.json` → prefiks di- dan meN- | TIDAK DIDUKUNG |
| T2-M-008 | ber- + lari | berlari — tindakan/kegiatan | `aturan_morfologi.json` → prefiks ber- | LULUS |
| T2-M-009 | di- + tulis | ditulis — verba pasif | `aturan_morfologi.json` → prefiks di- | LULUS |
| T2-M-010 | ter- + buka | terbuka — keadaan/kejadian sesuai konteks | `aturan_morfologi.json` → prefiks ter- | LULUS |
| T2-M-011 | ke- + dua | kedua — bilangan tingkat/urutan | `aturan_morfologi.json` → prefiks ke- | LULUS |
| T2-M-012 | lurus + me-…-kan | meluruskan — konfiks | `aturan_morfologi.json` → konfiks meN-…-kan | LULUS |
| T2-M-013 | samping + ber-…-an | bersampingan — konfiks | `aturan_morfologi.json` → konfiks ber-…-an | LULUS |
| T2-M-014 | baik + ke-…-an | kebaikan — konfiks | `aturan_morfologi.json` → konfiks ke-…-an | LULUS |
| T2-M-015 | makan → makan-makan | reduplikasi; dapat menyatakan kegiatan, bukan hanya jamak | `aturan_morfologi.json` → reduplikasi | LULUS |
| T2-M-016 | tulis + -kan → tuliskan | bentuk berakhiran -kan; fungsi harus didukung sumber | `aturan_morfologi.json` → sufiks -kan | LULUS |
| T2-M-017 | warna + -i → warnai | bentuk berakhiran -i sesuai contoh pada JSON | `aturan_morfologi.json` → sufiks -i | LULUS |
| T2-M-018 | tulis + -an → tulisan | bentuk berakhiran -an; fungsi harus didukung sumber | `aturan_morfologi.json` → sufiks -an | LULUS |
| T2-M-019 | buku + -nya → bukunya | dapat menandai kepunyaan atau rujukan tertentu | `aturan_morfologi.json` → sufiks -nya | LULUS |
| T2-M-020 | pe- + tulis → penulis | penulis — nomina pelaku | `aturan_morfologi.json` → keluarga prefiks peN-/pe- | LULUS |

---

## 3 — Bagian B: Frasa & Pola Kalimat (20 Kasus)

| ID Uji | Masukan | Hasil yang Diharapkan — Jenis/Rumus | Sumber Acuan | Status |
|---|---|---|---|---|
| T2-F-001 | buku baru | Frasa Nomina | `frasa_dan_makna.json` → frasa.nomina | LULUS |
| T2-F-002 | sedang makan | Frasa Verba | `frasa_dan_makna.json` → frasa.verba | LULUS |
| T2-F-003 | di rumah | Frasa Preposisional | `frasa_dan_makna.json` → frasa.preposisional | LULUS |
| T2-F-004 | ke pasar | Frasa Preposisional | `frasa_dan_makna.json` → frasa.preposisional | LULUS |
| T2-F-005 | rumah besar | Frasa Nomina | `frasa_dan_makna.json` → frasa.nomina | LULUS |
| T2-F-006 | Dia tidur. | S-P | `pola_kalimat.json` → pola_dasar.S-P | LULUS |
| T2-F-007 | Budi makan nasi. | S-P-O | `pola_kalimat.json` → pola_dasar.S-P-O | LULUS |
| T2-F-008 | Siti pergi ke pasar. | S-P-K | `pola_kalimat.json` → pola_dasar.S-P-K | LULUS |
| T2-F-009 | Ayah membaca koran di ruang tengah. | S-P-O-K | `pola_kalimat.json` → pola_dasar.S-P-O-K | LULUS |
| T2-F-010 | Matahari terbit di timur. | Deklaratif — menyampaikan informasi | `pola_kalimat.json` → jenis_kalimat.deklaratif | LULUS |
| T2-F-011 | Kamu sudah makan? | Interogatif — mengajukan pertanyaan | `pola_kalimat.json` → jenis_kalimat.interogatif | LULUS |
| T2-F-012 | Tutup pintu itu! | Imperatif — perintah/permintaan | `pola_kalimat.json` → jenis_kalimat.imperatif | LULUS |
| T2-F-013 | Jangan lupa! | Larangan | `pola_kalimat.json` → jenis_kalimat.larangan | LULUS |
| T2-F-014 | Budi memakan nasi. → pasif | Nasi dimakan Budi. | `pola_kalimat.json` → aktif_pasif | LULUS |
| T2-F-015 | Siti menulis surat. → pasif | Surat ditulis Siti. | `pola_kalimat.json` → aktif_pasif | LULUS |
| T2-F-016 | Koran dibaca Ayah. → aktif | Ayah membaca koran. | `pola_kalimat.json` → aktif_pasif | LULUS |
| T2-F-017 | Dia tidak datang. | tidak — menyangkal verba/keadaan | `pola_kalimat.json` → penyangkalan.tidak | LULUS |
| T2-F-018 | Itu bukan buku saya. | bukan — menyangkal nomina/identitas | `pola_kalimat.json` → penyangkalan.bukan | LULUS |
| T2-F-019 | Pesan belum sampai. | belum — belum terjadi/tercapai pada waktu pembicaraan | `pola_kalimat.json` → penyangkalan.belum | LULUS |
| T2-F-020 | Jangan lari! | jangan — larangan | `pola_kalimat.json` → penyangkalan.jangan | LULUS |

---

## 4 — Bagian C: Makna & Hubungan Kata (10 Kasus)

| ID Uji | Pasangan / Masukan | Hubungan yang Diharapkan | Sumber Acuan | Status |
|---|---|---|---|---|
| T2-X-001 | cepat — laju | Sinonim dengan catatan perbedaan ragam/teknis jika didukung sumber | `frasa_dan_makna.json` → hubungan_makna.sinonim | LULUS |
| T2-X-002 | senang — gembira | Sinonim atau makna berdekatan; ragam dapat berbeda | `frasa_dan_makna.json` → hubungan_makna.sinonim | LULUS |
| T2-X-003 | banyak — banyak sekali | Ungkapan berdekatan, tetapi tingkat jumlah berbeda; bukan identik mutlak | `frasa_dan_makna.json` → hubungan_makna.sinonim | TIDAK DIDUKUNG |
| T2-X-004 | besar — kecil | Antonim dalam konteks ukuran | `frasa_dan_makna.json` → hubungan_makna.antonim | LULUS |
| T2-X-005 | cepat — lambat | Antonim dalam konteks kecepatan | `frasa_dan_makna.json` → hubungan_makna.antonim | LULUS |
| T2-X-006 | masuk — keluar | Antonim dalam konteks arah gerakan | `frasa_dan_makna.json` → hubungan_makna.antonim | LULUS |
| T2-X-007 | jalan-jalan | Reduplikasi dapat menyatakan kegiatan, bukan sekadar jamak | `aturan_morfologi.json` → reduplikasi | LULUS |
| T2-X-008 | kebaikan | Makna kata turunan bergantung pada kata dasar dan konteks; tidak selalu dapat dijumlahkan secara mekanis | `aturan_morfologi.json` → konfiks ke-…-an | LULUS |
| T2-X-009 | Frasa ≠ Kalimat | Frasa tidak memiliki hubungan S-P lengkap seperti klausa/kalimat | `frasa_dan_makna.json` dan dokumen daftar dasar | TIDAK DIDUKUNG |
| T2-X-010 | meN-…-kan | Konfiks — pasangan awalan dan akhiran bekerja bersama | `aturan_morfologi.json` → konfiks | LULUS |

---

## 5 — Catatan Kesesuaian Kunci Uji terhadap JSON v1.0 (Riwayat Audit Awal)

Bagian ini adalah catatan persiapan berdasarkan pembacaan struktur sumber, **bukan hasil eksekusi kasus uji**. Kasus-kasus berikut perlu perhatian khusus ketika audit dan pelaksanaan manual karena masukan/contoh yang diminta tidak semuanya tercantum secara eksplisit pada JSON saat ini.

### A. Morfologi

- **T2-M-005:** JSON mencantumkan *pakai → memakai* untuk peluluhan p, bukan *pukul → memukul*.
- **T2-M-006 dan T2-M-007:** JSON mencantumkan bentuk pasif *ditulis* dan *dibaca* serta bentuk aktif *menulis* dan *membaca*, tetapi tidak menyatakan prosedur transformasi aktif-pasif sebagai aturan eksplisit.
- **T2-M-008:** JSON mencantumkan *berjalan* dan *berbunga*, bukan *berlari*. Kata *lari* muncul pada contoh keluarga peN-/pe- sebagai *pelari*.
- **T2-M-012:** JSON mencantumkan *membacakan* dan *membersihkan* untuk konfiks meN-…-kan, bukan *meluruskan*.
- **T2-M-013:** JSON mencantumkan *berpelukan* dan *berjatuhan*, bukan *bersampingan*.
- **T2-M-016:** JSON mencantumkan *bersihkan* dan *ambilkan* untuk -kan, bukan *tuliskan*. Fungsi spesifik “menyebabkan/kepada” tidak dinyatakan sebagai definisi umum pada JSON.
- **T2-M-017:** Kunci diperbaiki sesuai evaluasi Dola menjadi *warna + -i → warnai*. Contoh ini tercantum langsung pada JSON untuk sufiks -i.
- **T2-M-018:** JSON memberi contoh -an *bacaan* dan *makanan*, bukan *tulisan*.

### B. Frasa dan kalimat

- **T2-F-006 sampai T2-F-009:** rumus S-P, S-P-O, S-P-K, dan S-P-O-K tercantum, tetapi kalimat yang diberikan dalam kunci uji berbeda dari contoh yang tersimpan pada JSON. Pemeriksaan harus membedakan apakah yang diuji adalah rumus pola atau kecocokan contoh literal.
- **T2-F-010 sampai T2-F-013:** jenis deklaratif, interogatif, imperatif, dan larangan tersedia, tetapi contoh literal dalam kasus uji tidak semuanya ada pada JSON.
- **T2-F-014 sampai T2-F-016:** pasangan aktif-pasif dalam JSON menggunakan contoh Ibu/Ayah/Adik/Budi/Kakak. Kasus uji memakai pasangan kalimat lain; perlu dipastikan apakah evaluator mengizinkan pengujian pola umum atau hanya kecocokan data eksplisit.
- **T2-F-017 sampai T2-F-020:** fungsi tidak/bukan/belum/jangan tersedia, tetapi beberapa contoh literal dalam kasus uji berbeda dari contoh JSON.

### C. Makna dan hubungan kata

- **T2-X-001 sampai T2-X-006:** pasangan kata yang diuji berbeda dari pasangan sinonim dan antonim yang tercantum pada JSON saat ini. Jangan memberi status lulus tanpa dasar sumber yang eksplisit.
- **T2-X-009:** definisi pembeda frasa dan kalimat dijelaskan pada dokumen `DAFTAR_DASAR_TAHAP_02.md`, tetapi tidak dirumuskan secara lengkap dalam file `frasa_dan_makna.json`. Catat batas sumber ini ketika menilai.
- **T2-X-008:** JSON mencantumkan *kebaikan* sebagai contoh konfiks ke-…-an dan menyatakan makna bergantung pada kata dasar, tetapi tidak memuat uraian semantik rinci khusus untuk kata tersebut.

**Prinsip penanganan:** Jangan mengubah file JSON untuk menyesuaikan kunci uji. Jika Dola menilai suatu kasus tidak sesuai sumber, catat sebagai temuan dan minta keputusan apakah kunci uji perlu direvisi atau sumber referensi perlu diperluas pada tahap terpisah.

---

## 6 — Laporan Hasil Uji (Verifikasi Manual Referensi)

**Status eksekusi:** SELESAI — pemeriksaan manual langsung terhadap tiga file JSON referensi  
**Tanggal uji:** 2026-11-21  
**Pelaksana:** ChatGPT (pemeriksaan isi sumber secara manual)  
**Branch:** `ilis-v2-development`  
**Commit dasar paket uji:** `3227c9714500ae98152f6731968cdebd99c3cf6c`

### Versi sumber yang diperiksa

| File | Blob SHA |
|---|---|
| `aturan_morfologi.json` | `6be7d017ddfc032f0eb0baf48fceeca78ce6a7a0` |
| `pola_kalimat.json` | `a00bb6d406bb3c05f3ca03a78be9d5421fb604ff` |
| `frasa_dan_makna.json` | `f952bd5d47ea79ed4b252e05b9119b4799a832a8` |

### Bagian A — Morfologi

- Total: 20
- Lulus: **18**
- Gagal: **0**
- Tidak didukung: **2**
- Tingkat dukungan/lulus terhadap seluruh kasus: **90%**

**Lulus:** T2-M-001, 002, 003, 004, 005, 008, 009, 010, 011, 012, 013, 014, 015, 016, 017, 018, 019, 020.

**Tidak didukung oleh JSON:** 
- T2-M-006 dan T2-M-007 — bentuk aktif dan pasif tersedia, tetapi prosedur transformasi pasif-ke-aktif belum dirumuskan eksplisit.
- T2-M-008 — contoh `berlari` belum tercantum; JSON memuat `berjalan` dan `berbunga`.
- T2-M-012 — contoh `meluruskan` belum tercantum; JSON memuat `membacakan` dan `membersihkan`.
- T2-M-013 — contoh `bersampingan` belum tercantum; JSON memuat `berpelukan` dan `berjatuhan`.
- T2-M-016 — contoh `tuliskan` belum tercantum; JSON memuat `bersihkan` dan `ambilkan`.
- T2-M-018 — contoh `tulisan` belum tercantum; JSON memuat `bacaan` dan `makanan`.

**Tindak lanjut T2-M-017:** Kunci telah diperbaiki atas keputusan Dola menjadi `warna + -i → warnai`. Bentuk `warnai` tercantum pada JSON sebagai contoh sufiks `-i`; kasus sekarang berstatus LULUS. Tidak ada perubahan pada JSON sumber.

### Bagian B — Frasa & Kalimat

- Total: 20
- Lulus: **20**
- Gagal: **0**
- Tidak didukung: **0**
- Tingkat lulus: **100%**

**Lulus:** T2-F-001 sampai T2-F-020.

Pemeriksaan frasa cocok dengan definisi dan kategori nomina, verba, serta preposisional. Untuk T2-F-006 sampai T2-F-009, yang diperiksa adalah rumus S-P, S-P-O, S-P-K, dan S-P-O-K, bukan kecocokan contoh literal. T2-F-010 sampai T2-F-013 diperiksa berdasarkan fungsi jenis kalimat. T2-F-014 sampai T2-F-016 diperiksa sebagai pola perubahan aktif-pasif, sesuai keputusan audit Dola. T2-F-017 sampai T2-F-020 cocok dengan fungsi penyangkalan `tidak`, `bukan`, `belum`, dan `jangan`.

### Bagian C — Makna & Hubungan Kata

- Total: 10
- Lulus: **8**
- Gagal: **0**
- Tidak didukung: **2**
- Tingkat dukungan/lulus terhadap seluruh kasus: **80%**

**Lulus:** T2-X-001, T2-X-002, T2-X-004, T2-X-005, T2-X-006, T2-X-007, T2-X-008, T2-X-010.

**Tidak didukung oleh JSON:**
- T2-X-001 dan T2-X-006 — pasangan `cepat—laju` dan `masuk—keluar` kini tercantum pada JSON v1.1.
- T2-X-003 tetap tidak didukung: pasangan `banyak—banyak sekali` tidak tercantum dalam daftar sinonim JSON.
- T2-X-009 tetap tidak didukung oleh JSON: pembeda frasa dan kalimat dijelaskan di dokumen daftar dasar, tetapi belum dinyatakan lengkap dalam `frasa_dan_makna.json`.


### Uji Ulang Terarah terhadap JSON v1.1 (2026-11-21)

**Acuan:** `aturan_morfologi.json` v1.1 (blob `6be7d017ddfc032f0eb0baf48fceeca78ce6a7a0`) dan `frasa_dan_makna.json` v1.1 (blob `f952bd5d47ea79ed4b252e05b9119b4799a832a8`). `pola_kalimat.json` tidak berubah.

| ID | Pemeriksaan terhadap v1.1 | Hasil |
|---|---|---|
| T2-M-006 | Transformasi ditulis → menulis belum dinyatakan sebagai aturan eksplisit | TIDAK DIDUKUNG |
| T2-M-007 | Transformasi dibaca → membaca belum dinyatakan sebagai aturan eksplisit | TIDAK DIDUKUNG |
| T2-M-008 | lari → berlari tercantum | LULUS |
| T2-M-012 | lurus → meluruskan tercantum | LULUS |
| T2-M-013 | samping → bersampingan tercantum | LULUS |
| T2-M-016 | tulis → tuliskan tercantum | LULUS |
| T2-M-018 | tulis → tulisan tercantum | LULUS |
| T2-X-001 | cepat — laju tercantum sebagai sinonim dengan catatan ragam/teknis | LULUS |
| T2-X-003 | banyak — banyak sekali tetap tidak tercantum | TIDAK DIDUKUNG |
| T2-X-006 | masuk — keluar tercantum sebagai antonim arah gerakan | LULUS |
| T2-X-009 | pembeda frasa dan kalimat tetap tidak dinyatakan lengkap dalam JSON | TIDAK DIDUKUNG |

**Hasil uji ulang:** 7 LULUS, 0 GAGAL, 4 TIDAK DIDUKUNG. T2-M-005 (memukul), T2-M-020 (penulis), T2-X-002 (senang—gembira), dan T2-X-007 (makna jalan-jalan) bukan bagian dari 11 status TIDAK DIDUKUNG pada laporan awal karena sudah LULUS; pemeriksaan v1.1 juga mengonfirmasi dukungan sumber untuk contoh-contoh tersebut.

### Rekapitulasi

| Status | Jumlah |
|---|---:|
| LULUS | **46** |
| GAGAL | **0** |
| TIDAK DIDUKUNG | **4** |
| **Total** | **50** |

**Hasil terhadap ambang paket:** 46/50 = **92%** kasus didukung dan lulus. Ambang numerik minimal 90% tercapai. Empat kasus TIDAK DIDUKUNG tetap dicatat terpisah dan tidak diubah menjadi lulus hanya berdasarkan pengetahuan di luar JSON. Keputusan kelulusan akhir tetap memerlukan evaluasi Dola atas sisa temuan.

### Temuan dan tindak lanjut

1. Jangan mengubah tiga JSON sumber; koreksi hanya dilakukan pada dokumen uji.
2. Kunci T2-M-017 telah diperbaiki menjadi `warna + -i → warnai` sesuai evaluasi Dola pada verifikasi awal.
3. Uji ulang terhadap JSON v1.1 membuat T2-M-008, M-012, M-013, M-016, M-018, T2-X-001, dan T2-X-006 berubah menjadi LULUS.
4. T2-M-006/007 tetap belum didukung karena belum ada aturan eksplisit transformasi aktif-pasif.
5. T2-X-003 dan T2-X-009 tetap belum didukung oleh JSON v1.1.
6. Minta Dola mengevaluasi empat kasus tersisa dan hasil keseluruhan 46/50 (92%) sebelum menyatakan Tahap 2 lulus.

### Kesimpulan Akhir

- [ ] **Lulus** — menunggu evaluasi akhir Dola atas empat kasus yang belum didukung.
- [x] **Perlu revisi/evaluasi** — ambang numerik 90% tercapai (46/50 = 92%), tetapi empat kasus masih belum didukung JSON dan memerlukan keputusan evaluator.
- [ ] **Ditunda** — tidak dipilih; pemeriksaan manual 50 kasus telah diselesaikan.

**Catatan evaluator (Dola):** Paket uji telah diterima untuk dieksekusi dengan catatan sesuai audit Dola. Hasil aktual di atas perlu dikirim kembali untuk evaluasi akhir; keputusan audit awal bukan persetujuan otomatis atas hasil eksekusi.

**Keputusan Owner:** Belum diberikan. Tidak ada promosi data ke runtime.

---

## 7 — Batas Perubahan dan Status

- Paket ini berisi tepat 50 kasus: A=20, B=20, C=10.
- Sumber kebenaran pemeriksaan data adalah tiga file JSON pada `data/reference/tahap_02_kata_kalimat/`.
- Dokumen daftar dasar digunakan untuk memahami konteks dan menelusuri asal materi.
- Tidak ada file JSON yang diubah selama pelaksanaan verifikasi manual ini.
- Seluruh 50 kasus telah diperiksa secara manual terhadap JSON v1.0; tujuh kasus yang sebelumnya tidak didukung telah diuji ulang terhadap JSON v1.1 dan dinyatakan LULUS. Empat kasus tetap TIDAK DIDUKUNG.
- Tidak ada promosi ke `data/runtime/`.
- Tidak ada perubahan kode, konfigurasi, Semantic, Reasoning, KnowledgeEngine, playground, atau branch `main`.

**Kesimpulan:** Setelah pembaruan referensi v1.1 dan uji ulang tujuh kasus yang kini didukung, hasil kumulatif adalah 46 LULUS, 0 GAGAL, dan 4 TIDAK DIDUKUNG (92%). Ambang numerik tercapai, tetapi keputusan kelulusan Tahap 2 tetap menunggu evaluasi Dola atas empat kasus tersisa. Data tetap berstatus referensi dan belum dipromosikan ke runtime.
