# Audit 448 Record — Pilar B: Sentence Patterns

- **Basis branch:** `ilis-v2-development`
- **Basis SHA:** `57fe30b243e3c621ee5f0e7c2858a89b307cd1ae` (setelah merge PR #23)
- **Audit branch:** `audit-448-sentence-patterns`
- **Cakupan:** 90 record, `pat-0003` sampai `pat-0092`, 18 file JSONL.
- **Batas:** audit dan dokumentasi saja. Tidak ada perubahan JSONL, kode, SQLite, tes, workflow, atau `main`.
- **Status dataset:** seluruh record tetap `verification_status: draft`.

## 1. Ringkasan hasil

| Status audit | Jumlah | Arti |
|---|---:|---|
| PASS | 16 | Pola yang sama telah diperiksa secara spesifik pada Fase 2 dengan rujukan tata bahasa/ejaan dan hasilnya tercatat. |
| REVISE | 0 | Belum ditemukan kesalahan substansial yang cukup pasti untuk langsung menetapkan revisi record. |
| REVIEW | 74 | Sudah dibaca dan diperiksa secara awal, tetapi belum memiliki pemeriksaan sumber/tata bahasa spesifik yang cukup untuk PASS. |

Pemeriksaan awal mencakup struktur pola, intent, slots, constraints, contoh positif/negatif, register, dan catatan ambiguitas. Banyak record bersumber dari contoh sintetis untuk kurasi; hal itu dapat diterima untuk dataset pola, tetapi tetap membutuhkan penilaian konsistensi, kealamian, dan cakupan konstruksi sebelum status PASS.

**Penting:** REVIEW bukan berarti pola salah. Ini berarti bukti dan pemeriksaan belum cukup untuk menyatakan lolos. Tidak ada status audit yang mengubah `verification_status` JSONL.

## 2. Daftar status per record

### PASS — 16 record

| Record | Dasar pemeriksaan |
|---|---|
| pat-0067 | `mengapa`: TBBI Edisi Keempat, Bab 7.2.2.4; pola tanya sebab sesuai. |
| pat-0070 | `apakah`: TBBI §8.2.5.1; fungsi pertanyaan polar sesuai. |
| pat-0071 | `adakah`: contoh dan fungsi keberadaan/ketersediaan diperiksa pada TBBI §8.2.5.1. |
| pat-0073 | `di` sebagai preposisi lokasi dibedakan dari prefiks pasif `di-`; TBBI dan EYD. |
| pat-0076 | `pada`: penggunaan temporal dan relasi abstrak sesuai TBBI Tabel 9.3. |
| pat-0077 | `dalam`: pembedaan preposisi dan adjektiva sesuai; contoh leksikon terkait sudah direvisi dan diterima Dola. |
| pat-0079 | `sudah`: pemarkah aspektualitas; TBBI Bab 4. |
| pat-0080 | `telah`: aspek dan kecenderungan register formal; TBBI Bab 4. |
| pat-0081 | `pernah`: aspek pengalaman sebelum waktu acuan; TBBI dan Grangé (2010). |
| pat-0082 | `akan`: penanda prospektif dengan nuansa temporal/modal sesuai konteks; TBBI dan Grangé (2010). |
| pat-0085 | `seluruh`: cakupan kolektif; Petunjuk Praktis Berbahasa Indonesia dan TBBI. |
| pat-0086 | `setiap`: makna distributif dan pola umum nomina tunggal; TBBI. |
| pat-0088 | `meN-`: pola aktif dan morfofonemik nasal; TBBI Bab 4. |
| pat-0089 | `di-`: konstruksi pasif dan pembedaan dari preposisi `di`; TBBI/EYD. |
| pat-0091 | `ter-`: uraian polisemi telah dirumuskan ulang agar ketidaksengajaan tidak dianggap makna otomatis prefiks; diterima Dola. |
| pat-0092 | `-kan`: fungsi benefaktif/kausatif bergantung pangkal dan konstruksi; TBBI Bab 4. |

### REVIEW — 74 record

Record berikut sudah dibaca, tetapi belum memperoleh pemeriksaan sumber/tata bahasa spesifik yang cukup untuk PASS:

- `pat-0003`–`pat-0066` (64 record)
- `pat-0068`–`pat-0069` (2 record)
- `pat-0072`–`pat-0075` (4 record)
- `pat-0078` (1 record)
- `pat-0083`–`pat-0084` (2 record)
- `pat-0087` (1 record)

Total REVIEW: 64 + 2 + 4 + 1 + 2 + 1 = **74 record**.

## 3. Catatan pemeriksaan lanjutan

1. **pat-0003 — permintaan bantuan.** Struktur mencantumkan slot subjek, tetapi beberapa contoh imperatif seperti “Tolong jelaskan bagian ini” memiliki subjek orang kedua yang tersirat. Pastikan panduan pola menyatakan bahwa subjek dapat dihilangkan/tersirat.
2. **pat-0064 — pertanyaan dengan siapa.** Struktur ringkas “Siapa + ...” perlu mencakup bentuk berpreposisi seperti “Dengan siapa kamu berdiskusi?” dan posisi kata tanya yang tidak selalu di awal kalimat.
3. **pat-0065 — mana.** Satu intent mencakup pilihan (`yang mana`) dan relasi lokasi/arah (`di/ke/dari mana`). Periksa apakah subpola tersebut perlu dipisahkan agar intent dan slot jawaban tidak terlalu luas.
4. **pat-0072 — kenapa.** Hubungan makna dengan `mengapa` tepat sebagai pertanyaan sebab; register percakapan perlu dipertahankan sebagai kecenderungan, bukan batas mutlak.
5. **pat-0073–pat-0074 — di/ke.** Periksa contoh negatif dan relasi gerak/lokasi agar contoh benar-benar membedakan lokasi statis dari tujuan gerak, bukan sekadar terasa kurang lazim.
6. **pat-0083–pat-0087 — kuantifikasi.** Periksa cakupan `banyak`, `sedikit`, `seluruh`, `setiap`, dan `sebagian`; hindari menganggap kuantor saling dapat menggantikan atau menetapkan proporsi yang tidak dinyatakan.
7. **pat-0088–pat-0092 — morfologi.** Kelulusan pola umum tidak menggantikan pemeriksaan valensi per leksem. Khusus `ter-` dan `-kan`, pertahankan catatan polisemi dan ketergantungan pada konstruksi.

Catatan di atas adalah agenda review, bukan penetapan REVISE. Jika pemeriksaan sumber atau contoh lanjutan membuktikan ada kesalahan, status dapat diperbarui pada dokumen audit terpisah setelah review Dola.

## 4. Rujukan

- TBBI Edisi Keempat (2017): https://repositori.kemendikdasmen.go.id/16351/1/Tata%20Bahasa%20Baku%20Bahasa%20Ind.pdf
- EYD V — Kata Turunan: https://ejaan.kemendikdasmen.go.id/eyd/penulisan-kata/kata-turunan/
- Petunjuk Praktis Berbahasa Indonesia: https://repositori.kemendikdasmen.go.id/3420/1/Petunjuk%20praktis%20berbahasa%20indonesia.pdf
- Grangé (2010), *Aspect and modality in Indonesian: The case of sudah, telah, pernah and sempat*: https://doi.org/10.17510/wacana.v12i2.117

## 5. Batas kesimpulan

- 90 record sudah diinventarisasi dan dibaca dalam 18 file JSONL.
- PASS hanya diberikan pada 16 record dengan bukti pemeriksaan spesifik terdahulu.
- 74 REVIEW menunggu pemeriksaan lebih dalam; bukan berarti salah.
- 0 REVISE berarti belum ada kesalahan substansial yang cukup terbukti pada pemeriksaan ini, bukan jaminan seluruh pola sempurna.
- Seluruh record tetap DRAFT; tidak ada JSONL yang diedit.
- Pilar B belum final sampai seluruh REVIEW dituntaskan atau diterima sebagai batas audit yang eksplisit oleh Dola.
- Pilar C–E belum diaudit pada pekerjaan ini.
- Pemisahan Evaluation Dev/Validation/Final-Test tetap tahap tersendiri; Final-Test tidak boleh dipakai untuk tuning.
