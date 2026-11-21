# FORMAT DATASET — SPESIFIKASI FORMAT DAN STRUKTUR DATA ILIS

**Branch:** `ilis-v2-development`  
**Status:** Dokumen spesifikasi — BELUM ADA DATA BARU YANG DIBUAT  
**Acuan:** `docs/RENCANA_IMPLEMENTASI_NYATA.md`, `docs/DAFTAR_DASAR_TAHAP_01.md` sampai `docs/DAFTAR_DASAR_TAHAP_04.md`, serta dokumen kurikulum dan penguatannya  
**Batas:** Dokumen ini hanya menetapkan rancangan format dan struktur. Tidak membuat folder `data/` atau `tests/`, tidak membuat JSON data/uji, dan tidak mengubah dataset aktif, kode, konfigurasi, runtime, atau branch `main`.

---

## 1 — Prinsip Penamaan dan Penyimpanan

### 1.1 Nama file dan folder

1. Gunakan huruf kecil untuk nama file dan folder.
2. Gunakan garis bawah (`_`) sebagai pemisah kata; jangan gunakan spasi.
3. Gunakan ekstensi sesuai isi: `.md` untuk dokumen Markdown dan `.json` untuk data terstruktur.
4. Nama file harus menjelaskan tahap dan isi, misalnya `kata_dasar.json`, `aturan_ejaan.json`, dan `test_tahap_01_ejaan.json`.
5. Jangan menimpa versi runtime yang sudah disetujui tanpa proses revisi dan verifikasi. Perubahan harus dapat ditelusuri melalui riwayat Git dan catatan versi.

### 1.2 Dua area data

**REFERENSI — `data/reference/`**

- Tempat bahan hasil konversi dari daftar dasar, panduan, dan kurasi awal.
- Status data selalu `referensi`.
- Belum dianggap benar, belum lulus uji, dan tidak boleh dipakai runtime.
- Menjadi sumber kerja untuk koreksi dan revisi sebelum verifikasi.

**RUNTIME — `data/runtime/`**

- Tempat salinan versi materi yang sudah lulus gerbang tahap, ditinjau, dan disetujui.
- Status data selalu `aktif`.
- Hanya boleh diperbarui melalui revisi terkontrol: versi baru, pengujian ulang yang relevan, persetujuan, dan catatan perubahan.
- `aktif` berarti disetujui sebagai paket runtime; **bukan bukti bahwa kode ILIS sudah memuat atau menggunakan file tersebut**. Integrasi loader merupakan pekerjaan terpisah.

Data referensi dan runtime tidak boleh dicampur. Jangan memindahkan atau menghapus satu-satunya salinan referensi ketika mempromosikan data. Buat salinan rilis yang dapat ditelusuri kembali ke sumbernya.

## 2 — Rancangan Struktur Folder Proyek

Struktur berikut adalah **rancangan tujuan**, bukan struktur yang dibuat oleh commit dokumen ini.

```text
Sistem-Bahasa-universal/
├── docs/
│   ├── KURIKULUM_PEMAHAMAN_BAHASA.md
│   ├── TAHAP_01_FONDASI_DASAR.md
│   ├── TAHAP_02_KATA_DAN_KALIMAT.md
│   ├── TAHAP_03_MAKSUD_DAN_KONTEKS.md
│   ├── TAHAP_04_WACANA_DAN_VARIASI_BAHASA.md
│   ├── DAFTAR_DASAR_TAHAP_01.md
│   ├── DAFTAR_DASAR_TAHAP_02.md
│   ├── DAFTAR_DASAR_TAHAP_03.md
│   ├── DAFTAR_DASAR_TAHAP_04.md
│   ├── RENCANA_IMPLEMENTASI_NYATA.md
│   └── FORMAT_DATASET.md
├── data/
│   ├── reference/
│   │   ├── tahap_01_fondasi/
│   │   │   ├── kata_dasar.json
│   │   │   └── aturan_ejaan.json
│   │   ├── tahap_02_kata_kalimat/
│   │   ├── tahap_03_maksud_konteks/
│   │   └── tahap_04_wacana/
│   └── runtime/
│       ├── tahap_01_fondasi.json
│       ├── tahap_02_kata_kalimat.json
│       ├── tahap_03_maksud_konteks.json
│       └── tahap_04_wacana.json
└── tests/
    ├── tahap_01/
    │   ├── test_tahap_01_ejaan.json
    │   └── test_tahap_01_kelas_kata.json
    ├── tahap_02/
    ├── tahap_03/
    ├── tahap_04/
    └── README.md
```

**Keterangan:**

- `docs/`: panduan konsep, daftar referensi, spesifikasi format, rencana, keputusan, dan laporan.
- `data/reference/`: bahan yang belum lulus verifikasi. Subfolder dipisah per tahap agar materi tidak tercampur.
- `data/runtime/`: paket tahap yang telah disetujui. Setiap file harus memiliki sumber, versi, dan metadata verifikasi.
- `tests/`: paket kasus uji dan laporan hasil per tahap. Kasus uji dipisahkan dari data referensi dan data runtime.

Folder dan file pada pohon di atas tidak dibuat dalam tugas penyusunan spesifikasi ini. Pembuatan aktual memerlukan langkah persiapan tersendiri.

## 3 — Format Data Standar

Semua contoh JSON di bawah adalah **contoh spesifikasi**, bukan file data yang sudah dibuat. JSON harus valid: gunakan tanda kutip ganda, koma yang benar, dan nilai `null` tanpa tanda kutip.

### A. Referensi kata dasar

**Nama file:** `kata_dasar.json`  
**Lokasi rancangan:** `data/reference/tahap_01_fondasi/`

```json
{
  "versi_format": "1.0",
  "versi_data": "tahap_01-0.1.0",
  "sumber": "docs/DAFTAR_DASAR_TAHAP_01.md",
  "status": "referensi",
  "tahap": "tahap_01_fondasi",
  "tanggal_dibuat": "YYYY-MM-DD",
  "catatan": "Bahan referensi; belum diuji dan belum boleh digunakan runtime.",
  "daftar": [
    {
      "entri": "buku",
      "jenis": ["nomina"],
      "bentuk_dasar": true,
      "imbuhan": null,
      "catatan": "kata dasar umum"
    }
  ]
}
```

### B. Referensi aturan ejaan

**Nama file:** `aturan_ejaan.json`  
**Lokasi rancangan:** `data/reference/tahap_01_fondasi/`

```json
{
  "versi_format": "1.0",
  "versi_data": "tahap_01-0.1.0",
  "sumber": "docs/DAFTAR_DASAR_TAHAP_01.md",
  "status": "referensi",
  "tahap": "tahap_01_fondasi",
  "tanggal_dibuat": "YYYY-MM-DD",
  "daftar_aturan": [
    {
      "aturan_id": "T1-EJA-001",
      "aturan": "Kata depan di, ke, dan dari ditulis terpisah dari kata yang mengikutinya.",
      "contoh_benar": "di rumah",
      "contoh_salah": "dirumah",
      "penjelasan": "Bedakan kata depan di dari awalan di- pada kata kerja pasif, misalnya ditulis."
    }
  ]
}
```

### C. Paket runtime setelah lulus verifikasi

**Nama file rancangan:** `tahap_01_fondasi.json`  
**Lokasi rancangan:** `data/runtime/`

Struktur isi mengikuti data referensi yang sesuai, dengan metadata verifikasi tambahan dan status `aktif`.

```json
{
  "versi_format": "1.0",
  "versi_data": "tahap_01-1.0.0",
  "sumber": "docs/DAFTAR_DASAR_TAHAP_01.md",
  "status": "aktif",
  "tahap": "tahap_01_fondasi",
  "tanggal_dibuat": "YYYY-MM-DD",
  "tanggal_diverifikasi": "YYYY-MM-DD",
  "diverifikasi_oleh": "Dola",
  "referensi_hasil_uji": [
    "tests/tahap_01/test_tahap_01_ejaan.json",
    "tests/tahap_01/test_tahap_01_kelas_kata.json"
  ],
  "catatan_lulus": "Gerbang tahap telah ditinjau dan disetujui; hasil uji tercatat.",
  "daftar": [
    {
      "entri": "buku",
      "jenis": ["nomina"],
      "bentuk_dasar": true,
      "imbuhan": null,
      "catatan": "kata dasar umum"
    }
  ]
}
```

**Catatan:** Nama peninjau pada contoh hanya menunjukkan bentuk metadata yang diharapkan. Nilai sebenarnya harus mencerminkan peninjau yang benar-benar melakukan pemeriksaan. Jangan mengisi tanggal atau klaim kelulusan sebelum verifikasi berlangsung.

### D. Arti kolom utama

| Kolom | Wajib | Keterangan |
|---|---|---|
| `versi_format` | Ya | Versi struktur/skema JSON, misalnya `1.0`. Berubah jika aturan format berubah. |
| `versi_data` | Ya | Versi isi paket data. Naik ketika isi paket direvisi. |
| `sumber` | Ya | Jalur dokumen sumber yang dapat ditelusuri. |
| `status` | Ya | Hanya `referensi` untuk data referensi atau `aktif` untuk paket yang disetujui. |
| `tahap` | Ya | Identitas tahap, misalnya `tahap_01_fondasi`. |
| `tanggal_dibuat` | Ya | Tanggal paket dibuat dalam format `YYYY-MM-DD`. |
| `tanggal_diverifikasi` | Runtime | Tanggal verifikasi yang benar-benar dilakukan. |
| `diverifikasi_oleh` | Runtime | Nama evaluator/peninjau yang benar-benar memeriksa. |
| `referensi_hasil_uji` | Runtime | Jalur paket uji dan/atau laporan yang mendukung keputusan lulus. |
| `entri` | Ya untuk kata | Bentuk kata yang dicatat. |
| `jenis` | Ya untuk kata | Daftar label kelas kata yang didukung oleh contoh/konteks. |
| `bentuk_dasar` | Ya untuk kata | Boolean: `true` jika bentuk dasar; `false` jika bentuk turunan/berimbuhan. |
| `imbuhan` | Ya untuk kata | `null` jika bentuk dasar; rincian imbuhan jika bentuk turunan. |
| `catatan` | Ya | Penjelasan ringkas, batas pemakaian, atau catatan kurasi. |

Kolom khusus tahap dapat ditambahkan dalam rancangan tahap berikutnya setelah ditinjau. Jangan mengubah arti kolom inti antar tahap tanpa menaikkan `versi_format`.

## 4 — Aturan Pengisian dan Validasi

1. **Bentuk entri kata:** gunakan huruf kecil untuk lema/kata umum, misalnya `buku`, `makan`, `di`. Nama khusus mengikuti ejaan dan kapitalisasi yang benar. Kalimat contoh ditulis dengan ejaan normal, termasuk huruf kapital dan tanda baca.
2. **Satu bentuk dapat memiliki beberapa kelas:** gunakan array, misalnya `"jenis": ["nomina", "verba"]`, hanya jika setiap fungsi didukung contoh pemakaian yang jelas. Jangan memberi banyak label hanya karena kemungkinan teoretis.
3. **Bentuk dasar:** gunakan `"bentuk_dasar": true` dan `"imbuhan": null`. Untuk bentuk berimbuhan, gunakan `false` dan jelaskan imbuhan yang relevan. Jangan mencampur bentuk berimbuhan ke daftar kata dasar tanpa penandaan.
4. **Sumber wajib:** setiap paket mencantumkan dokumen sumber. Jika entri berasal dari lebih dari satu sumber, seluruh sumber harus dicatat dengan cara yang konsisten pada spesifikasi lanjutan.
5. **Tanggal:** semua tanggal menggunakan format ISO `YYYY-MM-DD`. Placeholder seperti `YYYY-MM-DD` hanya untuk contoh; tidak boleh dipakai sebagai nilai tanggal nyata.
6. **Status paket data:** hanya dua nilai yang diperbolehkan:
   - `referensi` — belum disetujui untuk runtime.
   - `aktif` — telah lulus gerbang, ditinjau, dan disetujui sebagai paket runtime.
7. **Status pengujian bukan status data:** hasil kasus uji seperti lulus/gagal/perlu-konteks dicatat pada paket uji atau laporan pengujian, bukan menambah nilai baru pada kolom `status` data.
8. **Tidak mengarang:** jika kelas kata, bentuk, atau aturan belum dapat dipastikan, catat sebagai isu untuk ditinjau. Jangan mengisi nilai tebakan sebagai fakta.
9. **JSON harus dapat dibaca mesin:** tidak boleh ada komentar di dalam file JSON, koma tambahan di akhir daftar, atau format non-JSON.
10. **Perubahan harus terlacak:** setiap revisi isi menaikkan `versi_data`; perubahan struktur menaikkan `versi_format`. Riwayat perubahan dicatat melalui commit dan laporan terkait.

## 5 — Aturan Promosi: Referensi ke Runtime

Promosi bukan penyalinan manual tanpa pemeriksaan. Paket referensi hanya dapat menjadi paket runtime jika seluruh syarat berikut terpenuhi:

1. Seluruh cakupan paket telah ditinjau oleh evaluator.
2. Paket uji untuk tahap yang bersangkutan tersedia, memiliki kunci/hasil yang diharapkan, dan mencakup materi yang akan dipromosikan.
3. Pengujian dijalankan pada versi materi dan versi sistem yang dicatat.
4. Ambang kelulusan tahap tercapai. Untuk rencana umum, target minimal adalah **90% benar**, dengan **tidak ada kesalahan kritis**. Ketentuan khusus tahap dapat menambahkan syarat yang lebih ketat.
5. Kesalahan kritis diperbaiki dan diuji ulang. Kasus ambigu ditangani secara jujur; tidak dihitung benar jika sistem menebak tanpa dasar.
6. Laporan verifikasi tertulis disimpan di folder tahap yang sesuai dalam `tests/`, lengkap dengan hasil aktual, hasil yang diharapkan, ringkasan skor, kasus gagal, dan catatan isu terbuka.
7. Evaluator meninjau bukti dan Owner menyetujui gerbang tahap.
8. Paket runtime dibuat sebagai salinan rilis dari referensi yang disetujui. Isi, `versi_data`, sumber, tanggal verifikasi, identitas peninjau, dan rujukan hasil uji dicatat.
9. Status paket referensi tetap `referensi`; status salinan runtime ditetapkan menjadi `aktif`. Jangan mengubah satu-satunya sumber referensi menjadi runtime.

**Paket berstatus `aktif` belum otomatis dimuat oleh aplikasi.** Penggunaan oleh runtime memerlukan integrasi teknis yang terpisah, pengujian integrasi, dan persetujuan tersendiri.

## 6 — Format Kasus Uji

Contoh berikut menjadi panduan penulisan kasus uji. Ini bukan kasus uji yang sudah dibuat atau dijalankan.

**Lokasi rancangan:** `tests/tahap_01/test_tahap_01_ejaan.json`

```json
{
  "versi_format": "1.0",
  "paket_uji_id": "T1-EJA",
  "tahap": "tahap_01_fondasi",
  "jenis": "ejaan",
  "sumber": "docs/DAFTAR_DASAR_TAHAP_01.md",
  "kasus": [
    {
      "uji_id": "T1-EJA-001",
      "masukan": "dirumah",
      "diharapkan": "di rumah",
      "keterangan": "Kata depan di ditulis terpisah.",
      "sumber_aturan": "data/reference/tahap_01_fondasi/aturan_ejaan.json#T1-EJA-001"
    }
  ]
}
```

**Panduan kolom kasus uji:**

- `uji_id`: ID unik dan stabil untuk satu kasus.
- `masukan`: input yang diberikan kepada sistem.
- `diharapkan`: keluaran atau perilaku yang benar menurut kunci uji.
- `keterangan`: alasan singkat hasil yang diharapkan.
- `sumber_aturan`: rujukan aturan/entri yang mendasari kunci uji.

Hasil aktual tidak ditulis sebagai hasil yang diharapkan. Hasil pelaksanaan, status lulus/gagal/perlu-konteks, versi sistem, versi data, tanggal uji, dan penilai dicatat pada laporan hasil terpisah di folder tahap yang sama. Dengan demikian, paket uji tetap stabil dan dapat dijalankan ulang.

## 7 — Risiko dan Pengaman

| Risiko | Pencegahan |
|---|---|
| Data referensi langsung dipakai runtime | Runtime hanya menerima salinan yang lulus gerbang dan disetujui. |
| Data aktif diubah tanpa jejak | Gunakan versi baru, commit, laporan uji, dan persetujuan revisi. |
| Sumber data tidak diketahui | Kolom `sumber` wajib; setiap kasus uji merujuk aturan atau materi sumber. |
| Status pengujian tercampur dengan status paket | Status paket hanya `referensi` atau `aktif`; hasil uji dicatat terpisah. |
| Contoh ambigu dipaksa satu kelas | Simpan contoh konteks dan catatan; tandai isu untuk evaluator. |
| File JSON tidak valid | Validasi sintaks dan kolom wajib sebelum paket ditinjau atau diuji. |
| Paket runtime dianggap otomatis aktif di aplikasi | Status `aktif` hanya menyatakan persetujuan paket; integrasi loader tetap terpisah. |
| Revisi menghapus jejak sebelumnya | Jangan menimpa sumber historis; naikkan versi dan pertahankan riwayat Git. |

## 8 — Hal yang Belum Dilakukan dan Batas Persetujuan

Dokumen ini hanya menetapkan spesifikasi format dan struktur.

**Belum dilakukan:**

- Belum membuat folder `data/reference/`, `data/runtime/`, atau `tests/`.
- Belum membuat `kata_dasar.json`, `aturan_ejaan.json`, file runtime, paket uji, atau laporan hasil.
- Belum mengonversi isi daftar dasar Tahap 1–4 ke JSON.
- Belum mengubah dataset JSONL aktif atau data pengetahuan umum.
- Belum mengubah kode, loader, Semantic, Reasoning, KnowledgeEngine, playground, konfigurasi, atau branch `main`.
- Belum menyatakan tahap mana pun lulus implementasi.

Pembuatan data aktual harus dilakukan bertahap sesuai `docs/RENCANA_IMPLEMENTASI_NYATA.md`, dimulai dari Tahap 1 setelah spesifikasi ini ditinjau dan disetujui. Penerimaan dokumen format tidak otomatis menjadi izin membuat seluruh folder/data atau mengubah runtime.

**Prinsip penutup: Sumber harus jelas, status harus jujur, versi harus terlacak, dan hanya materi yang benar-benar lulus verifikasi yang boleh dipromosikan ke runtime.**
