# ILIS PROJECT STATE — DOKUMEN INDUK SUMBER KEBENARAN PROYEK
> Versi: v1.0
> Tanggal: 19 Nov 2026
> Branch Acuan Utama: ilis-v2-development
> Commit SHA Acuan: 32903039f448a2427ee64cfa3a99c6dc9a2854ef
> Status Rilis: v3.1-beta (PRE-RELEASE / BELUM STABIL)

## 🧑‍🤝‍🧑 STRUKTUR & PERAN TIM
### 👑 Pemilik Proyek (Kamu)
- Pengambil keputusan AKHIR semua hal proyek
- Menyetujui perubahan kode, perubahan dokumen, jadwal rilis
- Menentukan prioritas backlog

### 🧾 Evaluator (Dola)
- Memeriksa kesesuaian pekerjaan terhadap dokumen induk ini
- Mengidentifikasi risiko teknis
- Review usulan perbaikan / perubahan dari Eksekutor
- Memverifikasi hasil pengujian sebelum persetujuan ke Pemilik Proyek

### ⚙️ Eksekutor Teknis (ChatGPT)
- Implementasi kode, kelola GitHub, Workflow CI / Playground
- Membuat draf perubahan untuk dokumen ini
- Jalankan semua rangkaian pengujian
- Kirim laporan status berkala ke Evaluator + Pemilik Proyek
- ❗ DILARANG commit perubahan kode / dokumen sebelum persetujuan penuh

## 📐 ARSITEKTUR + KONTRAK YANG TIDAK BOLEH DIUBAH (KECUALI ADA PERSETUJUAN TERTULIS DARI PEMILIK PROYEK)
✅ Semantic 12 fields
✅ Reasoning 6 keys
✅ Perilaku inti Commit A (Assertion: api menyentuh rumah kayu → TIDAK langsung disimpulkan kebakaran)
✅ Perilaku inti Commit B (Prefix identitas hanya muncul pada Identity Intent)
✅ Hotfix Greeting PR #18 (Sapaan alami tanpa prefix identitas)
✅ Status XFAIL non-strict untuk `tests/beta_suite.py` (JANGAN dihapus / diubah sekarang)
✅ Multi-turn in-memory (BUKAN persistent storage)

## ✅ DAFTAR PR YANG SUDAH MERGED
1. PR #16 → Commit A (Assertion)
2. PR #17 → Commit B (Prefix identitas)
3. PR #18 → Hotfix Greeting

## 🧪 HASIL PENGUJIAN TERVERIFIKASI + LINK
- CI Utama: 313 passed + 1 XFAIL
- Playground #34: Halo apa kabar? → Greeting lulus
- Playground #35: Siapa kamu? → Identity Intent lulus
- Playground #36: Api menyentuh rumah kayu → Assertion lulus
- Extended Playground Run #4 A-E: Semua skenario A/B/C/D/E lulus
> Link-link lengkap tersimpan di `docs/audit_report_v3.1_beta.md`

## 🤝 DAFTAR KEPUTUSAN YANG SUDAH DISEPAKATI
✅ Pertahankan v3.1-beta sebagai Pre-Release
✅ Masa pemantauan Beta aktif, kumpulkan bug dulu sebelum perbaikan
✅ Jangan ubah `beta_suite.py` untuk saat ini
✅ Dilarang menambahkan fitur besar baru selama masa Beta
✅ Dokumen ini adalah satu-satunya sumber kebenaran utama proyek

## 📋 BACKLOG / PEKERJAAN YANG DITUNDA (Dikerjakan SETELAH masa Beta selesai)
1. Perbaikan tes XFAIL `beta_suite.py`
2. Persistent Session Multi-Turn (riwayat percakapan permanen)
3. Perluasan seed Concept Engine untuk mode produksi

## ⚠️ DAFTAR BATASAN SISTEM V3.1-BETA
- Multi-turn hanya in-memory (hilang setelah restart)
- Satu tes lama berstatus XFAIL non-strict
- Belum teruji beban percakapan panjang yang berhari-hari
- Belum teruji secara luas variasi bahasa gaul / kalimat acak dari penguji luar

## 📝 PROSEDUR PERUBAHAN DOKUMEN INI
1. Eksekutor buat usulan perubahan teks
2. Kirim ke Evaluator (Dola) untuk diperiksa
3. Diteruskan ke Pemilik Proyek untuk persetujuan
4. Baru di-commit ke repo
5. Setiap perubahan dicatat di riwayat bawah halaman

## 📜 RIWAYAT DOKUMEN
- v1.0 (19-11-2026): Dokumen induk pertama kali dibuat
