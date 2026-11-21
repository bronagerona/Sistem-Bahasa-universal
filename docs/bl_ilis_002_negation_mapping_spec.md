# BL-ILIS-002 — Spesifikasi Final Desain Negation Mapping

> **Status:** Spesifikasi desain untuk evaluasi  
> **Backlog:** BL-ILIS-002 — Pemetaan boolean Negation kehilangan rincian  
> **Branch target:** `ilis-v2-development`  
> **Cakupan dokumen:** desain pemetaan dan rencana pengujian; bukan implementasi runtime  
> **Status dataset:** seluruh record tetap **DRAFT**  
> **Larangan perubahan:** tidak mengubah satu pun file JSONL, kode produksi, tes produksi, workflow CI, SQLite, atau branch `main`.

---

## 1. Ringkasan keputusan desain

BL-ILIS-002 diselesaikan melalui pemisahan tiga lapisan:

1. **Data Sumber JSONL:** nilai boolean `Negation` asli dipertahankan persis seperti tersimpan. Nilai tersebut tidak ditimpa, dikonversi, atau ditulis balik.
2. **Interpretasi Mapping:** interpreter membaca ujaran, konteks dialog, dan boolean sumber untuk menentukan label negasi yang lebih rinci. Teks dan konteks menjadi bukti utama; boolean adalah sinyal anotasi lama, bukan penentu tunggal.
3. **Keluaran Runtime:** hasil interpretasi disalurkan ke field `Negation` dalam Semantic 12 Fields. Struktur 12 field tetap, sedangkan Reasoning tetap menggunakan enam key yang sudah ditetapkan. Tidak ada perubahan kontrak runtime dalam tahap dokumen ini.

Enam label hasil interpretasi:

- `none`
- `negative`
- `not_yet`
- `identity_negative`
- `prohibitive`
- `ambiguous`

**Prinsip paling penting:** boolean `false` tidak boleh otomatis mengalahkan kata negasi yang jelas pada ujaran. Sebaliknya, boolean `true` tanpa bukti linguistik yang dapat ditemukan tidak boleh otomatis dipaksakan menjadi `negative`.

Desain ini merupakan spesifikasi untuk implementasi dan pengujian terpisah. Label hasil interpretasi bukan perubahan terhadap anotasi sumber dan tidak menaikkan status record dari DRAFT.

## 2. Konteks dan masalah yang diperbaiki

Dokumen review Owner Batch 001–018 mencatat 205 anotasi boolean Negation pada dialog. Eksperimen sebelumnya menggunakan normalisasi sederhana:

- boolean `false` → `none`
- boolean `true` + `belum` → `not_yet`
- boolean `true` + `bukan` → `identity_negative`
- boolean `true` + pemicu lain → `negative`
- fallback boolean `true` tanpa pemicu yang dikenali → `negative`

PR #20 mempertahankan pemetaan tersebut di harness eksperimen dan tidak mengubah JSONL. Namun, pendekatan itu masih memiliki dua keterbatasan:

1. `jangan` masih digabung ke `negative`, padahal secara fungsi dapat membentuk larangan/perintah negatif.
2. Boolean `false` langsung menjadi `none`, sekalipun ujaran mengandung penanda seperti `belum`. Contoh yang perlu menjadi regresi adalah ujaran `Aku belum paham cara membuat tabel di dokumen ini.` pada data dialog: teks mengandung `belum`, sementara anotasi boolean tercatat `false`.

Karena itu, boolean lama dipertahankan sebagai data sumber, tetapi interpretasi semantik harus memeriksa bukti pada teks dan konteks.

## 3. Arsitektur tiga lapisan

### Lapisan 1 — Data Sumber JSONL (immutable/read-only)

**Aturan wajib:**

- Field `semantic_annotation.Negation` tetap boolean asli `true` atau `false`.
- Tidak mengganti boolean menjadi string label.
- Tidak menambah field label baru ke record JSONL pada tahap ini.
- Tidak mengoreksi anotasi sumber secara otomatis.
- Tidak menulis hasil interpretasi kembali ke file sumber.
- Status `annotation_status` dan/atau `verification_status` tetap `draft`.

Boolean lama diperlakukan sebagai **legacy annotation signal**:

| Boolean sumber | Arti operasional pada interpreter |
|---|---|
| `false` | Anotator tidak menandai negasi pada field boolean. Ini bukan bukti mutlak bahwa ujaran tidak mengandung negasi. |
| `true` | Anotator menandai adanya negasi. Ini bukan bukti tentang jenis negasinya. |
| nilai hilang/tidak valid | Kesalahan atau ketidaklengkapan data yang harus dilaporkan; jangan diam-diam mengubahnya menjadi label. |

Interpreter wajib menyimpan nilai sumber dan jejak keputusan secara terpisah selama proses pengujian. Bentuk jejak internal yang disarankan:

- `source_boolean`: nilai asli JSONL;
- `detected_cues`: kata/frasa pemicu yang ditemukan;
- `scope`: bagian ujaran yang dinaungi negasi;
- `context_evidence`: konteks turn sebelumnya yang relevan;
- `mapping_label`: salah satu dari enam label;
- `mapping_reason`: alasan singkat;
- `annotation_discrepancy`: apakah bukti teks tidak sejalan dengan boolean sumber.

Jejak tersebut merupakan metadata diagnostik di luar record sumber. Jangan menambahkannya ke JSONL.

### Lapisan 2 — Interpretasi Mapping

Interpreter menerima sekurang-kurangnya:

1. teks ujaran asli;
2. boolean Negation sumber;
3. konteks dialog yang tersedia (urutan turn, rujukan turn, dan ujaran relevan sebelumnya).

Interpreter melakukan normalisasi untuk pencocokan—misalnya case-folding dan tokenisasi—tanpa mengubah teks asli yang disimpan.

Urutan proses:

1. Deteksi apakah pemicu negasi digunakan secara literal, atau hanya disebut/dikutip sebagai kata.
2. Temukan pemicu dan cakupan (scope) negasinya.
3. Periksa pola larangan, temporal, identitas, negasi biasa, atau negasi ganda.
4. Gunakan konteks turn sebelumnya hanya untuk menyelesaikan rujukan yang memang bergantung pada konteks.
5. Tentukan satu label. Jika bukti tidak cukup atau beberapa tafsir tetap bersaing, hasilkan `ambiguous`.
6. Bandingkan hasil dengan boolean sumber dan catat discrepancy; jangan mengubah boolean.

**Prioritas bukti:** konstruksi dan makna ujaran → konteks dialog yang relevan → boolean sumber sebagai sinyal pembanding. Boolean tidak boleh mengalahkan bukti linguistik yang eksplisit.

### Lapisan 3 — Keluaran Runtime

Hasil mapping diteruskan ke field `Negation` pada Semantic 12 Fields:

`Actor, Predicate, Patient/Object, Intent, Time, Aspect, Location, Recipient, Negation, Modality, Register, Confidence`

Aturan kompatibilitas:

- Tetap tepat 12 field; tidak menambah atau menghapus key.
- Nilai `Negation` memakai enam label yang ditetapkan spesifikasi ini.
- `ambiguous` adalah hasil yang sah, bukan error yang boleh dipaksa menjadi `negative`.
- `Confidence` harus mencerminkan kepastian interpretasi. Turunkan confidence ketika scope atau konteks tidak jelas.
- Reasoning tetap tepat enam key: `conclusion`, `confidence_score`, `evidence`, `reasoning_type`, `reasons`, `uncertainty`.
- Enam label ini adalah hasil interpretasi runtime, bukan field baru pada JSONL.
- Sebelum implementasi, validator dan seluruh konsumen Semantic wajib diperiksa untuk memastikan enam nilai Negation diterima. Perubahan validator/adapter, bila diperlukan, harus diajukan dan diuji sebagai pekerjaan implementasi tersendiri; dokumen ini tidak mengubahnya.

Jika sebuah komponen hilir belum dapat menangani `ambiguous`, komponen itu harus mempertahankan label dan menandai keterbatasan, bukan diam-diam mengubahnya menjadi `none` atau `negative`.

## 4. Definisi lengkap enam label

| Label | Definisi | Contoh |
|---|---|---|
| `none` | Tidak ditemukan tindakan menyangkal, penanda temporal negatif, penyangkalan identitas, atau larangan dalam cakupan ujaran. | `Saya membaca buku itu.` |
| `negative` | Negasi proposisi/pernyataan biasa: penutur menyangkal tindakan, keadaan, sifat, keberadaan, atau hubungan yang dinyatakan. Tidak termasuk negasi temporal khusus, identitas khusus, atau larangan. | `Saya tidak membaca buku itu.` |
| `not_yet` | Penanda temporal yang menyatakan peristiwa belum terjadi atau keadaan belum tercapai sampai waktu acuan, dengan kemungkinan terjadi kemudian. | `Saya belum membaca buku itu.` |
| `identity_negative` | Penyangkalan bahwa seseorang/benda termasuk identitas, kelas, kategori, atau hubungan nominal yang dilekatkan kepadanya. | `Orang itu bukan kakak saya.` |
| `prohibitive` | Larangan atau instruksi agar tindakan tidak dilakukan, biasanya diarahkan kepada lawan bicara atau pelaku tertentu. | `Jangan kirim berkas itu.` |
| `ambiguous` | Bukti tidak cukup, cakupan negasi tidak jelas, terdapat beberapa negasi yang berinteraksi, atau beberapa label tetap mungkin setelah konteks diperiksa. | `Saya tidak tidak setuju.` |

### Catatan batas makna

- `not_yet` bukan sekadar setiap kemunculan kata `belum`. Ungkapan seperti `belum tentu` dapat menyatakan ketidakpastian/kemungkinan, bukan peristiwa yang belum terjadi. Jika fungsi temporal tidak jelas, gunakan `ambiguous`.
- `identity_negative` bukan setiap kemunculan `bukan`. Gunakan label ini ketika `bukan` menyangkal identitas/kategori/relasi nominal. Jika `bukan` menyangkal proposisi atau fungsi lain, gunakan `negative` atau `ambiguous` sesuai scope.
- `prohibitive` dibedakan dari `negative`: `Jangan masuk` adalah larangan; `Dia tidak masuk` adalah penyangkalan peristiwa.
- `none` tidak berarti kalimat positif selalu benar; label ini hanya berarti tidak ada negasi yang terdeteksi dalam cakupan ujaran.
- Kata pemicu yang hanya sedang dibicarakan sebagai kata (contoh: `Kata “tidak” terdiri dari empat huruf`) tidak otomatis membentuk negasi.

## 5. Aturan pemetaan: pemicu → label

Pencocokan harus berbasis token/konstruksi, bukan substring bebas. Variasi ejaan dan register dapat ditambahkan ke kamus pemicu, tetapi tidak boleh membuat kecocokan di dalam kata lain.

### 5.1 `not_yet` — negasi temporal

Pemicu utama:

- `belum`
- variasi informal yang benar-benar setara dan telah diuji, bila ada

Pola contoh:

- `Saya belum makan.`
- `Dia belum datang.`
- `Pekerjaan itu belum selesai.`

Aturan: pilih `not_yet` jika `belum` menyatakan peristiwa/keadaan belum terjadi atau belum tercapai pada waktu acuan. Jika bentuk `belum` berada dalam ungkapan epistemik seperti `belum tentu`, jangan otomatis memakai `not_yet`.

### 5.2 `identity_negative` — penyangkalan identitas/kategori

Pemicu utama:

- `bukan`

Pola contoh:

- `Dia bukan kakak saya.`
- `Itu bukan rumah kami.`
- `Orang yang menelepon tadi bukan kakakku.`

Aturan: pilih `identity_negative` bila unsur setelah `bukan` adalah identitas, kelas, kategori, atau relasi nominal yang sedang disangkal. Periksa struktur kalimat, bukan kata `bukan` saja.

### 5.3 `prohibitive` — larangan

Pemicu utama/konstruksi:

- `jangan`, `janganlah`
- `dilarang`
- `tidak boleh`, `tak boleh`, dan variasi informal yang jelas bermakna larangan

Pola contoh:

- `Jangan kirim berkas itu dulu.`
- `Jangan masuk.`
- `Pengunjung dilarang merokok.`
- `Kamu tidak boleh menghapus berkas ini.`

Aturan: pilih `prohibitive` bila ujaran mengarahkan pelaku untuk tidak melakukan tindakan atau menyatakan larangan normatif. `Tidak boleh` dapat menjadi larangan meskipun tidak memakai kata `jangan`.

### 5.4 `negative` — negasi proposisional biasa

Pemicu utama:

- `tidak`, `tak`
- `enggak`, `nggak`, `gak`, `ga`, `ndak` dan variasi informal yang telah didaftarkan
- `bukan` ketika bukan penyangkalan identitas/kategori dan bukan konstruksi idiomatik
- `tiada`, `tanpa` bila benar-benar meniadakan unsur dalam proposisi

Pola contoh:

- `Saya tidak membaca buku itu.`
- `Dia tak datang hari ini.`
- `Saya enggak tahu.`
- `Rumah itu tanpa listrik.`

Aturan: gunakan `negative` untuk penyangkalan proposisi/keadaan yang bukan `not_yet`, `identity_negative`, atau `prohibitive`.

### 5.5 `none` — tanpa negasi

Gunakan `none` jika:

- tidak ditemukan pemicu yang berfungsi sebagai negasi;
- tidak ada konstruksi larangan;
- tidak ada cakupan negasi yang tersirat dari konteks;
- boolean sumber `false` konsisten dengan bukti teks.

Contoh: `Saya sudah membaca buku itu.`

### 5.6 `ambiguous` — bukti atau scope tidak memadai

Gunakan `ambiguous` jika:

- scope pemicu tidak dapat dipastikan;
- dua atau lebih jenis negasi muncul dalam satu ujaran dan hasil gabungannya tidak dapat direpresentasikan secara aman oleh satu label;
- terdapat negasi ganda yang berpotensi membalik atau melemahkan makna;
- boolean sumber `true`, tetapi tidak ditemukan bukti linguistik setelah pemeriksaan teks dan konteks;
- ujaran terpotong, kutipan, ironi, atau konstruksi idiomatik membuat fungsi negasi tidak pasti;
- konteks yang diperlukan tidak tersedia.

Jangan memakai `ambiguous` hanya karena sistem belum memiliki variasi kata tertentu. Catat pemicu yang belum dikenal untuk perluasan aturan terkontrol.

## 6. Prioritas, konflik, dan fallback

Urutan keputusan yang diwajibkan:

1. **Deteksi kutipan/penyebutan literal.** Jika kata negasi hanya disebut sebagai objek pembicaraan, jangan klasifikasikan sebagai negasi proposisional.
2. **Deteksi larangan.** Konstruksi larangan yang jelas → `prohibitive`.
3. **Deteksi negasi temporal.** `belum` dengan makna belum terjadi/belum tercapai → `not_yet`.
4. **Deteksi penyangkalan identitas.** `bukan` + identitas/kategori/relasi nominal → `identity_negative`.
5. **Deteksi negasi proposisional lain.** → `negative`.
6. **Tidak ada pemicu fungsional.** → `none`, kecuali boolean/context menimbulkan konflik yang belum terjelaskan.
7. **Bukti saling bertentangan atau scope tidak pasti.** → `ambiguous`.

### Boolean sumber bertentangan dengan teks

| Boolean sumber | Bukti ujaran | Hasil |
|---|---|---|
| `false` | Tidak ada pemicu negasi | `none` |
| `false` | Ada pemicu jelas dan scope jelas | Ikuti makna teks; catat discrepancy |
| `true` | Ada pemicu jelas | Ikuti jenis negasi dari teks |
| `true` | Tidak ada pemicu setelah teks/konteks diperiksa | `ambiguous`; catat anotasi yang tidak terjelaskan |
| hilang/tidak valid | Ada bukti jelas | Klasifikasikan dari teks, catat data sumber tidak lengkap |
| hilang/tidak valid | Tidak ada bukti jelas | `ambiguous` atau data error sesuai kebijakan loader; jangan mengarang nilai |

Contoh wajib: ujaran yang memuat `belum` tetapi boolean sumber `false` tetap dipetakan menjadi `not_yet` bila fungsi temporalnya jelas. Ketidaksesuaian dicatat untuk audit anotasi, bukan diperbaiki di JSONL.

### Fallback ketika interpreter tidak yakin

- Jangan menebak `negative` sebagai label default.
- Pilih `ambiguous` jika ada bukti negasi tetapi jenis/scope tidak dapat dipastikan.
- Pilih `none` hanya jika tidak ada bukti negasi yang berfungsi dan tidak ada konflik sumber yang belum terjelaskan.
- Simpan cue, alasan, dan discrepancy dalam log diagnostik.
- Turunkan confidence untuk `ambiguous`; jangan menyamarkan ketidakpastian sebagai keyakinan tinggi.

## 7. Penanganan negasi ganda dan scope

Negasi ganda tidak boleh otomatis dianggap saling menghapus. Interpreter harus memeriksa scope, struktur klausa, dan makna konstruksi.

| Pola | Keputusan desain | Alasan |
|---|---|---|
| `Saya tidak tidak setuju.` | `ambiguous` | Dapat bermakna litotes/pelemahan atau persetujuan tersirat; satu label tidak cukup tanpa konteks. |
| `Tidak ada yang tidak hadir.` | `ambiguous` pada tahap awal | Dua scope berinteraksi; pembacaan logis dapat berbeda dari maksud pragmatis. |
| `Saya belum pernah ke sana.` | `not_yet` jika bermakna pengalaman belum terjadi sampai waktu acuan | `belum` menjadi penanda temporal utama; `pernah` memperjelas domain pengalaman. |
| `Dia bukan tidak mampu.` | `ambiguous` | Penyangkalan terhadap negasi dapat menjadi litotes atau afirmasi tidak langsung. |
| `Jangan sampai dia tidak datang.` | `ambiguous` kecuali konteks memastikan scope | Larangan/peringatan dan negasi proposisional berada dalam satu konstruksi. |
| `Saya tidak pernah merokok.` | `negative` | Menyangkal kebiasaan/pengalaman secara umum; bukan penanda `belum` yang temporal. |

Untuk implementasi pertama, keselamatan interpretasi lebih penting daripada memaksakan satu label. Pola negasi ganda yang belum memiliki aturan eksplisit harus menghasilkan `ambiguous` dan masuk daftar perluasan tes. Aturan khusus baru boleh ditambahkan setelah contoh, scope, dan hasil yang diharapkan ditinjau.

## 8. Penggunaan konteks multi-turn

- Setiap dialog diproses dalam urutan turn asli.
- Konteks hanya digunakan jika rujukan ujaran memang bergantung pada turn sebelumnya.
- Jangan memindahkan negasi dari ujaran sebelumnya ke ujaran sekarang tanpa bukti anafora/elipsis.
- Negasi pada satu turn tidak otomatis berlaku pada turn berikutnya.
- Jika jawaban seperti `Tidak, belum.` tidak memiliki objek/aksi eksplisit, konteks turn sebelumnya boleh membantu menentukan apa yang belum terjadi.
- Jika ada lebih dari satu kandidat rujukan yang sama-sama mungkin, gunakan `ambiguous`.
- Turn assistant tetap dapat menjadi konteks percakapan, tetapi cakupan evaluasi 205 anotasi harus mengikuti definisi hitungan pada dataset/harness dan tidak boleh diam-diam mengubahnya menjadi hanya turn user.

## 9. Rencana uji regresi terhadap 205 anotasi dialog

### 9.1 Inventarisasi dan integritas sumber

1. Baca seluruh 18 file JSONL Pilar Dialogues secara read-only.
2. Enumerasi semua turn yang memiliki `semantic_annotation.Negation`.
3. Pastikan jumlah yang diuji tepat **205 anotasi**, sesuai bukti eksperimen A–E.
4. Simpan snapshot/hash sumber dan nilai boolean asli sebelum pengujian.
5. Pastikan semua file JSONL identik sebelum dan sesudah tes; tidak boleh ada write-back.
6. Jika hitungan bukan 205, hentikan tes dan laporkan perbedaan inventaris sebelum mengubah cakupan.

### 9.2 Pengujian dua jalur

**Jalur A — kompatibilitas legacy**

- Jalankan perilaku mapping lama PR #20 pada seluruh 205 anotasi sebagai baseline pembanding.
- Simpan hasil label lama, bukan untuk dianggap gold truth, melainkan untuk mengukur perubahan perilaku.
- Pastikan baseline reproduktif dan jumlah input sama.

**Jalur B — mapping enam label**

- Jalankan interpreter baru terhadap 205 ujaran dengan konteks dialog berurutan.
- Simpan label baru, cue, scope, alasan, confidence, dan discrepancy.
- Bandingkan hasil dengan baseline lama dan lakukan review khusus pada setiap perubahan label.
- Jangan menilai kesesuaian hanya dari boolean sumber; teks dan konteks harus diperiksa.

### 9.3 Matriks tes wajib

| Kelompok tes | Kasus minimum | Hasil yang diharapkan |
|---|---|---|
| Regresi `none` | Kalimat positif tanpa cue | `none` |
| Negasi biasa | `tidak`, `tak`, variasi informal | `negative` |
| Negasi temporal | `belum` dalam makna belum terjadi | `not_yet` |
| Identitas | `bukan` + identitas/kategori | `identity_negative` |
| Larangan | `jangan`, `dilarang`, `tidak boleh` | `prohibitive` |
| Boolean false + cue | Contoh `belum` dengan boolean `false` | Ikuti cue teks; discrepancy dicatat |
| Boolean true tanpa cue | Tidak ada cue setelah pemeriksaan | `ambiguous` |
| Negasi ganda | Dua penanda dengan scope berinteraksi | `ambiguous` kecuali aturan khusus telah divalidasi |
| Kutipan/penyebutan | Kata negasi hanya dibicarakan | `none` atau `ambiguous` sesuai fungsi kutipan |
| Multi-turn | Elipsis/rujukan negasi bergantung turn sebelumnya | Label dari konteks jika jelas; selain itu `ambiguous` |

### 9.4 Kriteria lulus

- Tepat 205 anotasi diproses; tidak ada anotasi yang hilang atau dihitung ganda.
- Seluruh boolean sumber tetap identik.
- Tidak ada perubahan pada 90 file JSONL/448 record.
- Setiap hasil memiliki salah satu dari enam label yang sah.
- Tidak ada fallback diam-diam dari kasus tidak pasti menjadi `negative`.
- Semua discrepancy boolean-vs-teks tercatat dan dapat ditelusuri ke dialogue ID serta turn ID.
- Kasus `jangan` yang merupakan larangan tidak lagi diklasifikasikan sebagai `negative`.
- Kasus `belum` dengan makna temporal yang jelas diklasifikasikan `not_yet`, termasuk ketika boolean sumber `false`.
- Semantic tetap tepat 12 field dan Reasoning tetap tepat enam key.
- Kegagalan kontrak Semantic dan Reasoning: **0**.
- Seluruh 88 sesi multi-turn tetap diproses berurutan pada satu instance chatbot per dialog dalam pengujian integrasi.
- Hasil tes dilaporkan sebagai validasi teknis interpreter, bukan bukti bahwa seluruh anotasi DRAFT sudah benar secara linguistik.

### 9.5 Laporan yang harus dihasilkan

Laporan pengujian harus memuat:

- jumlah file dan record sumber yang dibaca;
- jumlah anotasi Negation yang ditemukan (target 205);
- distribusi enam label;
- jumlah perubahan label dibanding baseline PR #20;
- jumlah discrepancy boolean-vs-teks;
- daftar kasus `ambiguous` beserta cue/scope dan alasan;
- daftar seluruh kasus `jangan` dan `belum`;
- hasil pemeriksaan immutability JSONL;
- hasil validasi Semantic 12 Fields dan Reasoning 6 Keys;
- hasil multi-turn;
- SHA sumber, SHA branch pengujian, dan tautan GitHub Actions/artifact.

## 10. Batas implementasi dan perubahan

Spesifikasi ini **tidak mengizinkan**:

- perubahan nilai boolean pada JSONL;
- penambahan label string ke record sumber;
- promosi status DRAFT menjadi verified;
- integrasi dataset ke KnowledgeEngine, Concept Engine, ChatbotAdapter, SQLite, atau runtime produksi;
- perubahan Semantic 12 Fields atau Reasoning 6 Keys;
- perubahan branch `main`.

Implementasi interpreter, validator enam label, dan regresi 205 anotasi merupakan tahap pekerjaan tersendiri setelah spesifikasi ini dievaluasi. Setiap implementasi harus tetap terisolasi dan membuktikan bahwa JSONL tidak berubah.

## 11. Hubungan dengan dokumen dan PR terkait

- `data/indonesian/knowledge/source_review_notes.md` — backlog verifikasi bahasa dan sumber Pilar D.
- `docs/ilis_batch_001_018_owner_review.md` pada branch `test-playground-batch016-018` — ringkasan 448 record, eksperimen A–E, 205 anotasi boolean, 88 sesi/146 giliran, dan status DRAFT.
- [PR #20 — Fix identity intent false positives and preserve dialogue negation types](https://github.com/bronagerona/Sistem-Bahasa-universal/pull/20) — perbaikan identity false-positive dan normalisasi negasi pada harness; JSONL tidak diubah.
- [PR #21 — Verify specific USGS sources for facts 0073–0076](https://github.com/bronagerona/Sistem-Bahasa-universal/pull/21) — perubahan provenance sumber Pilar D yang terpisah dari BL-ILIS-002.

## 12. Status akhir BL-ILIS-002

**DESAIN LENGKAP — DITERIMA DOLA.**

Desain menetapkan pemisahan data sumber, interpretasi, dan keluaran runtime; enam label; aturan pemicu dan prioritas; fallback konservatif; penanganan negasi ganda; serta rencana regresi 205 anotasi.

Status ini hanya menyatakan spesifikasi telah disusun. BL-ILIS-002 belum dinyatakan selesai secara implementasi sampai interpreter enam label diuji terhadap 205 anotasi dan seluruh kriteria lulus terpenuhi.


## 13. Catatan evaluasi Dola — diterima

**Keputusan evaluator: DITERIMA; siap di-merge ke `ilis-v2-development`.**

Lima poin evaluasi:

1. Boolean sumber `false` dengan cue teks eksplisit mengikuti makna teks dan dicatat sebagai discrepancy; JSONL tidak diubah — **diterima**.
2. Batas `identity_negative` dan `negative` — **diterima**.
3. `jangan` dan `tidak boleh` dipetakan sebagai `prohibitive` bila berfungsi sebagai larangan — **diterima**.
4. `ambiguous` sebagai fallback konservatif untuk negasi ganda/scope tak pasti — **sangat disetujui**.
5. Inventarisasi dan verifikasi jumlah 205 anotasi sebelum dan sesudah tes — **diterima**.

Catatan implementasi yang harus tetap diperhatikan:

- `belum tentu` tidak otomatis berarti `not_yet`; fungsi dan konteks harus diperiksa.
- Kata negasi yang hanya disebut atau dikutip tidak dihitung sebagai negasi fungsional.
- Confidence harus diturunkan untuk hasil `ambiguous`; jangan menampilkan kepastian palsu.
- Negasi ganda tetap `ambiguous` pada tahap awal sampai aturan khusus didukung contoh dan evaluasi yang memadai.
- Daftar pemicu dapat diperluas kemudian berdasarkan contoh terverifikasi.

Evaluasi ini menerima **dokumen desain**, bukan menyatakan implementasi runtime atau audit 205 anotasi telah selesai. Dataset tetap DRAFT dan seluruh JSONL tetap tidak berubah.
