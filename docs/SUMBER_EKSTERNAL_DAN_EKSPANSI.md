# SUMBER EKSTERNAL DAN RENCANA EKSPANSI DATA

**Status:** Panduan perencanaan — BELUM dieksekusi  
**Tanggal pencatatan:** 2026-11-21  
**Lokasi:** `docs/SUMBER_EKSTERNAL_DAN_EKSPANSI.md`

---

## 1. Tujuan

Dokumen ini mencatat kandidat sumber leksikon, korpus, dan dataset Bahasa Indonesia yang mungkin berguna untuk memperkaya referensi ILIS pada masa mendatang.

Sumber eksternal adalah bahan pelengkap, bukan pengganti kurikulum dan struktur empat tahap ILIS. Prinsip kerja:

**Fondasi bahasa diperkuat dan diverifikasi terlebih dahulu; ekspansi dari sumber luar dilakukan kemudian berdasarkan celah yang benar-benar ditemukan.**

Dokumen ini hanya rencana. Pencantuman sebuah sumber tidak berarti sumber tersebut sudah diperiksa secara menyeluruh, disetujui untuk digunakan, atau boleh langsung diimpor.

## 2. Prinsip penggunaan sumber luar

- **Jangan** mengimpor data mentah ke dataset atau runtime ILIS sebelum tahapan fondasi yang relevan selesai dan terverifikasi.
- **Jangan** mengubah struktur kurikulum, kontrak semantik, atau format dataset ILIS hanya agar cocok dengan format sumber eksternal.
- Gunakan sumber eksternal sebagai bahan kajian dan pembanding; pilih hanya materi yang relevan dengan kebutuhan ILIS.
- Setiap calon entri harus disesuaikan dengan skema ILIS dan diverifikasi secara manual.
- Catat sumber, lisensi, tanggal akses, transformasi, dan alasan pemilihan setiap data yang diadopsi.
- Sumber eksternal tidak otomatis benar. Periksa kualitas, cakupan, representativitas, duplikasi, bias domain, dan konteks pemakaiannya.
- Jangan menyalin korpus atau dataset secara massal sebelum lisensi dan ketentuan penggunaannya dipahami.
- Jangan menganggap tautan yang tercantum di katalog pihak ketiga memiliki lisensi yang sama. Lisensi harus diperiksa pada sumber asal masing-masing.
- Jika lisensi tidak jelas atau tidak mengizinkan penggunaan yang direncanakan, jangan gunakan datanya.

**Acuan utama tetap dokumen kurikulum dan daftar dasar Tahap 1–4 ILIS**, bersama spesifikasi format dataset yang berlaku.

## 3. Kandidat sumber eksternal

Daftar berikut merupakan titik awal eksplorasi, bukan daftar sumber yang telah disahkan. Isi repositori, tautan, lisensi, dan status pemeliharaan dapat berubah; lakukan pemeriksaan ulang ketika ekspansi benar-benar dimulai.

### 3.1 Kumpulan tautan sumber daya NLP Bahasa Indonesia

**louisowen6/NLP_bahasa_resources**  
https://github.com/louisowen6/NLP_bahasa_resources

- **Gambaran:** Kumpulan tautan menuju berbagai sumber daya NLP Bahasa Indonesia.
- **Potensi materi:** Leksikon, kata dasar, sinonim, kata informal/gaul, kata majemuk, dan pasangan bentuk formal–informal, bergantung pada sumber yang ditautkan.
- **Kemungkinan relevansi:** Tahap 2 untuk morfologi dan relasi makna; Tahap 4 untuk ragam bahasa.
- **Cara kaji nanti:** Telusuri sumber asal yang relevan, periksa lisensi dan definisinya, lalu pilih contoh yang benar-benar mengisi celah pada data ILIS.
- **Catatan:** Repositori ini merupakan katalog/kompilasi tautan; jangan menganggap seluruh sumber di dalamnya memiliki format, kualitas, atau lisensi seragam.

### 3.2 Kumpulan sumber daya NLP Bahasa Indonesia

**kmkurn/id-nlp-resource**  
https://github.com/kmkurn/id-nlp-resource

- **Gambaran:** Daftar sumber daya dan korpus NLP Bahasa Indonesia.
- **Potensi materi:** Korpus sintaksis seperti Indonesian Treebank atau Universal Dependencies Indonesian, serta korpus teks/percakapan yang ditautkan oleh repositori.
- **Kemungkinan relevansi:** Tahap 2 untuk pola sintaksis; Tahap 3 dan 4 untuk konteks kalimat serta variasi percakapan.
- **Cara kaji nanti:** Ambil pola atau contoh yang dibutuhkan untuk menjawab celah tertentu. Jangan menganggap frekuensi dalam korpus sebagai bukti bahwa sebuah bentuk selalu benar atau cocok di semua konteks.
- **Catatan:** Periksa lisensi masing-masing korpus di sumber asal. Korpus terjemahan atau subtitle dapat memiliki batasan hak cipta dan penggunaan yang berbeda dari korpus linguistik.

### 3.3 Dataset percakapan/chatbot Bahasa Indonesia

**binsarjr/chatbot-indonesia**  
https://github.com/binsarjr/chatbot-indonesia

- **Gambaran:** Kandidat repositori berisi contoh pasangan ujaran dan respons chatbot.
- **Potensi materi:** Sapaan, respons umum, pertanyaan sederhana, dan pola dialog.
- **Kemungkinan relevansi:** Tahap 4 untuk mengamati pola percakapan dasar.
- **Cara kaji nanti:** Pelajari struktur interaksi dan variasi respons; buat contoh ILIS sendiri sesuai prinsip, skema, dan tujuan sistem.
- **Catatan:** Dataset chatbot dapat mencerminkan gaya atau asumsi pembuatnya. Jangan menyalin respons mentah atau menganggapnya sebagai standar percakapan Bahasa Indonesia.

### 3.4 Katalog dataset IndoNLP

**IndoNLP/nusa-catalogue**  
https://github.com/IndoNLP/nusa-catalogue  
https://indonlp.github.io/

- **Gambaran:** Katalog untuk menemukan dataset NLP Indonesia dan bahasa daerah.
- **Potensi materi:** Dataset dari berbagai domain, misalnya teks umum, percakapan, berita, dan media sosial, sesuai isi katalog saat diakses.
- **Kemungkinan relevansi:** Eksplorasi jangka panjang ketika ILIS membutuhkan sumber khusus untuk mengisi celah tertentu.
- **Cara kaji nanti:** Cari berdasarkan kebutuhan yang telah dirumuskan, lalu periksa dokumentasi, lisensi, asal data, dan batas penggunaannya.
- **Catatan:** Jumlah dataset, filter, dan cakupan katalog dapat berubah. Angka atau deskripsi katalog harus diverifikasi kembali saat digunakan.

## 4. Urutan ekspansi yang direncanakan

| Urutan | Kegiatan | Waktu pelaksanaan | Acuan |
|---|---|---|---|
| 1 | Selesaikan dan verifikasi tahapan fondasi ILIS sesuai gerbang kelulusan masing-masing | Sebelum ekspansi | Dokumen Tahap 1–4 dan laporan uji |
| 2 | Identifikasi celah nyata dari hasil uji dan penggunaan | Setelah tahap terkait terverifikasi | Laporan verifikasi dan evaluasi |
| 3 | Tentukan kebutuhan data yang spesifik | Sebelum mencari sumber | Daftar celah yang disetujui |
| 4 | Telusuri kandidat sumber eksternal | Saat ekspansi dimulai | Daftar pada dokumen ini dan katalog lain yang relevan |
| 5 | Audit asal, lisensi, kualitas, cakupan, dan konteks data | Sebelum mengadopsi contoh | Dokumentasi sumber asal |
| 6 | Pilih dan adaptasi contoh ke format ILIS | Setelah audit sumber | `docs/FORMAT_DATASET.md` |
| 7 | Catat provenance dan alasan penambahan | Bersamaan dengan perubahan | Metadata dan catatan pembaruan |
| 8 | Jalankan paket uji terkait dan regresi | Setelah perubahan data | Paket uji tahap terkait |
| 9 | Minta evaluasi dan persetujuan sesuai tata kelola proyek sebelum promosi status | Sebelum perubahan status | Evaluator dan Owner |

Ekspansi tidak harus dilakukan sekaligus. Kerjakan per celah dan per kelompok data agar setiap perubahan dapat ditinjau serta ditelusuri.

## 5. Aturan provenance dan pencatatan

Setiap data yang diadaptasi dari sumber luar harus memiliki informasi yang cukup untuk ditelusuri, sekurang-kurangnya:

- nama sumber dan URL sumber asal;
- nama dataset atau bagian yang dirujuk, jika tersedia;
- lisensi dan ketentuan penggunaan yang telah diperiksa;
- tanggal akses atau pengambilan;
- bentuk data sebelum dan sesudah adaptasi, bila relevan;
- alasan data dipilih dan celah ILIS yang hendak diisi;
- hasil verifikasi dan paket uji yang terdampak.

Jika format JSON yang berlaku belum menyediakan kolom provenance yang memadai, jangan menambahkan kolom secara sepihak. Ajukan penyesuaian spesifikasi terlebih dahulu sesuai tata kelola ILIS.

## 6. Hal yang tidak boleh berubah tanpa keputusan resmi

| Aspek | Ketentuan |
|---|---|
| Struktur empat tahap ILIS | Tetap menjadi kerangka utama |
| Format dataset | Mengikuti `docs/FORMAT_DATASET.md` yang berlaku |
| Verifikasi manual | Tetap wajib untuk setiap penambahan |
| Data yang sudah terverifikasi | Tidak boleh ditimpa atau dihapus oleh impor eksternal |
| Status `referensi` dan `aktif` | Harus dibedakan secara tegas |
| Provenance dan lisensi | Wajib dapat ditelusuri |
| Integrasi runtime | Tidak otomatis terjadi karena data referensi bertambah |
| Perubahan struktur atau skema | Memerlukan evaluasi dan persetujuan sesuai tata kelola proyek |

## 7. Batas pelaksanaan saat ini

- Dokumen ini **tidak** memberi izin untuk mengunduh, mengimpor, atau mengolah dataset eksternal sekarang.
- Tidak ada file JSON yang diubah oleh dokumen ini.
- Tidak ada dataset yang dinaikkan statusnya menjadi aktif.
- Tidak ada perubahan runtime atau integrasi produksi.
- Prioritas proyek saat ini tetap memperkuat pemahaman Bahasa Indonesia melalui tahapan fondasi ILIS. Ekspansi sumber eksternal menunggu sampai gerbang tahap yang relevan terpenuhi dan kebutuhan nyata telah diidentifikasi.
- Pencantuman sumber di sini bukan pengesahan Dola atau keputusan penggunaan permanen. Evaluasi sumber dan rencana adopsi dilakukan saat waktunya tiba.

> **Intinya: sumber luar adalah buku di rak. Bisa dibaca dan dipelajari ketika dibutuhkan, tetapi tidak boleh mengganti struktur rumah ILIS yang sedang dibangun.**
>
> — Prinsip ILIS —
