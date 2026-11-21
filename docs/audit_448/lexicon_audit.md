# Audit 448 Record — Pilar A: Lexicon

- **Basis branch:** `ilis-v2-development`
- **Basis SHA:** `32d09cc52ee71bd7f3ab9e549c4e92f748e14915`
- **Audit branch:** `audit-448-lexicon`
- **Cakupan:** 90 record, `lex-0003` sampai `lex-0092`, 18 file JSONL.
- **Batas:** audit dan dokumentasi saja. Tidak ada perubahan JSONL, kode, SQLite, tes, workflow, atau `main`.
- **Status dataset:** seluruh record tetap `verification_status: draft`.

## 1. Hasil sementara yang dapat dipertanggungjawabkan

| Status audit | Jumlah | Arti |
|---|---:|---|
| PASS | 16 | Memiliki pemeriksaan bahasa/morfologi terdahulu yang spesifik dan tercatat pada backlog Fase 2; revisi yang disetujui Dola sudah tercermin pada record saat ini. |
| REVISE | 0 | Belum ada kesalahan yang cukup terbukti untuk menetapkan revisi tanpa pemeriksaan sumber/kelas kata lebih lanjut. |
| REVIEW | 74 | Sudah diinventarisasi dan dibaca, tetapi belum memiliki verifikasi sumber spesifik/penilaian lengkap yang cukup untuk dinyatakan PASS. |

**Penting:** ini bukan klaim bahwa 90 record telah lolos audit final. Pembacaan seluruh record dan pemeriksaan struktur/isi awal sudah dilakukan; 74 record masih menunggu verifikasi leksikografis/morfologis yang dapat ditelusuri. Karena itu Pilar A belum ditutup dan belum boleh dilanjutkan sebagai pilar selesai.

## 2. Status per record

| Record | Status | Dasar/catatan |
|---|---|---|
| lex-0003–lex-0066 | REVIEW | Isi telah dibaca. Mayoritas sumber masih berupa rujukan umum “KBBI Daring” tanpa URL/entri/rujukan spesifik per lema; definisi, kelas kata, bentuk turunan, sinonim/antonim, dan contoh perlu dicocokkan satu per satu. |
| lex-0067 | PASS | Pemeriksaan Fase 2: analisis `meng-` + `apa` dan fungsi tanya sebab dirujuk ke TBBI Edisi Keempat, Bab 7.2.2.4. |
| lex-0068–lex-0069 | REVIEW | Fungsi kata tanya sudah masuk akal secara semantik, tetapi kelas kata dan distribusi konstruksi perlu dicocokkan dengan rujukan spesifik. |
| lex-0070–lex-0071 | PASS | Pemeriksaan Fase 2: `-kah` dan konstruksi `apakah/adakah` dirujuk ke TBBI Edisi Keempat §8.2.5.1 dan contoh terkait. |
| lex-0072 | REVIEW | KBBI VI Daring memberi label `pron cak` untuk `kenapa`, sedangkan record memakai `adverbia_tanya`. **Catatan perbedaan taksonomi, bukan kesalahan yang terbukti.** Dola menerima `adverbia_tanya` sebagai kategori fungsional; tidak perlu mengubah JSONL sekarang. Peninjauan konsistensi taksonomi seluruh 90 record dapat dilakukan kemudian dan bukan penghalang audit/merge. |
| lex-0073 | PASS | Pemeriksaan Fase 2: pembedaan preposisi `di` dan prefiks pasif `di-` didukung TBBI; kaidah ejaan juga sesuai EYD V. |
| lex-0074–lex-0075 | REVIEW | Makna arah/tujuan dan asal/sumber tampak konsisten, tetapi belum ada pemeriksaan sumber leksikal spesifik untuk kedua lema. |
| lex-0076–lex-0077 | PASS | Pemeriksaan Fase 2: `pada` dirujuk ke TBBI Tabel 9.3; `dalam` sudah melalui revisi contoh dan diterima Dola. Record saat ini memuat contoh `Ia memikirkan persoalan itu dalam-dalam`, bukan contoh lama yang dinilai tidak idiomatis. |
| lex-0078 | REVIEW | Definisi aspek progresif masuk akal; sumber masih generik dan perlu pemeriksaan rujukan tata bahasa. |
| lex-0079–lex-0082 | PASS | Pemeriksaan Fase 2: `sudah`, `telah`, `pernah`, dan `akan` diperiksa dengan TBBI Bab 4 serta Grangé (2010); batas nuansa/aspek dipertahankan. |
| lex-0083–lex-0084 | REVIEW | Kuantitas banyak/sedikit masuk akal; perlu penetapan kelas kata yang konsisten dengan tata bahasa dan fungsi sebagai penentu frasa nominal. |
| lex-0085–lex-0086 | PASS | Pemeriksaan Fase 2: pembedaan `seluruh` dan `setiap` dirujuk ke Petunjuk Praktis Berbahasa Indonesia dan TBBI. |
| lex-0087 | REVIEW | Fungsi parsial masuk akal; bentuk `sebagian`, kelas kata, dan fungsi penentu perlu diperiksa secara spesifik. |
| lex-0088–lex-0089 | PASS | Pemeriksaan Fase 2: `meN-` pada `membaca` dan prefiks pasif `di-` pada `ditulis` telah diperiksa dengan TBBI dan kaidah ejaan. |
| lex-0090 | REVIEW | Definisi gerak/proses masuk akal, tetapi sumber khusus untuk valensi dan polisemi `berjalan` belum dicatat. |
| lex-0091–lex-0092 | PASS | Pemeriksaan Fase 2: uraian polisemi `ter-` sudah dirumuskan ulang dan diterima Dola; fungsi benefaktif `-kan` pada `membawakan` diperiksa dengan TBBI. |

## 3. Temuan dan hal yang harus diperiksa pada putaran lanjutan

1. **Provenance terlalu umum.** Banyak record hanya menyebut “KBBI Daring” atau “TBBI” tanpa URL/entri/bagian yang mendukung sense tertentu. Itu belum cukup untuk audit yang dapat direproduksi.
2. **Kelas kata kata tanya.** Samakan kerangka internal `pronomina_tanya`, `adverbia_tanya`, `numeralia_tanya`, dan `partikel_interogatif` dengan label rujukan dan tujuan anotasi ILIS. Jangan mengganti label hanya karena perbedaan istilah sebelum aturan taksonomi ditetapkan.
3. **lex-0072 / kenapa.** KBBI VI Daring menampilkan `pron cak`, sedangkan dataset memakai `adverbia_tanya`. Dola menerima label dataset sebagai kategori fungsional. Ini perbedaan sistem klasifikasi, bukan temuan kesalahan; tidak perlu mengubah JSONL. Konsistensi seluruh label kelas kata dapat ditinjau kemudian.
4. **lex-0022 / terlanjur.** Periksa bentuk lema dan hubungan dengan bentuk `telanjur` pada KBBI VI Daring sebelum memutuskan apakah perlu koreksi.
5. **Polisemi dan valensi.** Periksa bentuk turunan serta perubahan valensi, khususnya bentuk `meN-...-kan`, `ke-...-an`, `ter-`, preposisi, dan adverbia.
6. **Sinonim/antonim.** Pastikan hubungan tersebut berlaku untuk sense yang sama; parafrasa atau kata yang hanya dekat makna harus tetap diberi keterangan konteks.

## 4. Rujukan yang digunakan

- KBBI VI Daring — Badan Pengembangan dan Pembinaan Bahasa: https://kbbi.kemendikdasmen.go.id/
- Entri KBBI `mengapa`: https://kbbi.kemendikdasmen.go.id/entri/mengapa
- Entri KBBI `kenapa`: https://kbbi.kemendikdasmen.go.id/entri/kenapa
- TBBI Edisi Keempat (2017): https://repositori.kemendikdasmen.go.id/16351/1/Tata%20Bahasa%20Baku%20Bahasa%20Ind.pdf
- EYD V — Kata Turunan: https://ejaan.kemendikdasmen.go.id/eyd/penulisan-kata/kata-turunan/
- Petunjuk Praktis Berbahasa Indonesia: https://repositori.kemendikdasmen.go.id/3420/1/Petunjuk%20praktis%20berbahasa%20indonesia.pdf
- Grangé (2010), *Aspect and modality in Indonesian: The case of sudah, telah, pernah and sempat*: https://doi.org/10.17510/wacana.v12i2.117

## 5. Batas kesimpulan

- PASS pada log ini tidak mengubah `verification_status` JSONL.
- REVIEW berarti belum ada bukti memadai untuk menyatakan benar/salah; bukan berarti record salah.
- Belum ada record JSONL yang diedit atau dipromosikan.
- Pilar A **belum final** sampai 74 record REVIEW selesai dicocokkan dengan sumber. Catatan lex-0072 tidak menghalangi merge; perbedaan taksonomi diterima Dola.
- Pilar B–E belum diaudit pada pekerjaan ini.
- Tahap Evaluation split Dev/Validation/Final-Test tetap terpisah dan Final-Test tidak boleh dipakai untuk tuning.
