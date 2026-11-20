# Audit 448 Record — Pilar C: Dialogues

- **Basis branch:** `ilis-v2-development`
- **Basis SHA:** `8e92c2514f334a366135a107107c8c7d5842515b` (setelah merge PR #24)
- **Audit branch:** `audit-448-dialogues`
- **Cakupan:** 88 record (`dlg-0003`–`dlg-0090`), 18 file JSONL, 205 giliran.
- **Batas:** dokumentasi audit saja. Tidak mengubah JSONL, kode, tes, workflow, SQLite, atau `main`.
- **Status dataset:** semua record tetap DRAFT.

## 1. Ringkasan hasil audit awal

| Status audit | Jumlah | Arti |
|---|---:|---|
| PASS | 0 | Belum ada record yang cukup bukti untuk dinyatakan lolos seluruh pemeriksaan semantik, negasi, dan kesinambungan konteks. |
| REVISE | 0 | Belum menetapkan revisi dataset karena tahap ini dilarang mengubah JSONL dan setiap dugaan perlu review linguistik lebih lanjut. |
| REVIEW | 88 | Semua record telah diinventarisasi dan diperiksa secara struktural; pemeriksaan semantik penuh dan negation mapping per konteks belum tuntas. |

**REVIEW bukan berarti 88 dialog salah.** Ini status konservatif karena validitas struktur saja tidak cukup untuk PASS.

## 2. Pemeriksaan struktural yang telah dilakukan

- 18/18 file batch berhasil dibaca dan diparse sebagai JSONL.
- 88/88 record ditemukan, dari `dlg-0003` sampai `dlg-0090`.
- Total 205 giliran: 61 dialog dua giliran, 25 dialog tiga giliran, dan 2 dialog empat giliran.
- 205/205 anotasi memiliki tepat 12 key Semantic: Actor, Predicate, Patient/Object, Intent, Time, Aspect, Location, Recipient, Negation, Modality, Register, Confidence.
- 0 kegagalan struktur key Semantic.
- 0 rujukan `reference_to_previous_turn` yang menunjuk ke giliran yang tidak ada atau ke giliran yang sama/lebih baru.
- Pemeriksaan ini memvalidasi keberadaan dan bentuk field, bukan otomatis membuktikan ketepatan nilai Actor, Predicate, Intent, Time, Aspect, dan field lainnya.

## 3. Temuan penting — negasi perlu pemeriksaan lanjutan

Distribusi boolean sumber pada 205 giliran:
- `Negation: true` = 2
- `Negation: false` = 203

Pemeriksaan pemicu leksikal awal menemukan **37 giliran kandidat** yang memuat bentuk seperti `tidak`, `bukan`, `belum`, `jangan`, atau `tanpa`, sementara boolean sumbernya `false`.

Kandidat tersebut **belum otomatis dinyatakan salah**. Contohnya:
- `belum tentu` dapat menyatakan ketidakpastian, bukan `not_yet`.
- `bukan` bisa mengoreksi unsur atau kontras, dan labelnya bergantung pada scope.
- `tidak apa-apa` dapat menjadi ungkapan idiomatis.
- Penanda negasi dapat berada dalam klausa subordinat, kutipan, atau cakupan yang tidak sama dengan proposisi utama.

Karena itu, semua 37 kandidat harus diperiksa berdasarkan teks, scope, fungsi, dan konteks dialog sesuai spesifikasi `docs/bl_ilis_002_negation_mapping_spec.md`. Boolean JSONL tetap dipertahankan apa adanya. Jangan menulis label enam kategori ke JSONL.

Daftar kandidat untuk pemeriksaan negasi:
- `dlg-0003` turn 1, 3
- `dlg-0004` turn 2
- `dlg-0007` turn 2
- `dlg-0009` turn 2
- `dlg-0013` turn 3
- `dlg-0017` turn 1
- `dlg-0018` turn 3
- `dlg-0019` turn 2
- `dlg-0020` turn 2
- `dlg-0021` turn 1, 2
- `dlg-0024` turn 1, 2
- `dlg-0025` turn 3
- `dlg-0026` turn 3
- `dlg-0027` turn 2
- `dlg-0029` turn 1, 2
- `dlg-0033` turn 1, 2
- `dlg-0034` turn 2
- `dlg-0039` turn 2
- `dlg-0040` turn 2
- `dlg-0046` turn 1, 2
- `dlg-0047` turn 1, 2
- `dlg-0048` turn 1
- `dlg-0049` turn 1, 2
- `dlg-0050` turn 1, 2
- `dlg-0053` turn 2
- `dlg-0057` turn 1
- `dlg-0063` turn 2
- `dlg-0064` turn 1

## 4. Status per record

Semua record di bawah berstatus REVIEW sampai ketepatan semantik setiap giliran, negation scope, dan konteksnya diperiksa lebih lanjut.

| Record | Status | Catatan |
|---|---|---|
| dlg-0003 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0004 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0005 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0006 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0007 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0008 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0009 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0010 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0011 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0012 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0013 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0014 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0015 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0016 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0017 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0018 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0019 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0020 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0021 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0022 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0023 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0024 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0025 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0026 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0027 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0028 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0029 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0030 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0031 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0032 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0033 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0034 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0035 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0036 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0037 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0038 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0039 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0040 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0041 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0042 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0043 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0044 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0045 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0046 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0047 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0048 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0049 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0050 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0051 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0052 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0053 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0054 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0055 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0056 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0057 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0058 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0059 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0060 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0061 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0062 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0063 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0064 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0065 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0066 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0067 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0068 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0069 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0070 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0071 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0072 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0073 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0074 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0075 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0076 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0077 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0078 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0079 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0080 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0081 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0082 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0083 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0084 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0085 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0086 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0087 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0088 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0089 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |
| dlg-0090 | REVIEW | Pemeriksaan semantik penuh dan/atau negasi kontekstual belum dituntaskan. |

## 5. Cakupan review berikutnya

1. Periksa kesesuaian Actor, Predicate, Patient/Object, Intent, Time, Aspect, Location, Recipient, Modality, Register, dan Confidence dengan ujaran aktual.
2. Periksa kesinambungan referensi lintas giliran: koreksi, resolusi pronomina, perubahan topik, kembali ke topik, dan pembaruan informasi.
3. Audit 37 kandidat negasi secara kontekstual menggunakan enam label desain BL-ILIS-002: `none`, `negative`, `not_yet`, `identity_negative`, `prohibitive`, `ambiguous`.
4. Periksa dua boolean `true` dan pastikan bukti tekstual serta cakupannya mendukung anotasi.
5. Catat temuan substansial sebagai REVISE hanya setelah bukti jelas dan review; jangan mengubah JSONL dalam PR dokumentasi ini.

## 6. Batas dan keputusan

- Laporan ini adalah audit dokumentasi, bukan persetujuan final atas 88 record.
- Tidak ada perubahan pada file JSONL.
- Tidak ada perubahan `verification_status`; seluruh data tetap DRAFT.
- Tidak ada implementasi BL-ILIS-002 pada runtime.
- Tidak ada staging atau integrasi dataset ke produksi.
- Pilar C baru dapat ditutup setelah seluruh temuan kontekstual ditinjau dan Dola menerima hasilnya.
