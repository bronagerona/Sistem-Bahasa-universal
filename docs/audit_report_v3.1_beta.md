# Laporan Audit Final ILIS V3.1-Beta

**Status dokumen:** Disahkan  
**Status rilis:** Pre-release Beta (dipertahankan; belum menjadi rilis stabil)  
**Repository:** `bronagerona/Sistem-Bahasa-universal`  
**Branch basis audit:** `ilis-v2-development`  
**Commit basis audit:** `32903039f448a2427ee64cfa3a99c6dc9a2854ef`  
**Tag rilis:** `v3.1-beta`

## 1. Ringkasan kesimpulan

ILIS V3.1-Beta layak dipertahankan sebagai **Pre-release Beta**. Bukti pengujian mendukung perilaku inti yang menjadi sasaran audit. Rilis tidak perlu terburu-buru dinaikkan menjadi rilis stabil.

Bukti utama:
- Manual Playground Run #34–#36 lulus.
- Multi-Turn Playground Run #3 lulus.
- CI PR #18 Run #223: **313 passed + 1 xfailed** (314 tes terkumpul).
- Regression smoke tests mencakup Concept PARTIAL/UNKNOWN, persona Mode B/C, register formal/informal, dan reset sesi.
- PR V3-A sampai greeting hotfix (#12–#18) telah ter-merge ke `ilis-v2-development`.

Audit ini tidak menyatakan seluruh skenario telah diverifikasi manual. Keterbatasan dan celah bukti dicatat pada Bagian 5.

## 2. Bukti pengujian

### 2.1 Manual Playground: greeting, identity, assertion

| Run | Input | Hasil aktual | Metadata / pemeriksaan | Status |
|---|---|---|---|---|
| [#34](https://github.com/bronagerona/Sistem-Bahasa-universal/actions/runs/44455060424) | `Halo, apa kabar?` | `Halo! Saya siap membantu. Bagaimana kabar Anda?` | `reasoning_type=greeting`, `semantic_status=supported`; tanpa prefix identitas | Lulus |
| [#35](https://github.com/bronagerona/Sistem-Bahasa-universal/actions/runs/44455187890) | `Siapa kamu?` | Diawali `Saya ILIS, sistem kecerdasan bahasa.` | `reasoning_type=identity_intent` | Lulus |
| [#36](https://github.com/bronagerona/Sistem-Bahasa-universal/actions/runs/44455295787) | `Api menyentuh rumah kayu` | `Baik, saya sudah memahami pernyataanmu` | `reasoning_type=assertion`, `semantic_status=supported`; tidak menyimpulkan kebakaran dan tanpa prefix identitas | Lulus |

Ketiga run memeriksa checkout branch `ilis-v2-development` pada commit audit `32903039f448a2427ee64cfa3a99c6dc9a2854ef`.

### 2.2 Multi-turn Playground

[Run #3 — Multi-Turn Playground](https://github.com/bronagerona/Sistem-Bahasa-universal/actions/runs/44456727791)

| Turn | Input | Jawaban aktual | Metadata |
|---|---|---|---|
| 1 | `Apakah api bisa membakar kayu?` | `Ya, kemungkinan api bisa membakar kayu.` | `context_turns_used=0` |
| 2 | `Lalu apakah api juga bisa membakar kertas?` | `Ya, kemungkinan juga bisa membakar kertas.` | `context_turns_used=1`, `reasoning_type=verified_inference`, evidence `fact_3` |

Pemeriksaan memastikan session ID tetap sama, dua turn tersimpan dalam sesi yang sama, dan hasil `MULTI-TURN CHECK: PASS`.

### 2.3 CI dan regression smoke tests

[PR #18 — CI Run #223](https://github.com/bronagerona/Sistem-Bahasa-universal/actions/runs/44454635165)

- 314 tes terkumpul.
- **313 passed, 1 xfailed**.
- Empat regression smoke tests tambahan lulus:
  1. Concept Engine PARTIAL/UNKNOWN.
  2. Multi-turn, Identity Intent, dan reset sesi.
  3. Register formal/informal.
  4. Persona Mode B dan Mode C.

Pengujian kontrak juga memeriksa Semantic 12 fields dan Reasoning 6 keys.

### 2.4 Skenario Concept Engine

Regression smoke test menguji kondisi dengan `ILISCore(seed_core_knowledge=False)`:
- PARTIAL: reasoning bertipe `concept_inference_partial`; `generation.uncertainty_preserved=true`; jawaban mempertahankan penanda bahwa informasi belum lengkap dan hasil hanya dugaan.
- UNKNOWN: reasoning bertipe `concept_inference_unknown`; jawaban menyatakan informasi belum cukup untuk memastikan.

Hasil ini berasal dari regression smoke test, bukan dari manual Playground dengan konfigurasi default.

### 2.5 Persona dan register

Regression smoke tests PR #18 mencakup:
- Mode B: identitas aplikasi/narator digunakan.
- Mode C: identitas NPC digunakan.
- Register formal: respons diawali gaya formal, termasuk `Dengan senang hati,`.
- Register informal: respons menggunakan gaya informal, termasuk `Iya, kayaknya`.

## 3. Audit kontrak teknis

| Kontrak / perilaku | Hasil |
|---|---|
| Semantic 12 fields | Dipertahankan dan diperiksa dalam tes |
| Reasoning 6 keys | Dipertahankan dan diperiksa dalam tes |
| KnowledgeEngine | Prioritas fakta lama tercakup dalam regression smoke test |
| Concept Engine | PARTIAL dan UNKNOWN tercakup dalam regression smoke test |
| Multi-turn | Dua pesan menggunakan session ID yang sama |
| Identity Intent | Prefix ILIS muncul pada permintaan identitas |
| Greeting | Sapaan alami tanpa prefix identitas |
| Assertion | Pernyataan sentuhan tidak diubah menjadi kesimpulan kebakaran |
| Persona Mode B/C | Identitas aplikasi dan NPC tercakup dalam regression smoke test |
| Register | Formal dan informal tercakup dalam regression smoke test |
| Session reset | Tercakup dalam regression smoke test |

### Riwayat integrasi

| Komponen / tahap | PR | Status |
|---|---:|---|
| V3-A | #12 | Merged |
| V3-B | #13 | Merged |
| V3-C | #14 | Merged |
| LanguageGenerator Concept status | #15 | Merged |
| V3.1 Commit A | #16 | Merged |
| V3.1 Commit B | #17 | Merged |
| Greeting hotfix | #18 | Merged |

## 4. Checklist akhir

### Perilaku
- [x] Greeting alami tanpa prefix identitas.
- [x] Identity Intent dengan prefix ILIS.
- [x] Assertion tanpa inferensi kebakaran.
- [x] Multi-turn dua pesan dalam sesi yang sama.
- [x] Concept PARTIAL.
- [x] Concept UNKNOWN.
- [x] Persona Mode B.
- [x] Persona Mode C.
- [x] Register formal.
- [x] Register informal.
- [x] Reset sesi pada regression smoke test.

### Kontrak teknis
- [x] Semantic 12 fields diuji.
- [x] Reasoning 6 keys diuji.
- [x] Integrasi KnowledgeEngine diuji.
- [x] Integrasi Concept Engine diuji.
- [x] Persona dan Identity Intent diuji.
- [x] Regression suite PR #18: 313 passed + 1 xfailed.
- [ ] Extended Test Playground skenario A–E belum memperoleh hasil karena workflow berhenti sebelum skenario dijalankan.

## 5. Keterbatasan dan catatan transparansi

1. **Satu XFAIL lama:** `tests/beta_suite.py::test_beta_chatbot_full_pipeline_and_register`. Tes lama mengharapkan jawaban inferensi kebakaran untuk `Api menyentuh rumah kayu`, sedangkan perilaku assertion yang disepakati adalah pengakuan pernyataan tanpa inferensi kebakaran. Tes tetap dijalankan dan ditandai XFAIL pada CI yang dikonfigurasi.
2. **Extended Test Playground A–E:** Run #3 [gagal pada tahap regression suite](https://github.com/bronagerona/Sistem-Bahasa-universal/actions/runs/44456971992). Workflow menjalankan pytest tanpa konfigurasi XFAIL yang dipakai CI utama. Hasilnya 313 passed dan satu tes lama gagal; skenario A–E kemudian dilewati (skipped). Ini merupakan keterbatasan konfigurasi workflow dan berarti skenario A–E belum memiliki hasil dari run tersebut. Tidak boleh diklaim A–E lulus.
3. **Reset sesi:** Sudah tercakup dalam regression smoke test, tetapi belum diverifikasi lewat manual Playground terbaru.
4. **Concept PARTIAL/UNKNOWN:** Diuji dengan `seed_core_knowledge=False`, yaitu kondisi pengujian khusus. Hasil tersebut tidak membuktikan perilaku yang sama pada setiap konfigurasi seed default.
5. **Multi-turn bersifat in-memory:** Riwayat sesi tidak persisten setelah proses aplikasi dimulai ulang.
6. **Cakupan multi-turn manual:** Multi-Turn Playground Run #3 menguji dua pesan bebas dalam satu sesi; belum merupakan verifikasi manual penuh atas seluruh skenario Extended A–E.

## 6. Rencana setelah audit

### Jangka pendek — selama masa Beta
- Simpan dan pertahankan laporan audit ini sebagai arsip proyek.
- Pantau masukan dari penguji Beta.
- Jadwalkan penyesuaian tes lama/XFAIL untuk versi berikutnya; **jangan ubah sekarang sebagai bagian dari audit ini**.
- Jadwalkan penyelesaian dan verifikasi Extended Playground A–E pada pekerjaan audit berikutnya.

### Jangka panjang — menuju rilis stabil
- Implementasi persistent session untuk multi-turn.
- Perluasan seed ConceptEngine agar cakupan konsep KNOWN produksi lebih luas.
- Penanganan keterbatasan yang tercatat dalam laporan ini.
- Evaluasi ulang seluruh bukti sebelum menaikkan status ke rilis stabil.

## 7. Keputusan akhir

**ILIS V3.1-Beta LAYAK dipertahankan sebagai Pre-release Beta.**

Rilis `v3.1-beta` tetap berstatus Pre-release. Tidak ada keputusan untuk menaikkannya menjadi rilis stabil dalam audit ini.

Laporan ini mencatat hasil yang lulus sekaligus keterbatasan bukti secara transparan. Tidak ada perubahan kode, perubahan kontrak, PR, merge, atau penerbitan rilis baru yang dilakukan sebagai bagian dari penyusunan laporan ini.
