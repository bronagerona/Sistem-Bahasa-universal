# Pilar E — Evaluation Audit (90 Records)

> **Status:** DRAFT — menunggu review Dola  
> **Branch audit:** `audit-448-evaluation`  
> **Base branch:** `ilis-v2-development`  
> **Base SHA:** `7e5f78734a7e39496ef49035b627883bd7cb9959`  
> **Cakupan:** audit dokumentasi dan struktur; tidak mengubah JSONL, kode, tes, workflow, SQLite, atau branch `main`.

## 1. Ringkasan Eksekutif

Audit struktural mencakup 18 file `batch_001.jsonl` sampai `batch_018.jsonl`, total 90 record.

- 90/90 record berhasil diparse.
- 90/90 `evaluation_id` unik dan berurutan dari `eval-0006` sampai `eval-0095`.
- Semua record memiliki field inti yang diharapkan dan `verification_status: draft`.
- Pembagian split sudah ditulis, tetapi distribusinya terkonfounded dengan kelompok evaluasi.
- Ditemukan satu pasangan input identik di final_test: `eval-0010` dan `eval-0015`.
- Seluruh 18 record final_test secara eksplisit disebut konseptual/belum dijalankan sebagai tes otomatis.
- Tidak ada bukti penguncian operasional final_test dalam data/schema Pilar E yang diaudit.
- Pemeriksaan kemiripan otomatis internal tidak menemukan pasangan lintas split dengan kemiripan token tinggi pada ambang Jaccard 0,55. Pemindaian karakter trigram menghasilkan dua kandidat lemah yang perlu pemeriksaan manual; hasil heuristik ini bukan bukti bahwa tidak ada parafrasa semantik.
- Pemeriksaan lintas-pilar belum dapat dinyatakan tuntas. Spot-check menemukan setidaknya satu frasa contoh Pilar A yang muncul kembali di input evaluasi.

**Kesimpulan:** struktur JSONL rapi, tetapi Pilar E belum layak disebut dataset evaluasi final yang independen dan terkunci. Pembagian split perlu didesain ulang sebelum digunakan untuk mengukur kualitas secara sahih.

## 2. Inventaris dan Validasi Struktur

| Pemeriksaan | Hasil | Status |
|---|---:|---|
| File batch | 18 | PASS |
| Record | 90/90 | PASS |
| Record per batch | 5 | PASS |
| JSONL parse | 90/90 | PASS |
| ID unik | 90/90 | PASS |
| Rentang ID | eval-0006–eval-0095, tanpa celah | PASS |
| Field inti wajib | Lengkap pada 90 record | PASS |
| verification_status | 90 DRAFT | PASS |
| group vs test_group | Konsisten pada 90 record | PASS |

Folder juga memuat `sample.jsonl` dengan lima record terpisah (`eval-0001`–`eval-0005`). Lima sampel ini **tidak dihitung** ke dalam 90 record batch pada audit ini.

Catatan skema: `SCHEMA_TEMPORARY.md` mendeskripsikan field `test_group` dan `metric_name`, sedangkan `sample.jsonl` menggunakan bentuk awal `group` dan `metric`. Batch 001–018 memakai kedua pasangan field (`group` + `test_group`, serta `metric` + `metric_name`). Sebelum skema difinalkan, perlu ditetapkan field kanonis dan aturan kompatibilitas untuk sampel lama. Jika kelak ada loader, pastikan pemilihan file eksplisit agar `sample.jsonl` tidak ikut terhitung ganda atau diparse dengan skema berbeda.

## 3. Distribusi Split

| Kelompok | Development | Validation | Final-test | Total |
|---|---:|---:|---:|---:|
| Lexicon | 18 | 0 | 0 | 18 |
| Sentence patterns | 5 | 13 | 0 | 18 |
| Multi-turn | 13 | 5 | 0 | 18 |
| Knowledge | 0 | 18 | 0 | 18 |
| Regression | 0 | 0 | 18 | 18 |
| **Total** | **36** | **36** | **18** | **90** |

### Temuan kritis: split terkonfounded oleh kelompok

Pembagian 40% / 40% / 20% secara jumlah tampak teratur, tetapi jenis kasus tidak tersebar ke semua split:

- Lexicon hanya berada di development.
- Knowledge hanya berada di validation.
- Regression hanya berada di final_test.
- Sentence patterns dan multi-turn terbagi antara development dan validation, tetapi tidak masuk final_test.

Konsekuensinya:
1. Skor development dan validation tidak mengukur komposisi kemampuan yang sebanding.
2. Final-test tidak menguji holdout independen untuk Lexicon, Sentence Patterns, Multi-turn, atau Knowledge.
3. Kinerja pada final_test hanya akan mencerminkan kumpulan kasus regression konseptual, bukan kualitas keseluruhan Pilar E.
4. Perbandingan metrik lintas split berisiko salah ditafsirkan karena perbedaan split sekaligus berarti perbedaan jenis tugas.

**Rekomendasi:** buat desain ulang split berbasis kelompok dan keluarga kasus. Setiap kelompok yang memang akan dinilai perlu memiliki kasus independen di development, validation, dan final-test. Pemisahan harus dilakukan pada tingkat keluarga semantik/skenario, bukan sekadar membagi baris secara acak.

## 4. Duplikasi dan Kemiripan Prompt

### 4.1 Duplikasi persis

Ditemukan satu pasangan input identik:

| Record | Split | Input |
|---|---|---|
| eval-0010 | final_test | Halo, apa kabar? |
| eval-0015 | final_test | Halo, apa kabar? |

Keduanya juga mengarah ke `baseline_v3_1_beta_greeting` dan memiliki tujuan evaluasi yang hampir sama. Dua record ini tidak boleh dihitung sebagai dua kasus independen. Salah satunya perlu dihapus atau diganti dengan kasus greeting yang berbeda setelah audit lengkap dan persetujuan revisi.

### 4.2 Pemindaian kemiripan internal

- Normalisasi teks menemukan 89 input unik dari 90 record karena satu duplikasi di atas.
- Perbandingan token lintas split tidak menemukan pasangan dengan Jaccard ≥ 0,55.
- Pemindaian karakter trigram menghasilkan dua pasangan kandidat lemah (skor 0,30–0,32); kemiripan tersebut tampak dipengaruhi kata umum dan perlu tinjauan manual, bukan otomatis dinyatakan bocor.
- Heuristik ini tidak dapat memastikan kesamaan makna/parafrasa. Hasilnya hanya penyaring awal.

### 4.3 Risiko kemiripan lintas-pilar

`target_ref` menghubungkan kasus evaluasi ke record Pilar A–D. Ini berguna untuk provenance, tetapi juga menimbulkan risiko bila input evaluasi memakai ulang contoh yang sama dengan record target yang dipakai dalam pengembangan.

Spot-check menemukan:
- `eval-0006` memuat frasa “Kabar itu menyenangkan keluarga” yang juga tercantum sebagai contoh pada `lex-0003`.
- `eval-0011` sangat dekat dengan contoh `lex-0008` (“Petugas itu ramah kepada pengunjung.”).

Temuan ini belum cukup untuk menyimpulkan seluruh 90 kasus bocor, tetapi cukup untuk menandai bahwa pemeriksaan lintas-pilar harus menjadi langkah wajib. Audit ini **belum mengklaim** telah menyelesaikan pencocokan semantik menyeluruh terhadap seluruh 270 record Pilar A–D.

## 5. Status Final-Test dan Risiko Kebocoran

Semua 18 record dengan `split: final_test` berada pada `group: regression`.

Semua 18 `expected_behavior` atau `source` menyebut bahwa kasus bersifat konseptual, bukan tes otomatis, atau belum dijalankan. Dengan demikian:

- `final_test` saat ini adalah label pembagian sementara, bukan bukti adanya suite final-test operasional.
- Tidak ada bukti pada folder/skema Pilar E yang diaudit tentang manifest penguncian, checksum/versi terkunci, atau gate yang mencegah final-test digunakan saat tuning.
- Belum ada bukti bahwa akses terhadap final-test dibatasi atau bahwa perubahan terhadap isinya diaudit.
- Karena seluruh final-test adalah regression, holdout independen lintas empat kelompok konten belum tersedia.

**Keputusan audit:** final-test belum dapat dinyatakan LOCKED. Jangan gunakan 18 record ini sebagai tolok ukur final atau sebagai dasar klaim performa. Perlakukan sebagai kandidat skenario regression konseptual yang perlu direvisi dan diimplementasikan terpisah.

## 6. Kualitas Definisi Metrik

- `group` dan `test_group` konsisten.
- `metric` berisi label deskriptif berbahasa Indonesia, sedangkan `metric_name` berisi identifier teknis berbahasa Inggris. Hubungan keduanya belum didokumentasikan sebagai kamus/metrik kanonis.
- Terdapat 84 nilai `metric_name` unik untuk 90 record; identifier generik `baseline_regression_count` dipakai berulang pada beberapa kasus regression awal.
- Satu identifier metrik generik untuk kasus yang menguji perilaku berbeda dapat mengaburkan pelaporan per-kemampuan. Disarankan setiap perilaku memiliki nama metrik yang spesifik atau menggunakan skema metrik bertingkat yang terdokumentasi.

Belum ada definisi operasional yang cukup untuk menghitung accuracy/F1 atau skor regression secara konsisten dari semua record. `expected_behavior` masih berupa deskripsi bahasa alami, bukan expected output terstruktur atau rubrik penilaian yang dapat dieksekusi.

## 7. Penilaian Audit

| Area | Penilaian | Catatan |
|---|---|---|
| Parsing dan integritas dasar | PASS | 90/90 valid, ID unik |
| Kelengkapan field dasar | PASS | Field inti terisi |
| Konsistensi split | REVISE | Split terkonfounded oleh group |
| Duplikasi internal | REVISE | eval-0010 dan eval-0015 identik |
| Kemiripan internal otomatis | REVIEW | Tidak ada pasangan kuat; heuristik tidak membuktikan independensi semantik |
| Kemiripan lintas-pilar | REVIEW | Spot-check menemukan potensi penggunaan ulang contoh; audit penuh belum selesai |
| Final-test terkunci | REVISE | 18/18 konseptual, belum dijalankan, tidak ada bukti lock operasional |
| Definisi metrik | REVIEW | Dua nama field dan identifier metrik perlu kamus/kontrak |
| Kesiapan integrasi | NOT APPROVED | Skema masih temporary; tidak ada izin integrasi |

## 8. Tindak Lanjut yang Direkomendasikan

1. Pertahankan semua record sebagai DRAFT selama audit.
2. Susun ulang split berbasis kelompok dan keluarga kasus; jangan mengubah/memindahkan JSONL sebelum review Dola dan persetujuan Owner.
3. Tandai `eval-0015` sebagai duplikasi dari `eval-0010`; usulkan satu kasus pengganti yang berbeda.
4. Lakukan pemeriksaan lintas-pilar untuk seluruh input evaluasi terhadap contoh pada Lexicon, Sentence Patterns, dan Dialogues serta terhadap isi Knowledge yang menjadi dasar pertanyaan.
5. Rancang final-test independen untuk seluruh kelompok yang akan diukur. Final-test harus disimpan terpisah, diberi versi/checksum, dan tidak digunakan untuk tuning.
6. Tetapkan kontrak skema final, kamus `metric` ↔ `metric_name`, rubrik penilaian, dan prosedur scoring sebelum membuat runner.
7. Jangan mengintegrasikan skema Pilar E ke ILIS, test suite, CI/workflow, atau SQLite pada tahap audit ini.

## 9. Batas Audit dan Jaminan Tidak Ada Perubahan Data

- Audit ini membaca 18 batch Pilar E dan dokumen skema sementara.
- Pemindaian duplikasi internal dilakukan pada 90 input Pilar E.
- Pencocokan lintas-pilar baru berupa spot-check; belum merupakan audit semantik menyeluruh A–D.
- Audit ini bukan eksekusi tes terhadap runtime ILIS.
- Tidak ada JSONL yang diubah.
- Tidak ada kode, tes, workflow, SQLite, atau `main` yang diubah.
- Seluruh 90 record tetap `verification_status: draft`.

## 10. Permintaan Review Dola

Mohon Dola meninjau:
1. Apakah diagnosis split terkonfounded dan rekomendasi split berbasis kelompok sudah tepat.
2. Apakah `eval-0010` dan `eval-0015` harus diperlakukan sebagai satu duplikasi yang perlu diganti.
3. Apakah status final-test “belum terkunci/belum operasional” sudah tepat.
4. Apakah prosedur audit lintas-pilar dan rancangan final-test independen cukup untuk menjadi dasar revisi setelah seluruh audit 448 record selesai.

**Status akhir sementara: Pilar E belum lulus sebagai evaluasi independen/final. Laporan ini menunggu review Dola; tidak mengubah isi dataset.**
