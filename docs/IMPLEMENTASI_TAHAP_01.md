# IMPLEMENTASI TAHAP 01 — FONDASI DASAR

**Acuan utama:** `docs/TAHAP_01_FONDASI_DASAR.md` dan `docs/PENGUATAN_KURIKULUM_BAHASA.md`  
**Branch:** `ilis-v2-development`  
**Status:** Rencana Kerja — BELUM DIIMPLEMENTASIKAN  
**Cakupan:** Dokumen perencanaan dan rancangan pengujian; bukan perubahan kode atau dataset

---

## 1 — Pendahuluan & Prinsip Kerja

### Mengapa Tahap 1 dikerjakan lebih dahulu?

Fonologi, ejaan, dan pengenalan kelas kata merupakan lapisan awal untuk mengenali bentuk bahasa Indonesia. Tahap berikutnya bergantung pada kemampuan dasar ini: sistem perlu mengenali bentuk kata dan petunjuk kategorinya sebelum mempelajari pembentukan kata, susunan kalimat, maksud, dan alur percakapan.

### Prinsip kerja

1. **Kenali dulu, pahami nanti.** Tahap ini berfokus pada bentuk tulisan, ejaan dasar, dan pengenalan kelas kata.
2. **Kata dasar terlebih dahulu.** Jangan memperluas cakupan ke proses imbuhan, reduplikasi, atau pembentukan kata turunan. Bentuk berimbuhan hanya boleh muncul sebagai pembanding ejaan kata depan dan awalan yang memang sudah disebut dalam panduan.
3. **Petunjuk kelas kata bukan aturan mutlak.** Kategori sebuah bentuk dapat bergantung pada pemakaiannya. Jika konteks tidak cukup, tandai sebagai ambigu atau perlu konteks; jangan memaksakan satu label.
4. **Kualitas di atas kuantitas.** Mulai dari sedikit contoh yang ditinjau dengan baik, lalu lengkapi target minimum secara terukur.
5. **Tidak ada pengetahuan umum.** Jangan memasukkan fakta ensiklopedis, geografi, sains, sejarah, atau fakta dunia ke Tahap 1.

### Batasan

Tahap 1 tidak mencakup imbuhan sebagai materi, frasa/klausa/sintaksis, pemaknaan kontekstual, maksud tersirat, pragmatik, percakapan multi-giliran, maupun pengayaan pengetahuan umum.

---

## 2 — Daftar Tugas Rinci Tahap 1

Setiap tugas di bawah adalah rencana pekerjaan. Pelaksanaan teknis baru boleh dimulai setelah rencana ditinjau dan disetujui melalui alur evaluasi proyek. Tidak ada perubahan runtime atau dataset yang diizinkan oleh dokumen ini.

### A. Fonologi & Ejaan Dasar

**Tujuan:** Menyusun acuan konsisten agar sistem dapat mengenali bentuk huruf, pola ejaan dasar, dan tanda baca.

| ID | Tugas | Rincian pekerjaan | Keluaran yang harus tersedia |
|---|---|---|---|
| 1.1 | Daftar huruf vokal dan konsonan | Cantumkan 26 huruf abjad Latin; kelompokkan 5 huruf vokal (a, i, u, e, o) dan 21 huruf konsonan. Catat bahwa q dan x tetap bagian abjad meskipun lebih jarang digunakan. | Daftar huruf lengkap dan pengelompokan yang diperiksa |
| 1.2 | Pengenalan gabungan huruf | Catat diftong ai, au, oi, ei serta gabungan konsonan kh, ng, ny, sy sesuai contoh dalam panduan. Bedakan gabungan huruf dari huruf abjad baru. | Tabel bentuk dan contoh; tidak perlu analisis fonetik lanjutan |
| 1.3 | Huruf kapital | Susun contoh untuk awal kalimat, nama orang, nama tempat/wilayah, dan nama hari. Tambahkan contoh judul hanya sebagai pengenalan terbatas dan tandai bahwa aturan rinci judul perlu rujukan ejaan tersendiri sebelum diperluas. | Pasangan contoh benar/salah dan kunci koreksi |
| 1.4 | Kata depan di, ke, dari | Bedakan kata depan yang ditulis terpisah (di rumah, ke sekolah, dari kantor) dari awalan di- yang melekat pada kata kerja (ditulis, dibaca). Sertakan bentuk tanya **di mana** yang ditulis terpisah; bentuk **dimana** tidak dipakai untuk maksud tersebut. | Tabel benar/salah dan alasan singkat |
| 1.5 | Tanda baca dasar | Susun fungsi dan contoh titik, koma, tanda tanya, tanda seru, serta tanda petik untuk menandai kutipan langsung sederhana. | Tabel tanda baca dan latihan pemilihan tanda |
| 1.6 | Pemeriksaan konsistensi ejaan | Periksa apakah semua contoh konsisten, mudah dibaca, dan tidak diam-diam memasukkan materi Tahap 2–4. | Daftar pemeriksaan dan catatan koreksi |

**Catatan cakupan:** Panduan Tahap 1 secara eksplisit membahas huruf kapital pada awal kalimat, nama orang, tempat/wilayah, dan hari; tanda baca titik, koma, tanya, seru; serta kata depan di/ke/dari. Tanda petik dan kapitalisasi judul ditambahkan sebagai cakupan latihan terbatas sesuai rencana ini, bukan alasan untuk memperluas materi ke aturan ejaan lanjutan.

### B. Kelas Kata

**Tujuan:** Menyusun acuan pengenalan awal untuk 11 kelas kata dengan istilah linguistik baku.

#### B.1 Daftar 11 kelas kata

| No. | Istilah baku | Penjelasan sederhana |
|---|---|---|
| 1 | Nomina | Menamai orang, tempat, benda, makhluk, atau hal |
| 2 | Verba | Menyatakan tindakan, proses, atau keadaan |
| 3 | Adjektiva | Menyatakan sifat, keadaan, atau kualitas |
| 4 | Adverbia | Memberi keterangan, misalnya waktu, frekuensi, cara, atau tingkat |
| 5 | Pronomina | Menggantikan atau menunjuk orang, benda, atau hal |
| 6 | Numeralia | Menyatakan jumlah atau urutan |
| 7 | Preposisi | Menandai hubungan seperti tempat, arah, asal, atau tujuan |
| 8 | Konjungsi | Menghubungkan satuan bahasa |
| 9 | Interjeksi | Menyatakan seruan atau reaksi spontan |
| 10 | Artikula | Mendampingi nomina untuk penandaan tertentu |
| 11 | Partikel | Memberi fungsi gramatikal, penegasan, atau nuansa tertentu |

#### B.2 Kumpulan kata dasar

Susun **minimal 10 contoh untuk setiap kelas kata** (minimal 110 entri contoh seluruhnya). Daftar yang sudah ada pada panduan Tahap 1 menjadi titik awal, bukan batas akhir. Tambahan kata harus diperiksa agar:
- merupakan bentuk dasar atau bentuk leksikal yang memang tidak sedang diajarkan sebagai hasil proses imbuhan;
- lazim dan mudah dipahami;
- sesuai dengan kelas kata yang dicantumkan pada penggunaan contoh;
- tidak bergantung pada fakta pengetahuan umum;
- tidak dipaksakan menjadi satu kelas jika bentuknya dapat berfungsi berbeda dalam konteks lain.

Setiap entri sekurang-kurangnya memiliki: **bentuk kata, kelas kata, penjelasan/fungsi sederhana, dan contoh pemakaian singkat**. Contoh pemakaian hanya untuk memperjelas fungsi kata, bukan untuk mengajarkan sintaksis.

**Catatan status audit:** field penjelasan/makna sederhana dan contoh pemakaian pada `kata_dasar.json` belum terisi secara sistematis. Keduanya menjadi **backlog wajib sebelum Tahap 1 dinyatakan SELESAI PENUH**, tetapi bukan penghalang bagi kemampuan runtime terbatas yang sudah berjalan dan diuji saat ini. Jangan mengisi atau memperluas data sekarang tanpa tugas dan persetujuan tersendiri.

Untuk kelas yang jumlah anggotanya terbatas atau yang contoh umumnya berupa partikel terikat (misalnya -lah, -kah, -tah), jangan mengarang kata baru demi memenuhi angka. Catat bentuk yang valid, jelaskan batas jumlah contoh mandiri, dan minta evaluasi sebelum menetapkan cara menghitung target. Target 10 adalah sasaran kurasi, bukan izin membuat contoh yang tidak tepat.

#### B.3 Petunjuk pengenalan dasar

Susun petunjuk awal untuk setiap kelas kata berdasarkan fungsi dan contoh. Petunjuk tidak boleh diperlakukan sebagai aturan mutlak. Misalnya:
- nomina sering menamai sesuatu;
- verba sering menyatakan tindakan atau proses;
- adjektiva sering menyatakan sifat;
- adverbia sering memberi keterangan;
- pronomina sering menggantikan/menunjuk;
- numeralia menyatakan jumlah atau urutan;
- preposisi menandai hubungan;
- konjungsi menghubungkan unsur;
- interjeksi menyatakan seruan;
- artikula mendampingi nomina;
- partikel memberi fungsi gramatikal atau penegasan.

Satu bentuk dapat memiliki fungsi berbeda dalam pemakaian berbeda. Jika pengujian hanya memberi satu kata tanpa konteks dan kategorinya tidak dapat dipastikan, hasil yang benar dapat berupa **perlu konteks**, bukan tebakan.

### C. Pemeriksaan dan Persiapan Materi

| ID | Tugas | Rincian pekerjaan | Keluaran yang harus tersedia |
|---|---|---|---|
| 3.1 | Pemeriksaan istilah | Pastikan 11 nama kelas kata menggunakan istilah baku yang sama di seluruh materi. | Daftar istilah konsisten |
| 3.2 | Pemeriksaan contoh | Tinjau ejaan, kategori, kelaziman, dan penjelasan seluruh contoh. | Daftar contoh yang telah ditinjau |
| 3.3 | Pemeriksaan batas tahap | Tandai dan keluarkan materi imbuhan, sintaksis lanjutan, pragmatik, wacana, serta pengetahuan umum. | Catatan batas cakupan |
| 3.4 | Paket uji manual | Siapkan kasus uji, hasil yang diharapkan, dan alasan/kunci penilaian. | Paket uji Tahap 1 versi dokumen |
| 3.5 | Catatan ketidakpastian | Catat kata yang kategorinya bergantung pada konteks atau belum disepakati. | Daftar isu untuk evaluasi, bukan keputusan otomatis |

---

## 3 — Kriteria Keberhasilan Tahap 1

Tahap 1 **belum dinyatakan selesai** hanya karena dokumen atau daftar contoh telah dibuat. Semua gerbang berikut harus diperiksa:

- [ ] Daftar 26 huruf, kelompok vokal/konsonan, diftong, dan gabungan konsonan tersusun serta ditinjau.
- [ ] Acuan huruf kapital, kata depan di/ke/dari, dan tanda baca dasar tersusun dengan contoh benar/salah.
- [ ] Daftar 11 kelas kata menggunakan istilah baku dan penjelasan sederhana.
- [ ] Kumpulan contoh kata dasar untuk seluruh kelas telah dikurasi; target minimum 10 contoh per kelas dipenuhi atau keterbatasan kelas tertentu dijelaskan dan disetujui evaluator.
- [ ] Setiap contoh memiliki label kelas kata dan alasan/petunjuk pengenalan yang dapat diperiksa.
- [ ] Kasus yang ambigu tidak dipaksa menjadi satu label tanpa konteks yang cukup.
- [ ] Paket uji manual dan kunci hasil yang diharapkan tersedia.
- [ ] Evaluasi materi dan pengujian yang relevan telah dilakukan serta hasilnya dicatat.
- [ ] **BELUM** memasukkan aturan pembentukan imbuhan sebagai materi Tahap 1.
- [ ] **BELUM** memasukkan pengetahuan umum atau fakta ensiklopedis.
- [ ] Tidak ada perubahan dataset JSONL atau kode mesin inti sebagai bagian dari penyusunan rencana ini.

**Pemisahan status yang wajib dijaga:**
1. **Dokumen siap:** daftar tugas dan rancangan uji telah lengkap.
2. **Materi Tahap 1 tervalidasi:** contoh, istilah, dan kunci uji telah ditinjau.
3. **Implementasi Tahap 1 teruji:** hanya dapat dinyatakan setelah ada implementasi yang secara terpisah diizinkan, diuji, dan hasilnya diverifikasi.

Dokumen ini hanya menyiapkan rencana menuju gerbang-gerbang tersebut; tidak menyatakan bahwa sistem runtime sudah memiliki kemampuan di atas.

---

## 4 — Daftar Pengujian Sederhana

Kasus berikut adalah **rancangan uji**, bukan bukti bahwa sistem sudah mampu mengerjakannya. Pengujian runtime belum dilakukan.

| ID | Kasus uji | Hasil yang diharapkan |
|---|---|---|
| T1-01 | Kenali kelas kata: `buku` | Nomina |
| T1-02 | Kenali kelas kata: `makan` | Verba |
| T1-03 | Kenali kelas kata: `cepat` | Adjektiva pada penggunaan sifat; jika tanpa konteks, catat keterbatasan klasifikasi |
| T1-04 | Pilih nomina dari `minum, kursi, merah, tadi` | `kursi` |
| T1-05 | Perbaiki `budi pergi ke bandung` | `Budi pergi ke Bandung.` |
| T1-06 | Nilai ejaan `disekolah` untuk maksud lokasi | Salah; `di sekolah` |
| T1-07 | Nilai ejaan `dimana` untuk kata tanya tempat | Salah; `di mana` |
| T1-08 | Bedakan `di meja` dan `ditulis` | Kata depan terpisah; awalan pada kata kerja melekat |
| T1-09 | Pilih tanda akhir untuk `Kamu sudah makan` sebagai pertanyaan | Tanda tanya: `Kamu sudah makan?` |
| T1-10 | Kenali numeralia: `tiga` | Numeralia |
| T1-11 | Kenali preposisi: `dari` | Preposisi |
| T1-12 | Kenali konjungsi: `tetapi` | Konjungsi |
| T1-13 | Kenali interjeksi: `aduh` | Interjeksi |
| T1-14 | Kenali pronomina: `mereka` | Pronomina |
| T1-15 | Kenali partikel pada `bacalah` | `-lah` sebagai partikel; bukan kata dasar mandiri |

### Cara menjalankan pengujian saat tahap implementasi diizinkan

1. Gunakan daftar kasus yang sama agar hasil dapat dibandingkan.
2. Catat masukan, keluaran aktual, hasil yang diharapkan, status (sesuai/tidak sesuai/perlu konteks), dan catatan evaluator.
3. Jangan mengubah kunci jawaban hanya untuk menyesuaikan keluaran sistem. Jika kunci ternyata keliru, koreksi harus diberi alasan dan ditinjau.
4. Uji ejaan dan klasifikasi secara terpisah agar sumber kesalahan dapat dikenali.
5. Jangan mengklaim lulus berdasarkan pemeriksaan dokumen saja; hasil runtime harus berasal dari pengujian runtime yang benar-benar dijalankan dan direkam.

---

## 5 — Risiko & Hal yang Harus Dihindari

| Risiko | Pencegahan |
|---|---|
| Terlalu banyak kata sekaligus | Mulai dari daftar kecil yang ditinjau; perluas hingga target kurasi tanpa mengorbankan ketepatan |
| Memasukkan kata berimbuhan sebagai materi utama | Tahap 1 berfokus pada kata dasar; pembentukan kata berimbuhan milik Tahap 2 |
| Salah membedakan kata depan dan awalan | Uji pasangan seperti `di rumah` dan `ditulis`; tulis `di mana` terpisah |
| Memaksakan satu kelas kata untuk semua konteks | Gunakan contoh pemakaian; tandai kebutuhan konteks bila bentuk ambigu |
| Memenuhi target 10 dengan contoh yang tidak tepat | Jangan mengarang contoh, terutama untuk partikel; dokumentasikan keterbatasan untuk evaluasi |
| Mencampur pengetahuan umum | Jangan memasukkan fakta seperti “Jakarta ibu kota Indonesia”; fokus pada bentuk dan kategori bahasa |
| Istilah terlalu rumit | Gunakan istilah baku dengan penjelasan sederhana |
| Menganggap rancangan uji sebagai hasil uji | Bedakan rancangan, pelaksanaan, hasil, dan persetujuan |
| Mengubah kode/dataset saat masih merencanakan | Dokumen ini non-kode dan non-dataset; perubahan lain memerlukan tugas dan persetujuan terpisah |

---

## 6 — Langkah Selanjutnya Setelah Selesai

1. Periksa seluruh keluaran dokumen dan daftar tugas terhadap `TAHAP_01_FONDASI_DASAR.md` serta `PENGUATAN_KURIKULUM_BAHASA.md`.
2. Minta evaluator teknis (Dola) meninjau kelengkapan, ketepatan istilah, contoh, rancangan uji, dan risiko. Catat rekomendasi atau koreksi sebelum pekerjaan teknis.
3. Setelah materi dan rancangan uji siap, lakukan evaluasi sesuai tata kelola proyek. Jangan menyatakan Tahap 1 lulus sebelum bukti pengujian yang diperlukan tersedia.
4. Minta persetujuan Owner untuk menutup Tahap 1.
5. **Hanya setelah Tahap 1 disetujui**, buka penyusunan rencana Tahap 2. Tidak boleh melompat ke Tahap 2, 3, 4, atau pengetahuan umum sebelum gerbang Tahap 1 terpenuhi.

Persetujuan atas dokumen rencana ini tidak sama dengan persetujuan implementasi kode atau perubahan dataset. Setiap perubahan tersebut harus melalui keputusan dan ruang lingkup terpisah.

---

## 7 — Status dan Batas Dokumen

- Dokumen ini adalah rencana kerja Tahap 1.
- Tidak membuat, mengubah, atau memuat dataset JSONL.
- Tidak mengubah kode mesin inti, Semantic, Reasoning, KnowledgeEngine, maupun playground.
- Tidak mengubah branch `main`.
- Tidak memulai Tahap 2–4 dan tidak mengerjakan pengetahuan umum.
- Status penyelesaian Tahap 1 tetap **BELUM DINILAI** sampai seluruh kriteria dan gerbang evaluasi dipenuhi.

**Prinsip penutup: Kenali bentuk bahasa dengan benar terlebih dahulu. Bangun fondasi secara bertahap, ukur hasilnya, dan jangan melompat tahap.**
