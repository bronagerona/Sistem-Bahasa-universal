# RENCANA IMPLEMENTASI NYATA — PEMAHAMAN BAHASA INDONESIA ILIS

**Branch:** `ilis-v2-development`  
**Status:** Rencana implementasi bertahap — BELUM DIEKSEKUSI  
**Acuan:** `docs/DAFTAR_DASAR_TAHAP_01.md` sampai `docs/DAFTAR_DASAR_TAHAP_04.md`, dokumen kurikulum, dokumen penguatan kurikulum, dan `docs/IMPLEMENTASI_TAHAP_01.md`  
**Batas dokumen:** Hanya rencana. Tidak membuat folder/data, tidak mengubah dataset JSONL, kode, runtime, konfigurasi, atau branch `main`.

---

## 1 — Prinsip Implementasi

1. **Berurutan, tidak melompat.** Tahap 1 harus selesai dan melewati gerbang kelulusan sebelum pekerjaan implementasi Tahap 2 dimulai. Aturan yang sama berlaku untuk Tahap 2 ke 3 dan Tahap 3 ke 4.
2. **Referensi bukan data aktif.** Daftar dasar dan aturan di `data/reference/` hanya bahan kurasi. Isinya tidak otomatis dibaca atau digunakan oleh runtime ILIS.
3. **Runtime hanya berisi materi yang sudah disetujui.** Materi baru boleh dipromosikan ke `data/runtime/` setelah pemeriksaan, pengujian, pencatatan hasil, dan persetujuan gerbang tahap. Promosi dilakukan sebagai salinan/versi yang disetujui, bukan menghapus atau memindahkan satu-satunya sumber referensi.
4. **Setiap tahap memiliki bukti kelulusan.** Bukti minimal meliputi versi materi, paket uji, hasil aktual, hasil yang diharapkan, catatan kasus gagal/ambigu, dan keputusan evaluator.
5. **Pengetahuan umum tetap ditunda.** Tidak ada perluasan fakta ensiklopedis atau pengembangan Knowledge Base selama empat tahap fondasi bahasa belum selesai dan disetujui.
6. **Utamakan ketepatan.** Lebih sedikit materi yang benar dan teruji lebih baik daripada daftar besar yang belum diperiksa.
7. **Jujur terhadap ketidakpastian.** Sistem harus dapat menyatakan belum tahu, belum cukup konteks, atau meminta klarifikasi. Tidak boleh mengarang jawaban untuk mengejar skor.
8. **Dokumen, data, dan kemampuan runtime adalah hal berbeda.** Selesainya dokumen atau daftar referensi tidak membuktikan bahwa kemampuan tersebut sudah berjalan di sistem.

## 2 — Struktur Dataset yang Diusulkan

Struktur berikut adalah **rancangan saja**. Folder dan file ini belum dibuat oleh dokumen ini.

```text
docs/
  panduan konsep, kurikulum, daftar dasar, format, dan laporan evaluasi

data/
  reference/
    tahap_01/
      daftar_kata.json
      aturan_ejaan.json
    tahap_02/
      aturan_morfologi.json
      pola_frasa_kalimat.json
    tahap_03/
      pola_maksud_konteks.json
    tahap_04/
      pola_wacana_variasi.json
  runtime/
    tahap_01/
    tahap_02/
    tahap_03/
    tahap_04/

tests/
  tahap_01/
  tahap_02/
  tahap_03/
  tahap_04/
```

**Fungsi setiap bagian:**

- **`docs/`** — sumber penjelasan manusia: kurikulum, panduan tahap, daftar dasar, keputusan, dan laporan. Dokumen tetap menjadi rujukan; bukan otomatis file runtime.
- **`data/reference/`** — hasil konversi awal dari daftar dasar dan aturan. Status awal selalu referensi/belum diuji. Boleh diperbaiki tanpa mengubah runtime.
- **`data/runtime/`** — hanya versi materi yang telah melewati gerbang dan mendapat persetujuan. Tidak boleh mengambil langsung dari folder referensi.
- **`tests/`** — kasus uji, hasil yang diharapkan, dan catatan evaluasi per tahap. Paket uji harus dapat dijalankan ulang dengan versi materi yang jelas.

### Aturan promosi referensi ke runtime

1. Referensi diberi versi dan status.
2. Evaluator meninjau isi dan label.
3. Paket uji dijalankan dan hasilnya disimpan.
4. Semua kegagalan kritis diperbaiki atau dinyatakan sebagai batas yang disetujui secara eksplisit.
5. Gerbang tahap dinyatakan lulus oleh evaluator dan disetujui Owner.
6. Baru setelah itu dibuat salinan rilis ke folder runtime dengan nomor versi yang sama atau versi rilis baru.
7. Catatan sumber dan riwayat perubahan tetap dipertahankan. Jangan menghapus jejak asal materi.

**Penting:** Folder `data/runtime/` tidak berarti sistem otomatis memuatnya. Mekanisme pemuatan runtime, bila kelak diperlukan, merupakan pekerjaan teknis terpisah yang harus dirancang, ditinjau, dan disetujui. Rencana ini tidak memberi izin untuk mengubah loader atau kode.

## 3 — Urutan Langkah Per Tahap

### FASE PERSIAPAN — Sebelum Tahap 1

- [ ] Tinjau ulang empat daftar dasar dan dokumen penguatan kurikulum.
- [ ] Catat isu yang belum tuntas sebelum konversi, termasuk klasifikasi yang bergantung konteks.
- [ ] Rancang penyalinan daftar Tahap 1 ke `data/reference/tahap_01/`; **belum dilakukan sekarang**.
- [ ] Tetapkan format standar data sederhana dan aturan validasinya.
- [ ] Siapkan rancangan dokumen `docs/FORMAT_DATASET.md`; **file belum dibuat sekarang**.
- [ ] Tetapkan penamaan versi, status, sumber, dan catatan perubahan.
- [ ] Siapkan cara merekam hasil uji agar hasil antarversi dapat dibandingkan.
- [ ] Minta Dola meninjau rancangan teknis dan kriteria sebelum pekerjaan data dimulai.

**Gerbang Persiapan:** format dan status data dipahami, sumber referensi jelas, isu yang belum selesai tercatat, serta evaluator menyetujui rancangan. Belum ada materi yang diaktifkan.

### FASE TAHAP 1 — Fondasi Bentuk Bahasa

**Cakupan:** huruf dan bunyi dasar, ejaan, tanda baca dasar, kata depan `di/ke/dari`, pembedaan kata depan `di` dan awalan `di-` pada contoh yang ditentukan, serta 11 kelas kata.

Langkah kerja:

- [ ] Kurasi daftar kata dari `docs/DAFTAR_DASAR_TAHAP_01.md` ke format referensi. Target jumlah bukan alasan untuk menambah kata yang salah kelas.
- [ ] Periksa setiap entri: ejaan, kelas kata, fungsi, contoh penggunaan, dan kemungkinan ambiguitas.
- [ ] Buat paket uji Tahap 1 sekurang-kurangnya 20 kasus awal. Paket harus mencakup seluruh 11 kelas kata, ejaan, kapitalisasi, tanda baca, serta kata depan dan awalan. Tambahkan kasus sampai cakupan memadai; 20 kasus bukan batas maksimum.
- [ ] Jalankan pengujian pada versi sistem dan materi yang dicatat.
- [ ] Catat masukan, keluaran aktual, hasil yang diharapkan, status, dan alasan penilaian untuk setiap kasus.
- [ ] Perbaiki materi atau sistem melalui pekerjaan terpisah yang disetujui; jangan mengubah kunci uji hanya agar cocok dengan keluaran sistem.

**Gerbang Lulus Tahap 1 — syarat yang diusulkan:**

- Akurasi keseluruhan minimal **90%** pada paket uji yang telah ditinjau.
- **Tidak ada kesalahan kritis** pada pembedaan ejaan yang menjadi target, atau klasifikasi yang sudah memiliki konteks dan kunci jawaban tegas.
- Tidak ada tebakan pada kasus yang memang ambigu atau kekurangan konteks; jawaban yang benar dapat berupa “perlu konteks”.
- Seluruh 11 kelas kata tercakup dalam pengujian. Keterbatasan jumlah artikula yang telah dicatat pada daftar dasar harus diselesaikan melalui keputusan evaluator; **jangan mengarang contoh untuk memenuhi kuota**.
- Semua hasil dan isu terbuka terdokumentasi; Dola meninjau hasil; Owner menyetujui penutupan tahap.

**Jika lulus:** materi Tahap 1 dapat dipromosikan sebagai versi runtime yang disetujui. Tahap 2 baru boleh dimulai setelah keputusan lulus tercatat.  
**Jika belum lulus:** tetap di Tahap 1; perbaiki sumber masalah dan ulangi paket uji.

### FASE TAHAP 2 — Kata dan Kalimat

**Prasyarat:** Gerbang Tahap 1 telah lulus dan disetujui.

**Cakupan:** prefiks, sufiks, konfiks, reduplikasi, perubahan bunyi, frasa, pola kalimat dasar, jenis kalimat, aktif/pasif, serta makna dasar sesuai daftar Tahap 2.

Langkah kerja:

- [ ] Kurasi aturan dan contoh dari `docs/DAFTAR_DASAR_TAHAP_02.md` ke folder referensi Tahap 2.
- [ ] Pastikan setiap contoh pembentukan kata benar-benar lazim dan sesuai pola; jangan menganggap semua imbuhan dapat dipasangkan dengan semua kata.
- [ ] Siapkan kasus uji untuk mengenali kata dasar dan kata berimbuhan, perubahan bentuk, membedakan frasa dan kalimat, mengenali pola kalimat, aktif/pasif, dan makna penyangkalan dasar.
- [ ] Jalankan uji terpisah untuk setiap kelompok materi, lalu uji gabungan.
- [ ] Catat kesalahan, bentuk yang tidak teratur, dan kasus yang membutuhkan konteks.

**Gerbang Lulus Tahap 2 — syarat yang diusulkan:**

- Akurasi keseluruhan minimal **90%** pada paket uji yang ditinjau.
- Tidak ada kesalahan kritis pada contoh imbuhan, pembedaan kata depan/awalan yang diwarisi dari Tahap 1, atau pembedaan frasa dan kalimat pada kasus yang jelas.
- Sistem tidak membentuk kata yang tidak sah hanya karena pola imbuhan tampak cocok.
- Materi Tahap 1 tetap lulus pada uji regresi.
- Dola meninjau bukti dan Owner menyetujui gerbang.

**Jika lulus:** promosi versi Tahap 2 dilakukan secara terpisah dan Tahap 3 boleh dimulai. Jika gagal, perbaiki Tahap 2 tanpa melanjutkan.

### FASE TAHAP 3 — Maksud dan Konteks

**Prasyarat:** Gerbang Tahap 2 telah lulus dan disetujui.

**Cakupan:** perbedaan bentuk ujaran dan kemungkinan maksud, deiksis/rujukan, elipsis, negasi, aspek waktu, modalitas, makna kontekstual, serta klarifikasi dan perbaikan pemahaman.

Langkah kerja:

- [ ] Kurasi pola ujaran dan penanda dari `docs/DAFTAR_DASAR_TAHAP_03.md` ke folder referensi Tahap 3.
- [ ] Siapkan kasus yang membedakan permintaan langsung/tidak langsung, kemungkinan maksud, rujukan yang jelas/tidak jelas, ujaran tidak lengkap, serta penanda `tidak`, `bukan`, `belum`, `jangan`, `sudah`, `sedang`, `akan`, `mungkin`, dan `pasti`.
- [ ] Uji ujaran yang sama dalam konteks berbeda dan konteks yang sengaja dibuat tidak cukup.
- [ ] Pastikan sistem dapat menyampaikan beberapa kemungkinan atau meminta klarifikasi, bukan memastikan maksud tanpa bukti.
- [ ] Uji agar keyakinan penutur tidak diperlakukan sebagai bukti bahwa suatu pernyataan faktual benar.

**Gerbang Lulus Tahap 3 — syarat yang diusulkan:**

- Akurasi keseluruhan minimal **90%** pada kasus yang memiliki kunci penilaian jelas.
- Tidak ada kesalahan kritis berupa memastikan maksud, rujukan, waktu, atau fakta yang tidak didukung konteks.
- Kasus ambigu ditangani dengan penandaan ketidakpastian atau pertanyaan klarifikasi yang sesuai.
- Uji regresi Tahap 1 dan 2 tetap lulus.
- Dola meninjau bukti dan Owner menyetujui gerbang.

**Jika lulus:** promosi versi Tahap 3 dapat dilakukan dan Tahap 4 boleh dimulai. Jika gagal, tetap di Tahap 3.

### FASE TAHAP 4 — Wacana dan Variasi Bahasa

**Prasyarat:** Gerbang Tahap 3 telah lulus dan disetujui.

**Cakupan:** giliran bicara, kesinambungan dan perpindahan topik, rujukan lintas giliran, klarifikasi/koreksi, ragam baku dan sehari-hari, formal dan santai, lisan dan tulisan, serta ungkapan percakapan umum.

Langkah kerja:

- [ ] Kurasi penanda giliran bicara, kesinambungan topik, peralihan topik, klarifikasi, dan variasi bahasa dari `docs/DAFTAR_DASAR_TAHAP_04.md`.
- [ ] Siapkan minimal 3–5 dialog pendek sebagai uji awal. Setiap dialog harus memiliki beberapa giliran dan tujuan penilaian yang jelas.
- [ ] Perluas paket uji untuk mencakup topik berlanjut, topik berganti, kembali ke topik sebelumnya, koreksi, permintaan klarifikasi, dan perbedaan ragam.
- [ ] Uji percakapan multi-giliran, bukan hanya kalimat tunggal.
- [ ] Pastikan sistem tidak menyimpulkan emosi, hubungan pribadi, atau latar yang tidak dinyatakan.

**Gerbang Lulus Tahap 4 — syarat yang diusulkan:**

- Akurasi keseluruhan minimal **90%** pada paket dialog yang telah ditinjau.
- Tidak ada kesalahan kritis berupa kehilangan rujukan yang jelas, mencampur topik tanpa dasar, atau mengarang konteks/emosi.
- Sistem dapat meminta klarifikasi dan memperbaiki salah paham dengan wajar.
- Uji regresi Tahap 1, 2, dan 3 tetap lulus.
- Dola meninjau bukti dan Owner menyetujui gerbang.

**Jika lulus:** fondasi implementasi empat tahap bahasa dapat dinyatakan selesai berdasarkan bukti. Ini tidak otomatis mengaktifkan pengetahuan umum atau memberi izin perubahan lain.

## 4 — Format Data Sederhana yang Diusulkan

Berikut contoh **skema rancangan**, bukan file dataset yang dibuat atau diaktifkan:

```json
{
  "versi": "1.0-tahap1",
  "sumber": "docs/DAFTAR_DASAR_TAHAP_01.md",
  "status": "referensi/belum-diuji",
  "daftar_kata": [
    {
      "kata": "buku",
      "kelas": ["Nomina"],
      "catatan": "kata dasar",
      "contoh": ["Saya membaca buku."],
      "status_entri": "belum-ditinjau"
    }
  ]
}
```

**Arti kolom:**

- `versi`: versi skema atau paket materi; perubahan besar harus menghasilkan versi yang dapat dibedakan.
- `sumber`: dokumen asal agar setiap entri dapat ditelusuri.
- `status`: status keseluruhan paket, misalnya `referensi/belum-diuji`, `sedang-ditinjau`, `lulus-uji`, atau `disetujui-runtime`.
- `kata`: bentuk kata yang dicatat.
- `kelas`: satu atau lebih label kelas kata yang memang didukung bukti pemakaian. Lebih dari satu label harus disertai contoh/konteks yang membedakan fungsi.
- `catatan`: penjelasan ringkas, misalnya kata dasar atau batas pemakaian.
- `contoh`: kalimat singkat untuk memperlihatkan fungsi, bukan untuk menambah fakta pengetahuan umum.
- `status_entri`: status pemeriksaan entri, tidak boleh disamakan dengan status paket.

Untuk implementasi format yang sebenarnya, dokumen `docs/FORMAT_DATASET.md` nantinya perlu menetapkan daftar status yang sah, aturan kolom wajib, validasi, penanganan ambiguitas, dan versi skema. Dokumen tersebut **belum dibuat dalam tugas ini**. Skema final juga harus ditinjau Dola sebelum konversi massal.

## 5 — Risiko dan Pengaman

| Risiko | Pencegahan |
|---|---|
| Semua materi langsung dimasukkan ke sistem | Tahap demi tahap; referensi tidak dibaca runtime; satu gerbang pada satu waktu |
| Materi pengetahuan umum tercampur | Folder dan ruang lingkup terpisah; pengetahuan umum tetap ditunda |
| Tidak jelas mana yang sudah diuji | Status paket dan status entri dicatat terpisah; simpan hasil uji per versi |
| Revisi berulang mengubah hasil lama | Gunakan versi, catatan perubahan, dan simpan laporan uji versi sebelumnya |
| Target jumlah membuat contoh dipaksakan | Ketepatan lebih utama; keterbatasan kelas seperti artikula harus dievaluasi, bukan diisi dengan contoh palsu |
| Kata yang sama dipaksa satu kelas | Simpan konteks penggunaan; izinkan lebih dari satu fungsi jika benar-benar didukung |
| Sistem menebak ketika konteks kurang | Sertakan kasus ambigu; jawaban “belum cukup konteks” dapat menjadi hasil yang benar |
| Materi baru merusak kemampuan sebelumnya | Jalankan uji regresi semua tahap yang sudah lulus |
| Dokumen dianggap bukti kemampuan runtime | Pisahkan status dokumen, referensi tervalidasi, hasil uji runtime, dan persetujuan |
| Perubahan teknis melebar dari rencana | Setiap perubahan kode, loader, konfigurasi, atau dataset aktif memerlukan ruang lingkup dan persetujuan terpisah |

## 6 — Kriteria Berhenti dan Melanjutkan

- Setelah setiap fase, lakukan evaluasi: apakah bukti sudah cukup untuk lulus, atau masih ada masalah yang perlu diperbaiki?
- Jangan memulai tahap berikutnya hanya karena daftar tahap sebelumnya sudah selesai ditulis atau dikonversi.
- Jika ada kegagalan kritis, hentikan promosi dan tetap di tahap yang sedang dikerjakan.
- Jika hasil belum meyakinkan, tambah atau perbaiki kasus uji, lalu jalankan ulang. Jangan menurunkan standar hanya agar tahap cepat selesai.
- Pekerjaan boleh dihentikan kapan saja. Catat tahap aktif, versi materi, hasil terakhir, isu terbuka, dan langkah berikutnya agar dapat dilanjutkan tanpa mengulang dari awal.
- Perubahan pada materi yang sudah lulus harus memiliki versi baru dan uji regresi yang sesuai.
- Tahap 4 bukan tenggat yang harus dikejar. Kekuatan Tahap 1 lebih penting daripada kecepatan mencapai Tahap 4.

## 7 — Status, Batas, dan Langkah Berikutnya

Pada saat dokumen ini dibuat:

- Keempat daftar dasar merupakan **dokumen referensi konseptual**, bukan dataset runtime.
- Tahap 1 belum dinyatakan lulus implementasi hanya berdasarkan daftar dan dokumen yang tersedia.
- Struktur folder di Bagian 2 masih rancangan.
- Format dataset di Bagian 4 masih usulan.
- Tidak ada dataset aktif yang diubah atau dibuat.
- Tidak ada kode, loader, Semantic, Reasoning, KnowledgeEngine, playground, atau branch `main` yang diubah.
- Pengetahuan umum tetap ditunda.

**Urutan berikutnya yang disarankan:** evaluasi rencana ini oleh Dola; setelah koreksi diselesaikan dan rencana diterima, Owner dapat memberi keputusan terpisah untuk memulai Fase Persiapan. Penerimaan dokumen rencana tidak otomatis menjadi izin membuat dataset atau mengubah runtime.

**Prinsip penutup: Bangun satu lapisan bahasa dengan benar, buktikan melalui pengujian, catat hasilnya, lalu lanjut hanya setelah gerbangnya benar-benar lulus.**
