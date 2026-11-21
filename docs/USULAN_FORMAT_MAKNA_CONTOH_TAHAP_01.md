# SPESIFIKASI USULAN MAKNA DAN CONTOH PENGGUNAAN — TAHAP 1

**Status:** DRAF USULAN — MENUNGGU EVALUASI DOLA DAN KEPUTUSAN OWNER  
**Branch acuan:** `ilis-v2-development`  
**Cakupan:** Rancangan struktur data leksikal Tahap 1 saja  
**Tidak termasuk:** Pengisian 152 entri, perubahan JSON, perubahan kode/runtime, integrasi chatbot, promosi data, atau perubahan `main`.

---

## 1. Tujuan

Menetapkan format yang aman dan dapat ditelusuri untuk melengkapi dua kekurangan wajib Tahap 1:

1. makna/fungsi sederhana untuk setiap kata dasar dan setiap kelas kata yang dicatat;
2. contoh penggunaan singkat yang memperlihatkan fungsi tersebut.

Format harus dapat menampung kata dengan lebih dari satu kelas atau lebih dari satu makna tanpa memaksakan satu arti untuk semua konteks.

Dokumen ini hanya mengusulkan struktur. Persetujuan atas dokumen ini **tidak** otomatis mengizinkan pengisian dataset atau perubahan runtime.

## 2. Temuan audit format saat ini

Pemeriksaan pada branch acuan menemukan kondisi berikut:

- `kata_dasar.json` berisi 152 entri.
- Setiap entri saat ini memiliki `entri`, `jenis`, `bentuk_dasar`, `imbuhan`, dan `catatan`.
- Belum ada field khusus untuk makna sederhana maupun contoh penggunaan.
- Entri `dekat` mencatat dua kelas: `adjektiva` dan `preposisi`.
- `catatan` saat ini dipakai untuk keterangan bentuk/batas entri, bukan sebagai tempat baku untuk definisi dan contoh. Field ini tidak boleh diam-diam dialihfungsikan.
- Ada ketidaksinkronan metadata yang perlu diselesaikan: `docs/FORMAT_DATASET.md` menyatakan `versi_data` wajib, tetapi objek root `kata_dasar.json` yang diperiksa belum memiliki field tersebut.

Ketidaksinkronan `versi_data` dicatat sebagai prasyarat revisi data. Jangan menambahkannya diam-diam dalam pekerjaan pengisian makna.

## 3. Prinsip rancangan

1. **Makna dipisahkan per kelas kata.** Jika satu entri memiliki dua kelas, uraian untuk masing-masing kelas tidak boleh digabung menjadi satu definisi.
2. **Satu kelas dapat memiliki lebih dari satu makna, dengan batas maksimal tiga makna per kelas kata.** Jika rujukan memuat lebih dari tiga, pilih paling banyak tiga makna yang paling umum dan relevan untuk cakupan Tahap 1. Jangan memaksakan semua rincian kamus masuk ke dataset.
3. **Contoh harus menunjukkan makna yang dijelaskan.** Contoh bukan sekadar kalimat yang kebetulan memuat kata tersebut.
4. **Sumber makna wajib dapat ditelusuri.** Definisi ditulis ulang secara sederhana, bukan menyalin panjang definisi kamus. Rujukan sumber dicatat per makna.
5. **Contoh penggunaan dikurasi.** Contoh ditulis untuk kebutuhan ILIS dan harus diperiksa; tidak dibuat otomatis hanya demi mengisi kolom.
6. **Ketidakpastian dinyatakan.** Jika makna atau kelas tidak dapat dipastikan dari rujukan yang tersedia, jangan mengarang. Tandai sebagai isu kurasi di luar data final.
7. **Data lama dipertahankan.** Tidak menghapus atau mengubah nilai `entri`, `jenis`, `bentuk_dasar`, `imbuhan`, atau `catatan` dalam pekerjaan pengisian nanti, kecuali ada revisi terpisah yang disetujui.
8. **Referensi tetap referensi.** Status root tetap `referensi`; penambahan makna tidak berarti data lulus atau boleh dipakai runtime.
9. **Tidak memperluas tahap.** Makna leksikal dasar dan contoh pemakaian hanya menjelaskan kata/kelas yang sudah dicatat. Tidak mengajarkan imbuhan, analisis sintaksis umum, pragmatik, makna kiasan yang kompleks, atau pengetahuan ensiklopedis.

## 4. Struktur field yang diusulkan

Tambahkan satu field opsional selama proses migrasi pada setiap objek entri:

- `uraian_per_jenis`: array uraian yang dipisahkan berdasarkan kelas kata.

Setiap objek dalam array memuat:

| Field | Tipe | Ketentuan |
|---|---|---|
| `kelas_kata` | string | Wajib. Harus sama persis dengan salah satu label pada array lama `jenis` milik entri. |
| `makna` | array | Wajib untuk setiap kelas yang telah dikurasi; berisi 1–3 objek makna. |

Setiap objek `makna` memuat field berikut:

| Field | Tipe | Status | Ketentuan |
|---|---|---|---|
| `makna_id` | string | Wajib | ID stabil dan unik di dalam entri, misalnya `nomina-01`. |
| `definisi` | string | Wajib | Uraian sederhana, ringkas, dan ditulis ulang dengan bahasa sendiri. |
| `contoh_penggunaan` | string | Wajib | Kalimat sederhana 2–5 kata yang benar-benar menunjukkan makna tersebut. |
| `rujukan` | array objek | Wajib | Minimal satu rujukan yang mendukung definisi makna. |
| `catatan_penggunaan` | string | Opsional | Keterangan tambahan yang benar-benar diperlukan; boleh tidak dicantumkan. |

Dengan demikian, elemen wajib pada data makna adalah kelas kata (di objek induk), definisi, contoh penggunaan, dan rujukan. `catatan_penggunaan` secara tegas opsional dan tidak menjadi syarat kelengkapan.

Setiap objek `rujukan` memuat:

| Field | Tipe | Ketentuan |
|---|---|---|
| `nama_sumber` | string | Nama kamus atau rujukan kebahasaan yang benar-benar diperiksa. |
| `entri_rujukan` | string | Lema/istilah yang dicari pada sumber. |
| `lokator` | string | Penunjuk bagian/nomor entri/halaman jika tersedia. |
| `url` | string atau null | URL sumber jika tersedia dan benar-benar diperiksa. |
| `tanggal_akses` | string | Tanggal akses nyata dalam format `YYYY-MM-DD`. |

Field `lokator` dan `url` dapat disesuaikan jika jenis sumber tidak menyediakan salah satunya. Nama sumber, entri rujukan, dan tanggal akses tetap wajib. Jangan mengisi URL atau tanggal dengan tebakan.

### 4.1 Contoh bentuk JSON usulan

Contoh berikut hanya menunjukkan struktur. Uraian dan rujukan di dalamnya adalah ilustrasi format, bukan kurasi yang telah disetujui untuk dataset.

```json
{
  "entri": "dekat",
  "jenis": [
    "adjektiva",
    "preposisi"
  ],
  "bentuk_dasar": true,
  "imbuhan": null,
  "catatan": "",
  "uraian_per_jenis": [
    {
      "kelas_kata": "adjektiva",
      "makna": [
        {
          "makna_id": "adjektiva-01",
          "definisi": "<definisi sederhana yang telah diperiksa>",
          "contoh_penggunaan": "<kalimat sederhana 2–5 kata>",
          "rujukan": [
            {
              "nama_sumber": "<nama kamus/rujukan>",
              "entri_rujukan": "dekat",
              "lokator": "<bagian entri jika tersedia>",
              "url": null,
              "tanggal_akses": "<YYYY-MM-DD>"
            }
          ]
        }
      ]
    },
    {
      "kelas_kata": "preposisi",
      "makna": [
        {
          "makna_id": "preposisi-01",
          "definisi": "<definisi sederhana yang telah diperiksa>",
          "contoh_penggunaan": "<kalimat sederhana 2–5 kata>",
          "rujukan": [
            {
              "nama_sumber": "<nama kamus/rujukan>",
              "entri_rujukan": "dekat",
              "lokator": "<bagian entri jika tersedia>",
              "url": null,
              "tanggal_akses": "<YYYY-MM-DD>"
            }
          ]
        }
      ]
    }
  ]
}
```

Placeholder dalam contoh di atas tidak boleh dipakai sebagai data nyata. Contoh ini juga tidak menetapkan definisi final untuk kata `dekat`.

## 5. Aturan konsistensi dan validasi yang diusulkan

1. `uraian_per_jenis` tidak boleh berisi `kelas_kata` yang tidak ada pada array lama `jenis`.
2. Untuk entri yang sudah lengkap, setiap label pada `jenis` harus memiliki tepat satu objek `uraian_per_jenis`.
3. Setiap objek kelas harus memiliki 1–3 objek `makna`; maksimal tiga makna per kelas kata. Jika sumber memuat lebih dari tiga, pilih paling banyak tiga makna yang paling umum dan relevan untuk Tahap 1.
4. `makna_id` tidak boleh kosong dan harus unik di dalam entri. ID yang sudah dipakai tidak diganti tanpa alasan dan catatan revisi.
5. Setiap objek makna wajib memiliki `definisi`, `contoh_penggunaan`, dan sekurang-kurangnya satu `rujukan` yang valid.
6. `catatan_penggunaan` bersifat opsional. Ketiadaannya tidak membuat objek makna tidak valid.
7. Teks wajib tidak boleh hanya berisi spasi atau placeholder.
8. `contoh_penggunaan` harus berupa kalimat sederhana sepanjang 2–5 kata, bukan kalimat kompleks dan bukan uraian/analisis struktur kalimat. Kalimat harus memperlihatkan bentuk sasaran dalam pemakaian yang wajar. Untuk partikel terikat seperti `-kah`, contoh boleh menampilkan partikel melekat pada bentuk yang mengikutinya sesuai ejaan.
9. Untuk entri multi-kelas, contoh pada setiap kelas harus membedakan fungsi kelas tersebut. Jangan memakai satu contoh yang sama untuk mengklaim dua fungsi berbeda.
10. Untuk entri multi-makna dalam kelas yang sama, buat objek makna terpisah hanya jika contoh dan definisinya memang menunjukkan perbedaan yang relevan.
11. Ejaan, kapitalisasi, dan tanda baca contoh mengikuti kaidah bahasa Indonesia.
12. Contoh tidak boleh mengandung fakta ensiklopedis yang tidak diperlukan untuk memperlihatkan fungsi kata.
13. Nilai lama pada field inti harus tetap sama selama migrasi makna/contoh. Perubahan leksikal atau kelas kata memerlukan evaluasi terpisah.

### 5.1 Status selama migrasi

- Entri yang belum dikurasi boleh belum memiliki `uraian_per_jenis`; jangan mengisi array kosong atau teks seperti `"belum ada"` sebagai pengganti data.
- Ketiadaan field selama migrasi berarti belum dikurasi, bukan berarti kata tidak memiliki makna.
- Klaim bahwa dataset telah lengkap baru boleh dibuat setelah seluruh cakupan yang disetujui diperiksa dengan validator dan laporan kurasi.
- Field opsional selama migrasi tidak berarti opsional pada gerbang kelengkapan akhir, kecuali Owner dan evaluator menyetujui pengecualian tertulis.

## 6. Sumber, penulisan, dan mutu kurasi

1. Gunakan kamus atau rujukan kebahasaan yang dapat diidentifikasi dan diperiksa. Pilihan sumber utama dan aturan jika dua sumber berbeda harus disetujui evaluator sebelum kurasi massal.
2. Penjelasan ditulis sebagai parafrasa ringkas dengan bahasa yang mudah dipahami; jangan menyalin definisi panjang dari kamus.
3. Jangan memperluas definisi melebihi informasi yang didukung sumber.
4. Jika rujukan hanya mendukung satu kelas, jangan menambahkan kelas lain berdasarkan intuisi.
5. Jika ada perbedaan makna, label kelas, atau kelaziman penggunaan antar sumber, catat sebagai isu untuk evaluator; jangan memilih secara diam-diam.
6. Contoh penggunaan boleh disusun sendiri, tetapi harus diperiksa agar alami, tepat kelas, dan tidak menambahkan aturan Tahap 2–4.
7. Hindari definisi melingkar, misalnya menjelaskan kata hanya dengan sinonim yang sama sulitnya.
8. Jangan menganggap satu makna kamus harus dimasukkan seluruhnya. Prioritaskan makna dasar yang relevan untuk target pengenalan Tahap 1 dan catat batas cakupan.

## 7. Dampak terhadap versi dan kompatibilitas

Rancangan ini mengubah struktur entri sehingga **jika disetujui dan diterapkan**, usulan awalnya adalah:

- menaikkan `versi_format` dari `1.0` menjadi `1.1` saat struktur baru benar-benar diterapkan;
- sebelum satu pun entri diubah ke format 1.1, lakukan Tugas Pendahuluan #1 melalui PR data terpisah: tambahkan `"versi_data": "1.0"` pada root `kata_dasar.json`;
- setelah itu, naikkan `versi_data` pada setiap batch perubahan isi sesuai kebijakan versi dataset;
- mempertahankan `status` root sebagai `referensi`;
- tidak mengubah data runtime karena paket runtime Tahap 1 belum disetujui.

Sebelum migrasi entri, Tugas Pendahuluan #1 wajib diselesaikan terlebih dahulu melalui PR terpisah: menambahkan `"versi_data": "1.0"` pada root `kata_dasar.json`. PR dokumentasi ini tidak melakukan perubahan tersebut. Perubahan `versi_format` menjadi 1.1 baru dilakukan ketika struktur baru benar-benar diterapkan; dokumen usulan ini sendiri tidak mengubah versi apa pun.

**Kompatibilitas runtime:** `load_word_reference()` saat ini memvalidasi field inti dan mengembalikan objek entri; kode yang ada belum menetapkan kontrak runtime untuk membaca `uraian_per_jenis`. Penambahan field data tidak otomatis membuat `lookup_word()` mengembalikan makna atau membuat chatbot memahami definisi. Jika kelak field ini akan dikonsumsi runtime, diperlukan tugas implementasi dan pengujian terpisah serta persetujuan tersendiri.

## 8. Rencana validasi sebelum pengisian massal

Sebelum seluruh 152 entri diisi:

1. Evaluator menyetujui struktur dan aturan sumber.
2. Pilih sejumlah kecil entri perwakilan untuk uji skema, termasuk:
   - satu entri dengan satu kelas dan satu makna;
   - satu entri dengan satu kelas dan dua makna;
   - `dekat` sebagai entri dua kelas;
   - partikel terikat seperti `-kah`;
   - entri multi-kata seperti `lima belas`.
3. Kurasi sampel dilakukan hanya setelah ada tugas data terpisah yang disetujui Owner.
4. Jalankan pemeriksaan struktur: tipe field, kecocokan kelas, ID unik, rujukan, contoh nonkosong, dan konsistensi field inti.
5. Minta evaluator memeriksa ketepatan makna dan contoh, bukan hanya validitas JSON.
6. Perbaiki skema jika sampel menunjukkan masalah; jangan lanjut ke seluruh entri sebelum sampel diterima.
7. Setelah skema dan sampel diterima, buat rencana batch bertahap dengan daftar entri, sumber, penanggung jawab kurasi, dan gerbang review.

## 9. Batas pekerjaan dan hal yang belum diizinkan

Dokumen ini **tidak**:

- menambahkan atau mengubah satu pun dari 152 entri `kata_dasar.json`;
- mengubah `versi_format`, `versi_data`, atau metadata dataset; Tugas Pendahuluan #1 untuk menambahkan `versi_data` tetap merupakan PR data terpisah;
- mengubah `aturan_ejaan.json`;
- mengubah kode `foundation.py` atau kontrak API;
- mengintegrasikan makna ke Semantic 12, Reasoning 6, KnowledgeEngine, ChatbotAdapter, atau playground;
- mengubah dataset pengetahuan umum;
- menyatakan makna/contoh sudah dikurasi atau diverifikasi;
- mempromosikan data ke `data/runtime/` atau branch `main`;
- memperluas cakupan ke Tahap 2–4.

Pekerjaan pengisian data harus menjadi tugas tersendiri setelah struktur, sumber, sampel, dan batas kurasi disetujui.

## 10. Pertanyaan evaluasi untuk Dola

Mohon evaluasi secara khusus:

1. Apakah pemisahan `uraian_per_jenis` sudah tepat untuk kata multi-kelas seperti `dekat`?
2. Apakah struktur `makna[]` cukup untuk menampung beberapa makna dalam satu kelas tanpa mendorong pengisian berlebihan?
3. Apakah metadata `rujukan` sudah cukup untuk audit sumber dan parafrasa?
4. Apakah aturan satu uraian untuk setiap kelas pada gerbang kelengkapan akhir tepat, dengan field yang boleh belum ada selama migrasi?
5. Apakah usulan `versi_format` 1.1 dan penyelesaian `versi_data` sudah tepat atau perlu langkah kompatibilitas terpisah?
6. Apakah sampel uji skema mencakup kasus khusus yang diperlukan?
7. Apakah batas contoh sebagai kalimat sederhana 2–5 kata sudah cukup menjaga cakupan Tahap 1 tanpa mendorong analisis sintaksis?

**Keputusan yang diminta:** evaluasi dokumen rancangan ini saja. Belum ada permintaan persetujuan untuk mengisi dataset atau mengubah runtime.

---

**Kesimpulan:** Struktur yang diusulkan menempatkan makna dan contoh per kelas kata, menjaga sumber tetap dapat ditelusuri, serta mempertahankan batas antara data referensi, validasi materi, dan kemampuan runtime. Kualitas dan ketepatan kurasi lebih penting daripada kecepatan melengkapi 152 entri.
