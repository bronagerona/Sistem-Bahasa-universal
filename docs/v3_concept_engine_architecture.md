# Arsitektur Desain Knowledge & Concept Engine ILIS V3

**Status:** Dokumen desain; belum merupakan spesifikasi implementasi final.  
**Basis acuan:** branch `ilis-v2-development` setelah rilis `v2.2-beta`.  
**Tujuan:** Merancang lapisan Concept Engine deterministik untuk penalaran berbasis konsep, kategori, sifat, dan relasi, tanpa mengganti KnowledgeEngine lama.  
**Batas tugas:** Hanya membuat dokumen desain ini. Tidak ada kode, tes, kontrak, atau skema SQLite yang diubah.

---

## 0. Prinsip desain dan batas kompatibilitas

V3 memperluas kemampuan inferensi ILIS melalui lapisan baru yang terpisah. Concept Engine bukan pengganti KnowledgeEngine dan bukan tempat baru untuk menyimpan transcript percakapan.

Prinsip yang wajib dipertahankan:

1. **Semantic tetap 12 field.** Nama, tipe, urutan, dan jumlah field pada kontrak Semantic tidak berubah. Concept Engine menerima hasil Semantic sebagai input baca-saja; tidak menambahkan field konsep ke objek Semantic.
2. **Reasoning tetap 6 key.** Output Reasoning tetap tepat berisi `conclusion`, `confidence_score`, `evidence`, `reasoning_type`, `reasons`, dan `uncertainty`. Tiga tingkat keyakinan V3 dipetakan ke nilai/isi field yang sudah ada, bukan key baru.
3. **Multi-turn V2.2 tetap utuh.** SessionManager, ConversationSession, batas riwayat, reset, dan alur snapshot konteks tidak diubah. Snapshot hanya membantu memahami rujukan pesan; snapshot bukan bukti fakta dunia.
4. **SQLite tetap utuh.** Desain Concept Engine tidak memerlukan perubahan skema SQLite yang sudah ada. Penyimpanan konsep awal dirancang sebagai ConceptStore terpisah dan statis. Pilihan backend persisten di masa depan memerlukan desain dan persetujuan terpisah.
5. **Deterministik dan tanpa LLM.** Hasil diturunkan dari data konsep, relasi, provenance, dan aturan eksplisit. Tidak ada generasi fakta atau pengisian celah secara spekulatif.
6. **KnowledgeEngine lama dipertahankan.** Komponen, data, perilaku, dan API KnowledgeEngine yang ada tetap menjadi jalur kompatibilitas V2.2.
7. **Tidak mengarang jawaban.** Sistem wajib membedakan Tahu Pasti, Tahu Sebagian, dan Tidak Tahu. Ketiadaan bukti tidak boleh diubah menjadi jawaban positif maupun negatif.

### 0.1 Batas tanggung jawab

| Komponen | Tanggung jawab dalam desain V3 |
|---|---|
| Semantic Engine | Memahami teks saat ini menggunakan kontrak 12 field yang ada. |
| Reasoning Engine | Mengatur proses penalaran dengan kontrak enam key yang ada. |
| KnowledgeEngine lama | Lookup fakta eksplisit/persis yang sudah tersedia; prioritas pertama. |
| Concept Engine | Menyediakan konsep, sifat, kategori, relasi, dan aturan inferensi berbasis konsep saat lookup fakta lama tidak menemukan fakta persis. |
| Inference | Menilai kecocokan aturan, kelengkapan bukti, konflik, dan tingkat keyakinan. |
| Language Generator / adapter | Menyampaikan hasil dan tingkat keyakinan tanpa mengubah hasil faktual. |
| SessionManager V2.2 | Tetap mengelola riwayat percakapan dan mengirim snapshot seperti sebelumnya; bukan bagian dari Concept Engine. |

---

## 1. Diagram alur penuh

### 1.1 Peta komponen: V2.2 yang dipertahankan dan tambahan V3

Diagram berikut menunjukkan komponen yang terlibat dan lapisan baru. Kotak berlabel V2.2 adalah komponen yang sudah ada; kotak V3 adalah rancangan baru.

```text
                         INPUT PENGGUNA
                               |
                               v
                 +---------------------------+
                 | Semantic Engine           |
                 | V2.2 — SUDAH ADA           |
                 | Output: kontrak 12 field   |
                 +---------------------------+
                               |
                               v
                 +---------------------------+
                 | Reasoning Engine           |
                 | V2.2 — SUDAH ADA           |
                 | Output: kontrak 6 key      |
                 +---------------------------+
                               |
                               v
                 +---------------------------+
                 | Concept Engine             |
                 | V3 — LAPISAN BARU          |
                 | Konsep, sifat, kategori,   |
                 | relasi, dan kandidat rule  |
                 +---------------------------+
                               |
                               v
                 +---------------------------+
                 | KnowledgeEngine lama       |
                 | V2.2 — TETAP ADA           |
                 | Lookup fakta persis        |
                 +---------------------------+
                               |
                               v
                 +---------------------------+
                 | Inference / Decision       |
                 | V3 — ATURAN KEPUTUSAN      |
                 | Prioritas fakta lama,      |
                 | fallback konsep, confidence|
                 +---------------------------+
                               |
                               v
                 +---------------------------+
                 | Jawaban akhir              |
                 | Tahu Pasti / Sebagian /    |
                 | Tidak Tahu                 |
                 +---------------------------+
```

**Catatan penting tentang urutan eksekusi:** diagram di atas adalah peta komponen dan aliran informasi. Untuk memenuhi kompatibilitas mundur, urutan keputusan aktual harus selalu melakukan lookup fakta persis pada KnowledgeEngine lama terlebih dahulu. Concept Engine boleh menyiapkan kandidat konsep/aturan secara pasif, tetapi **inferensi berbasis konsep hanya boleh dijalankan setelah KnowledgeEngine menyatakan tidak ada fakta persis yang cocok**. Dengan demikian, gambar tidak boleh ditafsirkan sebagai izin bagi Concept Engine untuk menimpa hasil KnowledgeEngine.

### 1.2 Urutan keputusan aktual (wajib)

```text
Input
  |
  v
Semantic V2.2 (12 field, tidak berubah)
  |
  v
Reasoning V2.2 (6 key, tidak berubah)
  |
  v
KnowledgeEngine lama: cari fakta persis
  |
  +---- Fakta persis ditemukan ----------------------+
  |                                                   |
  |   Gunakan hasil KnowledgeEngine lama              |
  |   (termasuk perilaku konflik/validasi yang ada)   |
  |                                                   |
  +---------------------------------------------------+
  |
  +---- Fakta persis TIDAK ditemukan
                 |
                 v
          Concept Engine V3
          - temukan konsep
          - periksa kategori/sifat
          - cocokkan relasi dan aturan
                 |
                 v
          Inference V3
          - validasi seluruh prasyarat
          - periksa bukti/provenance
          - periksa konflik dan data yang hilang
          - tentukan tingkat keyakinan
                 |
                 v
          Jawaban melalui kontrak Reasoning yang sama
```

Tidak ada jalur Concept Engine yang boleh melewati pemeriksaan fakta persis KnowledgeEngine lama. Jika Concept Engine gagal, hasilnya tidak boleh menghapus, menulis ulang, atau mengubah fakta lama.

### 1.3 Hubungan dengan Multi-turn V2.2

```text
Adapter / SessionManager V2.2
          |
          +--> Conversation snapshot (read-only)
                         |
                         v
                ILIS Core / Reasoning
                         |
              Semantic dan Reasoning
                 tetap sesuai kontrak
                         |
             KnowledgeEngine lama -> Concept Engine
                         |
                  hasil penalaran
```

SessionManager tetap berada pada tanggung jawab adapter. Snapshot percakapan dapat membantu mengidentifikasi entitas atau rujukan yang sedang dibicarakan, tetapi tidak dapat menjadi bukti bahwa suatu sifat atau relasi benar.

---

## 2. Model data Concept Engine

Model berikut adalah struktur konseptual untuk implementasi V3. Nama class dan field adalah rancangan, bukan klaim bahwa class tersebut sudah ada dalam kode.

### 2.1 Class `Concept`

Mewakili entitas atau gagasan yang dapat dirujuk dalam penalaran.

| Atribut | Tipe konseptual | Keterangan |
|---|---|---|
| `concept_id` | string | ID stabil dan unik. |
| `name` | string | Nama kanonis, misalnya `api`, `kayu`, `kertas`, `besi`. |
| `description` | string | Deskripsi ringkas yang bersumber dari data terkurasi. |
| `parent_categories` | list[string] | Kategori induk, dapat lebih dari satu bila datanya mendukung. |
| `aliases` | list[string] | Nama alternatif yang eksplisit/terdaftar. |
| `data_status` | enum | `complete`, `partial`, atau `unknown`. |
| `provenance` | list[ProvenanceRef] | Asal dan status verifikasi data konsep. |

Contoh data awal (ilustratif dan harus diverifikasi sebelum dijadikan seed implementasi):

| Konsep | Deskripsi | Kategori induk |
|---|---|---|
| api | Fenomena panas yang dapat menghasilkan pembakaran dalam kondisi tertentu. | fenomena |
| kayu | Material yang umumnya berasal dari jaringan tumbuhan. | material organik |
| kertas | Material lembaran yang umumnya berbasis serat selulosa. | material selulosa |
| besi | Unsur logam. | logam |
| air | Zat yang pada kondisi lingkungan umum dikenal dalam bentuk cair. | zat, cairan |

### 2.2 Class `Property`

Mewakili sifat yang dapat dimiliki suatu konsep.

| Atribut | Tipe konseptual | Keterangan |
|---|---|---|
| `property_id` | string | ID sifat unik. |
| `name` | string | Nama kanonis, misalnya `mudah_terbakar`, `tahan_panas`, `cair`, `padat`. |
| `description` | string | Makna operasional sifat. |
| `value_type` | enum/string | Boolean, kategori, atau nilai terukur bila kelak diperlukan. |
| `scope_conditions` | object/record | Kondisi yang membatasi kebenaran sifat, misalnya suhu atau keadaan material. |
| `provenance` | list[ProvenanceRef] | Sumber/verifikasi sifat. |

Sifat bukan label bebas yang otomatis menghasilkan kesimpulan. Sifat harus memiliki definisi operasional dan kondisi berlaku. Contohnya, `mudah_terbakar` tidak boleh disamakan dengan `pasti terbakar pada semua kondisi`.

### 2.3 Class `Relation`

Mewakili hubungan eksplisit antar konsep atau antara konsep dan sifat.

| Atribut | Tipe konseptual | Keterangan |
|---|---|---|
| `relation_id` | string | ID relasi unik. |
| `subject_concept_id` | string | Konsep subjek. |
| `relation_type` | enum/string | Misalnya `has_property`, `can_interact_with`, `belongs_to_category`. |
| `object_id` | string | ID konsep, kategori, atau sifat yang menjadi objek relasi. |
| `conditions` | object/record | Prasyarat dan batas berlakunya relasi. |
| `polarity` | enum | `positive` atau `negative`, jika didukung data. |
| `provenance` | list[ProvenanceRef] | Sumber dan status verifikasi relasi. |

Relasi `can_interact_with` harus spesifik. Relasi tersebut tidak boleh dianggap ada hanya karena dua konsep berbagi satu sifat.

### 2.4 Class `ConfidenceLevel`

Mewakili tiga status keyakinan yang harus tampak pada jawaban ILIS.

| Nilai konseptual | Label pengguna | Arti dan syarat |
|---|---|---|
| `KNOWN` | **Tahu Pasti** | Ada fakta persis yang diterima dari KnowledgeEngine lama, atau semua prasyarat aturan konsep terpenuhi oleh data terverifikasi, lengkap, relevan, dan tidak berkonflik. |
| `PARTIAL` | **Tahu Sebagian** | Ada data relevan, tetapi sebagian prasyarat, kondisi, atau verifikasi belum lengkap sehingga kesimpulan penuh belum dapat dipastikan. |
| `UNKNOWN` | **Tidak Tahu** | Tidak ada fakta persis dan tidak tersedia data konsep relevan yang cukup untuk membentuk inferensi yang didukung. |

Nilai ini adalah status internal konseptual. Untuk menjaga kompatibilitas, implementasi tidak menambahkan key ke output Reasoning. Status dapat direpresentasikan melalui isi `conclusion`, nilai `confidence_score` yang sesuai kebijakan, `reasoning_type`, `reasons`, dan `uncertainty`.

### 2.5 Provenance dan kualitas data

Setiap fakta konsep, sifat, dan relasi yang digunakan untuk inferensi harus dapat ditelusuri ke provenance. Rancangan minimum provenance:

- sumber atau referensi data;
- status verifikasi (misalnya `verified`, `unverified`);
- cakupan/kondisi berlakunya;
- versi atau waktu kurasi bila tersedia.

Data `unverified` tidak boleh sendirian memenuhi syarat Tahu Pasti. Jika provenance tidak tersedia, aturan harus menurunkan hasil menjadi Tahu Sebagian atau Tidak Tahu sesuai banyaknya bukti yang tersisa.

### 2.6 Contoh representasi konseptual

Contoh berikut hanya ilustrasi model, bukan data implementasi atau perubahan database:

```yaml
concepts:
  - concept_id: fire
    name: api
    parent_categories: [fenomena]
    properties:
      - property: menghasilkan_panas
        status: verified
      - property: dapat_membakar_material_mudah_terbakar
        status: verified

  - concept_id: paper
    name: kertas
    parent_categories: [material_selulosa]
    properties:
      - property: mudah_terbakar
        status: verified

  - concept_id: iron
    name: besi
    parent_categories: [logam]
    properties:
      - property: sulit_terbakar
        status: verified
```

Relasi kemampuan api dan sifat mudah terbakar harus tercatat sebagai relasi/aturan yang diverifikasi secara terpisah. Sistem tidak boleh menyimpulkan kemampuan tersebut hanya dari nama kategori.

---

## 3. Aturan penalaran (Inference)

### 3.1 Aturan utama

**Rule C-01 — kemampuan dan sifat yang cocok**

Jika:
1. konsep objek X ditemukan;
2. X memiliki sifat `mudah_terbakar` yang terverifikasi dan berlaku pada kondisi yang relevan;
3. konsep Y (misalnya api) memiliki kemampuan/relasi terverifikasi `dapat_membakar_material_mudah_terbakar`;
4. relasi kemampuan Y secara eksplisit menerima sifat tersebut;
5. tidak ada kondisi wajib yang hilang atau bukti konflik yang belum terselesaikan;

maka ILIS boleh menyimpulkan bahwa Y dapat membakar X dengan status **Tahu Pasti**.

Bentuk aturan:

```text
has_property(X, mudah_terbakar)
AND has_capability(Y, membakar_material_mudah_terbakar)
AND capability_applies_to(Y, mudah_terbakar)
AND all_required_conditions_verified
THEN can_burn(Y, X) => KNOWN
```

**Penting:** kemampuan Y dan hubungan kemampuan tersebut dengan sifat objek harus memiliki data eksplisit/terverifikasi. Jangan menganggap semua benda yang memiliki satu sifat sama pasti dapat saling berinteraksi.

### 3.2 Data tidak lengkap — Tahu Sebagian

**Rule C-02 — bukti relevan tetapi tidak lengkap**

Jika konsep ditemukan dan terdapat satu atau lebih data relevan, tetapi satu atau lebih prasyarat aturan belum diketahui, belum terverifikasi, atau kondisi penerapannya belum lengkap, hasilnya **Tahu Sebagian**.

Contoh:
- objek memiliki data sifat `mudah_terbakar`, tetapi status verifikasi sifat belum tersedia;
- sifat objek diketahui, tetapi kondisi interaksi yang diwajibkan belum diketahui;
- konsep memiliki sebagian atribut, namun data yang diperlukan untuk kesimpulan tidak lengkap.

Jawaban harus menyebutkan bagian yang diketahui dan batas yang belum dapat dipastikan. Jangan menyatakan kesimpulan penuh sebagai fakta.

### 3.3 Tidak ada data — Tidak Tahu

**Rule C-03 — tidak ada konsep/bukti yang relevan**

Jika:
- KnowledgeEngine tidak menemukan fakta persis; dan
- ConceptStore tidak menemukan konsep atau sifat/relasi yang relevan;

maka hasilnya **Tidak Tahu**.

ILIS harus menyatakan bahwa informasi belum tersedia. Sistem dilarang mengisi kekosongan dengan pengetahuan umum yang tidak ada di store atau aturan terdaftar.

### 3.4 Larangan inferensi dari satu kesamaan sifat

**Rule C-04 — kesamaan sifat bukan bukti relasi**

Jika kayu dan kertas sama-sama memiliki sifat `mudah_terbakar`, hal itu tidak berarti:
- kayu dapat membakar kertas;
- kertas dapat membakar kayu;
- semua benda yang mudah terbakar pasti terbakar pada setiap kondisi;
- semua benda dengan satu sifat sama memiliki hubungan kausal atau kemampuan berinteraksi.

Satu sifat hanya dapat menjadi salah satu prasyarat sebuah aturan. Kesimpulan memerlukan relasi kemampuan yang tepat, kondisi berlaku, serta bukti yang cukup.

### 3.5 Aturan konflik dan batas aman

1. Fakta persis KnowledgeEngine lama selalu diperiksa dan diprioritaskan sebelum inferensi konsep.
2. Jika KnowledgeEngine mengembalikan fakta persis yang valid, Concept Engine tidak boleh menimpa kesimpulan tersebut.
3. Jika KnowledgeEngine menemukan konflik, gunakan mekanisme konflik lama; jangan menyelesaikannya dengan memilih hasil Concept Engine yang lebih disukai.
4. Jika data konsep saling bertentangan atau provenance tidak memadai, jangan keluarkan Tahu Pasti.
5. Jangan melakukan pewarisan sifat dari kategori induk secara otomatis kecuali aturan pewarisan itu eksplisit, dibatasi, dan terverifikasi.
6. Jangan menyamakan ketiadaan data dengan bukti negatif. Tidak ditemukannya sifat bukan bukti bahwa sifat lawannya benar.
7. Terapkan batas jumlah rule yang dievaluasi, kedalaman relasi, dan ukuran kandidat untuk menjaga biaya komputasi.

### 3.6 Pemetaan ke output Reasoning V2.2

Output Reasoning tetap enam key berikut:

| Key yang sudah ada | Pemakaian untuk status V3 |
|---|---|
| `conclusion` | Memuat jawaban dan label Tahu Pasti / Tahu Sebagian / Tidak Tahu. |
| `confidence_score` | Skor keyakinan numerik sesuai kebijakan kalibrasi; bukan pengganti status atau bukti. |
| `evidence` | Referensi fakta lama atau ID konsep/sifat/relasi/provenance yang benar-benar dipakai. |
| `reasoning_type` | Menandai jalur, misalnya fakta persis lama atau inferensi konsep, tanpa menambah key. |
| `reasons` | Menjelaskan aturan dan prasyarat yang terpenuhi/tidak terpenuhi. |
| `uncertainty` | Menyebutkan data yang hilang, kondisi yang belum pasti, atau konflik. |

Nilai numerik `confidence_score` harus dikalibrasi pada tahap implementasi melalui tes. Jangan menetapkan ambang angka arbitrer dalam dokumen ini sebagai fakta. Status tiga tingkat adalah klasifikasi keputusan yang eksplisit, bukan sekadar pembagian angka secara kosmetik.

### 3.7 Contoh hasil konseptual

| Pertanyaan | Data yang tersedia | Hasil yang diharapkan |
|---|---|---|
| Apakah api bisa membakar kertas? | Fakta persis lama tidak ditemukan; sifat kertas dan kemampuan api cocok, terverifikasi, serta seluruh prasyarat rule terpenuhi. | **Tahu Pasti** melalui inferensi konsep. |
| Apakah api bisa membakar objek baru Z? | Konsep Z ditemukan, sebagian sifat tercatat, tetapi prasyarat penting belum lengkap. | **Tahu Sebagian**; jelaskan apa yang belum diketahui. |
| Apakah api bisa membakar objek Q? | Tidak ada fakta persis dan Q tidak ada dalam ConceptStore. | **Tidak Tahu**. |
| Apakah kayu dapat membakar kertas? | Keduanya memiliki sifat mudah terbakar, tetapi tidak ada relasi kemampuan kayu untuk membakar objek lain. | Jangan simpulkan; **Tidak Tahu** atau **Tahu Sebagian** hanya jika ada bukti relevan lain. |
| Apakah api membakar besi? | Data besi menunjukkan sifat sulit terbakar, tetapi tidak ada aturan lengkap yang membuktikan hasil interaksi pada kondisi pertanyaan. | Jangan membuat klaim absolut; **Tahu Sebagian** atau **Tidak Tahu** sesuai kelengkapan data. |

---

## 4. Kompatibilitas mundur V2.2

### 4.1 Prioritas KnowledgeEngine lama

Urutan wajib:

1. Reasoning menerima hasil Semantic dan input konteks yang tersedia sesuai jalur V2.2.
2. KnowledgeEngine lama melakukan lookup fakta persis menggunakan mekanisme yang sudah berjalan.
3. Jika fakta persis ditemukan dan lolos validasi yang sudah berlaku, hasil KnowledgeEngine lama dipakai. Concept Engine tidak dijalankan untuk menggantikan hasil tersebut.
4. Hanya jika fakta persis tidak ditemukan, Reasoning boleh meminta fallback ke Concept Engine.
5. Jika Concept Engine tidak dapat menghasilkan inferensi yang cukup didukung, kembalikan Tahu Sebagian atau Tidak Tahu; jangan mengarang jawaban.
6. Tidak ada perubahan format data atau skema penyimpanan KnowledgeEngine lama dalam desain ini.

Contoh kompatibilitas:
- Fakta lama `api → can_burn → kayu` tetap menjadi hasil prioritas.
- Fakta lama `api → can_burn → kertas`, jika tersedia, juga tetap menjadi hasil prioritas.
- Untuk objek yang tidak memiliki fakta persis, Concept Engine dapat menjadi fallback jika data konsep dan aturan lengkap.

### 4.2 Semantic dan Reasoning tidak berubah

- Semantic tetap mengeluarkan tepat 12 field sesuai `docs/semantic_contract.md`.
- Reasoning tetap mengeluarkan tepat enam key yang dipakai V2.2.
- Data konsep, status keyakinan, dan provenance tidak ditambahkan ke objek Semantic.
- Tidak ada key Reasoning baru seperti `concepts`, `confidence_level`, atau `concept_evidence`. Informasi tersebut dipetakan ke enam key yang sudah ada.

### 4.3 SessionManager dan snapshot Multi-turn tidak berubah

- SessionManager V2.2 tetap berada pada lapisan adapter.
- Adapter tetap mengambil snapshot riwayat dan meneruskannya ke Core dengan mekanisme yang sudah berjalan.
- Concept Engine tidak membuat session, tidak menyimpan transcript, tidak mengubah batas lima turn, dan tidak menangani reset percakapan.
- Snapshot dapat membantu interpretasi rujukan seperti “yang tadi”, tetapi tidak membuktikan sifat `mudah_terbakar` atau relasi `can_burn`.
- Core tetap tidak menyimpan state percakapan baru akibat Concept Engine.

### 4.4 SQLite tidak berubah

- Tidak menambah tabel, kolom, indeks, atau migrasi pada SQLite yang sudah ada.
- ConceptStore tahap awal adalah store terpisah dan statis.
- Integrasi penyimpanan konsep ke database di masa depan bukan bagian dari desain implementasi awal ini dan membutuhkan proposal terpisah, termasuk strategi migrasi dan kompatibilitas.

---

## 5. Rencana file implementasi (belum dibuat pada tugas ini)

Daftar berikut adalah rencana untuk tahap implementasi setelah dokumen desain disetujui. Tidak satu pun file berikut dibuat atau diubah dalam tugas dokumentasi ini.

| Path | Rencana tanggung jawab |
|---|---|
| `src/ilis/concept_engine/` | Folder/package baru untuk lapisan Concept Engine. |
| `src/ilis/concept_engine/concept_store.py` | Definisi model konsep dan penyimpanan data konsep statis tahap awal. |
| `src/ilis/concept_engine/inference_rules.py` | Aturan deterministik, validasi prasyarat, dan evaluasi tingkat keyakinan. |
| `tests/test_v3_concept_engine.py` | Tes unit dan integrasi Concept Engine V3. |
| `docs/v3_concept_engine_developer_guide.md` | Panduan developer setelah API implementasi disepakati. |

Integrasi ke ILIS Core pada tahap V3-C harus menggunakan titik ekstensi aditif yang menjaga API lama. Nama file Core yang akan disentuh belum ditetapkan dalam tugas ini; penentuannya harus dilakukan melalui audit kode terpisah sebelum implementasi. Jangan menganggap daftar di atas sebagai izin untuk mengubah file lain.

---

## 6. Rencana test case implementasi

Test case berikut adalah target penerimaan untuk tahap implementasi, bukan hasil tes yang sudah dijalankan.

### 6.1 Positif — inferensi konsep terverifikasi

**Kasus:** “Apakah api bisa membakar kertas?”

Prasyarat:
- KnowledgeEngine tidak menemukan fakta persis untuk pasangan tersebut pada fixture khusus pengujian fallback.
- ConceptStore memiliki konsep api dan kertas.
- Sifat kertas `mudah_terbakar` terverifikasi.
- Kemampuan api untuk membakar material dengan sifat tersebut terverifikasi.
- Seluruh kondisi rule terpenuhi dan tidak ada konflik.

Ekspektasi: jawaban **Tahu Pasti**, evidence menunjuk data/relasi yang digunakan, dan Reasoning tetap tepat enam key.

Catatan: pada dataset produksi yang masih memiliki fakta persis api–kertas, jalur yang diharapkan adalah KnowledgeEngine lama, bukan Concept Engine. Tes fallback harus mengisolasi atau menonaktifkan fakta persis hanya pada fixture tes; jangan menghapus fakta produksi.

### 6.2 Sebagian — konsep baru dengan sifat tidak lengkap

**Kasus:** objek baru memiliki sebagian atribut, tetapi satu prasyarat penting untuk inferensi belum tercatat atau belum terverifikasi.

Ekspektasi:
- status **Tahu Sebagian**;
- jawaban menjelaskan informasi yang sudah diketahui;
- `uncertainty` dan `reasons` menjelaskan data yang belum tersedia;
- tidak ada klaim pasti yang melampaui bukti.

### 6.3 Negatif — konsep tidak dikenal

**Kasus:** objek tidak ditemukan di KnowledgeEngine maupun ConceptStore dan tidak ada aturan yang relevan.

Ekspektasi:
- status **Tidak Tahu**;
- tidak membuat kategori, sifat, atau relasi baru;
- tidak mengubah ketiadaan data menjadi klaim negatif.

### 6.4 Pengaman inferensi

Tambahan tes wajib:
- Kesamaan satu sifat antara dua konsep tidak menghasilkan relasi kausal/kemampuan.
- Konsep tanpa provenance terverifikasi tidak menghasilkan Tahu Pasti.
- Konflik sifat atau relasi menurunkan keyakinan dan tidak disembunyikan.
- Kategori induk tidak mewariskan sifat tanpa aturan pewarisan eksplisit.
- Kondisi interaksi yang tidak diketahui tidak boleh dianggap terpenuhi.
- Batas jumlah rule dan kedalaman relasi dipatuhi.

### 6.5 Regresi V2.2

Jalankan seluruh tes regresi yang relevan dan verifikasi bahwa fitur berikut tetap normal:

- Multi-turn: Session ID, snapshot konteks, batas lima turn, isolasi sesi, dan reset.
- Persona: Mode A (ILIS), Mode B (identitas aplikasi), dan Mode C (identitas NPC).
- Identity Intent: perilaku identitas tetap berada pada jalur khusus yang sudah ada.
- Instruksi register/gaya: formal/sopan/santai tetap diterapkan.
- Semantic: tepat 12 field.
- Reasoning: tepat enam key.
- KnowledgeEngine lama dan penyimpanan SQLite: perilaku serta skema tidak berubah.

Kriteria lulus V3 bukan hanya tes Concept Engine. Seluruh regresi V2.2 harus tetap lulus.

---

## 7. Risiko dan mitigasi

| Risiko | Dampak | Mitigasi desain |
|---|---|---|
| Concept Engine mengubah jawaban V2.2 yang sudah berjalan | Regresi atau perubahan perilaku fakta lama | KnowledgeEngine lama selalu lookup pertama; Concept Engine hanya fallback setelah fakta persis tidak ditemukan. |
| ILIS terlalu sering menyimpulkan salah | Jawaban tidak didukung dianggap fakta | Ambang Tahu Pasti ketat; semua prasyarat dan provenance wajib; default ke Tahu Sebagian/Tidak Tahu. |
| Kesamaan sifat dianggap sebagai hubungan sebab-akibat | Inferensi liar, misalnya kayu dianggap dapat membakar kertas | Wajib ada relasi kemampuan yang cocok; satu sifat tidak cukup. |
| Data konsep tidak lengkap atau tidak terverifikasi | Confidence berlebihan | Provenance per data; data tidak terverifikasi tidak memenuhi Tahu Pasti. |
| Pewarisan sifat kategori terlalu luas | Semua anggota kategori diberi sifat yang belum tentu benar | Tidak ada inheritance implisit; aturan pewarisan harus eksplisit, terbatas, dan diuji. |
| Beban komputasi meningkat | Latensi dan penggunaan sumber daya bertambah | Batasi jumlah rule, kandidat konsep, kedalaman relasi, dan hentikan pencarian saat batas tercapai. |
| Perubahan merembet ke kontrak atau session V2.2 | Kerusakan kompatibilitas | API aditif, input baca-saja, tes kontrak 12 field/enam key, serta tes regresi Multi-turn. |
| ConceptStore berkembang tanpa tata kelola | Data duplikat atau saling bertentangan | ID stabil, nama kanonis/alias eksplisit, provenance, validasi duplikasi, dan proses review data. |

---

## 8. Peta tahapan implementasi V3

Seluruh tahapan di bawah merupakan rencana. Tidak ada tahap implementasi yang dimulai atau disetujui otomatis oleh pembuatan dokumen ini.

### V3-A — ConceptStore statis

Tujuan:
- Membuat package Concept Engine baru.
- Menentukan model Concept, Property, Relation, ConfidenceLevel, dan provenance.
- Menyediakan seed konsep awal: api, kayu, kertas, besi, dan air.
- Memvalidasi ID, referensi, alias, kategori, dan provenance.
- Tidak mengubah KnowledgeEngine lama, SQLite, Semantic, Reasoning, atau SessionManager.

Kriteria selesai:
- Store dapat dibaca secara deterministik.
- Data seed memiliki definisi dan sumber/verifikasi yang jelas.
- Konsep yang tidak terdaftar menghasilkan hasil lookup kosong, bukan data buatan.

### V3-B — Aturan Inference dasar

Tujuan:
- Menerapkan Rule C-01 sampai C-04 dan pengaman konflik.
- Menghasilkan status KNOWN/PARTIAL/UNKNOWN.
- Mengumpulkan evidence dan alasan yang dapat ditelusuri.
- Menerapkan batas jumlah rule dan kedalaman relasi.

Kriteria selesai:
- Tes positif, sebagian, negatif, dan pengaman inferensi lulus.
- Tidak ada Tahu Pasti tanpa seluruh prasyarat yang diverifikasi.

### V3-C — Integrasi ke ILIS Core

Tujuan:
- Melakukan audit titik ekstensi Core dan Reasoning sebelum perubahan kode.
- Memasang fallback Concept Engine setelah lookup fakta persis KnowledgeEngine lama gagal.
- Memetakan hasil ke enam key Reasoning yang sudah ada.
- Mempertahankan input Semantic 12 field dan alur snapshot Multi-turn V2.2.
- Tidak mengubah skema SQLite.

Kriteria selesai:
- Fakta persis KnowledgeEngine selalu menang.
- Concept Engine hanya berjalan sebagai fallback.
- Kontrak dan fitur V2.2 tidak berubah.

### V3-D — Pengujian luas dan regresi V2.2

Tujuan:
- Menjalankan seluruh tes unit/integrasi Concept Engine.
- Menjalankan regresi Semantic, Reasoning, KnowledgeEngine, SQLite, Multi-turn, Persona, Identity Intent, dan register.
- Menguji data parsial, konflik, konsep tidak dikenal, dan batas komputasi.
- Mendokumentasikan batas kemampuan serta contoh jawaban untuk ketiga tingkat keyakinan.

Kriteria selesai:
- Seluruh suite regresi V2.2 lulus.
- Tidak ada perubahan kontrak atau skema yang tidak disetujui.
- Semua inferensi Tahu Pasti dapat ditelusuri ke fakta dan aturan yang terverifikasi.
- Hasil tes dan batasan didokumentasikan sebelum kandidat rilis V3 dipertimbangkan.

---

## 9. Keputusan desain yang perlu disetujui sebelum implementasi

1. Definisi operasional dan provenance untuk setiap sifat/relasi seed.
2. Kebijakan konflik ketika beberapa fakta konsep memberi hasil berbeda.
3. Ambang dan kalibrasi `confidence_score` untuk tiga status; angka final harus ditentukan melalui pengujian, bukan tebakan.
4. Batas maksimum rule, kandidat konsep, dan kedalaman relasi untuk V3 awal.
5. Titik integrasi aditif ke Core/Reasoning setelah audit kode.
6. Bentuk penyimpanan konsep jangka panjang. Desain awal menggunakan ConceptStore statis dan tidak mengubah SQLite.

**Status akhir dokumen:** Desain arsitektur V3 untuk ditinjau. Dokumen ini bukan persetujuan implementasi, bukan migrasi database, dan bukan perubahan pada kode V2.2.
