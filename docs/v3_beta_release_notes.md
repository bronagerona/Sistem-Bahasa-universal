# ILIS V3-Beta — Catatan Rilis

> Tag rilis: `v3-beta`  
> Status: Beta Candidate untuk pengujian, bukan untuk lingkungan produksi

## 1. Ringkasan Utama

ILIS V3 memperkenalkan lapisan Knowledge & Concept Engine untuk memperluas penalaran berbasis konsep secara deterministik, tanpa menggantikan KnowledgeEngine lama.

Pembaruan utama:

- ✅ Penambahan lapisan **Knowledge & Concept Engine (V3)** sebagai fallback setelah KnowledgeEngine tidak menemukan fakta persis yang cocok.
- ✅ Tiga tingkat keyakinan:
  - **KNOWN (Tahu Pasti):** seluruh persyaratan inferensi dan bukti terverifikasi terpenuhi. Pada tahap beta ini, status KNOWN penuh baru dibuktikan melalui fixture pengujian; belum tersedia pada seed data produksi.
  - **PARTIAL (Tahu Sebagian):** tersedia sebagian data yang relevan, tetapi belum cukup untuk memastikan kesimpulan. Jawaban disertai peringatan bahwa hasilnya masih dugaan.
  - **UNKNOWN (Tidak Tahu):** informasi yang tersedia belum cukup untuk menghasilkan kesimpulan yang didukung bukti.
- ✅ LanguageGenerator disesuaikan agar teks jawaban selaras dengan status keyakinan hasil penalaran.
- ✅ Fitur V2.1 dan V2.2 tetap dipertahankan, termasuk Persona, Identity Intent, Multi-turn, reset percakapan, serta penerusan instruksi gaya bahasa sopan dan santai.

V3 tetap deterministik dan tidak menggunakan LLM. Ketiadaan bukti tidak boleh diubah menjadi jawaban yang seolah-olah pasti.

## 2. Daftar Fitur Baru V3

- **ConceptStore (V3-A):** menyediakan penyimpanan konsep, sifat, relasi, dan provenance secara statis di memori.
- **InferenceEngine (V3-B):** menerapkan aturan penalaran berbasis konsep dengan pemeriksaan kelengkapan data, provenance, kondisi, dan tingkat keyakinan.
- **Integrasi ReasoningEngine (V3-C):** menghubungkan Concept Engine ke alur penalaran yang sudah ada. Lookup fakta persis pada KnowledgeEngine lama tetap dijalankan PERTAMA; Concept Engine hanya digunakan sebagai fallback jika tidak ditemukan fakta persis dan tidak ada konflik yang menghalangi.
- **Perbaikan LanguageGenerator:** menangani status `concept_inference_known`, `concept_inference_partial`, dan `concept_inference_unknown`, sehingga tingkat kepastian pada teks jawaban tidak bertentangan dengan hasil penalaran.

## 3. Daftar yang Tidak Berubah (Kompatibilitas Mundur)

Komponen dan kontrak berikut dipertahankan:

- Kontrak Semantic: tetap **12 field**.
- Kontrak Reasoning: tetap **6 key**.
- KnowledgeEngine lama beserta prioritas lookup fakta persis.
- Skema SQLite.
- SessionManager dan alur Multi-turn V2.2.
- Persona Mode A / B / C.
- Identity Intent.
- Penerusan instruksi gaya bahasa, termasuk sopan dan santai.

V3 menambahkan jalur fallback, bukan mengganti atau mengubah kontrak inti V2.

## 4. Batasan yang Diketahui

**Perhatikan batasan berikut sebelum menggunakan ILIS V3-Beta:**

1. Sebagian besar seed konsep bawaan pada ConceptStore produksi masih berstatus **PARTIAL**. Karena itu, hasil inferensi berbasis konsep belum boleh dianggap sebagai pengetahuan yang terverifikasi penuh.
2. Status **KNOWN** dengan seluruh data dan provenance terverifikasi saat ini hanya tersedia pada fixture pengujian terisolasi. Fixture tersebut tidak dimasukkan ke seed data produksi.
3. Multi-turn masih menggunakan penyimpanan **in-memory**. Riwayat percakapan akan hilang ketika proses atau aplikasi dimulai ulang. Persistent session belum tersedia.
4. Penanganan ambiguitas pada kalimat kompleks dan bahasa kiasan belum sempurna. Interpretasi untuk kasus-kasus tersebut masih dapat keliru atau tidak lengkap.
5. Ini adalah versi **beta** untuk pengujian. Bug, keterbatasan data, dan perilaku yang belum terduga masih mungkin ditemukan. Jangan mengandalkannya sebagai rilis produksi.

## 5. Bukti Pengujian

Pengujian yang menjadi dasar catatan rilis ini:

- **CI Full-System Smoke Test Run #2:** berhasil, dengan **312/312 tes lulus** pada suite regresi penuh.
- **Pengujian manual Playground:**
  - Jalur fakta persis KnowledgeEngine lama: ✔
  - Jalur Concept Engine PARTIAL: ✔
  - Jalur Concept Engine UNKNOWN: ✔
- Regresi fitur V2.1 dan V2.2, termasuk Persona, Identity Intent, Multi-turn, reset percakapan, dan instruksi gaya bahasa, tercakup dalam pengujian regresi yang lulus.
- Jalur Concept Engine **KNOWN** juga telah diuji melalui fixture terisolasi khusus pengujian. Hasil ini membuktikan jalur implementasi dan LanguageGenerator, tetapi **bukan** bukti bahwa seed produksi saat ini memiliki data KNOWN terverifikasi.

Hasil 312/312 menunjukkan seluruh tes pada suite yang dijalankan lulus; hasil tersebut bukan jaminan bahwa semua kemungkinan penggunaan bebas dari bug.

## 6. Backlog dan Rencana Masa Depan (V3.1 / V4)

Rencana pengembangan berikut belum termasuk dalam rilis beta ini:

- Menambahkan seed ConceptStore produksi yang terverifikasi agar inferensi berstatus KNOWN dapat digunakan berdasarkan data produksi yang memenuhi seluruh persyaratan.
- Mengembangkan persistent session untuk mempertahankan riwayat Multi-turn setelah aplikasi atau proses dimulai ulang.
- Memperluas penanganan kalimat ambigu, bahasa kiasan, dan percakapan yang lebih kompleks.

## 7. Catatan untuk Developer

- **Urutan eksekusi wajib:** KnowledgeEngine melakukan lookup fakta persis terlebih dahulu. Hanya jika fakta persis tidak ditemukan dan tidak ada konflik yang menghalangi, Concept Engine boleh dijalankan sebagai fallback.
- Jangan mengubah kontrak Semantic **12 field** atau Reasoning **6 key** sebagai bagian dari integrasi V3 tanpa desain dan persetujuan terpisah.
- Context snapshot dari SessionManager hanya membantu memahami rujukan percakapan; snapshot bukan bukti fakta dunia.
- Pertahankan pemisahan Concept Engine dari KnowledgeEngine lama, SQLite, dan SessionManager.
- Dokumentasi pendukung:
  - `docs/v3_concept_engine_architecture.md`
  - `docs/v3_concept_engine_developer_guide.md`

---

**Status dokumen:** Catatan rilis untuk Beta Candidate. Dokumen ini tidak menyatakan bahwa ILIS V3 telah siap untuk lingkungan produksi.
