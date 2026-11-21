# AUDIT AWAL PILOT MAKNA DAN CONTOH — 5 ENTRI TAHAP 1

**Branch:** `ilis-v2-development`  
**Status:** Dokumen persiapan pilot — BELUM mengubah dataset  
**Acuan format:** `docs/USULAN_FORMAT_MAKNA_CONTOH_TAHAP_01.md`  
**Acuan entri:** `data/reference/tahap_01_fondasi/kata_dasar.json`  
**Versi metadata saat audit:** `versi_format: 1.0`, `versi_data: 1.0`  
**Tanggal pemeriksaan sumber:** 2026-11-21

---

## 1. Tujuan dan batas

Dokumen ini menyiapkan pilot lima entri sebelum migrasi data format 1.1. Lima entri dipilih untuk mencakup lima bentuk uji yang disebut dalam spesifikasi:

1. satu kelas kata dengan satu makna;
2. satu kelas kata dengan dua makna;
3. satu lema dengan dua kelas kata;
4. partikel terikat;
5. bentuk multi-kata.

**Dokumen ini bukan migrasi data.** Tidak ada entri di `kata_dasar.json` yang diubah. Tidak ada versi yang dinaikkan. Tidak ada perubahan kode/runtime, Semantic 12, Reasoning 6, KnowledgeEngine, ChatbotAdapter, playground, atau `main`.

Definisi dan contoh di bawah adalah **calon kurasi untuk dievaluasi**, bukan data final yang sudah disahkan.

## 2. Daftar sampel dan hasil pemeriksaan awal

| Entri | Bentuk uji | Data lama | Hasil pemeriksaan awal |
|---|---|---|---|
| `buku` | Satu kelas, satu makna | nomina | Sumber resmi mendukung makna benda berupa lembaran berjilid. Kandidat relatif siap dievaluasi. |
| `jalan` | Satu kelas, dua makna | nomina | Sumber resmi mendukung beberapa makna nomina; dua makna dasar dipilih sebagai kandidat, bukan seluruh makna kamus. |
| `dekat` | Dua kelas | adjektiva, preposisi | KBBI VI Daring yang diperiksa memberi label adjektiva. Dukungan kelas preposisi belum ditemukan pada sumber yang diperiksa. Jangan mengisi uraian preposisi sebelum evaluator menyelesaikan perbedaan ini. |
| `-kah` | Partikel terikat | partikel | KBBI VI Daring memberi dua fungsi bentuk terikat. Contoh harus melekat pada kata sebelumnya sesuai ejaan. |
| `lima belas` | Bentuk multi-kata | numeralia | Daftar dasar memberi catatan bahwa ini bilangan majemuk, bukan satu kata dasar tunggal. Rujukan kamus resmi untuk lema gabungan persis belum terverifikasi. |

## 3. Kandidat kurasi untuk evaluasi

### 3.1 `buku` — nomina, satu makna

**Parafrasa definisi kandidat:** kumpulan lembaran yang disatukan atau dijilid dan memuat tulisan, gambar, atau keduanya.

**Contoh kandidat:** “Buku itu tebal.”

**Rujukan yang diperiksa:**
- Nama sumber: KBBI VI Daring.
- Entri: `buku`, entri `buku¹`, makna nomina pertama.
- URL: https://kbbi.kemendikdasmen.go.id/entri/buku
- Tanggal akses: 2026-11-21.

Catatan: KBBI juga memuat homonim `buku²` dan `buku³` dengan makna lain. Pilot ini hanya menguji satu makna nomina umum yang relevan untuk Tahap 1; tidak menggabungkan homonim tersebut secara otomatis.

### 3.2 `jalan` — nomina, dua makna

**Makna kandidat 1 — definisi:** tempat yang disediakan untuk lalu lintas orang atau kendaraan.

**Contoh kandidat:** “Jalan itu sempit.”

**Makna kandidat 2 — definisi:** cara atau sarana untuk mencapai sesuatu.

**Contoh kandidat:** “Cari jalan lain.”

**Rujukan yang diperiksa:**
- Nama sumber: KBBI VI Daring.
- Entri: `jalan`, entri `jalan¹`, makna nomina nomor 1 dan nomor 8.
- URL: https://kbbi.kemendikdasmen.go.id/entri/jalan
- Tanggal akses: 2026-11-21.

Catatan: Definisi ditulis ulang secara ringkas. Evaluator perlu memastikan kedua makna cukup berbeda untuk menjadi dua objek `makna` dalam kelas `nomina`, serta contoh benar-benar mewakili makna masing-masing.

### 3.3 `dekat` — adjektiva dan preposisi

**Kandidat adjektiva — definisi:** memiliki jarak yang pendek atau tidak jauh.

**Contoh kandidat:** “Rumahnya dekat.”

**Rujukan yang diperiksa:**
- Nama sumber: KBBI VI Daring.
- Entri: `dekat`, makna adjektiva nomor 1.
- URL: https://kbbi.kemendikdasmen.go.id/entri/dekat
- Tanggal akses: 2026-11-21.

**Status kelas preposisi: BELUM TERVERIFIKASI.**

Dataset lama mencatat `dekat` sebagai adjektiva dan preposisi, tetapi halaman KBBI VI Daring yang diperiksa hanya menampilkan label adjektiva. Karena field lama `jenis` tidak boleh diubah dalam pilot ini, jangan menghapus label preposisi dan jangan pula membuat definisi/rujukan preposisi berdasarkan intuisi.

Keputusan yang diminta dari evaluator:
- apakah ada rujukan kebahasaan lain yang sah dan cukup untuk mendukung kelas preposisi;
- apakah kelas tersebut perlu ditandai sebagai isu kurasi dan dibiarkan tanpa `uraian_per_jenis` selama pilot;
- atau apakah perlu evaluasi terpisah atas label kelas lama.

### 3.4 `-kah` — partikel terikat

**Definisi kandidat:** bentuk terikat yang ditambahkan pada kata sebelumnya untuk mengukuhkan atau memperhalus pertanyaan.

**Contoh kandidat:** “Siapakah namamu?”

**Rujukan yang diperiksa:**
- Nama sumber: KBBI VI Daring.
- Entri: `-kah`, makna 1 dan 2.
- URL: https://kbbi.kemendikdasmen.go.id/entri/kah
- Tanggal akses: 2026-11-21.

Catatan: Contoh menampilkan bentuk yang sudah melekat pada kata sebelumnya. Bentuk `-kah` tidak boleh diperlakukan sebagai kata bebas. Evaluator perlu menentukan apakah dua fungsi dalam sumber perlu menjadi satu makna ringkas untuk cakupan Tahap 1 atau dua makna terpisah.

### 3.5 `lima belas` — numeralia, bentuk multi-kata

**Status definisi dan rujukan: MENUNGGU VERIFIKASI.**

Daftar dasar Tahap 1 menyebut `lima belas` sebagai bentuk bilangan majemuk, bukan satu kata dasar tunggal. Ini penting untuk menguji apakah format entri dapat mempertahankan bentuk multi-kata tanpa mengubahnya menjadi lema tunggal.

**Contoh kandidat:** “Umurnya lima belas tahun.”

Rujukan langsung KBBI VI Daring untuk lema gabungan persis `lima belas` belum berhasil diverifikasi pada pemeriksaan ini. Jangan mengisi objek makna final atau mengarang URL/lokator. Perlu rujukan yang secara eksplisit mendukung bentuk numeralia gabungan tersebut, atau keputusan evaluator tentang sumber kebahasaan alternatif.

## 4. Temuan lintas-sampel

1. **Sumber harus diperiksa per kelas dan per makna.** Satu halaman kamus yang tidak mendukung suatu kelas tidak boleh dipakai seolah-olah mendukung kelas itu.
2. **Homonim tidak otomatis menjadi makna dalam satu kelas yang sama.** Contoh `buku` menunjukkan perlunya membedakan nomor entri/homonim.
3. **Dua makna `jalan` dipilih dari kelas nomina yang sama.** Pemilihan ini perlu dinilai berdasarkan relevansi Tahap 1, bukan banyaknya makna dalam kamus.
4. **Kelas lama tidak diubah diam-diam.** Ketidaksesuaian kelas `dekat` dicatat sebagai isu, bukan diselesaikan dengan menghapus atau menambah label.
5. **Bentuk multi-kata perlu sumber yang tepat.** Statusnya sebagai bentuk gabungan sudah tercatat pada dokumen daftar dasar, tetapi definisi dan sumber lema persis masih harus diperiksa.
6. **Contoh adalah kandidat buatan untuk ILIS.** Contoh harus diperiksa dari sisi kealamian, kecocokan makna, ejaan, dan batas 2–5 kata.

## 5. Gerbang sebelum file data pilot dibuat

Jangan membuat atau mengubah file data pilot format 1.1 sebelum evaluator memberi keputusan atas:

1. kelayakan definisi dan contoh `buku`;
2. pemisahan dua makna nomina `jalan`;
3. bukti kelas preposisi `dekat` atau perlakuan yang tepat terhadap isu tersebut;
4. apakah fungsi `-kah` digabung atau dipisah menjadi dua makna;
5. sumber yang mendukung `lima belas` sebagai numeralia gabungan;
6. format rujukan dan metadata yang wajib dicatat per makna.

Setelah keputusan evaluator, buat file pilot terpisah berisi tepat lima entri. Jangan mengubah 152 entri sumber pada tahap itu. Pertahankan `versi_format: 1.0` pada file sumber sampai struktur 1.1 benar-benar diterapkan melalui PR data yang disetujui. Setiap perubahan versi harus mengikuti spesifikasi versi yang telah disetujui.

## 6. Permintaan evaluasi Dola

Mohon evaluasi dokumen persiapan ini saja. Fokus pada ketepatan pemilihan sampel, kualitas kandidat definisi/contoh, dan dua isu sumber yang belum tuntas. Belum ada permintaan untuk menyetujui isi data final atau migrasi massal.

**Keputusan yang dibutuhkan:** apakah lima sampel dan perlakuan terhadap temuan di atas sudah tepat untuk dilanjutkan ke file pilot terpisah, atau perlu revisi terlebih dahulu?
