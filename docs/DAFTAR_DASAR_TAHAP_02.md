# DAFTAR DASAR TAHAP 02 — PEMBENTUKAN KATA & KALIMAT SEDERHANA

**Acuan utama:**
- `docs/TAHAP_02_KATA_DAN_KALIMAT.md`
- `docs/DAFTAR_DASAR_TAHAP_01.md`

**Branch:** `ilis-v2-development`  
**Status:** Daftar Referensi — BELUM DIMUAT KE DATASET AKTIF  
**Cakupan:** Morfologi, frasa, pola kalimat dasar, jenis kalimat, dan semantik dasar  
**Batas perubahan:** Hanya dokumen ini; tidak mengubah dataset JSONL, kode, konfigurasi runtime, atau branch `main`.

---

## 1 — Morfologi: Afiks dan Perubahan Kata

Morfologi mempelajari bentuk kata dan proses pembentukannya. **Kata dasar** menjadi dasar pembentukan kata lain, sedangkan **kata berimbuhan** terbentuk setelah kata dasar mendapat afiks (imbuhan).

Contoh kata dasar di bawah dipilih dari `DAFTAR_DASAR_TAHAP_01.md` jika memungkinkan. Bentuk hasil harus merupakan bentuk bahasa Indonesia yang benar-benar digunakan; tidak semua imbuhan dapat dipasangkan dengan semua kata dasar.

### A. Prefiks (Awalan)

Prefiks diletakkan di depan kata dasar.

| Awalan | Contoh Kata Dasar | Kata Berimbuhan |
|---|---|---|
| meN- (keluarga awalan me-) | tulis | menulis |
| meN- | baca | membaca |
| ber- | jalan | berjalan |
| ber- | bunga | berbunga |
| di- | tulis | ditulis |
| di- | baca | dibaca |
| ter- | jatuh | terjatuh |
| ter- | buka | terbuka |
| ke- | dua | kedua |
| ke- | tiga | ketiga |
| peN-/pe- (keluarga awalan pe-) | tulis | penulis |
| peN-/pe- | baca | pembaca |
| pe- | lari | pelari |
| pe- | kerja | pekerja |

**Catatan bentuk awalan:**
- Bentuk `meN-` dan `peN-` adalah lambang keluarga awalan. Bentuk nyata menyesuaikan bunyi awal kata dasar, misalnya `men-` pada *menulis*, `mem-` pada *membaca*, `meng-` pada *mengambil*, serta `pen-` pada *penulis* dan `pem-` pada *pembaca*.
- Awalan `di-` pada kata kerja pasif ditulis melekat: *ditulis*, *dibaca*. Bedakan dari kata depan `di` yang ditulis terpisah: *di rumah*.
- `ke-` pada *kedua* dan *ketiga* membentuk bilangan tingkat. Jangan menyamakan bentuk ini dengan kata depan `ke`, seperti *ke pasar*.

### B. Sufiks (Akhiran)

Sufiks diletakkan di belakang kata dasar.

| Akhiran | Contoh Kata Dasar | Kata Berimbuhan |
|---|---|---|
| -kan | bersih | bersihkan |
| -kan | ambil | ambilkan |
| -an | baca | bacaan |
| -an | makan | makanan |
| -i | warna | warnai |
| -i | garam | garami |
| -nya | buku | bukunya |
| -nya | rumah | rumahnya |

**Catatan:** Akhiran `-kan` dan `-i` dapat membentuk kata kerja dengan fungsi berbeda. `-an` sering membentuk nomina. `-nya` dapat menandai kepunyaan atau rujukan tertentu. Pemilihan makna tetap bergantung pada kalimat.

### C. Konfiks (Awalan dan Akhiran Bersama)

Konfiks adalah pasangan awalan dan akhiran yang bekerja bersama mengapit kata dasar.

| Konfiks | Contoh Kata Dasar | Kata Berimbuhan |
|---|---|---|
| meN-…-kan | baca | membacakan |
| meN-…-kan | bersih | membersihkan |
| ber-…-an | peluk | berpelukan |
| ber-…-an | jatuh | berjatuhan |
| ke-…-an | baik | kebaikan |
| ke-…-an | hujan | kehujanan |

**Catatan ketepatan:**
- Bentuk `meN-…-kan` pada *membacakan* dan *membersihkan* menunjukkan awalan yang menyesuaikan bunyi serta akhiran `-kan`.
- *Berpelukan* dan *berjatuhan* menunjukkan pola `ber-…-an`; makna kata turunannya tidak selalu dapat diterjemahkan hanya dengan menjumlahkan arti imbuhan.
- *Kebaikan* dan *kehujanan* menunjukkan pola `ke-…-an`, tetapi makna keduanya berbeda menurut kata dasar dan pemakaian.

### D. Reduplikasi (Kata Ulang)

Reduplikasi adalah pengulangan kata atau bagian kata. Berikut lima contoh pengulangan seluruh kata.

| Kata Dasar | Kata Ulang | Catatan Makna |
|---|---|---|
| rumah | rumah-rumah | Dapat menyatakan banyak rumah |
| buku | buku-buku | Dapat menyatakan banyak buku |
| anak | anak-anak | Dapat menyatakan lebih dari satu anak |
| jalan | jalan-jalan | Dapat menyatakan kegiatan berjalan santai |
| makan | makan-makan | Dapat menyatakan kegiatan makan bersama/santai |

**Penting:** Kata ulang tidak selalu bermakna jamak. *Jalan-jalan* dan *makan-makan*, misalnya, dapat menyatakan kegiatan. Makna harus diperiksa dari pemakaian dalam kalimat.

### E. Perubahan Bunyi pada Pembentukan Kata

Ketika keluarga awalan `meN-` ditambahkan, bentuk awalan menyesuaikan bunyi awal kata dasar. Pada sejumlah kata, bunyi awal `p`, `t`, `k`, atau `s` luluh; pada kata lain, bunyi awal tetap.

| Kata Dasar | Kata Berimbuhan | Penjelasan |
|---|---|---|
| tulis | menulis | Bunyi awal `t` luluh; awalan tampil sebagai `men-`. |
| pakai | memakai | Bunyi awal `p` luluh; awalan tampil sebagai `mem-`. |
| sapu | menyapu | Bunyi awal `s` luluh; awalan tampil sebagai `meny-`. |
| kirim | mengirim | Bunyi awal `k` luluh; awalan tampil sebagai `meng-`. |
| ambil | mengambil | Bunyi awal vokal `a` tetap; awalan tampil sebagai `meng-`. |
| baca | membaca | Bunyi awal `b` tetap; awalan tampil sebagai `mem-`. |
| lihat | melihat | Bunyi awal `l` tetap; awalan tampil sebagai `me-`. |
| ukur | mengukur | Bunyi awal vokal `u` tetap; awalan tampil sebagai `meng-`. |

**Penegasan:** Pada *ambil → mengambil*, huruf/bunyi awal `a` tidak hilang. Pada *tulis → menulis*, bunyi awal `t` mengalami peluluhan. Jangan menerapkan satu aturan perubahan bunyi secara otomatis pada semua kata.

---

## 2 — Frasa

**Frasa** adalah gabungan dua kata atau lebih yang membentuk satu kesatuan fungsi, tetapi tidak memiliki hubungan subjek-predikat lengkap seperti sebuah klausa.

### A. Frasa Nomina

Frasa nomina adalah frasa yang intinya berupa nomina (kata benda).

| No. | Contoh Frasa Nomina |
|---:|---|
| 1 | buku baru |
| 2 | rumah besar |
| 3 | air dingin |
| 4 | meja kayu |
| 5 | anak kecil |

### B. Frasa Verba

Frasa verba adalah frasa yang intinya berupa verba (kata kerja).

| No. | Contoh Frasa Verba |
|---:|---|
| 1 | sedang makan |
| 2 | sudah tidur |
| 3 | akan pergi |
| 4 | sedang membaca |
| 5 | ingin minum |

### C. Frasa Preposisional

Frasa preposisional adalah frasa yang diawali preposisi (kata depan), lalu diikuti unsur yang melengkapinya.

| No. | Contoh Frasa Preposisional |
|---:|---|
| 1 | di rumah |
| 2 | ke pasar |
| 3 | dari sekolah |
| 4 | dengan ibu |
| 5 | untuk adik |

**Pembeda:** *buku baru* dan *di rumah* adalah frasa. *Buku itu baru* dan *Ibu tidur di rumah* adalah kalimat karena memiliki hubungan subjek dan predikat.

---

## 3 — Pola Kalimat Dasar

Pola berikut adalah pola pengenalan sederhana. **S** = Subjek, **P** = Predikat, **O** = Objek, dan **K** = Keterangan.

- **Subjek (S):** unsur yang menjadi pokok pembicaraan.
- **Predikat (P):** unsur yang menyatakan tindakan, keadaan, atau identitas subjek.
- **Objek (O):** unsur yang dikenai tindakan pada predikat transitif.
- **Keterangan (K):** unsur tambahan, misalnya waktu, tempat, atau cara.

### A. Pola S-P

**Rumus:** Subjek + Predikat.

| No. | Contoh |
|---:|---|
| 1 | Budi tidur. |
| 2 | Ibu datang. |
| 3 | Kucing duduk. |

### B. Pola S-P-O

**Rumus:** Subjek + Predikat + Objek.

| No. | Contoh |
|---:|---|
| 1 | Ibu memasak nasi. |
| 2 | Adik membaca buku. |
| 3 | Ayah membuka pintu. |

### C. Pola S-P-K

**Rumus:** Subjek + Predikat + Keterangan.

| No. | Contoh |
|---:|---|
| 1 | Ibu tidur di kamar. |
| 2 | Kami pergi pagi tadi. |
| 3 | Ayam makan di halaman. |

### D. Pola S-P-O-K

**Rumus:** Subjek + Predikat + Objek + Keterangan.

| No. | Contoh |
|---:|---|
| 1 | Ibu memasak nasi di dapur. |
| 2 | Adik membaca buku di kamar. |
| 3 | Ayah mencuci mobil pagi tadi. |

**Catatan:** Keterangan dapat menyatakan tempat (*di kamar*), waktu (*pagi tadi*), atau informasi lain. Tidak semua kalimat harus memiliki objek atau keterangan. Contoh di atas sengaja dibuat sederhana agar fungsi setiap unsur mudah dikenali.

---

## 4 — Jenis Kalimat

### A. Kalimat Deklaratif

Kalimat deklaratif adalah kalimat yang menyampaikan pernyataan atau informasi.

1. Ibu memasak nasi.
2. Kucing tidur di kamar.

### B. Kalimat Interogatif

Kalimat interogatif adalah kalimat yang mengajukan pertanyaan dan umumnya diakhiri tanda tanya.

1. Siapa yang datang?
2. Kamu membaca buku?

### C. Kalimat Imperatif

Kalimat imperatif adalah kalimat yang meminta atau memerintahkan seseorang melakukan sesuatu.

1. Tutup pintu!
2. Tolong ambil buku itu.

### D. Kalimat Larangan

Kalimat larangan adalah kalimat yang meminta seseorang tidak melakukan sesuatu. Kata `jangan` sering digunakan.

1. Jangan berlari di rumah!
2. Jangan membuka pintu itu!

### E. Kalimat Aktif dan Pasif

Kalimat aktif umumnya menempatkan pelaku sebagai subjek dan, pada contoh transitif berikut, menggunakan predikat berawalan `meN-`. Kalimat pasif menempatkan unsur yang dikenai tindakan sebagai subjek; bentuk pasif umum menggunakan awalan `di-`.

| No. | Kalimat Aktif | Kalimat Pasif |
|---:|---|---|
| 1 | Ibu membaca buku. | Buku dibaca Ibu. |
| 2 | Ayah membuka pintu. | Pintu dibuka Ayah. |
| 3 | Adik mencuci tangan. | Tangan dicuci Adik. |
| 4 | Budi menulis surat. | Surat ditulis Budi. |
| 5 | Kakak membeli buku. | Buku dibeli Kakak. |

**Catatan:** Pasangan ini memakai kalimat aktif transitif yang memiliki objek. Objek pada kalimat aktif menjadi subjek pada kalimat pasif. Tidak semua kalimat aktif dapat diubah menjadi pasif dengan pola yang sama.

### F. Penyangkalan

Penyangkalan adalah penggunaan kata yang menolak atau menyangkal isi pernyataan. Empat bentuk berikut memiliki fungsi yang berbeda.

#### 1. Tidak

`Tidak` lazim digunakan untuk menyangkal verba atau adjektiva.

1. Ibu tidak tidur.
2. Air itu tidak panas.

#### 2. Bukan

`Bukan` lazim digunakan untuk menyangkal nomina atau identitas.

1. Itu bukan buku saya.
2. Budi bukan guru.

#### 3. Belum

`Belum` menyatakan bahwa sesuatu belum terjadi atau belum tercapai sampai waktu pembicaraan.

1. Adik belum makan.
2. Ibu belum datang.

#### 4. Jangan

`Jangan` digunakan untuk menyatakan larangan atau meminta agar tindakan tidak dilakukan.

1. Jangan berlari!
2. Jangan membuka pintu!

**Pembeda penting:** *tidak* dan *bukan* sama-sama dapat menyangkal, tetapi penggunaannya tidak selalu dapat saling menggantikan. *Belum* berkaitan dengan keadaan yang belum terjadi, sedangkan *jangan* membentuk larangan.

---

## 5 — Semantik Dasar

Semantik mempelajari makna bahasa. Pada daftar ini, hubungan makna dibatasi pada sinonim dan antonim yang umum.

### A. Sinonim

Sinonim adalah dua kata atau lebih yang memiliki makna sama atau hampir sama. Kesamaan makna tidak selalu membuat kata-kata tersebut dapat saling menggantikan dalam semua kalimat.

| No. | Kata | Sinonim |
|---:|---|---|
| 1 | pintar | cerdas |
| 2 | senang | gembira |
| 3 | cepat | lekas |
| 4 | indah | elok |
| 5 | cantik | elok |
| 6 | sulit | sukar |
| 7 | mudah | gampang |
| 8 | melihat | memandang |
| 9 | berkata | berbicara |
| 10 | haus | dahaga |

**Catatan:** Beberapa pasangan memiliki perbedaan ragam atau konteks. Misalnya *dahaga* lebih formal/sastrawi daripada *haus*, sedangkan *raya* tidak dapat menggantikan *besar* dalam semua konteks. Daftar ini menunjukkan kedekatan makna, bukan kesamaan mutlak.

### B. Antonim

Antonim adalah kata-kata yang memiliki makna berlawanan.

| No. | Kata | Antonim |
|---:|---|---|
| 1 | besar | kecil |
| 2 | tinggi | rendah |
| 3 | panas | dingin |
| 4 | jauh | dekat |
| 5 | cepat | lambat |
| 6 | baik | buruk |
| 7 | bersih | kotor |
| 8 | mahal | murah |
| 9 | datang | pergi |
| 10 | naik | turun |

**Catatan:** Hubungan antonim perlu dilihat dari makna kata dalam pemakaian. Pasangan di atas dipilih karena memiliki pertentangan makna yang umum dan mudah dikenali.

---

## 6 — Pemeriksaan Mandiri dan Batas Penggunaan

Pemeriksaan berikut adalah pemeriksaan isi dokumen, bukan validasi ahli eksternal dan bukan pengujian runtime ILIS.

| Pemeriksaan | Hasil | Catatan |
|---|---|---|
| Prefiks, sufiks, dan konfiks yang diminta tercakup | ✅ | Bentuk dan contoh dicantumkan |
| Lima contoh reduplikasi tersedia | ✅ | Pengulangan seluruh kata |
| Perubahan bunyi dijelaskan | ✅ | Termasuk *tulis → menulis* dan *ambil → mengambil* |
| Tiga jenis frasa masing-masing memiliki lima contoh | ✅ | Nomina, verba, preposisional |
| Empat pola kalimat masing-masing memiliki tiga contoh | ✅ | S-P, S-P-O, S-P-K, S-P-O-K |
| Jenis kalimat dan penyangkalan tercakup | ✅ | Deklaratif, interogatif, imperatif, larangan, aktif-pasif, tidak/bukan/belum/jangan |
| Sinonim dan antonim masing-masing sepuluh pasangan | ✅ | Dengan catatan perbedaan konteks |
| Mengutamakan kata dari daftar Tahap 1 | ⚠️ | Dipakai sejauh sesuai; beberapa contoh tambahan diperlukan agar kalimat dan bentuk imbuhan alami |
| Siap menjadi dataset aktif | ❌ | Belum melalui audit evaluator, konversi skema, atau pengujian |

### Batas Aktivasi

- Dokumen ini **hanya daftar referensi Tahap 2**, bukan dataset.
- Tidak ada perubahan pada file JSONL, kode, mesin inti, atau konfigurasi runtime.
- Tidak ada fakta ensiklopedis atau perluasan basis pengetahuan umum.
- Tidak ada materi Tahap 3 atau Tahap 4 yang diimplementasikan.
- Setiap entri masih memerlukan audit linguistik dan persetujuan terpisah sebelum dapat dipertimbangkan untuk dataset aktif.
- Contoh yang memiliki perbedaan ragam, konteks, atau fungsi harus dipahami sebagai bahan belajar, bukan aturan mutlak untuk semua kalimat.

**Kesimpulan:** Daftar ini menghubungkan kata dasar dengan proses pembentukan kata, frasa, pola kalimat sederhana, jenis kalimat, serta hubungan makna dasar. Prinsipnya tetap: **dari bentuk kata menuju susunan kalimat, secara bertahap dan dengan contoh yang dapat dipertanggungjawabkan.**
