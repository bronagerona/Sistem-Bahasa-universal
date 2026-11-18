# ILIS V2 Alpha — Laporan Evaluasi

**Status:** kandidat rilis alpha, menunggu hasil GitHub Actions untuk benchmark V2  
**Branch evaluasi:** `ilis-v2-development`  
**Arsitektur inti:** deterministik, tanpa LLM/model AI sebagai mesin inti.

## 1. Ringkasan

ILIS V2 memperluas fondasi V1 pada beberapa jalur yang dapat diuji: interpretasi pertanyaan dan perintah sederhana, inferensi berbasis aturan dengan bukti dan ketidakpastian, variasi keluaran bahasa, serta opsi persistensi SQLite. V2 tetap merupakan sistem berbasis pola, representasi semantik eksplisit, fakta, dan aturan—bukan model bahasa umum.

Benchmark V2 menguji alur dari input bahasa hingga hasil reasoning/generasi, dua skenario penalaran domain, serta pemulihan data setelah koneksi SQLite ditutup dan dibuka kembali.

## 2. Kemampuan baru V2

1. **Semantic Engine:** mengenali pola pertanyaan sederhana dan perintah sederhana; memperluas penanganan negasi, waktu, lokasi, serta beberapa variasi bahasa Indonesia. Kontrak semantik tetap versi 1.0 dengan 12 field.
2. **Reasoning Engine:** menerima hasil semantik untuk pertanyaan, membedakan intent question, command, dan assertion, serta mempertahankan evidence, confidence score, alasan, dan uncertainty.
3. **Inferensi domain:** aturan api–kayu–rumah menghasilkan penilaian kemungkinan secara hati-hati; aturan naga–lonceng memakai dua premis yang saling terhubung melalui suara keras.
4. **Language Generator:** menghasilkan jawaban pertanyaan, acknowledgement perintah, serta variasi formal, informal, dan slang untuk skenario naga–lonceng. Penanda ketidakpastian tetap disertakan.
5. **SQLite opsional:** Knowledge facts, provenance, session, dan episodic memory dapat dipulihkan setelah provider ditutup dan dibuka kembali. Mode in-memory tetap menjadi default untuk kompatibilitas.

## 3. Dataset dan benchmark end-to-end

File `tests/benchmark_v2_suite.py` berisi skenario pytest berikut:

| Skenario | Yang diverifikasi |
|---|---|
| Pertanyaan sederhana | Semantic question → inferensi berbukti → jawaban generator |
| Perintah sederhana | Semantic command → intent command → acknowledgement |
| Api–kayu–rumah | Dua premis, confidence, evidence, dan uncertainty |
| Naga–lonceng | Dua premis aturan V2, bukti, dan tiga register keluaran |
| Premis naga tidak lengkap | Hasil unknown, bukan kesimpulan positif |
| SQLite restart | Simpan fakta/provenance/episode → tutup core → buat core baru → muat ulang |

Benchmark ini adalah suite regresi fungsional, bukan pengukuran throughput, latensi, kualitas linguistik berskala besar, atau kalibrasi statistik.

## 4. Perbandingan singkat V1 dan V2

| Area | V1 Prototype | V2 Alpha |
|---|---|---|
| Semantik | Pola pernyataan sederhana | Tambahan pola pertanyaan, perintah, negasi dan frasa waktu/lokasi |
| Reasoning | Aturan burn-risk dasar | Inferensi pertanyaan dan aturan naga–lonceng |
| Generator | Keluaran dasar dengan register | Jawaban, acknowledgement perintah, dan variasi register untuk skenario V2 |
| Memori | In-memory sebagai jalur utama | In-memory tetap default; SQLite opsional untuk persistensi |
| Evaluasi | Suite pengujian fondasi | Ditambah benchmark end-to-end khusus fitur V2 |

Perbandingan ini menjelaskan cakupan implementasi, bukan klaim bahwa V2 memahami bahasa secara umum atau setara LLM.

## 5. Batasan V2 Alpha

- Semantic Engine masih mengenali pola dan kosakata terbatas; kalimat kompleks, ambigu, atau di luar pola dapat berstatus low-confidence/unsupported.
- Dukungan pertanyaan dan perintah belum mencakup seluruh bentuk sintaksis, pragmatik, dialog multi-langkah, atau semua variasi bahasa Indonesia.
- Inferensi hanya berlaku jika fakta dan aturan yang diperlukan tersedia; sistem tidak otomatis mengetahui fakta dunia.
- Confidence score adalah nilai heuristik internal, bukan probabilitas yang telah dikalibrasi.
- Aturan naga–lonceng dan api–kayu–rumah merupakan contoh domain terbatas, bukan simulasi fisika atau pengetahuan universal.
- Generator memiliki variasi register terbatas dan belum menjamin keluaran alami untuk semua konteks.
- SQLite menyimpan jenis data yang saat ini didukung; belum merupakan solusi replikasi, sinkronisasi multi-perangkat, migrasi skema lanjutan, atau konkurensi tinggi.
- Benchmark saat ini memeriksa perilaku fungsional; belum mengukur performa, beban, robustness korpus besar, fairness, atau kualitas percakapan jangka panjang.
- ILIS tetap bukan LLM dan tidak mengklaim kemampuan setara LLM.

## 6. Kriteria kesiapan alpha

Rilis V2.0-alpha layak dipertimbangkan setelah:
- seluruh tes regresi lama tetap lulus;
- seluruh skenario benchmark V2 lulus pada GitHub Actions;
- perubahan hanya berada pada branch pengembangan sampai keputusan integrasi dibuat;
- catatan batasan alpha dan roadmap tersedia.

Status kelulusan CI harus mengikuti hasil run GitHub Actions pada commit benchmark, bukan diasumsikan dari dokumen ini.

## 7. Arah berikutnya

Rincian prioritas pengembangan setelah alpha tersedia di [Roadmap ILIS V3](v3_roadmap.md).
