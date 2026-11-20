# BL-ILIS-002 — Laporan Implementasi Eksperimental v0.1

- Branch: implement-bl-ilis-002-negation-mapping
- Basis: ilis-v2-development @ 759b4684bcc453eb5c2087724d084c2a0950427b
- Head terverifikasi: 71d8f58920ef4ca595d4e4827c431fc65126e4a4
- Status: IMPLEMENTASI EKSPERIMENTAL — MENUNGGU REVIEW DOLA
- Sumber desain: docs/bl_ilis_002_negation_mapping_spec.md
- CI: [GitHub Actions #44722629934](https://github.com/bronagerona/Sistem-Bahasa-universal/actions/runs/44722629934)

## 1. Cakupan implementasi

Interpreter enam label ditambahkan di src/ilis/experimental/negation_mapping.py dan sengaja tidak dihubungkan ke SemanticEngine, ChatbotAdapter, ReasoningEngine, SQLite, atau runtime produksi.

Label yang didukung:
- none
- negative
- not_yet
- identity_negative
- prohibitive
- ambiguous

Trace diagnostik mengembalikan boolean sumber, cue terdeteksi, scope, label, alasan, confidence, dan status discrepancy. Fungsi baseline legacy PR #20 disertakan untuk pembanding.

## 2. Integritas inventaris dan sumber

| Pemeriksaan | Hasil |
|---|---:|
| File Dialogues | 18 |
| Record/dialogue | 88 |
| Turn | 205 |
| Anotasi Negation | 205 |
| Boolean sumber true | 2 |
| Boolean sumber false | 203 |
| Anotasi hilang/tidak valid | 0 |
| Perubahan byte JSONL sebelum/sesudah tes | 0 |

Seluruh 18 file dibaca sebagai read-only. Tes menyimpan byte sumber sebelum pemindaian dan membandingkannya kembali setelah pemetaan. Semua 205 nilai sumber tetap boolean dan identik.

## 3. Distribusi hasil enam label

| Label hasil | Jumlah |
|---|---:|
| none | 166 |
| negative | 13 |
| not_yet | 16 |
| identity_negative | 2 |
| prohibitive | 2 |
| ambiguous | 6 |
| **Total** | **205** |

Distribusi ini merupakan keluaran interpreter eksperimental, bukan gold label linguistik dan bukan promosi status dataset.

## 4. Perbandingan dengan baseline legacy PR #20

- Perubahan label dibanding baseline: 37 anotasi.
- Discrepancy boolean-vs-teks: 37 anotasi.
- Semua 37 discrepancy berasal dari boolean sumber false yang memiliki cue negasi fungsional pada ujaran.
- Dua anotasi dengan boolean true tetap dipetakan not_yet berdasarkan cue belum.
- Tidak ada boolean sumber yang dikoreksi atau ditulis ulang.

Daftar 37 discrepancy (dialogue/turn):
- dlg-0003: 1, 3
- dlg-0004: 2
- dlg-0007: 2
- dlg-0009: 2
- dlg-0013: 3
- dlg-0017: 1
- dlg-0018: 3
- dlg-0019: 2
- dlg-0020: 2
- dlg-0021: 1, 2
- dlg-0024: 1, 2
- dlg-0025: 3
- dlg-0026: 3
- dlg-0027: 2
- dlg-0029: 1, 2
- dlg-0033: 1, 2
- dlg-0034: 2
- dlg-0039: 2
- dlg-0040: 2
- dlg-0046: 1, 2
- dlg-0047: 1, 2
- dlg-0048: 1
- dlg-0049: 1, 2
- dlg-0050: 1, 2
- dlg-0053: 2
- dlg-0057: 1
- dlg-0063: 2
- dlg-0064: 1

## 5. Kasus ambiguous untuk review linguistik

Enam kasus dipertahankan sebagai ambiguous, bukan dipaksa menjadi label pasti:
- dlg-0007 turn 2 — “Tidak apa-apa...” (ungkapan idiomatis/pragmatis)
- dlg-0021 turn 1 — “jadwalku belum pasti” (epistemik)
- dlg-0027 turn 2 — “belum tentu...” (epistemik)
- dlg-0034 turn 2 — “belum tentu...” (epistemik)
- dlg-0047 turn 2 — negasi identitas dan temporal dalam satu ujaran; scope gabungan belum aman
- dlg-0057 turn 1 — belum dan tidak dalam konstruksi dengan scope yang berinteraksi

Confidence seluruh hasil ambiguous dibatasi maksimum 0.49.

## 6. Regresi cue penting

- Belum temporal terdeteksi termasuk pada boolean sumber false; discrepancy dicatat, sumber tidak diubah.
- Belum tentu tidak otomatis menjadi not_yet; dua kasus epistemik tetap ambiguous.
- Jangan → prohibitive (dlg-0049 turn 1).
- Tidak boleh → prohibitive (dlg-0049 turn 2).
- Bukan kakakku dikenali sebagai identity_negative (dlg-0047 turn 1).
- Kata negasi yang hanya disebut di dalam kutipan tidak diperlakukan sebagai negasi fungsional.
- Boleh tanpa negator tidak diperlakukan sebagai cue negasi.

## 7. Hasil CI dan batas klaim

GitHub Actions #44722629934: **339 passed, 1 xfailed**. Satu XFAIL adalah kasus beta lama yang telah terdokumentasi sebelumnya; bukan kegagalan BL-ILIS-002.

Tes BL-ILIS-002:
- unit tests untuk enam label dan fallback;
- input validation;
- baseline legacy;
- inventarisasi 18 file, 88 dialog, 205 turn/anotasi;
- pemeriksaan immutability JSONL;
- pencatatan distribusi label, perubahan baseline, discrepancy, dan kasus ambiguous.

Batas interpretasi:
1. Tidak ada gold label independen untuk 205 anotasi; hasil ini memvalidasi perilaku interpreter, bukan kebenaran linguistik semua record.
2. Seluruh 88 sesi dipindai berurutan dengan prior-turn context; tidak ada negasi yang diwariskan otomatis dari turn sebelumnya.
3. Ini bukan integrasi ke Semantic 12 fields. Kontrak runtime dan Reasoning 6 keys tidak diubah atau diperluas dalam PR ini.
4. Semua record dataset tetap DRAFT.
5. Tidak ada perubahan JSONL, production runtime, SQLite, workflow, atau main.
6. Belum ada staging atau integrasi dataset.

## 8. Keputusan yang diminta dari Dola

Mohon review:
- ketepatan enam label dan prioritas aturan;
- 37 discrepancy boolean-vs-teks;
- enam kasus ambiguous;
- cakupan cue jangan, tidak boleh, belum, dan bukan;
- kecukupan tes serta batas isolasi dari runtime produksi.

**Status BL-ILIS-002:** implementasi interpreter eksperimental dan regresi teknis 205 anotasi selesai pada PR ini; backlog belum boleh dinyatakan selesai final sampai Dola menerima hasil dan Owner menentukan tahap berikutnya.
