# AUDIT KETERLACAKAN RUNTIME TAHAP 1

**Tanggal audit:** 21 November 2026  
**Acuan branch:** `ilis-v2-development`  
**Acuan commit:** `bd810342694569426f7159b4612ed1c2826ab433`  
**Status:** Laporan audit kemampuan dan backlog — bukan deklarasi penyelesaian Tahap 1  
**Batas audit:** Dokumentasi kurikulum, spesifikasi Tahap 1, modul fondasi, referensi JSON, paket uji, dan bukti CI yang tersedia pada commit acuan.

---

## 1. Tujuan dan kesimpulan eksekutif

Audit ini membandingkan target Tahap 1 pada dokumen kurikulum dan implementasi dengan kemampuan runtime yang benar-benar tersedia serta bukti pengujiannya.

**Kesimpulan:** Tahap 1 telah memiliki fondasi runtime awal yang nyata dan diuji, tetapi **belum memenuhi seluruh target kurikulum**. Status yang tepat adalah *terimplementasi sebagian; belum lengkap*.

Kemampuan yang telah tersedia:
1. Lookup kata dasar secara persis dari referensi.
2. Pemeriksaan kapitalisasi EJA-04 pada pola tanggal eksplisit yang dibatasi.
3. Disambiguasi kelas kata untuk satu kata, `dekat`, melalui dua pola struktural yang sangat terbatas.

Kekurangan utama yang masih menghalangi penyelesaian penuh:
1. Entri kata dasar belum memiliki makna/penjelasan sederhana dan contoh penggunaan secara sistematis.
2. Fonologi dasar belum dibuktikan melalui kemampuan runtime dan paket uji khusus.
3. Sebelas aturan ejaan selain EJA-04 belum diimplementasikan sebagai pemeriksaan runtime.
4. Lookup kelas kata belum sama dengan kemampuan mengklasifikasikan kata dalam kalimat secara kontekstual.
5. Belum ada bukti bahwa kemampuan fondasi ini sudah terintegrasi dan tervalidasi melalui alur percakapan chatbot.

Laporan ini tidak mengusulkan penambahan fitur langsung. Fungsinya menetapkan kondisi aktual, pekerjaan tersisa, serta syarat evaluasi akhir.

## 2. Prinsip dan batas audit

Audit menggunakan prinsip berikut:

- **Dokumen bukan runtime.** Materi yang dijelaskan dalam dokumen atau dicatat dalam JSON tidak otomatis menjadi kemampuan yang berjalan.
- **Uji unit bukan uji percakapan.** Pemanggilan API fondasi secara langsung tidak membuktikan chatbot menggunakan kemampuan tersebut.
- **Jumlah entri bukan kelengkapan semantik.** Banyaknya kata atau kelas yang tercatat tidak membuktikan makna dan penggunaan kata telah dipahami.
- **Status konservatif dipertahankan.** `unknown` berarti tidak ditemukan dalam referensi yang tersedia, bukan berarti kata tersebut bukan bahasa Indonesia.
- **Tidak mengarang kemampuan.** Pola yang belum didukung harus tetap ditandai belum didukung atau memerlukan konteks.
- **Tidak memperluas cakupan.** Tahap 2–4, integrasi produksi, dan dataset pengetahuan umum berada di luar audit ini.

Audit bersifat inspeksi dokumentasi, kode, data, dan hasil uji yang sudah tersedia. Tidak ada kode, JSON referensi, atau konfigurasi runtime yang diubah untuk menyusun laporan ini.

## 3. Matriks keterlacakan kurikulum Tahap 1

| Target kurikulum/kemampuan | Kondisi dokumen/referensi | Kemampuan runtime dan bukti | Status audit |
|---|---|---|---|
| Lookup persis inventaris kata | 152 entri dalam `kata_dasar.json`, mencakup 11 label kelas | `lookup_word()` mengambil kelas dari entri yang cocok secara persis; diuji langsung. **Tidak mengembalikan makna**, karena makna belum tersedia dalam JSON | **TERPENUHI untuk lookup persis saja** |
| Pengenalan 26 huruf, vokal dan konsonan | Materi konseptual tersedia dalam dokumen kurikulum/penguatan | Belum ditemukan API pemeriksaan atau paket uji runtime khusus | **BELUM DIMULAI di runtime** |
| Diftong dan gabungan konsonan | Materi dan contoh dijelaskan pada dokumen penguatan | Belum ada pemeriksaan runtime dan paket uji khusus yang tervalidasi | **BELUM DIMULAI; ditunda** |
| Pemeriksaan ejaan umum | Dua belas aturan tekstual tercatat di `aturan_ejaan.json` | `inspect_spelling()` baru menjalankan EJA-04; EJA-01–03 dan EJA-05–12 belum diperiksa | **TERBATAS pada EJA-04** |
| Kapitalisasi nama hari/bulan dalam tanggal (EJA-04) | Aturan EJA-04 dijelaskan dalam spesifikasi | Berjalan pada pola tanggal eksplisit yang disetujui dan diuji | **TERBATAS pada pola yang disetujui** |
| Disambiguasi kelas kata berdasarkan konteks | Spesifikasi dan implementasi dibatasi khusus untuk `dekat` | Dua pola yang disetujui untuk `dekat`; memerlukan `target_span` eksplisit | **TERBATAS — bukan classifier umum** |
| Makna leksikal dasar setiap kata | Kurikulum meminta penjelasan/fungsi sederhana | Tidak ada field makna/penjelasan pada 152 entri yang diperiksa | **BELUM DIMULAI; backlog** |
| Contoh penggunaan singkat setiap kata | Kurikulum meminta contoh pemakaian | Tidak ada field contoh penggunaan pada 152 entri yang diperiksa | **BELUM DIMULAI; backlog** |

**Arti status pada matriks:** `TERPENUHI` hanya berlaku untuk kemampuan sempit yang disebut secara eksplisit; `TERBATAS` berarti implementasi berjalan pada sebagian cakupan/pola; `BELUM DIMULAI` berarti belum ada implementasi runtime yang dibuktikan. Status `TERPENUHI` pada lookup tidak boleh dibaca sebagai pemahaman makna atau klasifikasi kontekstual.

### 3.1 Inventaris kelas kata aktual

Pemeriksaan terhadap `kata_dasar.json` menemukan 152 entri dengan distribusi:

| Kelas kata | Jumlah |
|---|---:|
| Nomina | 20 |
| Verba | 20 |
| Adjektiva | 20 |
| Numeralia | 15 |
| Adverbia | 12 |
| Pronomina | 12 |
| Preposisi | 12 |
| Konjungsi | 12 |
| Interjeksi | 12 |
| Partikel | 12 |
| Artikula | 6 |
| **Total** | **152** |

Catatan artikula yang telah disepakati tetap berlaku: **6 tercatat dari 10 yang direncanakan; kelas terbatas, belum lengkap.** Tidak boleh menambah entri buatan hanya untuk mengejar jumlah rencana.

Kata `dekat` tercatat dengan dua kelas, adjektiva dan preposisi. Kata `sekolah` dan `sangat` tidak tercatat pada referensi saat audit; karena itu pola yang membutuhkan kata tersebut tidak boleh dinyatakan terdukung. Keputusan ini sudah dicerminkan dalam kunci uji yang diselaraskan melalui PR #56.

## 4. Audit kemampuan runtime aktual

### 4.1 Lookup kata dasar

API: `lookup_word()`

**Batas penting:** lookup saat ini mengembalikan informasi entri yang tersedia, terutama kelas kata. Ia **belum mengembalikan makna dasar**, karena field makna/penjelasan belum ada pada referensi 152 entri. Jadi status “lookup berjalan” tidak sama dengan “kamus makna sudah berjalan”.

Kemampuan yang dibuktikan:
- Pencarian bentuk kata secara persis pada file referensi.
- Hasil membedakan kata ditemukan, ambigu menurut data kelas, dan tidak ditemukan.
- Referensi dibaca ulang per operasi; tidak mengandalkan cache data yang menahan isi lama.
- Operasi bersifat baca-saja dan tidak mengubah JSON.

Batas:
- Ini bukan pemahaman makna kata.
- Ini bukan penentuan kelas kata dalam setiap kalimat.
- Hasil `unknown` hanya menyatakan tidak ada kecocokan pada referensi saat ini.
- Disambiguasi `dekat` **bukan sistem pemilah kelas kata**. Kemampuan ini hanya berlaku untuk kata `dekat` melalui dua pola yang disetujui; tidak berlaku untuk kata lain. Batas ini tidak boleh diperluas tanpa revisi spesifikasi dan persetujuan terpisah.

### 4.2 Pemeriksaan ejaan EJA-04

API: `inspect_spelling()`

Kemampuan yang dibuktikan:
- Pemeriksaan kapitalisasi nama bulan setelah tanggal numerik eksplisit.
- Pemeriksaan nama hari hanya pada pola tanggal eksplisit yang disetujui.
- Temuan membedakan `issue`, `no_issue`, dan `needs_context`.
- Input asli dipertahankan; tidak ada `corrected_text` atau pengubahan otomatis.
- Aturan yang belum diperiksa dinyatakan sebagai cakupan tertunda, bukan dianggap lulus.

Batas:
- EJA-04 bukan pemeriksa format tanggal numerik seperti `05/10/2026`.
- Nama hari/bulan di luar pola yang didukung tidak boleh diberi koreksi otomatis.
- **Hanya EJA-04 yang berjalan.** EJA-01–03 dan EJA-05–12 belum diimplementasikan sebagai pemeriksaan runtime. Jangan menganggap sistem sudah memeriksa ejaan lengkap.
- Pemeriksa belum boleh dipromosikan sebagai pemeriksa ejaan umum.

### 4.3 Disambiguasi kontekstual kata `dekat`

API: `classify_word_in_context(text, target_span)`

**Peringatan cakupan:** Disambiguasi `dekat` ≠ sistem pemilah kelas kata. Ini hanya satu kata, dua pola yang disetujui, dan belum berlaku umum. Batas ini tidak akan dihilangkan tanpa revisi dokumen terpisah.

Dua pola yang didukung:
1. Pola adjektiva terbatas: nomina/pronomina + `itu` + `dekat` pada akhir klausa sederhana, misalnya `Rumah itu dekat.`
2. Pola preposisi terbatas: pronomina + verba + `dekat` + nomina terdaftar, misalnya `Kami duduk dekat pintu.`

Batas:
- Hanya untuk kata `dekat`, bukan classifier umum.
- Pemanggil wajib memberikan `target_span`; fungsi tidak menebak kemunculan kata yang dimaksud jika ada pengulangan.
- Komponen pola harus didukung referensi aktual. Jika ada komponen yang tidak terdaftar atau strukturnya di luar pola, hasil konservatif adalah `needs_context` atau `unknown` sesuai kondisi.
- Tidak ada parser umum, analisis klausa mendalam, skor probabilitas, atau inferensi semantik bebas.

### 4.4 Integrasi ke chatbot

Uji yang tersedia terutama membuktikan API fondasi secara langsung. Audit ini tidak menemukan bukti yang cukup untuk menyatakan bahwa `lookup_word()`, `inspect_spelling()`, dan `classify_word_in_context()` sudah menjadi bagian dari alur percakapan chatbot yang aktif.

Karena itu, **kemampuan modul fondasi tidak boleh disamakan dengan kemampuan chatbot end-to-end**. Kebutuhan integrasi dan cara mengujinya harus diputuskan terpisah, setelah batas dan target Tahap 1 disepakati. Tidak ada integrasi yang diusulkan atau dilakukan oleh laporan ini.

## 5. Bukti pengujian dan cara membacanya

Bukti yang tersedia harus dibedakan berdasarkan jenisnya:

| Bukti | Hasil | Yang dibuktikan | Yang tidak dibuktikan |
|---|---|---|---|
| Verifikasi manual referensi Tahap 1 | 60/60 lulus pada pemeriksaan yang dilaporkan | Kunci verifikasi manual terhadap referensi yang diperiksa | Akurasi runtime atau chatbot |
| Uji unit fondasi | Termasuk lookup, validasi bentuk data, dan sifat baca-saja | Perilaku API fondasi yang dipanggil langsung | Pemahaman semua kata dalam kalimat |
| Uji khusus EJA-04 | Kasus positif, negatif, konteks, span, dan batas keselamatan | Perilaku pola EJA-04 yang disetujui | Sebelas aturan ejaan lain |
| Uji khusus classifier `dekat` | Kasus B-DEKAT, span eksplisit, kata tak dikenal, dan batas pola | Dua pola terbatas serta perilaku konservatifnya | Klasifikasi umum 11 kelas kata |
| Peta uji runtime pasca-PR #57 | 30 kasus kelas kata dipetakan; 20 kasus ejaan dipetakan; 10 kasus khusus dipetakan | Keterlacakan kasus manual ke API dan batas runtime | Kelulusan penuh seluruh target kurikulum |
| CI terbaru pada commit PR #59 | 646 passed, 1 xfailed, 1 warning, 0 failed | Seluruh suite pada commit PR tersebut berhasil dengan satu expected failure yang terdokumentasi | Penyelesaian seluruh kurikulum Tahap 1 |

CI yang menjadi bukti terakhir laporan ini:
- Workflow run #481, status SUCCESS.
- Commit yang diuji: `8fd155628deeb917d9a2a2418ecfb8bb9516ebd1` (head PR #59 sebelum merge).
- Hasil: 646 passed, 1 xfailed, 1 warning, 0 failed.
- Tautan: https://github.com/bronagerona/Sistem-Bahasa-universal/actions/runs/44897626001

Angka 646 adalah hasil keseluruhan suite proyek, bukan jumlah kasus kurikulum Tahap 1. Satu `xfail` merupakan expected failure yang sudah ditandai; bukan kegagalan baru EJA-04 atau classifier `dekat`. Peringatan yang tercatat tidak mengubah status test menjadi gagal, tetapi tetap merupakan catatan pemeliharaan.

## 6. Daftar pekerjaan tersisa menurut prioritas

Item backlog adalah pekerjaan yang dicatat secara transparan untuk keputusan dan pengembangan berikutnya. **Keberadaan backlog tidak otomatis menggagalkan penutupan Tahap 1**, sepanjang item tersebut diberi status dan dampak yang jelas serta setiap pengecualian dari target wajib disetujui secara eksplisit oleh Owner dan evaluator. Tanpa keputusan pengecualian tersebut, item yang ditetapkan wajib tetap menjadi target yang harus dipenuhi.

### P0 — Target wajib default sebelum penutupan, kecuali dikecualikan secara resmi

1. **Makna/penjelasan sederhana untuk entri kata dasar.** Tentukan definisi sederhana yang sesuai untuk setiap entri dan kelasnya. Untuk entri multi-kelas, makna/fungsi tiap kelas harus dibedakan atau dinyatakan memerlukan konteks.
2. **Contoh penggunaan singkat.** Sediakan contoh yang benar-benar menunjukkan penggunaan kata dan kelas yang dimaksud. Contoh harus ditinjau, tidak dibuat otomatis hanya demi mengisi kolom.
3. **Gerbang pengujian akhir yang dapat diaudit.** Setiap target yang dipertahankan sebagai wajib harus dipetakan ke kasus uji dan bukti runtime yang relevan. Kasus manual, unit API, dan chatbot end-to-end harus tetap dibedakan.

### P1 — Perluasan bertahap / keputusan cakupan

1. **Perluasan aturan ejaan EJA-01–03 dan EJA-05–12.** Implementasikan dan uji satu per satu setelah spesifikasi masing-masing disetujui; jangan menjadikannya klaim kemampuan sebelum benar-benar berjalan.
2. **Integrasi helper fondasi ke chatbot.** Putuskan secara terpisah apakah integrasi ini termasuk kriteria Tahap 1 atau tahap setelah fondasi; bila diwajibkan, buktikan dengan uji end-to-end.
3. **Caveat artikula 6/10.** Pertahankan catatan bahwa enam entri tercatat dari sepuluh yang direncanakan; jangan menambah entri tanpa validasi.

### P2 — Dapat ditunda / di luar jalur wajib saat ini

1. **Modul fonologi terpisah.** Materi dasar tetap tercatat dalam kurikulum, tetapi implementasi runtime fonologi dapat ditunda sebagai modul dan paket uji tersendiri; jangan mengklaim sudah berjalan.
2. **Classifier kata lain selain `dekat`.** Belum dimulai dan ditempatkan setelah Tahap 1 selesai, dengan spesifikasi dan evaluasi terpisah. Tidak ada perluasan otomatis dari pola `dekat`.
3. Analisis fonetik/bunyi yang lebih mendalam di luar cakupan dasar.
4. Perluasan pola kontekstual `dekat` atau parser umum sebelum ada kebutuhan dan spesifikasi baru.
5. Penyempurnaan status `ambiguous` pada API kontekstual. Definisi dokumentasinya tetap dipertahankan: `ambiguous` untuk beberapa kelas terdaftar tanpa bukti pembeda memadai; `needs_context` untuk informasi yang belum cukup memastikan pola yang dikenali. Implementasi saat ini memakai `needs_context` pada kasus konservatif dan belum membuktikan seluruh kontrak status.

## 7. Ketidaksinkronan dokumentasi yang perlu dirapikan

Audit menemukan beberapa label status atau uraian lama yang belum sepenuhnya mencerminkan implementasi terbaru:
- `docs/IMPLEMENTASI_TAHAP_01.md` masih memiliki status dokumen tingkat atas “Rencana Kerja — BELUM DIIMPLEMENTASIKAN”, walaupun sebagian kemampuan runtime kini sudah ada. Status tingkat atas perlu diperjelas sebagai status rencana/target, bukan status seluruh modul.
- `docs/TAHAP_01_SPESIFIKASI_PEMERIKSA_EJAAN.md` masih menyebut EJA-04 sebagai kandidat dan gerbang sebelum implementasi, padahal implementasi terbatas sudah selesai melalui PR #54. Spesifikasi perlu diberi status pasca-implementasi dan tautan ke bukti uji.
- `docs/ilis_project_state.md` perlu diselaraskan dengan posisi Tahap 1 dan backlog terbaru agar menjadi ringkasan status proyek yang akurat.

Temuan ini adalah pekerjaan dokumentasi, bukan alasan untuk mengubah perilaku runtime dalam audit ini. Perbaikannya sebaiknya dilakukan pada PR dokumentasi terpisah setelah isi laporan ini ditinjau.

## 8. Syarat untuk menyatakan Tahap 1 lengkap

Tahap 1 tidak boleh dinyatakan lengkap hanya karena CI hijau atau beberapa API telah berjalan. Minimal, semua kondisi berikut harus dipenuhi atau dikecualikan melalui keputusan Owner yang terdokumentasi dan diterima evaluator:

1. Semua target wajib Tahap 1 mempunyai definisi operasional yang tidak ambigu.
2. Entri kata dasar memiliki makna/fungsi sederhana dan contoh penggunaan yang telah ditinjau, termasuk penanganan entri multi-kelas.
3. Cakupan fonologi yang disepakati mempunyai bukti implementasi dan uji yang relevan.
4. Cakupan ejaan wajib mempunyai pemeriksaan runtime dan pengujian yang sesuai; aturan yang tidak didukung tetap dinyatakan di luar cakupan.
5. Kemampuan kelas kata yang diklaim tidak melampaui cakupan lookup/pola yang benar-benar diuji.
6. Bila integrasi chatbot diwajibkan, ada bukti uji end-to-end bahwa kemampuan fondasi dipakai secara benar dalam percakapan.
7. Peta kasus uji dan hasil pengujian akhir dapat ditelusuri ke setiap target wajib.
8. Dokumentasi status, kode, data, dan laporan audit konsisten.
9. Evaluator menyetujui hasil akhir dan Owner menyatakan penerimaan. Tidak ada perubahan otomatis pada status dataset atau promosi referensi tanpa proses persetujuan tersendiri.
10. Tidak ada perluasan ke Tahap 2–4 yang dimasukkan sebagai syarat Tahap 1. Batas antartahap tetap dijaga.
11. Backlog yang belum selesai dicatat secara transparan beserta status dan dampaknya. Backlog tidak otomatis menghalangi penutupan apabila Owner dan evaluator secara eksplisit menerima pengecualian atas target tersebut; tanpa pengecualian, target wajib tetap berlaku.
12. Tidak ada implementasi runtime Tahap 1 dari rangkaian pekerjaan ini yang dipromosikan ke branch `main` tanpa persetujuan rilis terpisah. Baseline `main` harus diverifikasi tetap pada SHA yang disetujui sebelum dan sesudah pekerjaan.

Jika sebagian target kurikulum sengaja dikecualikan, pengecualian harus tertulis, memiliki alasan, dampak, dan persetujuan eksplisit. Pengecualian tidak boleh disamarkan sebagai implementasi yang sudah selesai.

## 9. Batas perubahan dan keputusan yang diminta

Laporan ini hanya mengusulkan pencatatan kondisi aktual. Seluruh pekerjaan Tahap 1 pada rangkaian PR #50–#59 tetap berada di `ilis-v2-development`; tidak ada implementasi runtime Tahap 1 dari rangkaian tersebut yang dipromosikan ke `main`. Ini tidak berarti `main` tidak pernah menerima perubahan historis lain yang tidak terkait Tahap 1. Tidak ada perubahan pada:
- kode runtime;
- file JSON referensi atau isi entri;
- Semantic 12 atau Reasoning 6;
- KnowledgeEngine, ChatbotAdapter, atau playground;
- workflow CI;
- branch `main`;
- Tahap 2, Tahap 3, atau Tahap 4;
- dataset pengetahuan umum.

**Keputusan yang diminta dari evaluator:** tinjau apakah matriks status, prioritas backlog, dan syarat kelulusan di laporan ini akurat. Jika ada koreksi, koreksi harus merujuk pada dokumen, kode, atau bukti uji yang spesifik.

**Keputusan yang diminta dari Owner setelah evaluasi:** menerima laporan sebagai baseline audit Tahap 1 atau meminta revisi. Penerimaan laporan tidak berarti Tahap 1 dinyatakan selesai dan tidak mengizinkan implementasi fitur berikutnya secara otomatis.

---

**Kesimpulan akhir audit:** ILIS telah memiliki fondasi runtime Tahap 1 yang berjalan pada beberapa kemampuan terbatas. Kualitas fondasi berikutnya ditentukan oleh ketepatan melengkapi target wajib, bukti uji yang sesuai, dan konsistensi dokumentasi—bukan oleh banyaknya fitur baru atau status CI hijau semata.
