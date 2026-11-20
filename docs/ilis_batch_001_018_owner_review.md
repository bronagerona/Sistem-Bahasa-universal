# REVIEW OWNER — DATASET PENGAYAAN BAHASA INDONESIA ILIS
> Dokumen gabungan: backlog isu sisa, pengajuan kandidat pemindahan dataset, dan ringkasan eksperimen A–E  
> Tanggal: 20 November 2026  
> Status dataset: **DRAFT — belum diintegrasikan ke runtime produksi**  
> Status dokumen: **Pengajuan untuk review Owner dan Evaluator**

## 1. Backlog resmi — dua isu tersisa

### BL-ILIS-001 — False-positive regex identitas pada pertanyaan “Dengan siapa kamu…”
- **Status:** OPEN — bug produksi belum diperbaiki.
- **Contoh reproduksi:**
  - “Dengan siapa kamu pergi?”
  - “Dengan siapa kamu berdiskusi?”
- **Dampak:** pola identitas yang terlalu luas menangkap substring “siapa kamu” dan mengarahkan pertanyaan relasional tersebut ke jalur respons identitas. Akibatnya, analisis Semantic/Reasoning baseline dapat terlewati.
- **Mitigasi eksperimen:** guard khusus pada harness Test 2; regresi dua contoh lulus 2/2.
- **Batas mitigasi:** guard tidak mengubah ILIS produksi dan tidak memperbaiki Test 1.
- **Tindak lanjut:** rancang perbaikan berbasis intent/pola pertanyaan yang lebih presisi; tambahkan pasangan uji positif identitas (“Siapa kamu?”) dan negatif/relasional (“Dengan siapa…?”). Pastikan prefix identitas hanya muncul untuk Identity Intent.
- **Kriteria selesai:** kedua contoh tidak lagi masuk jalur identitas, sementara pertanyaan identitas asli tetap benar; tes regresi relevan lulus.

### BL-ILIS-002 — Pemetaan boolean Negation kehilangan rincian
- **Status:** OPEN — normalisasi eksperimen berjalan, keterbatasan semantik masih ada.
- **Perilaku eksperimen saat ini:** boolean `true` dipetakan menjadi label `negative`; `false` menjadi `none`.
- **Dampak/risiko:** boolean sumber tidak membedakan jenis negasi yang lebih rinci, misalnya negasi temporal, identitas, larangan, atau aspek lain. Pemetaan tersebut bersifat lossy bila dipakai sebagai representasi semantik lengkap.
- **Tindak lanjut:** evaluasi skema anotasi yang mempertahankan jenis negasi secara eksplisit; jangan mengubah data sumber atau kontrak runtime tanpa proposal dan persetujuan terpisah.
- **Kriteria selesai:** jenis negasi yang relevan dapat dipertahankan dan diuji tanpa mengubah makna data secara diam-diam; kompatibilitas kontrak ditinjau.

---

## 2. Dokumen pengajuan resmi — kandidat pemindahan Batch 001–018

### 2.1 Keputusan yang dimohon
Mengajukan seluruh dataset Batch 001–018 sebagai **kandidat siap dipindahkan ke branch `ilis-v2-development` dalam status DRAFT**, setelah review Evaluator dan persetujuan Owner.

Pengajuan ini **bukan** permintaan integrasi ke runtime produksi. Pemindahan yang dimaksud hanya menempatkan salinan data dan dokumen pendukung di branch pengembangan untuk kurasi/verifikasi lanjutan. Seluruh entri tetap DRAFT dan tidak boleh diperlakukan sebagai fakta atau label gold yang telah tervalidasi.

### 2.2 Cakupan kandidat
Lima pilar dataset:
1. Lexicon — 90 record.
2. Sentence Patterns — 90 record.
3. Dialogues — 88 record.
4. Knowledge — 90 record.
5. Evaluation — 90 record.

**Total: 448 record dalam 90 file JSONL.** Cakupan 18 batch untuk setiap pilar. Semua entri tetap DRAFT. Seluruh Knowledge harus tetap diperlakukan sebagai `hypothesis`, dengan uncertainty yang menyatakan status DRAFT/belum diverifikasi.

### 2.3 Bukti kesiapan teknis
- Loader generik membaca 90 file JSONL dan 448 record.
- Seluruh 18 batch lulus pemeriksaan loader, pemetaan, dan kontrak output pada 565 kasus.
- Semantic 12 Field dan Reasoning 6 Keys memenuhi kontrak; kegagalan struktural masing-masing 0.
- Pengujian multi-turn berjalan berurutan dalam satu instance chatbot per dialog: 88 sesi dan 146 giliran pengguna.
- Regresi Tahap A–D dipertahankan, termasuk dua prompt guard identitas pada Test 2.
- Dataset sumber tidak diubah selama eksperimen.

### 2.4 Batasan dan syarat pemindahan
1. Status semua record tetap DRAFT; hasil eksperimen bukan verifikasi linguistik/faktual.
2. Isu BL-ILIS-001 dan BL-ILIS-002 tetap tercatat sebagai backlog terbuka.
3. Tidak ada integrasi dataset ke KnowledgeEngine, Concept Engine, ChatbotAdapter, PersonaRenderer, SQLite, atau jalur runtime lainnya.
4. Tidak ada perubahan kode produksi, tes produksi, workflow produksi, atau kontrak Semantic 12 Field / Reasoning 6 Keys.
5. Pemindahan ke `ilis-v2-development` hanya dilakukan setelah pengajuan ini ditinjau dan disetujui. Dokumen ini sendiri tidak melakukan pemindahan tersebut.

### 2.5 Rekomendasi
**Direkomendasikan untuk disetujui sebagai kandidat pemindahan data DRAFT ke `ilis-v2-development`**, dengan dua backlog di atas tetap terbuka dan tanpa integrasi runtime. Setelah pemindahan, tahap berikutnya adalah verifikasi sumber, review kualitas anotasi, dan penanganan isu sesuai persetujuan terpisah.

---

## 3. Ringkasan final eksperimen A–E

### 3.1 Identitas eksperimen dan batas perubahan
- Branch eksperimen final: `test-playground-batch016-018`
- SHA final Tahap E: `f6d3a7d3956b9795531bdca6cd4a280fcaf6db9a`
- Basis Tahap E: `6547a414d8c117162c24272761ad3920c5fdbbe2`
- Sumber dataset: `ilis-v2-development` SHA `80475e0f5e7c78c92a84109522777946dd9fb797`
- File JSONL: 90; record: 448; kasus A/B: 565.
- Seluruh dataset tetap DRAFT.

### 3.2 Hasil A/B keseluruhan
| Ukuran | Test 1 — ILIS baseline | Test 2 — loader + adapter dataset |
|---|---:|---:|
| Rata-rata Semantic confidence | 0.3629 | 0.6542 |
| Rata-rata Reasoning confidence | 0.0000 | 0.4091 |
| Kegagalan kontrak Semantic | — | 0 |
| Kegagalan kontrak Reasoning | — | 0 |
| Status batch | — | 18/18 LULUS |

Catatan interpretasi: confidence adalah skor observasi dari runtime/adapter, **bukan pengukuran akurasi**. Test 2 menggunakan anotasi dataset DRAFT; angka yang lebih tinggi tidak membuktikan peningkatan akurasi linguistik. Nilai Reasoning baseline 0.0000 merupakan hasil yang diamati pada jalur baseline, bukan bukti bahwa kontrak enam key tidak diperiksa.

### 3.3 Hasil per batch
| Batch | Kasus | Lulus | Gagal | T1 Semantic | T2 Semantic | T2 Reasoning |
|---|---:|---:|---:|---:|---:|---:|
| 001 | 35 | 35 | 0 | 0.3288 | 0.6186 | 0.3728 |
| 002 | 34 | 34 | 0 | 0.3706 | 0.6676 | 0.4231 |
| 003 | 34 | 34 | 0 | 0.3129 | 0.6794 | 0.4351 |
| 004 | 33 | 33 | 0 | 0.3313 | 0.6712 | 0.4267 |
| 005 | 33 | 33 | 0 | 0.4938 | 0.6712 | 0.4267 |
| 006 | 30 | 30 | 0 | 0.4125 | 0.6433 | 0.3982 |
| 007 | 30 | 30 | 0 | 0.3913 | 0.6567 | 0.4118 |
| 008 | 28 | 28 | 0 | 0.3781 | 0.6214 | 0.3757 |
| 009 | 28 | 28 | 0 | 0.4000 | 0.6214 | 0.3757 |
| 010 | 25 | 25 | 0 | 0.4429 | 0.6300 | 0.3845 |
| 011 | 27 | 27 | 0 | 0.3463 | 0.6241 | 0.3784 |
| 012 | 28 | 28 | 0 | 0.2732 | 0.6214 | 0.3757 |
| 013 | 33 | 33 | 0 | 0.3637 | 0.6612 | 0.4159 |
| 014 | 34 | 34 | 0 | 0.2906 | 0.6712 | 0.4257 |
| 015 | 35 | 35 | 0 | 0.4076 | 0.6669 | 0.4216 |
| 016 | 33 | 33 | 0 | 0.3719 | 0.6742 | 0.4290 |
| 017 | 33 | 33 | 0 | 0.3109 | 0.6742 | 0.4290 |
| 018 | 32 | 32 | 0 | 0.3661 | 0.6750 | 0.4306 |
| **Total** | **565** | **565** | **0** | | | |

### 3.4 Multi-turn dan kontrak
- Total multi-turn: 88 sesi, 146 giliran pengguna.
- Giliran diproses berurutan dalam instance chatbot yang sama per dialog.
- Regresi Tahap A: 5/5 lulus.
- Regresi dialog Tahap B: 23 sesi / 47 giliran.
- Regresi dialog Tahap C: 48 sesi / 77 giliran.
- Regresi kumulatif Tahap D: 73 sesi / 116 giliran.
- Guard dua prompt “Dengan siapa…” pada Test 2: 2/2 lulus.
- Semantic 12 Field: 0 kegagalan kontrak.
- Reasoning 6 Keys: 0 kegagalan kontrak.
- Knowledge: seluruhnya `hypothesis`; uncertainty tetap DRAFT/belum diverifikasi.
- Normalisasi boolean Negation dialog: 205 nilai.

### 3.5 Riwayat error/false-positive A–E
1. **Multi-turn awal belum berupa sesi percakapan berurutan (Tahap B):** awalnya prompt dialog dievaluasi terpisah; kemudian diperbaiki menjadi satu instance chatbot per dialog dengan urutan giliran tetap.
2. **Negation boolean tidak sama dengan label string runtime (Tahap B–E):** dinormalisasi untuk eksperimen (`true → negative`, `false → none`); keterbatasan hilangnya rincian jenis negasi masih menjadi backlog BL-ILIS-002.
3. **False-positive regex identitas (terdeteksi Tahap D, diregresikan Tahap E):** dua pertanyaan “Dengan siapa…” salah masuk jalur identitas di baseline. Guard sementara hanya ada di Test 2; bug produksi masih terbuka sebagai BL-ILIS-001.
4. **Lookup Reasoning tidak konsisten dengan normalisasi casefold (Tahap D):** masalah harness diperbaiki sebelum CI final hijau.
5. **Agregasi confidence gagal saat hasil Semantic baseline kosong/None (Tahap D):** penanganan nilai kosong diperbaiki sebelum CI final hijau.

Tidak ada kegagalan kontrak Semantic/Reasoning pada hasil final A–E. Status batch LULUS hanya menyatakan pemeriksaan teknis loader, pemetaan, dan kontrak; bukan validasi isi dataset.

### 3.6 Bukti CI Tahap E
- Workflow run: [GitHub Actions #44698974830](https://github.com/bronagerona/Sistem-Bahasa-universal/actions/runs/44698974830) — **SUCCESS**.
- Artifact: [tahap-e-batch016-018-proof](https://github.com/bronagerona/Sistem-Bahasa-universal/actions/runs/44698974830/artifacts/14611728537).
- Branch eksperimen: [test-playground-batch016-018](https://github.com/bronagerona/Sistem-Bahasa-universal/tree/test-playground-batch016-018).

### 3.7 Pernyataan perlindungan branch dan status data
Pada Tahap E, bukti CI mencatat:
- `JSONL_MODIFIED=NO`
- `PRODUCTION_MODIFIED=NO`
- `MAIN_MODIFIED=NO`
- `ILIS_V2_DEVELOPMENT_MODIFIED=NO`

Dengan demikian, dokumen ini merupakan pengajuan dan ringkasan pada branch eksperimen. **Tidak ada perubahan ke `main`, `ilis-v2-development`, kode produksi, atau file JSONL; dataset tetap DRAFT dan belum terintegrasi ke runtime.**
