# PAKET UJI VERIFIKASI TAHAP 1 — FONDASI DASAR

**Branch:** `ilis-v2-development`  
**Status:** Dokumen rencana uji — BELUM DIEKSEKUSI  
**Lingkungan data:** `data/reference/tahap_01_fondasi/`  
**Acuan format:** `docs/FORMAT_DATASET.md`  
**Acuan kata:** `data/reference/tahap_01_fondasi/kata_dasar.json`  
**Acuan ejaan:** `data/reference/tahap_01_fondasi/aturan_ejaan.json`

---

## 1 — Pendahuluan

### Tujuan

Paket ini merinci 60 kasus untuk memeriksa apakah daftar kata dan aturan ejaan Tahap 1 akurat, konsisten, serta layak dipertimbangkan sebagai bahan tahap berikutnya. Pemeriksaan meliputi klasifikasi kelas kata, penerapan aturan ejaan, dan kasus khusus/batas yang tidak boleh dijawab dengan tebakan.

### Lingkungan dan batas

- Seluruh materi yang diuji berada di area **referensi**: `data/reference/tahap_01_fondasi/`.
- Data belum dimuat ke sistem aktif, belum menjadi bagian runtime, dan belum dipromosikan.
- Dokumen ini hanya berisi rencana/kunci yang diharapkan. **Belum ada eksekusi, hasil aktual, skor, atau klaim kelulusan.**
- Pelaksanaan kelak harus mencatat versi data, versi sistem/alat yang diuji, tanggal, pelaksana, hasil aktual, dan bukti kasus gagal.

### Kriteria kelulusan

- Sedikitnya **90% benar**. Untuk keseluruhan 60 kasus, ambang minimal adalah **54 dari 60**.
- **Tidak boleh ada kesalahan kritis**, sekalipun skor total mencapai 90%.
- Kesalahan kritis mencakup salah klasifikasi yang bertentangan dengan konteks/kunci, pembetulan ejaan yang justru menghasilkan bentuk salah, menganggap bentuk majemuk/partikel terikat sebagai kata dasar tunggal, atau mengarang kelas/fakta untuk masukan yang tidak didukung referensi.
- Kasus ambigu yang ditangani dengan meminta konteks atau menyatakan belum dapat dipastikan tidak otomatis dianggap gagal; penilai harus mencocokkan perilaku dengan catatan tiap kasus.
- Skor tinggi tidak menggantikan pemeriksaan manual atas seluruh kesalahan kritis dan isu terbuka.

---

## 2 — Bagian A: Uji Kelas Kata (30 kasus)

**Instruksi:** Cocokkan kata dengan kelas yang dicantumkan pada referensi. Untuk kata yang dapat menjalankan lebih dari satu fungsi, konteks kalimat menjadi penentu. Label ganda tidak boleh diberikan tanpa dasar konteks.

| ID Uji | Kata | Diharapkan Kelas Kata | Catatan |
|---|---|---|---|
| T1-K-001 | buku | Nomina | Dari daftar referensi; menamai benda |
| T1-K-002 | rumah | Nomina | Dari daftar referensi; menamai tempat/bangunan |
| T1-K-003 | kucing | Nomina | Dari daftar referensi; menamai makhluk |
| T1-K-004 | makan | Verba | Dari daftar referensi; tindakan |
| T1-K-005 | tidur | Verba | Dari daftar referensi; keadaan/kegiatan |
| T1-K-006 | tulis | Verba | Dari daftar referensi; bentuk dasar |
| T1-K-007 | baik | Adjektiva | Dari daftar referensi; menyatakan kualitas |
| T1-K-008 | dingin | Adjektiva | Dari daftar referensi; menyatakan keadaan/suhu |
| T1-K-009 | tinggi | Adjektiva | Dari daftar referensi; menyatakan ukuran/sifat |
| T1-K-010 | sering | Adverbia | Dari daftar referensi; keterangan frekuensi |
| T1-K-011 | segera | Adverbia | Dari daftar referensi; keterangan waktu |
| T1-K-012 | mungkin | Adverbia | Dari daftar referensi; keterangan kemungkinan |
| T1-K-013 | aku | Pronomina | Dari daftar referensi; kata ganti orang |
| T1-K-014 | mereka | Pronomina | Dari daftar referensi; kata ganti orang |
| T1-K-015 | siapa | Pronomina | Dari daftar referensi; pronomina tanya |
| T1-K-016 | dua | Numeralia | Dari daftar referensi; bilangan |
| T1-K-017 | pertama | Numeralia | Dari daftar referensi; bilangan tingkat/urutan |
| T1-K-018 | di | Preposisi | Dari daftar referensi; kata depan dalam konstruksi tempat |
| T1-K-019 | dari | Preposisi | Dari daftar referensi; menandai asal |
| T1-K-020 | kepada | Preposisi | Dari daftar referensi; menandai arah/penerima |
| T1-K-021 | karena | Konjungsi | Dari daftar referensi; menghubungkan sebab |
| T1-K-022 | tetapi | Konjungsi | Dari daftar referensi; menghubungkan pertentangan |
| T1-K-023 | aduh | Interjeksi | Dari daftar referensi; seruan/reaksi |
| T1-K-024 | halo | Interjeksi | Dari daftar referensi; sapaan |
| T1-K-025 | sang | Artikula | Dari daftar referensi; kata sandang yang mendampingi nomina |
| T1-K-026 | para | Artikula | Dari daftar referensi; penanda kelompok sebelum nomina |
| T1-K-027 | -kah | Partikel | Dari daftar referensi; partikel terikat, bukan kata bebas |
| T1-K-028 | dong | Partikel | Dari daftar referensi; partikel percakapan |
| T1-K-029 | dekat | Adjektiva | Konteks uji: “Rumah itu dekat.” Fungsi menyatakan sifat/jarak |
| T1-K-030 | dekat | Preposisi | Konteks uji: “Mereka duduk dekat rumah.” Fungsi menandai hubungan lokasi |

**Cakupan kelas:** 11 kelas kata tercakup: nomina, verba, adjektiva, adverbia, pronomina, numeralia, preposisi, konjungsi, interjeksi, artikula, dan partikel. Dua kasus terakhir menguji dua fungsi berbeda dari bentuk `dekat`; keduanya harus dinilai berdasarkan konteks, bukan semata-mata bentuk katanya.

---

## 3 — Bagian B: Uji Ejaan & Penulisan (20 kasus)

**Instruksi:** Terapkan aturan dari `aturan_ejaan.json`. Hasil yang diharapkan merupakan bentuk pembetulan untuk masukan yang diberikan.

| ID Uji | Masukan | Diharapkan Hasil | Aturan Acuan |
|---|---|---|---|
| T1-E-001 | disekolah | di sekolah | Kata depan di ditulis terpisah |
| T1-E-002 | Budi pergi ke bandung | Budi pergi ke Bandung | Huruf kapital nama tempat |
| T1-E-003 | rina sedang membaca | Rina sedang membaca | Huruf kapital pada awal kalimat dan nama orang |
| T1-E-004 | senin kami belajar | Senin kami belajar | Huruf kapital nama hari dan awal kalimat |
| T1-E-005 | kami berangkat pada januari | Kami berangkat pada Januari | Huruf kapital awal kalimat dan nama bulan |
| T1-E-006 | mereka datang dari surabaya | Mereka datang dari Surabaya | Huruf kapital awal kalimat dan nama tempat |
| T1-E-007 | ibu pergi kepasar | Ibu pergi ke pasar | Kata depan ke ditulis terpisah |
| T1-E-008 | surat itu darisekolah | Surat itu dari sekolah | Kapital awal kalimat; kata depan dari terpisah |
| T1-E-009 | buku itu di baca adik | Buku itu dibaca adik. | Awalan di- menyatu; kapital awal kalimat; titik penutup |
| T1-E-010 | pintu di tutup penjaga | Pintu ditutup penjaga. | Awalan di- menyatu; kapital awal kalimat; titik penutup |
| T1-E-011 | budi menulis surat | Budi menulis surat. | Kapital awal kalimat dan nama orang; tanda titik |
| T1-E-012 | saya membeli roti susu dan telur | Saya membeli roti, susu, dan telur. | Kapital awal kalimat; koma dalam perincian; titik |
| T1-E-013 | kamu sudah makan. | Kamu sudah makan? | Kapital awal kalimat; tanda tanya untuk pertanyaan |
| T1-E-014 | awas? | Awas! | Tanda seru untuk seruan/peringatan |
| T1-E-015 | apakah kamu tinggal di jakarta. | Apakah kamu tinggal di Jakarta? | Kapital awal kalimat/nama tempat; tanda tanya |
| T1-E-016 | ani pergi ke bandung pada selasa | Ani pergi ke Bandung pada Selasa. | Kapital nama orang/tempat/hari; kapital awal kalimat; titik |
| T1-E-017 | kami pulang dari bali | Kami pulang dari Bali. | Kapital awal kalimat/nama tempat; kata depan dari terpisah; titik |
| T1-E-018 | dia tinggal dirumah | Dia tinggal di rumah. | Kapital awal kalimat; kata depan di terpisah; titik |
| T1-E-019 | surat itu ditulis rina | Surat itu ditulis Rina. | Awalan di- menyatu; kapital awal kalimat/nama orang; titik |
| T1-E-020 | apakah ibu datang pada desember | Apakah Ibu datang pada Desember? | Kapital awal kalimat dan nama bulan; tanda tanya |

**Catatan penilaian:** Kasus T1-E-009, T1-E-010, dan T1-E-019 menguji pembedaan kata depan `di` dengan awalan `di-`. Bentuk `di baca`/ `di tutup` salah untuk kata kerja pasif, sedangkan `di rumah`/ `di sekolah` benar sebagai kata depan.

---

## 4 — Bagian C: Kasus Khusus & Batas (10 kasus)

**Instruksi:** Periksa apakah sistem menjaga batas data referensi, membedakan bentuk majemuk/terikat, dan tidak memaksakan jawaban saat sumber tidak mendukungnya.

| ID Uji | Masukan | Diharapkan Hasil | Alasan |
|---|---|---|---|
| T1-X-001 | lima belas | Numeralia majemuk; BUKAN satu kata dasar tunggal | Sudah dicatat dalam referensi; terdiri atas dua kata |
| T1-X-002 | kah | Tidak diperlakukan sebagai entri partikel bebas; rujukan bentuk terikat adalah -kah | Referensi mencatat -kah sebagai partikel terikat |
| T1-X-003 | [kata tidak ada di daftar] | Belum dikenal dalam referensi ini; jangan memaksakan kelas kata | Prinsip kejujuran; ketiadaan di daftar bukan bukti bahwa kata tidak ada dalam bahasa |
| T1-X-004 | tiga puluh | Numeralia majemuk; BUKAN satu kata dasar tunggal | Sudah dicatat dalam referensi; terdiri atas dua kata |
| T1-X-005 | -lah | Partikel terikat; bukan imbuhan pembentuk kata dan bukan kata bebas | Catatan partikel terikat pada daftar referensi |
| T1-X-006 | -tah | Partikel terikat; bukan imbuhan pembentuk kata dan bukan kata bebas | Catatan partikel terikat pada daftar referensi |
| T1-X-007 | dekat — “Rumah itu dekat.” | Adjektiva dalam konteks ini | Kelas kata ditentukan oleh fungsi dalam kalimat |
| T1-X-008 | dekat — “Duduk dekat rumah.” | Preposisi dalam konteks ini | Kelas kata ditentukan oleh fungsi dalam kalimat |
| T1-X-009 | ditulis | Bentuk berawalan di-; bukan entri kata dasar `tulis` yang sama bentuknya | Referensi kata dasar menetapkan `tulis`; awalan di- ditulis menyatu |
| T1-X-010 | para siswa | `para` = artikula; `siswa` tidak boleh otomatis dianggap entri dalam daftar ini | `para` tercantum sebagai artikula; kata di luar daftar tidak boleh diklaim tercatat |

**Batas interpretasi:** Jika masukan tidak ditemukan dalam referensi, hasil yang benar adalah menyatakan batas cakupan referensi atau meminta konteks. Jangan menyimpulkan bahwa kata tersebut tidak ada dalam bahasa Indonesia secara umum.

---

## 5 — Lembar Hasil UJI

**Tanggal verifikasi:** 2026-11-21  
**Pelaksana:** ChatGPT — pemeriksaan manual terstruktur terhadap isi file referensi pada branch `ilis-v2-development`  
**Metode:** Pencocokan langsung setiap kasus dengan `kata_dasar.json` dan `aturan_ejaan.json`. Tidak menjalankan chatbot, tidak menguji runtime, dan tidak mengubah file referensi.

### Bagian A — Kelas Kata

- Total kasus: 30
- Lulus: **30**
- Gagal: **0**
- Tingkat keberhasilan: **100%**

| ID Uji | Keluaran aktual dari referensi | Status | Catatan |
|---|---|---|---|
| T1-K-001 | `buku` → nomina | PASS | Entri cocok. |
| T1-K-002 | `rumah` → nomina | PASS | Entri cocok. |
| T1-K-003 | `kucing` → nomina | PASS | Entri cocok. |
| T1-K-004 | `makan` → verba | PASS | Entri cocok. |
| T1-K-005 | `tidur` → verba | PASS | Entri cocok. |
| T1-K-006 | `tulis` → verba | PASS | Entri cocok; tercatat sebagai bentuk dasar. |
| T1-K-007 | `baik` → adjektiva | PASS | Entri cocok. |
| T1-K-008 | `dingin` → adjektiva | PASS | Entri cocok. |
| T1-K-009 | `tinggi` → adjektiva | PASS | Entri cocok. |
| T1-K-010 | `sering` → adverbia | PASS | Entri cocok. |
| T1-K-011 | `segera` → adverbia | PASS | Entri cocok. |
| T1-K-012 | `mungkin` → adverbia | PASS | Entri cocok. |
| T1-K-013 | `aku` → pronomina | PASS | Entri cocok. |
| T1-K-014 | `mereka` → pronomina | PASS | Entri cocok. |
| T1-K-015 | `siapa` → pronomina | PASS | Entri cocok. |
| T1-K-016 | `dua` → numeralia | PASS | Entri cocok. |
| T1-K-017 | `pertama` → numeralia | PASS | Entri cocok. |
| T1-K-018 | `di` → preposisi | PASS | Entri cocok. |
| T1-K-019 | `dari` → preposisi | PASS | Entri cocok. |
| T1-K-020 | `kepada` → preposisi | PASS | Entri cocok. |
| T1-K-021 | `karena` → konjungsi | PASS | Entri cocok. |
| T1-K-022 | `tetapi` → konjungsi | PASS | Entri cocok. |
| T1-K-023 | `aduh` → interjeksi | PASS | Entri cocok. |
| T1-K-024 | `halo` → interjeksi | PASS | Entri cocok. |
| T1-K-025 | `sang` → artikula | PASS | Entri cocok. |
| T1-K-026 | `para` → artikula | PASS | Entri cocok. |
| T1-K-027 | `-kah` → partikel terikat | PASS | Entri tercatat sebagai partikel terikat, bukan kata bebas. |
| T1-K-028 | `dong` → partikel | PASS | Entri cocok. |
| T1-K-029 | `dekat` → adjektiva dan preposisi; catatan menyebut fungsi bergantung konteks | PASS | Referensi mendukung dua fungsi; contoh konteks pada kasus uji selaras dengan kunci. |
| T1-K-030 | `dekat` → adjektiva dan preposisi; catatan menyebut fungsi bergantung konteks | PASS | Referensi mendukung dua fungsi; contoh konteks pada kasus uji selaras dengan kunci. |

### Bagian B — Ejaan & Penulisan

- Total kasus: 20
- Lulus: **18**
- Gagal: **2**
- Tingkat keberhasilan: **90%**

| ID Uji | Keluaran aktual berdasarkan aturan referensi | Status | Catatan |
|---|---|---|---|
| T1-E-001 | Kata depan `di` harus terpisah → `di sekolah` | PASS | Sesuai aturan kata depan. |
| T1-E-002 | Awal kalimat kapital; nama tempat `Bandung` kapital | PASS | Sesuai aturan kapitalisasi. |
| T1-E-003 | Awal kalimat dan nama orang `Rina` kapital | PASS | Sesuai aturan kapitalisasi. |
| T1-E-004 | Awal kalimat dan nama hari `Senin` kapital | PASS | Sesuai aturan kapitalisasi. |
| T1-E-005 | Awal kalimat dan nama bulan `Januari` kapital | PASS | Sesuai aturan kapitalisasi. |
| T1-E-006 | Awal kalimat dan nama tempat `Surabaya` kapital | PASS | Sesuai aturan kapitalisasi. |
| T1-E-007 | Kata depan `ke` harus terpisah → `ke pasar` | PASS | Sesuai aturan kata depan. |
| T1-E-008 | Kata depan `dari` harus terpisah → `dari sekolah`; awal kalimat kapital | PASS | Sesuai aturan kata depan dan kapitalisasi. |
| T1-E-009 | Awalan pasif `di-` melekat → `dibaca`; awal kalimat kapital; pernyataan diakhiri titik | PASS | Seluruh perubahan didukung aturan. |
| T1-E-010 | Awalan pasif `di-` melekat → `ditutup`; awal kalimat kapital; pernyataan diakhiri titik | PASS | Seluruh perubahan didukung aturan. |
| T1-E-011 | Awal kalimat dan nama `Budi` kapital; pernyataan diakhiri titik | PASS | Sesuai aturan kapitalisasi dan titik. |
| T1-E-012 | Awal kalimat kapital; koma memisahkan unsur perincian; titik penutup | PASS | Sesuai aturan kapitalisasi, koma, dan titik. |
| T1-E-013 | Aturan menyatakan tanda tanya untuk kalimat pertanyaan; masukan berakhir titik dan tidak memberi penanda bahwa kalimat itu pertanyaan | FAIL | Kunci mengubah pernyataan menjadi pertanyaan tanpa konteks yang membenarkan perubahan maksud. Aturan referensi tidak cukup untuk menetapkan `?`. Perlu evaluasi Dola atas kunci kasus. |
| T1-E-014 | Contoh benar aturan tanda seru adalah `Awas!`; seruan/peringatan memakai tanda seru | PASS | Kata `awas` merupakan peringatan; keluaran sesuai contoh dan aturan. |
| T1-E-015 | Bentuk tanya `Apakah` memakai tanda tanya; `Jakarta` kapital; awal kalimat kapital | PASS | Sesuai aturan pertanyaan dan kapitalisasi. |
| T1-E-016 | `Ani`, `Bandung`, dan `Selasa` kapital; pernyataan diakhiri titik | PASS | Sesuai aturan kapitalisasi dan titik. |
| T1-E-017 | `Bali` kapital; `dari` terpisah; pernyataan diakhiri titik | PASS | Sesuai aturan kapitalisasi, kata depan, dan titik. |
| T1-E-018 | Kata depan `di` terpisah → `di rumah`; awal kalimat kapital; titik penutup | PASS | Sesuai aturan. |
| T1-E-019 | Awalan pasif `di-` melekat → `ditulis`; nama `Rina` dan awal kalimat kapital; titik | PASS | Sesuai aturan. |
| T1-E-020 | Aturan yang tersedia mengatur kapital awal kalimat serta nama orang/tempat/hari/bulan; tidak ada aturan eksplisit tentang kapitalisasi `Ibu` sebagai sapaan/kekerabatan pada konteks ini | FAIL | Kunci `Ibu` belum dapat dibuktikan dari aturan yang tercantum. Konteks sapaan juga tidak dinyatakan. Perlu evaluasi Dola; jangan mengubah aturan atau kunci secara diam-diam. |

### Bagian C — Kasus Khusus & Batas

- Total kasus: 10
- Lulus: **9**
- Gagal: **1**
- Tingkat keberhasilan: **90%**

| ID Uji | Keluaran aktual dari referensi | Status | Catatan |
|---|---|---|---|
| T1-X-001 | `lima belas` tercatat sebagai numeralia dengan catatan bentuk bilangan majemuk, bukan satu kata dasar tunggal | PASS | Sesuai kunci. |
| T1-X-002 | `kah` tidak tercatat sebagai entri bebas; `-kah` tercatat sebagai partikel terikat | PASS | Sesuai kunci. |
| T1-X-003 | Masukan literal masih berupa `[kata tidak ada di daftar]`; tidak ada token kata tertentu untuk dicari | FAIL | Kasus belum dapat dieksekusi secara konkret. Status ini menandai kekurangan spesifikasi kasus, bukan bukti bahwa kata tertentu tidak ada. |
| T1-X-004 | `tiga puluh` tercatat sebagai numeralia dengan catatan bentuk bilangan majemuk | PASS | Sesuai kunci. |
| T1-X-005 | `-lah` tercatat sebagai partikel terikat; catatan menyatakan bukan imbuhan pembentuk kata | PASS | Sesuai kunci. |
| T1-X-006 | `-tah` tercatat sebagai partikel terikat; catatan menyatakan bukan imbuhan pembentuk kata | PASS | Sesuai kunci. |
| T1-X-007 | `dekat` memiliki jenis adjektiva dan preposisi; catatan menyebut fungsi bergantung konteks | PASS | Referensi mendukung fungsi adjektiva pada konteks yang diberikan. |
| T1-X-008 | `dekat` memiliki jenis adjektiva dan preposisi; catatan menyebut fungsi bergantung konteks | PASS | Referensi mendukung fungsi preposisi pada konteks yang diberikan. |
| T1-X-009 | `ditulis` tidak tercatat sebagai entri; `tulis` tercatat sebagai verba dasar; aturan menyatakan awalan `di-` melekat | PASS | Sesuai batas referensi dan aturan awalan. |
| T1-X-010 | `para` tercatat sebagai artikula; `siswa` tidak tercatat sebagai entri | PASS | Sesuai kunci; tidak mengklaim `siswa` ada dalam daftar. |

### Rekapitulasi

| Bagian | Total | PASS | FAIL | Keberhasilan |
|---|---:|---:|---:|---:|
| A — Kelas kata | 30 | 30 | 0 | 100% |
| B — Ejaan | 20 | 18 | 2 | 90% |
| C — Kasus khusus | 10 | 9 | 1 | 90% |
| **Keseluruhan** | **60** | **57** | **3** | **95%** |

### Temuan yang memerlukan evaluasi

1. **T1-E-013:** perubahan kalimat pernyataan menjadi pertanyaan tidak dapat ditentukan hanya dari aturan tanda baca tanpa konteks maksud.
2. **T1-E-020:** kapitalisasi `Ibu` pada konteks tersebut belum ditopang aturan eksplisit dalam `aturan_ejaan.json`.
3. **T1-X-003:** placeholder tidak menyebut kata konkret sehingga tidak dapat diverifikasi sebagai kasus tertentu.

**Catatan hitung:** Rekapitulasi yang benar adalah 57 PASS dan 3 FAIL (95%). Dua kegagalan pada Bagian B dan satu pada Bagian C merupakan ketidaksiapan/kekurangan dukungan pada kunci atau spesifikasi kasus, bukan bukti otomatis bahwa isi JSON salah. Belum ada promosi data.

### KESIMPULAN AKHIR

- [ ] Lulus — Akurasi ≥90%, tidak ada kesalahan kritis → siap dipertimbangkan untuk promosi ke runtime
- [x] Perlu evaluasi Dola — Ambang angka tercapai, tetapi ada 3 kasus yang belum didukung/tidak dapat dieksekusi sebagaimana ditulis
- [ ] Ditunda — Belum siap

**Kesalahan kritis pada data referensi:** Belum dapat disimpulkan dari verifikasi ini.  
**Isu kritis pada paket/kunci uji:** T1-E-013 berpotensi mengubah maksud kalimat; perlu keputusan evaluator sebelum paket dinyatakan bersih.

**Status promosi:** TIDAK DIPROMOSIKAN. Kedua JSON tetap berstatus `referensi`.

**Tanda persetujuan evaluator:** Menunggu Dola  
**Tanggal persetujuan:** __________

---

## 6 — Aturan Pelaksanaan dan Batas Persetujuan

1. Jalankan seluruh 60 kasus; jangan memilih hanya kasus yang mudah.
2. Catat keluaran aktual secara verbatim, lalu bandingkan dengan hasil yang diharapkan dan catatan konteks.
3. Hitung skor per bagian dan keseluruhan. Laporkan jumlah kasus yang lulus/gagal serta persentasenya.
4. Tandai setiap kesalahan kritis secara terpisah. Kesalahan kritis menggagalkan gerbang meskipun skor total mencapai ambang.
5. Jika kasus ternyata ambigu atau kunci uji perlu diperbaiki, hentikan penilaian kasus tersebut, dokumentasikan alasannya, dan minta evaluator meninjau kunci. Jangan mengubah kunci diam-diam setelah melihat keluaran.
6. Simpan laporan hasil pelaksanaan sebagai artefak terpisah setelah uji benar-benar dilakukan. Dokumen rencana ini tetap menjadi acuan kasus dan tidak boleh diisi dengan hasil rekaan.
7. Kelulusan dokumen uji atau keberhasilan menyusun 60 kasus **tidak sama dengan kelulusan data**. Promosi ke `data/runtime/` tetap memerlukan eksekusi, evaluasi Dola, pemeriksaan kesalahan kritis, dan persetujuan Owner sesuai `docs/FORMAT_DATASET.md`.

**Status akhir:** 60 kasus uji telah dirancang (30 kelas kata, 20 ejaan, 10 kasus khusus). Belum dieksekusi; belum ada hasil atau rekomendasi promosi.
