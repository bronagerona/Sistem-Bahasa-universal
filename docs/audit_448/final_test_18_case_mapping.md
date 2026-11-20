# Matriks Pemetaan 18 Kasus Final-Test ke Pilar A–D dan Runtime ILIS

**Status:** DRAFT — hasil penelusuran teknis untuk review Dola  
**Branch basis:** ilis-v2-development  
**Base SHA:** 0acf34ee2f47b4e2f8898d8db9965d71bf317192  
**Run observasi:** [GitHub Actions #44742324017](https://github.com/bronagerona/Sistem-Bahasa-universal/actions/runs/44742324017)  
**Artifact:** [ilis-chatbot-playground-1](https://github.com/bronagerona/Sistem-Bahasa-universal/actions/runs/44742324017/artifacts/14631900733)

## 1. Tujuan dan batas pemeriksaan

Dokumen ini memetakan 18 record Evaluation Final-Test terhadap:
1. Pilar A — Lexicon.
2. Pilar B — Sentence Patterns.
3. Pilar C — Multi-turn Dialogues.
4. Pilar D — Knowledge.
5. Modul runtime yang semestinya memproses kemampuan tersebut.
6. Hasil aktual dari artefak Playground dan diagnosis awal.

**Penting tentang referensi:** field target_ref pada 18 record Evaluation berisi label baseline konseptual seperti baseline_v3_1_beta_greeting, bukan foreign key langsung ke ID lex/pat/dlg/fact. Karena itu, pemetaan A–D di bawah adalah hubungan semantik yang ditemukan melalui pemeriksaan isi record, bukan relasi foreign key yang sudah dideklarasikan pada skema Evaluation. Hubungan yang tidak ditemukan secara langsung tidak dipaksakan.

Pemeriksaan hanya membaca dataset dan kode. Tidak ada JSONL, kode runtime, workflow, SQLite, atau main yang diubah. Semua record tetap DRAFT.

## 2. Ringkasan hasil observasi artefak

| Indikator | Hasil |
|---|---:|
| Kasus dieksekusi | 18/18 |
| Total turn | 59 |
| Semantic supported | 9 |
| Semantic low_confidence | 48 |
| Semantic unsupported | 2 |
| Reasoning confidence_score 0.0 | 59/59 |
| Reasoning type unknown | 52 |
| Reasoning type assertion | 5 |
| Reasoning type greeting | 2 |
| Jawaban fallback generik utama | 50 |
| Jawaban acknowledgment pernyataan | 5 |
| Jawaban sapaan alami | 2 |

Tidak ada runtime exception. Ini adalah keberhasilan eksekusi, bukan PASS perilaku.

Catatan koreksi penting untuk interpretasi sapaan: pada artefak, metadata reasoning_type untuk eval-0010 dan eval-0015 adalah greeting, bukan assertion. Namun Semantic Intent pada kedua kasus masih assertion dan confidence akhir Reasoning tetap 0.0. Jadi temuan P1 yang lebih tepat adalah ketidaksesuaian klasifikasi Semantic Intent serta confidence Reasoning yang tidak mencerminkan jalur sapaan, bukan sekadar reasoning_type salah.

## 3. Matriks utama 18 kasus

| Evaluation | Fokus | Pilar A — Lexicon | Pilar B — Patterns | Pilar C — Dialogues | Pilar D — Knowledge | Hasil runtime |
|---|---|---|---|---|---|---|
| eval-0010 | Sapaan “Halo, apa kabar?” | Tidak ditemukan record sapaan langsung | Tidak ditemukan pola sapaan khusus | Tidak ditemukan dialog sapaan langsung | — | supported 1/1; jawaban alami; Semantic Intent assertion; metadata reasoning_type greeting; confidence 0.0 |
| eval-0015 | Sapaan “Hai!” | Tidak ditemukan record sapaan langsung | Tidak ditemukan pola sapaan khusus | Tidak ditemukan dialog sapaan langsung | — | supported 1/1; jawaban alami; Semantic Intent assertion; metadata reasoning_type greeting; confidence 0.0 |
| eval-0020 | Pergantian topik dan pemulihan konteks buku | — | pat-0029 hanya mendukung penanda urutan lalu/kemudian; bukan pengelolaan topik | dlg-0010 — perubahan topik sementara lalu kembali ke topik awal | — | low_confidence 3/3; konteks turn bertambah, tetapi topik awal tidak dipulihkan |
| eval-0025 | Urutan temporal: laporan setelah rapat yang belum berlangsung | — | pat-0019 sebelum; pat-0020 setelah | dlg-0018 — urutan peristiwa tanpa menyimpulkan sebab-akibat; dlg-0027 — urutan waktu vs sebab-akibat | — | low_confidence 3/3; tidak memproses urutan/status peristiwa |
| eval-0030 | Modalitas kemungkinan dan belum terkonfirmasi | lex-0048 — belum | pat-0027 — perkiraan dengan mungkin/barangkali; pat-0048 — belum | dlg-0025 — mempertahankan ketidakpastian dan tidak mengubah kemungkinan menjadi fakta | — | low_confidence 3/3; tidak mempertahankan kemungkinan lintas turn |
| eval-0035 | Atribusi laporan Budi dan status belum resmi | lex-0048 — belum; lema pelaporan langsung yang cocok belum ditemukan | pat-0028 — pelaporan isi dengan bahwa | dlg-0026 — mempertahankan atribusi pada informasi yang dilaporkan | — | low_confidence 3/3; atribusi dan status verifikasi tidak diproses |
| eval-0040 | Rotasi sideris, hari Matahari, dan orbit Merkurius | — | Pola tanya umum tersedia, tetapi pola astronomi khusus tidak ditemukan | — | fact-0033 — rotasi sideris sekitar 1.407,6 jam/58,65 hari; fact-0034 — periode orbit sekitar 88 hari | low_confidence 3/3; tidak ada fakta/evidence yang muncul di jawaban |
| eval-0045 | Frekuensi sesekali, habitual, dan setiap hari | lex-0041 — biasanya; lex-0042 — kadang-kadang | pat-0041 — biasanya; pat-0042 — kadang-kadang | dlg-0039 — biasanya vs selalu; dlg-0040 — kadang-kadang | — | low_confidence 3/3; penanda frekuensi tidak dianalisis |
| eval-0050 | Selama, hingga, dan sampai | lex-0044 — selama; lex-0045 — hingga; lex-0046 — sampai | pat-0044 — durasi selama; pat-0045 — batas akhir hingga; pat-0046 — batas/tujuan sampai | dlg-0042 — selama; dlg-0043 — hingga; dlg-0044 — sampai sebagai verba tiba | — | low_confidence 4/4; ketiga fungsi tidak dibedakan |
| eval-0055 | Belum, bukan, jangan, tanpa | lex-0048 sampai lex-0052 | pat-0048 sampai pat-0052 | dlg-0046 sampai dlg-0050 | — | low_confidence 4/5; supported 1/5 tetapi hanya diakui sebagai pernyataan; tidak ada pemetaan negasi yang memadai |
| eval-0060 | Wajib, mampu, berhak, seharusnya | lex-0053 sampai lex-0057 | pat-0053 sampai pat-0057 | dlg-0051 sampai dlg-0055 | — | low_confidence 5/5; jenis modalitas tidak dibedakan |
| eval-0065 | Saya, kita, kami, Anda | lex-0058 sampai lex-0062 | pat-0058 sampai pat-0062 | dlg-0056 sampai dlg-0060 | — | supported 2/3; unsupported 1/3; referen dan inklusivitas kelompok belum terjaga |
| eval-0070 | Siapa, kapan, di mana, mengapa, berapa | lex-0064 sampai lex-0069 | pat-0064 sampai pat-0069 | dlg-0061, dlg-0063 sampai dlg-0065 | — | supported 2/5; low_confidence 3/5; pertanyaan dikenali sebagian tetapi slot jawaban tidak lengkap |
| eval-0075 | Pertanyaan polar, keberadaan, jumlah, metode | lex-0068 sampai lex-0072 | pat-0068 sampai pat-0072 | dlg-0066 sampai dlg-0070 | — | low_confidence 4/4; bentuk pertanyaan tidak terbedakan |
| eval-0080 | Lokasi, tujuan, asal, interior | lex-0073 sampai lex-0077 | pat-0073 sampai pat-0077 | dlg-0071 sampai dlg-0075 | — | low_confidence 4/4; preposisi belum diolah menjadi relasi yang benar |
| eval-0085 | Sedang, sudah, pernah, akan/besok | lex-0078 sampai lex-0082 | pat-0078 sampai pat-0082 | dlg-0076 sampai dlg-0080 | — | low_confidence 4/4; penanda aspek ada, tetapi predikat dan pengalaman tidak teranalisis |
| eval-0090 | Banyak, setiap, sebagian, seluruh | lex-0083 sampai lex-0087 | pat-0083 sampai pat-0087 | dlg-0081 sampai dlg-0085 | — | supported 2/4; low_confidence 2/4; kuantifier tidak direpresentasikan sebagai cakupan |
| eval-0095 | Membaca, ditulis, berjalan, terjatuh, membawakan | lex-0088 sampai lex-0092 | pat-0088 sampai pat-0092 | dlg-0086 sampai dlg-0090 | — | unsupported 1/1; input berupa deskripsi konseptual, bukan kalimat uji |

Catatan rentang ID: rentang A/B/C pada baris tertentu menunjuk record pendukung yang relevan dengan fokus kemampuan, bukan berarti setiap record dalam rentang itu identik dengan setiap kalimat pada input Evaluation.

## 4. Bukti integrasi runtime

### 4.1 Dataset Pilar A–C tidak otomatis menjadi aturan runtime

Modul Semantic Engine adalah parser berbasis aturan yang memiliki kosakata dan marker hard-coded. Modul tersebut tidak membaca record JSONL lexicon atau sentence_patterns saat menganalisis kalimat.

Bukti utama:
- src/ilis/semantics/semantic_engine.py
- src/ilis/language/pipeline.py
- src/ilis/interfaces/ilis_core.py

Akibatnya, keberadaan record lex/pat di repositori tidak otomatis berarti parser runtime sudah memiliki kosakata, slot, atau constraint yang sama.

Contoh:
- Daftar verba pada Semantic Engine tidak mencakup banyak predikat dari kasus, seperti berotasi, berlangsung, mengirim, dipindahkan, berolahraga, menyiapkan, menghubungi, menyimpan, dan berhak.
- Penanda seperti selama dan hingga tidak menjadi bagian dari parser temporal khusus.
- Penanda pernah belum termasuk kelompok marker aspek di Semantic Engine.
- Berhak dan seharusnya belum termasuk marker modality.
- Kuantifier banyak/sebagian/seluruh tidak memiliki field cakupan tersendiri dalam Semantic 12 Fields.
- Anda belum tercantum dalam kamus pronomina runtime, meskipun record leksikon Anda tersedia.

Ini merupakan bukti kuat bahwa cakupan dataset lebih luas daripada cakupan parser runtime saat ini.

### 4.2 Knowledge JSONL belum dimuat ke KnowledgeEngine

Bukti utama:
- src/ilis/interfaces/ilis_core.py
- src/ilis/cognition/knowledge_engine.py
- src/ilis/cognition/fact_store.py
- data/indonesian/knowledge/batch_007.jsonl

ILISCore membuat KnowledgeEngine dengan seed_core_knowledge. KnowledgeEngine hanya menambahkan tiga fakta inti bawaan:
- api — can_burn — kayu
- rumah — made_of — kayu
- api — can_burn — kertas

Tidak ditemukan pemuatan otomatis data/indonesian/knowledge/*.jsonl pada jalur inisialisasi tersebut.

Karena itu:
- fact-0033 benar-benar ada pada dataset Knowledge, tetapi tidak otomatis tersedia di FactStore runtime.
- fact-0034 juga ada pada dataset, tetapi tidak otomatis tersedia di FactStore runtime.
- eval-0040 tidak dapat dijadikan bukti bahwa fact-0033 salah atau tidak memadai. Runtime belum memuat record tersebut.

Tambahan: fact-0033 secara eksplisit menjelaskan bahwa 58,65 hari adalah periode rotasi sideris, bukan hari Matahari. fact-0034 menyatakan orbit sekitar 88 hari. Jika expected behavior mengharuskan angka durasi hari Matahari Merkurius, perlu diperiksa apakah angka tersebut tersedia di record lain; jangan mengarang nilai dari dua fakta ini.

### 4.3 BL-ILIS-002 sudah ada, tetapi terisolasi

Bukti utama:
- src/ilis/experimental/negation_mapping.py
- docs/bl_ilis_002_negation_mapping_spec.md

File negation_mapping.py secara eksplisit menyatakan modul ini terisolasi dan belum terhubung ke runtime utama. Jadi kegagalan eval-0055 tidak boleh ditafsirkan sebagai kekurangan dataset negasi.

Dataset leksikon, pola, dan dialog untuk negasi sudah tersedia:
- lex-0048 sampai lex-0052
- pat-0048 sampai pat-0052
- dlg-0046 sampai dlg-0050

Pekerjaan yang relevan adalah integrasi terkontrol, pengujian kontrak, dan regression test; bukan menambah JSONL terlebih dahulu.

### 4.4 Multi-turn: riwayat tersimpan, resolusi konteks terbatas

Bukti utama:
- src/ilis/interfaces/chatbot_adapter.py
- src/ilis/interfaces/session_manager.py
- src/ilis/cognition/reasoning_engine.py
- src/ilis/interfaces/ilis_core.py

SessionManager menyimpan riwayat percakapan sampai lima turn. Artefak juga menunjukkan context_turns_used bertambah pada turn berikutnya. Jadi penyimpanan riwayat memang berjalan.

Namun:
- ILISCore.analyze_text memanggil analyze_semantics(text) tanpa memasukkan konteks ke Semantic Engine.
- ReasoningEngine hanya mencoba resolusi konteks terbatas ketika kalimat lanjutan diawali penanda tertentu, seperti lalu, kemudian, terus, kalau begitu, atau bagaimana dengan.
- Kasus eval-0020 menggunakan perubahan topik “Ngomong-ngomong” dan kembali dengan “Kembali ke buku tadi”; keduanya tidak tercakup oleh resolver terbatas tersebut.
- Tidak terlihat mekanisme topic stack atau pengambilan kembali topik terdahulu secara umum.

Kesimpulan: riwayat ada, tetapi pengelolaan topik dan resolusi referensi lintas topik belum memadai.

### 4.5 Reasoning dan generation

Bukti utama:
- src/ilis/cognition/reasoning_engine.py
- src/ilis/generation/language_generator.py
- docs/reasoning_engine.md

ReasoningEngine V1 bukan mesin penalaran umum. Jalur inferensi semantik mensyaratkan Actor, Predicate, dan Patient/Object yang lengkap, lalu mencari fakta yang cocok. Relasi khusus yang terlihat pada jalur tersebut sangat terbatas, termasuk alias membakar/bakar ke can_burn dan aturan naga–lonceng.

Konsekuensi:
- Pertanyaan “Siapa yang datang?” dapat berstatus Semantic supported tetapi tetap tidak mempunyai slot jawaban yang cukup untuk Reasoning.
- ReasoningEngine menolak membuat jawaban faktual jika triple tidak lengkap atau fakta tidak ditemukan.
- LanguageGenerator kemudian menghasilkan fallback unknown atau acknowledgment generik.

Untuk eval-0070, diagnosisnya bukan generation gap murni. Artefak memperlihatkan Semantic dapat memberi status supported pada dua pertanyaan, tetapi Actor/Patient tidak lengkap atau keliru. Ini lebih dahulu merupakan parser/slot-extraction dan Reasoning integration gap; generation ikut terdampak setelahnya.

## 5. Diagnosis awal per prioritas

| Prioritas | Kasus | Diagnosis yang didukung bukti | Fokus pemeriksaan |
|---|---|---|---|
| P1 | eval-0010, eval-0015 | Semantic Intent dan confidence path | Sapaan menghasilkan jawaban baik, metadata greeting benar, tetapi Semantic Intent assertion dan confidence akhir 0.0 |
| P2 | eval-0055 | Integration gap + parser coverage | Hubungkan BL-ILIS-002 ke jalur runtime tanpa mengubah Boolean sumber JSONL |
| P2 | eval-0040 | Integration gap + parser/Reasoning gap | Muat Knowledge secara eksplisit; kemudian uji pemetaan istilah astronomi dan relasi pertanyaan |
| P3 | eval-0020 | Runtime/algorithm gap | Topic tracking, context retrieval, dan parser predikat |
| P3 | eval-0025, eval-0030, eval-0035 | Runtime/algorithm gap | Temporal scope, modalitas epistemik, dan atribusi reported proposition |
| P3 | eval-0045, eval-0050, eval-0060 sampai eval-0090 | Runtime/algorithm gap | Perluas parser dan pemetaan semantic slots sesuai bukti dataset |
| P3 | eval-0095 | Test-design gap + runtime coverage gap | Ubah deskripsi konseptual menjadi input kalimat nyata sebelum menilai kemampuan morfologi |

### Catatan khusus P1 sapaan

Artefak menunjukkan:
- metadata.reasoning_type = greeting untuk kedua kasus;
- LanguageGenerator mengenali Predicate menyapa dan menghasilkan respons sapaan;
- Semantic Intent tetap assertion;
- Reasoning confidence akhir tetap 0.0.

Dengan demikian, jangan melakukan perubahan hanya dengan asumsi reasoning_type salah. Definisikan lebih dahulu kontrak yang diharapkan: apakah greeting merupakan Intent tersendiri atau tetap assertion dengan response_type khusus, dan bagaimana confidence untuk jalur sosial non-faktual harus direpresentasikan.

## 6. Kategori gap yang disepakati

| Kategori | Penetapan berdasarkan pemeriksaan |
|---|---|
| Data gap | Belum terbukti sebagai penyebab utama pada 18 kasus. Potensi kekurangan spesifik, misalnya nilai numerik hari Matahari Merkurius, perlu pemeriksaan terpisah. |
| Integration gap | Terbukti pada Knowledge JSONL yang belum dimuat dan BL-ILIS-002 yang masih terisolasi. |
| Runtime/algorithm gap | Terbukti dari keterbatasan daftar verba, marker, slot semantik, triple lookup, dan resolusi konteks. |
| Generation gap | Terlihat sebagai dampak pada jawaban fallback; pada beberapa kasus sumber masalah lebih dahulu berada di Semantic/Reasoning, bukan generator saja. |

## 7. Rekomendasi urutan pekerjaan berikutnya

1. Dola meninjau matriks dan koreksi temuan sapaan serta Knowledge loading.
2. Setelah matriks diterima, rancang perbaikan eval-0095 menjadi input kalimat nyata. Jangan mengubah record sebelum ada keputusan dan PR terisolasi.
3. Rancang field test_ready untuk Evaluation dan aturan runner:
   - true: kasus operasional yang boleh dijalankan;
   - false: kasus konseptual yang dilewati dan dilaporkan sebagai KONSEPTUAL.
   Perubahan skema JSONL dan runner dilakukan pada tahap terpisah setelah persetujuan eksplisit.
4. Siapkan desain integrasi BL-ILIS-002, dengan Boolean sumber JSONL tetap read-only.
5. Siapkan desain pemuatan Knowledge JSONL yang eksplisit, aman, dan mempertahankan status DRAFT/provenance; jangan otomatis menganggap DRAFT sebagai verified.
6. Setelah integrasi dan tes terisolasi tersedia, lakukan pengujian ulang. Jangan menyebut hasilnya Final-Test resmi sebelum status test_ready, expected behavior, dan lock policy diselesaikan.

## 8. Batas perubahan dan keputusan

Dokumen ini hanya hasil pemetaan dan pembacaan kode/dataset.

- Tidak ada JSONL yang diubah.
- Tidak ada kode runtime yang diubah.
- Tidak ada workflow yang diubah.
- Tidak ada perubahan SQLite.
- Tidak ada perubahan main.
- Semua record tetap DRAFT.
- Final-Test tetap belum terkunci.
- Tidak ada staging atau integrasi produksi.

**Kesimpulan:** basis pendukung Pilar A–D ditemukan untuk sebagian besar kemampuan yang diuji. Dua masalah integrasi yang paling jelas adalah Knowledge JSONL yang belum dimuat ke KnowledgeEngine dan BL-ILIS-002 yang belum terhubung ke runtime. Di luar itu, banyak kegagalan berasal dari cakupan parser, semantic slots, ReasoningEngine, dan pengelolaan konteks yang masih terbatas. Penambahan JSONL bukan tindakan pertama yang disarankan.

**Dokumen ini diajukan untuk review Dola.**
