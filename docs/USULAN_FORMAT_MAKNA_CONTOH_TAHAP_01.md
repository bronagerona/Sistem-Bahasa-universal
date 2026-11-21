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
2. **Satu kelas dapat memiliki lebih dari satu makna.** Tambahkan makna hanya jika memang diperlukan untuk menjelaskan penggunaan yang dicatat; jangan mengejar banyaknya definisi.
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
| `jenis` | string | Harus sama persis dengan salah satu label pada array `jenis` milik entri. |
| `makna` | array | Minimal satu makna yang telah dikurasi untuk kelas tersebut. |
| `makna_id` | string | ID stabil dan unik di dalam entri, misalnya `nomina-01`. |
| `penjelasan` | string | Uraian sederhana, ringkas, dan ditulis ulang dengan bahasa sendiri. |
| `contoh_penggunaan` | string | Satu contoh singkat yang benar-benar menunjukkan makna tersebut. |
| `rujukan` | array objek | Minimal satu rujukan yang mendukung penjelasan makna. |

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
      "jenis": "adjektiva",
      "makna": [
        {
          "makna_id": "adjektiva-01",
          "penjelasan": "<uraian sederhana yang telah diperiksa>",
          "contoh_penggunaan": "<contoh yang menunjukkan fungsi adjektiva>",
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
      "jenis": "preposisi",
      "makna": [
        {
          "makna_id": "preposisi-01",
          "penjelasan": "<uraian sederhana yang telah diperiksa>",
          "contoh_penggunaan": "<contoh yang menunjukkan fungsi preposisi>",
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

1. `uraian_per_jenis` tidak boleh berisi label kelas yang tidak ada pada `jenis`.
2. Untuk entri yang sudah lengkap, setiap label pada `jenis` harus memiliki tepat satu objek uraian kelas pada `uraian_per_jenis`.
3. Satu objek kelas harus memiliki sedikitnya satu objek `makna`.
4. `makna_id` tidak boleh kosong dan harus unik di dalam entri. ID yang sudah dipakai tidak diganti tanpa alasan dan catatan revisi.
5. Setiap makna harus memiliki `penjelasan`, `contoh_penggunaan`, dan sekurang-kurangnya satu `rujukan` yang valid.
6. Teks tidak boleh hanya berisi spasi atau placeholder.
7. `contoh_penggunaan` harus memperlihatkan bentuk sasaran dalam pemakaian yang wajar. Untuk partikel terikat seperti `-kah`, contoh boleh menampilkan partikel melekat pada bentuk yang mengikutinya sesuai ejaan.
8. Untuk entri multi-kelas, contoh pada setiap kelas harus membedakan fungsi kelas tersebut. Jangan memakai satu contoh yang sama untuk mengklaim dua fungsi berbeda.
9. Untuk entri multi-makna dalam kelas yang sama, buat objek makna terpisah hanya jika contoh dan penjelasannya memang menunjukkan perbedaan yang relevan.
10. Ejaan, kapitalisasi, dan tanda baca contoh mengikuti kaidah bahasa Indonesia.
11. Contoh tidak boleh mengandung fakta ensiklopedis yang tidak diperlukan untuk memperlihatkan fungsi kata.
12. Nilai lama pada field inti harus tetap sama selama migrasi makna/contoh. Perubahan leksikal atau kelas kata memerlukan evaluasi terpisah.

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

- menaikkan `versi_format` dari `1.0` menjadi `1.1`;
- menambahkan/melengkapi `versi_data` sesuai ketentuan versi data pada `docs/FORMAT_DATASET.md`;
- menaikkan `versi_data` pada setiap batch perubahan isi;
- mempertahankan `status` root sebagai `referensi`;
- tidak mengubah data runtime karena paket runtime Tahap 1 belum disetujui.

Sebelum implementasi, ketidaksinkronan `versi_data` yang ditemukan pada file saat ini harus diselesaikan secara eksplisit. Perubahan `versi_format` dan `versi_data` tidak boleh dilakukan sekarang hanya karena dokumen usulan ini dibuat.

**Kompatibilitas runtime:** `load_word_reference()` saat ini memvalidasi field inti dan mengembalikan objek entri; kode yang ada belum menetapkan kontrak runtime untuk membaca `uraian_per_jenis`. Penambahan field data tidak otomatis membuat `lookup_word()` mengembalikan makna atau membuat chatbot memahami definisi. Jika kelak field ini akan dikonsumsi runtime, diperlukan tugas implementasi dan pengujian terpisah serta persetujuan tersendiri.

## 8. Rencana validasi sebelum pengisian massal

Sebelum seluruh 152 entri diisi:

1. Evaluator menyetujui struktur dan aturan sumber.
2. Pilih sejumlah kecil entri perwakilan untuk uji skema, termasuk:
   - satu entri satu kelas;
   - `dekat` sebagai entri dua kelas;
   - satu entri yang memiliki lebih dari satu makna dalam kelas yang sama, jika ditemukan dan disetujui;
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
- mengubah `versi_format`, `versi_data`, atau metadata dataset;
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
7. Adakah risiko bahwa contoh penggunaan mendorong sistem melakukan analisis sintaksis di luar batas Tahap 1? Jika ada, usulkan batas yang lebih aman.

**Keputusan yang diminta:** evaluasi dokumen rancangan ini saja. Belum ada permintaan persetujuan untuk mengisi dataset atau mengubah runtime.

---

**Kesimpulan:** Struktur yang diusulkan menempatkan makna dan contoh per kelas kata, menjaga sumber tetap dapat ditelusuri, serta mempertahankan batas antara data referensi, validasi materi, dan kemampuan runtime. Kualitas dan ketepatan kurasi lebih penting daripada kecepatan melengkapi 152 entri.
