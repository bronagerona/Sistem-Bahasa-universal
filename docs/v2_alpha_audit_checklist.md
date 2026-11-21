# Checklist Audit ILIS v2.0-alpha

> **Tujuan:** menyiapkan audit teknis V2 Alpha sebelum keputusan kelanjutan menuju V2 Beta.
>
> **Batas tugas dokumen ini:** checklist dan rencana audit saja. Pembuatan dokumen ini tidak mengubah kode, tidak menjalankan pengujian baru, tidak mengubah tag rilis, dan tidak menggabungkan PR.

## Metadata audit

| Properti | Nilai |
|---|---|
| Repository | `bronagerona/Sistem-Bahasa-universal` |
| Branch audit | `ilis-v2-development` |
| Rilis acuan | `v2.0-alpha` |
| PR | [#2](https://github.com/bronagerona/Sistem-Bahasa-universal/pull/2) — masih Draft |
| Baseline branch saat dokumen dibuat | `33e77a661480bb4b66a68c8c4ac4db98ad0dc7c5` |
| Branch `main` | Tidak disentuh |
| Status audit | Belum dilakukan; dokumen ini adalah daftar kerja |

## Cara menggunakan checklist

Status yang digunakan:

- **Belum diaudit** — pemeriksaan belum dilakukan.
- **Terverifikasi CI** — ada hasil GitHub Actions yang tercatat, tetapi belum otomatis membuktikan seluruh edge case.
- **Lulus audit** — pemeriksaan manual/otomatis khusus sudah dilakukan dan bukti dicatat.
- **Perlu perbaikan** — ditemukan masalah yang perlu ditangani.
- **N/A** — tidak relevan, dengan alasan dicatat.

Jangan mengubah status menjadi **Lulus audit** hanya karena tes umum berhasil. Catat bukti berupa nama tes, tautan workflow, commit, langkah reproduksi, dan hasil aktual.

## 1. Arsitektur & kontrak

| Item | Status | Catatan |
|---|---|---|
| Semantic Engine mempertahankan kontrak V1.0 dengan tepat 12 field | Belum diaudit | Bandingkan nama field, tipe, nilai default, dan bentuk JSON dengan `docs/semantic_contract.md` versi kontrak 1.0. |
| Penambahan intent V2 tidak menghapus atau mengganti field Semantic V1 | Belum diaudit | Uji output untuk assertion lama serta intent question dan command. |
| Output Reasoning Engine tetap memiliki 6 field V1 | Belum diaudit | Verifikasi `conclusion`, `confidence_score`, `evidence`, `reasoning_type`, `reasons`, `uncertainty`; pastikan tidak ada perubahan bentuk yang mematahkan konsumen lama. |
| Reasoning V1 tetap menghasilkan tipe dan struktur data yang kompatibel | Belum diaudit | Bandingkan fixture/output V1 sebelum dan sesudah perubahan. |
| Pemanggilan `ILISCore()` tanpa argumen storage tetap berjalan | Belum diaudit | Pastikan in-memory tetap menjadi default dan tidak membuat file SQLite secara tidak sengaja. |
| Antarmuka/pemanggilan ILISCore lama tetap kompatibel | Belum diaudit | Periksa constructor, metode publik, nilai balik, exception, dan contoh penggunaan lama. |
| Storage SQLite bersifat opsional dan tidak menjadi dependensi wajib untuk mode in-memory | Belum diaudit | Pastikan import dan inisialisasi default tidak gagal bila SQLite tidak dipilih. |
| Kontrak antar Semantic → Reasoning → Generator konsisten | Belum diaudit | Periksa nama key, tipe, nilai kosong, intent tak dikenal, serta confidence/uncertainty. |
| Dokumentasi kontrak sesuai implementasi aktual | Belum diaudit | Cocokkan dokumentasi Semantic, Reasoning, Generator, dan README dengan kode. |

## 2. SQLite Persistensi

| Item | Status | Catatan |
|---|---|---|
| Validasi `db_path` menolak input yang tidak valid | Belum diaudit | Uji string kosong, whitespace, tipe selain path/string yang didukung, direktori sebagai path file, dan path dengan komponen traversal. Tetapkan kebijakan path relatif/absolut. |
| Kebijakan lokasi database aman dan terdokumentasi | Belum diaudit | Pastikan aplikasi tidak menulis ke lokasi sensitif atau lokasi tak terduga; dokumentasikan direktori kerja dan hak akses. |
| Query SQL memakai parameter binding | Belum diaudit | Audit seluruh pemanggilan sqlite3. Nilai dari pengguna harus dikirim sebagai parameter, bukan interpolasi/f-string ke SQL. |
| Nama tabel/kolom dinamis dibatasi atau di-whitelist | Belum diaudit | Parameter binding tidak dapat menggantikan identifier SQL; hindari identifier dinamis yang berasal dari input. |
| Tidak ada SQL Injection melalui fakta, provenance, sesi, atau memori | Belum diaudit | Uji payload kutip, komentar SQL, delimiter, dan string mirip perintah SQL sebagai data biasa. |
| Koneksi database ditutup melalui `ilis.close()` | Belum diaudit | Verifikasi API tersedia, aman dipanggil berulang, menutup seluruh koneksi/statement yang dimiliki, dan tidak merusak mode in-memory. |
| Perilaku setelah `close()` jelas | Belum diaudit | Tentukan apakah operasi berikutnya menolak dengan exception terkontrol atau membuka ulang koneksi; dokumentasikan dan uji. |
| File database rusak ditangani dengan aman | Belum diaudit | Uji file kosong, file berisi byte acak, database terpotong, dan database dengan skema tidak kompatibel. Hindari kehilangan data diam-diam. |
| Folder database tidak ada atau tidak memiliki izin tulis | Belum diaudit | Pastikan error informatif, tidak meninggalkan state setengah terinisialisasi, dan tidak membuat fallback tersembunyi. |
| Izin baca/tulis database ditangani | Belum diaudit | Uji read-only, permission denied, disk penuh bila lingkungan CI memungkinkan, dan kegagalan saat commit. |
| Transaksi dan rollback konsisten | Belum diaudit | Uji kegagalan di tengah penyimpanan beberapa record; pastikan tidak ada data parsial yang dianggap sukses. |
| Persistensi Knowledge facts dan provenance benar | Belum diaudit | Simpan, tutup, buat instance baru, muat ulang, lalu bandingkan isi dan relasi provenance. |
| Persistensi Episodic Memory benar setelah restart | Belum diaudit | Uji urutan sesi, data kosong, data besar, dan pemuatan ulang pada instance baru. |
| Penanganan konkurensi/koneksi ganda jelas | Belum diaudit | Uji dua instance atau proses yang mengakses file sama; tetapkan batas dukungan dan kebijakan timeout/locking. |
| Migrasi/perubahan skema database direncanakan | Belum diaudit | Periksa versi skema, strategi upgrade, dan perilaku saat membuka database dari versi ILIS berbeda. |
| Data sensitif tidak bocor melalui log/error | Belum diaudit | Pastikan pesan exception/log tidak mencetak isi memori atau fakta yang tidak perlu. |

## 3. Fitur-fitur baru V2

| Item | Status | Catatan |
|---|---|---|
| Semantic V2 mengenali pertanyaan sederhana | Belum diaudit | Uji pola dengan/tanpa kata tanya, tanda tanya hilang, variasi urutan kata, dan pertanyaan ambigu. |
| Semantic V2 mengenali perintah sederhana | Belum diaudit | Uji bentuk imperatif, subjek tersirat, objek opsional, dan frasa yang hanya tampak seperti perintah. |
| Semantic V2 menangani negasi | Belum diaudit | Uji `tidak`, `tak`, `nggak`, `belum`, `bukan`, negasi ganda, cakupan negasi, dan posisi negasi. |
| Semantic V2 mempertahankan fallback low-confidence/unsupported | Belum diaudit | Pastikan input di luar cakupan tidak dipaksakan menjadi intent/relasi yang keliru. |
| Semantic V2 tidak salah mengklasifikasikan frasa nominal/verb awal sebagai command | Belum diaudit | Uji contoh seperti “Makan nasi” dalam konteks berbeda. |
| Ekspresi waktu dan lokasi tidak salah batas | Belum diaudit | Uji “setiap pagi”, “pagi ini”, “besok malam”, nama tempat, dan frasa yang tumpang tindih. |
| Reasoning V2 menyimpulkan skenario naga-lonceng sesuai bukti | Belum diaudit | Pastikan dua premis yang diperlukan hadir; uji jika salah satu premis hilang atau berubah. |
| Reasoning V2 mendukung jawaban dari input Semantic question | Belum diaudit | Uji pertanyaan yang dapat dijawab, tidak dapat dijawab, dan predikat yang belum dipetakan. |
| Reasoning membedakan question, command, dan assertion | Belum diaudit | Pastikan command tidak dijawab seolah-olah pertanyaan dan assertion tidak diperlakukan sebagai instruksi. |
| Reasoning mempertahankan evidence dan uncertainty | Belum diaudit | Cocokkan bukti dengan fakta sumber; uji confidence rendah, fakta konflik, dan data kosong. |
| Reasoning menangani fakta tidak diketahui/bertentangan | Belum diaudit | Tidak boleh mengarang kesimpulan positif saat status unknown atau conflicting. |
| Generator menjawab pertanyaan dengan benar | Belum diaudit | Uji jawaban benar, unknown, conflicting, confidence rendah, dan input yang tidak lengkap. |
| Generator memberi respons untuk perintah | Belum diaudit | Pastikan respons adalah acknowledgement, bukan klaim bahwa aksi eksternal benar-benar telah dilakukan. |
| Generator menghasilkan tiga register untuk skenario naga-lonceng | Belum diaudit | Verifikasi formal, informal, dan slang berbeda secara wajar tetapi mempertahankan makna inti. |
| Generator mempertahankan ketidakpastian sesuai confidence | Belum diaudit | Uji batas confidence dan metadata uncertainty; jangan menyajikan hipotesis sebagai kepastian. |
| Generator mempertahankan kontrak output V1 | Belum diaudit | Pastikan key output lama tetap ada dan bentuk nilainya kompatibel. |
| Variasi bahasa tidak mengubah makna semantik inti | Belum diaudit | Uji parafrasa/variasi register dengan hasil reasoning yang ekuivalen. |

## 4. Benchmark & Test Suite

| Item | Status | Catatan |
|---|---|---|
| GitHub Actions menjalankan suite yang mencakup 113 tes | Terverifikasi CI | Catatan CI terakhir: run [44286312620](https://github.com/bronagerona/Sistem-Bahasa-universal/actions/runs/44286312620), 113 collected, 113 passed. Ulangi pada commit audit terbaru sebelum menyatakan audit final. |
| Penemuan file benchmark oleh pytest benar | Terverifikasi CI | `pyproject.toml` memasukkan `benchmark_v2_suite.py` ke pola penemuan tes; pastikan tetap demikian. |
| Benchmark pertanyaan sederhana berjalan end-to-end | Terverifikasi CI | Termasuk dalam enam skenario benchmark; audit kualitas assertion dan variasi input secara terpisah. |
| Benchmark perintah sederhana berjalan end-to-end | Terverifikasi CI | Termasuk dalam enam skenario benchmark; periksa bahwa respons tidak mengklaim aksi sungguhan. |
| Benchmark skenario api–kayu–rumah berjalan end-to-end | Terverifikasi CI | Termasuk dalam enam skenario benchmark; periksa premis, kesimpulan, dan bukti. |
| Benchmark skenario naga–lonceng berjalan end-to-end | Terverifikasi CI | Termasuk dalam enam skenario benchmark; periksa juga kasus premis hilang/konflik secara manual. |
| Benchmark SQLite save/restart/reload berjalan end-to-end | Terverifikasi CI | Termasuk dalam enam skenario benchmark; perlu perluasan ke file rusak, permission, dan transaksi gagal. |
| Seluruh 107 tes lama tetap lulus bersama benchmark baru | Terverifikasi CI | Run terakhir mencatat 113/113 lulus; 107 tes lama + 6 benchmark. |
| Tes gagal bila benchmark tidak ditemukan pytest | Belum diaudit | Uji konfigurasi discovery agar penghilangan benchmark tidak menghasilkan CI hijau palsu. |
| Edge case Semantic dan Reasoning ditambahkan ke suite | Belum diaudit | Lihat daftar skenario belum diuji di bawah. |
| Edge case SQLite dan lifecycle koneksi ditambahkan ke suite | Belum diaudit | Khususnya close, reopen, corrupt DB, permission, rollback, dan concurrent access. |
| Hasil CI terbaru dilampirkan pada keputusan rilis Beta | Belum diaudit | Catat URL run, SHA commit, jumlah collected/passed/skipped/failed, dan versi Python/dependensi. |

### Skenario yang belum tercakup atau perlu dikonfirmasi melalui audit manual

Daftar berikut adalah kandidat pemeriksaan tambahan, bukan klaim bahwa seluruhnya pasti belum ada di semua tes.

**Semantic / bahasa**
- Input kosong, hanya spasi, tanda baca saja, emoji, angka, dan campuran angka-teks.
- Typo berat, pengulangan huruf, singkatan, slang, variasi kapitalisasi, dan token tidak dikenal.
- Negasi ganda atau bertingkat: “tidak mungkin tidak…”, “belum tentu…”, “bukan tidak…”.
- Perbedaan cakupan negasi: “Naga tidak takut lonceng” vs “Naga takut bukan lonceng”.
- Pertanyaan tanpa tanda tanya, pertanyaan retoris, pertanyaan multi-klausa, dan pertanyaan dengan kata tanya yang ambigu.
- Perintah sopan/tidak langsung, larangan, perintah negatif, dan kalimat deklaratif yang diawali kata kerja.
- Frasa waktu relatif, rentang waktu, lokasi multi-kata, dan urutan waktu/lokasi yang bervariasi.
- Kalimat panjang, banyak subjek/objek, koordinasi, dan ambiguitas struktur.
- Campur kode Indonesia–Inggris serta istilah game/nama entitas yang tidak dikenal.

**Reasoning / Generator**
- Salah satu premis naga-lonceng hilang, duplikat, terbalik, atau bertentangan.
- Dua atau lebih fakta mendukung kesimpulan berbeda.
- Confidence tepat di sekitar ambang keputusan dan evidence kosong/tidak lengkap.
- Pertanyaan yang membutuhkan inferensi berantai atau jawaban di luar rule base.
- Command yang tidak dikenali, command berbahaya/tidak didukung, dan acknowledgement tanpa eksekusi aksi.
- Register formal/informal/slang untuk input typo, kalimat negatif, dan hasil unknown/conflicting.
- Konsistensi makna dan metadata antar tiga register.

**SQLite / lifecycle**
- Path relatif vs absolut, symlink, path traversal, path dengan karakter khusus, dan lokasi di luar direktori kerja.
- Database rusak, terpotong, skema lama/baru, file terkunci, read-only, folder hilang, dan disk penuh.
- Pemanggilan `close()` dua kali, operasi setelah close, inisialisasi gagal, dan cleanup saat exception.
- Kegagalan commit di tengah operasi, rollback, dan pemulihan setelah proses berhenti mendadak.
- Dua instance/proses menulis bersamaan, pembacaan saat penulisan, dan batas timeout.
- Data besar, teks Unicode/emoji, string mirip SQL, nilai null/kosong, serta duplikasi record.

## Risiko yang teridentifikasi / perlu divalidasi

Risiko di bawah adalah **area risiko audit**, bukan temuan kerentanan yang sudah terbukti. Belum ada perubahan kode atau audit keamanan pada tugas ini.

1. **Path database tidak tervalidasi secara ketat** — dapat menyebabkan database dibuat di lokasi tak diinginkan, kegagalan izin, atau perilaku berbeda antar lingkungan.
2. **SQL dibangun melalui interpolasi string** — berpotensi SQL Injection jika nilai data atau identifier tidak dibatasi. Pastikan parameter binding digunakan untuk semua nilai.
3. **Lifecycle koneksi tidak eksplisit** — koneksi yang tidak ditutup dapat mengunci file, membocorkan resource, atau membuat hasil flush tidak pasti.
4. **Kegagalan database tidak pulih dengan jelas** — file korup, skema tidak cocok, atau permission denied dapat menyebabkan kehilangan data atau state parsial.
5. **Transaksi dan konkurensi belum dibuktikan** — beberapa instance/proses dapat menghasilkan lock, overwrite, atau data parsial.
6. **Kontrak lintas-engine dapat bergeser** — perubahan intent/field/tipe dapat merusak konsumen V1 meskipun tes internal lulus.
7. **Rule-based coverage terbatas** — variasi bahasa Indonesia, typo, ambiguitas, negasi, dan kalimat panjang berisiko salah dipahami.
8. **Generasi jawaban terlalu yakin** — confidence/uncertainty yang tidak dipertahankan dapat menyajikan hipotesis sebagai fakta.
9. **Acknowledgement command disalahartikan sebagai eksekusi** — generator hanya menyusun respons; integrasi aksi game/chatbot harus mengonfirmasi aksi secara terpisah.
10. **Benchmark terlalu sempit** — enam skenario end-to-end dan 113 tes yang lulus belum membuktikan ketahanan untuk semua variasi bahasa atau beban produksi.

## Rekomendasi perbaikan untuk V2 Beta

Prioritas berikut adalah rekomendasi; implementasi ditunda sampai audit selesai dan disetujui.

### P0 — Keamanan dan keandalan storage
- Audit semua query sqlite3; wajib gunakan parameter binding untuk nilai dan whitelist untuk identifier.
- Terapkan validasi path database, kebijakan direktori, serta pesan error yang aman dan informatif.
- Pastikan API `close()` menutup koneksi secara deterministik; tentukan perilaku operasi setelah close.
- Tambahkan tes untuk corrupt DB, permission denied, folder tidak ada, rollback, dan kegagalan inisialisasi.
- Tetapkan strategi transaksi, locking, timeout, dan dukungan multi-instance.

### P1 — Kontrak dan kompatibilitas
- Buat golden tests untuk output Semantic 12-field, Reasoning 6-field, dan output Generator V1.
- Tambahkan tes kompatibilitas yang memanggil `ILISCore()` tanpa argumen dan seluruh pola penggunaan lama.
- Validasi skema output lintas engine secara eksplisit, termasuk tipe data dan fallback.
- Jadikan perubahan kontrak sebagai perubahan versi yang disengaja dan terdokumentasi.

### P1 — Kualitas bahasa dan reasoning
- Perluas corpus uji Indonesia formal, santai, gaul, singkatan, typo, negasi, dan kalimat ambigu.
- Tambahkan uji negatif untuk mencegah false positive intent question/command.
- Tambahkan uji konflik, premis hilang, evidence tidak lengkap, dan confidence rendah.
- Definisikan batas kemampuan V2 Beta dengan jelas; gunakan fallback daripada mengarang interpretasi.

### P2 — Generator dan integrasi
- Uji kesetaraan makna formal/informal/slang dengan golden examples.
- Bedakan respons acknowledgement dari status eksekusi aksi game atau chatbot.
- Pastikan metadata confidence, evidence, dan uncertainty konsisten di semua register.
- Tambahkan contoh integrasi yang menunjukkan penanganan unknown, conflicting, dan unsupported.

### P2 — Benchmark dan kualitas rilis
- Tambahkan benchmark variasi bahasa, regresi V1, dan edge case storage.
- Catat metrik selain pass/fail: akurasi intent, false-positive command, ketepatan fallback, konsistensi output, dan latensi.
- Jalankan CI pada setiap perubahan branch dan simpan tautan run serta SHA commit.
- Tetapkan kriteria penerimaan Beta: tidak ada regresi kontrak, seluruh tes wajib lulus, dan temuan P0 ditutup.

## Hasil audit dan keputusan

Isi bagian ini setelah audit benar-benar dilakukan.

| Area | Hasil | Bukti / issue | Pemilik | Tanggal |
|---|---|---|---|---|
| Arsitektur & kontrak | Belum dinilai | — | — | — |
| SQLite persistensi | Belum dinilai | — | — | — |
| Fitur Semantic V2 | Belum dinilai | — | — | — |
| Fitur Reasoning V2 | Belum dinilai | — | — | — |
| Language Generator V2 | Belum dinilai | — | — | — |
| Benchmark & CI | Sebagian terverifikasi | [CI run 44286312620](https://github.com/bronagerona/Sistem-Bahasa-universal/actions/runs/44286312620) | — | — |

**Keputusan V2 Beta:** Belum diputuskan.

**Catatan penting:** dokumen ini hanya menyiapkan checklist audit. Branch `main` tidak diubah; PR #2 tetap Draft dan belum digabung.
