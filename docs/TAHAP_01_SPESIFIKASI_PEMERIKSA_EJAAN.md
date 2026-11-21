# SPESIFIKASI DAN PAKET UJI JALUR A — PEMERIKSAAN EJAAN TAHAP 1

**Branch:** `docs/tahap-01-spelling-spec`  
**Status:** Rancangan perilaku dan kasus uji — BELUM IMPLEMENTASI  
**Acuan utama:** `data/reference/tahap_01_fondasi/aturan_ejaan.json`  
**Acuan desain:** `docs/RENCANA_PENGEMBANGAN_RUNTIME_TAHAP_01.md`  
**Batas:** hanya Jalur A; tidak mengubah kode, referensi JSON, runtime aktif, chatbot, atau `main`.

---

## 1. Tujuan dan prinsip

Dokumen ini menerjemahkan 12 aturan referensi menjadi batas kemampuan pemeriksaan yang dapat diuji sebelum kode ditulis.

Pemeriksa harus:
1. deterministik dan hanya memakai aturan/pola yang dinyatakan;
2. membaca sumber referensi tanpa mengubahnya;
3. mempertahankan teks asli secara persis;
4. melaporkan temuan dan alasan, bukan menulis ulang masukan;
5. menggunakan `needs_context` ketika bentuk teks saja tidak cukup;
6. tidak mengklaim bahwa aturan yang belum didukung sudah diperiksa;
7. tidak mengubah maksud, fungsi ujaran, atau tanda baca berdasarkan tebakan.

**Pemeriksaan ejaan bukan penilaian apakah kalimat masuk akal.** Pemeriksa hanya boleh menyatakan temuan yang berada dalam cakupan aturan dan pola yang sudah divalidasi.

## 2. Audit determinisme seluruh 12 aturan

ID di bawah adalah ID internal spesifikasi untuk merujuk urutan aturan pada JSON v1.0. ID ini tidak ditambahkan ke atau ditulis kembali ke file referensi.

| ID | Aturan referensi | Kebutuhan bukti | Keputusan tahap awal |
|---|---|---|---|
| EJA-01 | Huruf kapital pada awal kalimat | Segmentasi kalimat dan pembedaan kalimat dari fragmen, judul, kutipan, atau input parsial | **Tunda.** Tidak boleh menganggap awal setiap string pasti awal kalimat. |
| EJA-02 | Huruf kapital pada nama orang | Pengenalan nama diri dan pembedaan dari kata biasa | **Tunda.** Belum ada daftar entitas atau anotasi nama yang disetujui. |
| EJA-03 | Huruf kapital pada nama tempat | Pengenalan nama geografi dan pembedaan dari pemakaian umum | **Tunda.** Tidak boleh menebak nama tempat dari kapitalisasi atau frekuensi. |
| EJA-04 | Huruf kapital pada nama hari dan bulan | Pengenalan bentuk hari/bulan dalam konteks tanggal yang cukup jelas | **Kandidat implementasi terbatas.** Hanya pola tanggal eksplisit yang masuk daftar uji; bentuk lepas/ambigu harus `needs_context`. |
| EJA-05 | Kata depan di, ke, dari ditulis terpisah | Pembedaan kata depan dari bentuk yang menempel atau konstruksi lain | **Tunda.** Pemeriksaan substring seperti `disekolah` tidak boleh digeneralisasi menjadi pemisahan otomatis tanpa analisis fungsi. |
| EJA-06 | Awalan di- pada verba pasif ditulis menyatu | Pengenalan morfologi dan pembedaan awalan dari kata depan | **Tunda.** Memerlukan analisis morfologi/konteks; jangan memutuskan hanya dari awalan karakter. |
| EJA-07 | Titik mengakhiri kalimat pernyataan | Jenis ujaran dan batas kalimat | **Tunda.** Fragmen, judul, pesan singkat, dan kalimat tanpa titik tidak selalu salah. |
| EJA-08 | Koma memisahkan unsur perincian | Pengenalan struktur perincian dan batas unsur | **Tunda.** Jangan menyisipkan koma hanya karena menemukan beberapa kata yang tampak seperti daftar. |
| EJA-09 | Tanda tanya pada akhir pertanyaan | Maksud/fungsi interogatif, bukan hanya bentuk kata tanya | **Tunda.** Tidak boleh mengubah titik menjadi tanda tanya tanpa bukti fungsi ujaran. |
| EJA-10 | Tanda seru pada seruan/perintah kuat | Maksud, tekanan, dan fungsi ujaran | **Tunda.** Tidak boleh mengubah `Awas?` menjadi `Awas!` tanpa konteks. |
| EJA-11 | Tanda pisah (—) untuk sisipan/penegasan | Fungsi tanda dan struktur sisipan | **Tunda.** Jangan mengganti tanda hubung dengan tanda pisah hanya berdasarkan bentuk karakter. |
| EJA-12 | Kapitalisasi sapaan/kekerabatan untuk rujukan khusus | Pembedaan sapaan/rujukan khusus dari penggunaan umum | **Tunda.** Kata seperti `ibu` dan `ayah` tidak boleh dikapitalisasi tanpa konteks referensial. |

### Keputusan cakupan pertama

Jalur A **tidak** akan mengklaim memeriksa 12 aturan sekaligus. Kandidat pertama adalah EJA-04 dalam pola tanggal eksplisit yang didefinisikan di bawah. Aturan lainnya harus dinyatakan belum didukung pada laporan cakupan, bukan diam-diam dianggap lulus.

EJA-04 pun tidak boleh diterapkan ke setiap kemunculan kata hari/bulan tanpa konteks. Contoh `Minggu` dapat merujuk nama hari atau satuan pekan; nama hari juga dapat muncul sebagai nama orang. Karena itu pola yang belum dapat menentukan fungsi harus menghasilkan `needs_context`.

## 3. Pola EJA-04 yang diizinkan untuk kandidat pertama

Pola awal dibatasi pada bentuk tanggal yang eksplisit dan telah dicantumkan dalam paket uji, misalnya:
- nama bulan setelah angka tanggal: `2 januari 2026`;
- nama hari sebelum tanggal: `senin, 2 januari 2026`;
- nama hari setelah penanda tanggal yang eksplisit: `pada senin` atau `hari senin`, sepanjang pola persis tersebut lolos evaluasi.

Daftar leksikal yang boleh dikenali:
- Hari: `Senin, Selasa, Rabu, Kamis, Jumat, Sabtu, Minggu`.
- Bulan: `Januari, Februari, Maret, April, Mei, Juni, Juli, Agustus, September, Oktober, November, Desember`.

Ketentuan konservatif:
1. Nama bulan dalam pola tanggal eksplisit boleh ditandai jika huruf awalnya tidak kapital.
2. Nama hari hanya boleh ditandai jika berada dalam pola tanggal eksplisit yang sudah diuji.
3. `Minggu` yang tidak memiliki konteks tanggal jelas wajib `needs_context`, karena dapat berarti hari Minggu atau pekan.
4. Nama hari/bulan yang muncul sebagai kemungkinan nama orang, judul, kutipan, atau fragmen tidak boleh dikoreksi otomatis.
5. Jika batas pola tidak jelas, tidak ada saran koreksi; keluarkan `needs_context`.
6. Tidak boleh menggunakan kamus nama orang/tempat yang tidak ada dalam sumber/acuan yang disetujui.
7. Tidak boleh mengubah karakter lain, spasi, tanda baca, atau kapitalisasi selain span yang benar-benar didukung pola EJA-04.

**Catatan:** pola di atas adalah proposal yang harus ditinjau evaluator. Pola belum dianggap sah hanya karena tertulis di dokumen ini.

## 4. Kontrak keluaran yang diusulkan

Keluaran pemeriksaan tetap memuat teks asli dan memisahkan temuan per span. Bentuk konseptual:

- `input`: string asli, tidak diubah;
- `coverage.checked_rules`: ID aturan yang benar-benar diperiksa;
- `coverage.deferred_rules`: ID aturan yang belum didukung;
- `findings`: daftar temuan, setiap item memuat:
  - `rule_id`;
  - `span.start` dan `span.end` sebagai indeks karakter dengan rentang awal-inklusif/akhir-eksklusif;
  - `observed`;
  - `status`: `issue`, `no_issue`, atau `needs_context`;
  - `suggestion`: teks saran atau `null`;
  - `explanation`: alasan singkat dalam bahasa Indonesia.

Ketentuan:
- `issue` hanya jika pola yang disetujui membuktikan bentuk yang perlu diperbaiki.
- `no_issue` hanya jika suatu pola yang memang diperiksa terbukti sesuai aturan; bukan status default untuk teks yang tidak dianalisis.
- `needs_context` jika bentuk cocok sebagian tetapi konteks tidak cukup untuk memutuskan.
- Tidak ada temuan untuk aturan tertunda yang boleh ditafsirkan sebagai `no_issue`.
- Tidak ada field `corrected_text` dan tidak ada operasi rewrite pada tahap ini.
- Span harus menunjuk tepat ke teks asli; pengujian harus memastikan Unicode dan tanda baca tidak menggeser rentang.
- Status pemeriksaan keseluruhan, jika disediakan, harus menunjukkan cakupan parsial secara eksplisit dan tidak boleh menyatakan "semua ejaan benar".

Bentuk JSON final/API adalah keputusan implementasi setelah spesifikasi ini disetujui evaluator; contoh di atas adalah kontrak semantik, bukan kewajiban nama field tambahan yang belum ditinjau.

## 5. Paket kasus uji kandidat EJA-04

Semua kasus di bawah merupakan kunci rancangan yang perlu ditinjau evaluator. `issue` berarti ada temuan kapitalisasi; `no_issue` berarti pola tanggal dikenali dan kapitalisasi benar; `needs_context` berarti pola atau fungsi belum dapat dipastikan.

| ID | Masukan | Target | Hasil yang diharapkan | Alasan |
|---|---|---|---|---|
| A-E04-001 | `Kami berangkat pada senin, 2 januari 2026.` | `senin`, `januari` | `issue` pada dua span; saran `Senin`, `Januari` | Pola hari + tanggal eksplisit. |
| A-E04-002 | `Rapat dimulai pada 2 februari 2026.` | `februari` | `issue`; saran `Februari` | Bulan mengikuti angka tanggal. |
| A-E04-003 | `Acara berlangsung hari selasa.` | `selasa` | `needs_context` kecuali pola `hari + nama hari` disetujui sebagai pola yang cukup kuat | Tidak ada tanggal numerik; pola harus divalidasi evaluator. |
| A-E04-004 | `Senin, 2 Januari 2026.` | `Senin`, `Januari` | `no_issue` | Pola tanggal eksplisit dan kapitalisasi benar. |
| A-E04-005 | `Tanggal 17 agustus 1945 diperingati.` | `agustus` | `issue`; saran `Agustus` | Bulan berada setelah angka tanggal. |
| A-E04-006 | `Kami bertemu pada minggu depan.` | `minggu` | `needs_context` atau tidak diperiksa; tidak boleh menyarankan `Minggu` | `minggu` bermakna pekan, bukan nama hari. |
| A-E04-007 | `Minggu, 3 mei 2026.` | `Minggu`, `mei` | `issue` pada `mei`; hari sudah kapital | Tanggal eksplisit memperjelas nama hari. |
| A-E04-008 | `Senin hadir lebih awal.` | `Senin` | `needs_context` | Dapat berupa nama orang; tidak ada pola tanggal. |
| A-E04-009 | `Kami pulang pada desember.` | `desember` | `needs_context` dalam pola pertama; jangan memberi saran otomatis tanpa pola tanggal eksplisit | Nama bulan tanpa tanggal tidak cukup untuk kontrak konservatif awal. |
| A-E04-010 | `2 desember 2026` | `desember` | `issue`; saran `Desember` | Fragmen tanggal numerik eksplisit tetap dapat diperiksa pada aturan bulan. |
| A-E04-011 | `2 Desember 2026` | `Desember` | `no_issue` | Pola tanggal dan kapitalisasi benar. |
| A-E04-012 | `Minggu ini kami beristirahat.` | `Minggu` | `needs_context` atau tidak diperiksa; tidak boleh dipastikan sebagai nama hari | Dapat berarti pekan ini; kapitalisasi awal kalimat tidak menjadi bukti bahwa kata itu nama hari. |
| A-E04-013 | `Pada rabu, 4 maret 2026, kami berangkat.` | `rabu`, `maret` | `issue` pada dua span | Hari dan bulan dalam konstruksi tanggal eksplisit. |
| A-E04-014 | `Kami bertemu Rabu di kantor.` | `Rabu` | `needs_context` | Bisa nama hari atau nama orang; tidak ada tanggal eksplisit. |
| A-E04-015 | `Jadwal: 5 november 2026.` | `november` | `issue`; saran `November` | Label + tanggal numerik eksplisit. |
| A-E04-016 | `Bulan depan, pada 5 januari, kegiatan dimulai.` | `januari` | `issue`; saran `Januari` | Bulan mengikuti angka tanggal. |

### Syarat validasi paket uji

- Evaluator harus meninjau setiap kunci, terutama A-E04-003, A-E04-006, A-E04-009, A-E04-012, dan A-E04-014.
- Jika evaluator menilai suatu pola belum cukup kuat, kasus harus tetap `needs_context` atau dipindahkan ke daftar belum didukung; jangan mengubah kunci demi memperluas cakupan.
- Tambahkan kasus positif/negatif untuk setiap pola yang disetujui sebelum implementasi.
- Paket ini tidak menguji aturan EJA-01 sampai EJA-03 dan EJA-05 sampai EJA-12 sebagai kemampuan runtime.

## 6. Kasus keselamatan lintas aturan

| ID | Masukan | Perilaku wajib |
|---|---|---|
| A-SAFE-001 | `Awas?` | Teks dan tanda tanya tetap persis; jangan sarankan tanda seru. |
| A-SAFE-002 | `Kamu sudah makan.` | Jangan ubah titik menjadi tanda tanya tanpa bukti maksud bertanya. |
| A-SAFE-003 | `ibu datang.` | Jangan mengubah `ibu` menjadi `Ibu` tanpa konteks sapaan/rujukan khusus; aturan awal kalimat dan EJA-12 harus dipisahkan. |
| A-SAFE-004 | `budi tinggal di bandung.` | Jangan mengklaim dapat mengenali nama orang/tempat jika EJA-02/EJA-03 belum didukung. |
| A-SAFE-005 | `Buku itu di baca.` | Jangan otomatis menggabungkan `di baca` menjadi `dibaca` sampai EJA-05/EJA-06 memiliki pola morfologi dan uji yang disetujui. |
| A-SAFE-006 | `disekolah` | Jangan otomatis mengubah menjadi `di sekolah` hanya dengan pencocokan awalan karakter. |
| A-SAFE-007 | `Pilihan itu-menurut saya-cukup baik.` | Jangan mengganti tanda hubung menjadi tanda pisah tanpa pola fungsi sisipan yang tervalidasi. |

## 7. Gerbang sebelum implementasi

Implementasi kandidat EJA-04 belum boleh dimulai sebelum:
1. evaluator menerima klasifikasi 12 aturan;
2. evaluator menerima atau merevisi pola tanggal EJA-04;
3. seluruh kunci paket uji disepakati, terutama kasus ambigu;
4. kontrak keluaran dan definisi span disepakati;
5. batas cakupan yang belum didukung dicatat eksplisit.

Setelah disetujui, implementasi harus berada pada branch/PR terpisah dan hanya mengubah modul pemeriksaan ejaan serta tes khususnya. Jangan mengubah loader kata, classifier Jalur B, JSON referensi, Semantic 12, Reasoning 6, KnowledgeEngine, ChatbotAdapter, playground, workflow, atau `main`.

## 8. Pernyataan batas

Dokumen ini **belum merupakan implementasi dan belum membuktikan kemampuan runtime**. Keberhasilan CI untuk dokumen ini hanya membuktikan integritas perubahan dokumen. Pemeriksa yang kelak dibangun hanya boleh mengklaim aturan/pola yang benar-benar diimplementasikan dan diuji.
