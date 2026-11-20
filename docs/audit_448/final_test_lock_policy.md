# Kebijakan Penguncian Final-Test — ILIS Evaluation

> **Versi:** draf v0.1  
> **Status:** PROPOSAL — menunggu review Dola dan keputusan Owner  
> **Branch acuan:** `ilis-v2-development`  
> **Basis:** PR #31 merge `5bb83443517cae226a7490e075dfa9e81466efef`  
> **Cakupan:** tata kelola, pemisahan, pembekuan versi, akses, pembukaan, dan pelaporan Final-Test.  
> **Batas:** dokumen ini tidak mengunci dataset, tidak memindahkan record, tidak mengubah JSONL, dan tidak memberi izin staging atau integrasi.

## 1. Tujuan dan istilah

Kebijakan ini mencegah data Final-Test dipakai untuk pengembangan/tuning, menjaga integritas versi yang dievaluasi, dan memastikan hasil evaluasi dapat direproduksi.

Label `split: final_test` di JSONL **bukan** bukti bahwa suite sudah terkunci. Status lock harus dicatat terpisah dari `verification_status`.

Istilah status yang diusulkan:

- **CONCEPTUAL:** label split sementara; belum menjadi suite yang dapat dijalankan.
- **CANDIDATE:** record sudah dipilih untuk calon Final-Test, tetapi semua gerbang pra-lock belum lulus.
- **LOCKED-INTEGRITY:** isi dan versi dibekukan dengan manifest/checksum dan proses perubahan terkendali; data masih terlihat bagi pihak yang dapat membaca repositori.
- **LOCKED-BLIND:** selain integritas terkunci, akses terhadap prompt/expected behavior dibatasi sehingga pihak yang mengembangkan sistem tidak dapat melihatnya sebelum evaluasi resmi.
- **UNLOCKED / RETIRED:** versi lama dibuka secara resmi atau dipensiunkan; tidak boleh diam-diam ditimpa.

Status lock tidak mengubah status verifikasi konten. Record boleh tetap `verification_status: draft`; penguncian hanya menyatakan bahwa versi kandidat tidak boleh berubah tanpa prosedur resmi.

## 2. Kondisi Pilar E saat kebijakan disusun

Pemeriksaan pada `ilis-v2-development` menemukan 18 record berlabel `final_test`, seluruhnya berada pada kelompok `regression` dan tersebar di 18 batch:

| ID | File |
|---|---|
| eval-0010 | batch_001.jsonl |
| eval-0015 | batch_002.jsonl |
| eval-0020 | batch_003.jsonl |
| eval-0025 | batch_004.jsonl |
| eval-0030 | batch_005.jsonl |
| eval-0035 | batch_006.jsonl |
| eval-0040 | batch_007.jsonl |
| eval-0045 | batch_008.jsonl |
| eval-0050 | batch_009.jsonl |
| eval-0055 | batch_010.jsonl |
| eval-0060 | batch_011.jsonl |
| eval-0065 | batch_012.jsonl |
| eval-0070 | batch_013.jsonl |
| eval-0075 | batch_014.jsonl |
| eval-0080 | batch_015.jsonl |
| eval-0085 | batch_016.jsonl |
| eval-0090 | batch_017.jsonl |
| eval-0095 | batch_018.jsonl |

Semua 18 record masih DRAFT dan bersifat konseptual, belum merupakan tes otomatis. PR #31 sudah diterima Dola dan merged: `eval-0010` tetap “Halo, apa kabar?”, sementara `eval-0015` menjadi “Hai!”. Duplikasi exact-match itu sudah ditangani.

**Batas interpretasi:** 18 record ini hanya mewakili regression, bukan holdout menyeluruh untuk Lexicon, Sentence Patterns, Multi-turn, dan Knowledge. Karena split saat ini terkonfounded oleh kelompok, jangan menyebutnya evaluasi final menyeluruh ILIS atau membandingkan skor split seolah-olah komposisinya setara.

## 3. Gerbang wajib sebelum Final-Test dapat dikunci

Semua syarat berikut harus dipenuhi sebelum status berubah dari CONCEPTUAL/CANDIDATE:

1. **Cakupan ditetapkan.** Nyatakan kemampuan dan kelompok yang benar-benar hendak diukur. Jika hanya regression, beri nama eksplisit `Regression Holdout`; jangan klaim mewakili semua pilar.
2. **Kurasi selesai.** Setiap record ditinjau dari sisi bahasa, semantik, sumber/target_ref, expected behavior, dan kesesuaian metrik. Record yang belum cukup bukti tetap DRAFT dan tidak otomatis layak menjadi holdout.
3. **Independensi diperiksa.** Lakukan exact-match, normalisasi, kemiripan leksikal, parafrasa/kemiripan semantik, dan pemeriksaan lintas-pilar terhadap seluruh kandidat. Catat metode, ambang, kandidat, keputusan manual, dan keterbatasan; jangan mengklaim bebas kebocoran absolut.
4. **Keluarga kasus dipisahkan.** Pemisahan dilakukan pada tingkat skenario/keluarga semantik, bukan pengacakan baris. Parafrasa dekat dari satu skenario tidak boleh tersebar lintas development, validation, dan final-test.
5. **Expected behavior dapat dinilai.** Setiap kasus memiliki kriteria lulus/gagal yang jelas dan rubrik yang disepakati. Deskripsi bahasa alami yang terlalu umum tidak cukup untuk skor otomatis.
6. **Skema dibekukan.** Tetapkan field kanonis, versi skema, definisi `group`, `test_group`, `metric`, `metric_name`, serta aturan validasi. Selesaikan ketidaksamaan `sample.jsonl` dan batch sebelum loader dibuat.
7. **Tidak dipakai untuk tuning.** Buktikan bahwa loader development/validation dan proses eksperimen tidak memuat kandidat Final-Test.
8. **Review dan otorisasi.** Dola menerima inventaris, audit kebocoran, rubrik, manifest, dan prosedur; Owner menyetujui cakupan serta lock secara eksplisit.

Jika satu gerbang gagal, status tetap CANDIDATE/CONCEPTUAL. Jangan mengubah label split atau status verifikasi hanya untuk membuat checklist tampak lulus.

## 4. Pemisahan fisik dan manifest

Setelah seluruh gerbang lulus dan Owner mengizinkan, kandidat Final-Test dipisahkan dari file batch development/validation ke lokasi khusus, misalnya:

- `data/indonesian/evaluation/final_test/` untuk berkas kandidat yang dikunci;
- `data/indonesian/evaluation/manifests/` untuk manifest dan catatan lock.

Lokasi tersebut **belum dibuat oleh PR ini**. Struktur final harus ditinjau Dola terlebih dahulu. Loader development/validation wajib menggunakan daftar file eksplisit dan menolak memuat folder Final-Test. Jangan mengandalkan filter nama file yang longgar atau glob seluruh folder.

Manifest lock minimal mencatat:

- nama suite, cakupan kemampuan, status lock, dan versi;
- daftar lengkap `evaluation_id`, sumber file/record asal, jumlah record, dan versi skema;
- SHA-256 untuk setiap record kanonis serta hash keseluruhan artefak Final-Test;
- commit SHA sumber dan commit SHA yang memuat artefak terkunci;
- versi kode/runner, konfigurasi, dan rubrik yang akan digunakan;
- tanggal/waktu UTC pembuatan lock;
- keputusan review Dola dan otorisasi Owner (tautan PR/commit);
- riwayat perubahan, pembukaan, akses, atau pensiun versi.

Hash dihitung atas representasi byte yang ditentukan secara eksplisit (UTF-8, normalisasi newline yang ditetapkan, satu JSON object per baris). Jangan menghitung hash dari hasil parse lalu serialisasi ulang yang dapat mengubah urutan field atau whitespace tanpa aturan kanonis.

Setelah manifest disetujui, setiap perubahan isi menghasilkan versi baru dan hash baru. Dilarang mengedit versi terkunci secara in-place.

## 5. Dua tingkat penguncian dan keterbatasan repositori

Repositori `bronagerona/Sistem-Bahasa-universal` saat ini **public**. Artinya, pemisahan folder, manifest, checksum, dan disiplin PR dapat menjaga integritas versi, tetapi **tidak dapat merahasiakan prompt atau expected behavior** dari orang yang dapat membaca GitHub.

Karena itu:

- **LOCKED-INTEGRITY** dapat diterapkan pada repositori publik: versi dibekukan, hash dapat diverifikasi, loader mengecualikannya, perubahan harus melalui prosedur unlock/version-bump.
- **LOCKED-BLIND** tidak dapat diklaim selama isi Final-Test tetap berada di repositori publik. Untuk blind holdout, artefak harus disimpan di lokasi privat dengan kontrol akses yang sesuai. Lokasi privat, pemegang akses, dan prosedur pengelolaannya perlu diputuskan Owner secara terpisah.

Jangan menggunakan kata “rahasia”, “blind”, atau “akses terbatas” untuk Final-Test yang masih berada di repositori publik.

## 6. Aturan penggunaan dan larangan tuning

Setelah terkunci:

1. Loader development, validation, kurasi, dan tuning dilarang membaca atau menggabungkan Final-Test.
2. Tidak boleh menggunakan prompt, expected behavior, jawaban, hasil per kasus, atau pola kegagalan Final-Test untuk memilih fitur, mengubah aturan, menyusun contoh, atau menyetel parameter sebelum evaluasi resmi selesai.
3. Pemeriksaan integritas (hash/manifest) boleh dilakukan tanpa membuka isi prompt.
4. Akses untuk evaluasi resmi harus memiliki tujuan, pelaksana, waktu, versi kode, dan hasil yang tercatat.
5. Hasil evaluasi yang telah dibuka dianggap informasi yang dapat memengaruhi pengembangan. Jangan terus memakai holdout yang sama sebagai tolok ukur “tak tersentuh” setelah hasilnya dipakai untuk perbaikan.
6. Bila hasil Final-Test dipakai untuk mengubah sistem, versi holdout tersebut ditandai **RETIRED** untuk klaim blind/independen berikutnya. Siapkan holdout versi baru yang independen sebelum evaluasi final berikutnya.

## 7. Prosedur unlock, revisi, dan pensiun

Unlock hanya dapat dilakukan setelah:

1. alasan dan lingkup perubahan ditulis;
2. Dola meninjau dampak terhadap independensi dan kebocoran;
3. Owner memberi otorisasi eksplisit;
4. versi lama, manifest, hash, dan log akses tetap diarsipkan;
5. versi baru dibuat dengan nomor versi dan hash baru;
6. audit independensi diulang pada kandidat yang berubah.

Jangan menghapus jejak versi lama atau mengganti artefak terkunci tanpa catatan. Perubahan satu record saja tetap membentuk versi baru.

## 8. Prosedur evaluasi resmi dan bukti reproduksibilitas

Setiap run resmi harus mencatat sekurang-kurangnya:

- Final-Test suite/version dan manifest SHA-256;
- commit SHA kode ILIS yang diuji;
- versi runner, dependency/environment, konfigurasi, dan seed bila relevan;
- waktu mulai/selesai UTC;
- jumlah kasus yang dijalankan, dilewati, gagal, atau tidak dapat dinilai;
- hasil agregat dan laporan per kasus dengan perlindungan akses yang sesuai;
- identitas/otorisasi pelaksana dan tautan artefak hasil.

Hasil Final-Test tidak boleh menjadi data tuning. Jika perubahan kode dilakukan setelah hasil dibuka, evaluasi berikutnya harus menyatakan dengan jujur bahwa holdout lama sudah terekspos dan tidak lagi blind terhadap perubahan tersebut.

## 9. Status saat ini dan larangan

Status yang diusulkan untuk inventaris Final-Test sekarang: **CONCEPTUAL — NOT LOCKED**.

Belum dilakukan:
- pemindahan 18 record;
- pembuatan folder Final-Test atau manifest lock;
- penghitungan checksum resmi;
- pengaturan loader atau kontrol akses;
- pembuatan runner atau eksekusi tes Final-Test;
- perubahan status DRAFT;
- staging atau integrasi ke runtime/SQLite.

PR kebijakan ini hanya mengusulkan aturan. Penerimaan dokumen tidak otomatis mengunci 18 record, tidak otomatis mengesahkan Final-Test sebagai suite komprehensif, dan tidak memberi izin staging.

## 10. Keputusan yang diminta dari Dola

Mohon Dola meninjau dan memberi keputusan atas hal berikut:

1. Apakah gerbang pra-lock, manifest, checksum per-record/artefak, dan version-bump sudah memadai?
2. Apakah pemisahan fisik dan loader allowlist/explicit-file-list cukup mencegah Final-Test ikut termuat ke development/validation?
3. Apakah pembedaan LOCKED-INTEGRITY vs LOCKED-BLIND tepat mengingat repositori saat ini public?
4. Apakah 18 record sekarang sebaiknya hanya disebut `Regression Holdout Candidate`, bukan Final-Test umum, sampai empat kelompok lain memiliki holdout independen?
5. Apakah prosedur unlock, access log, retirement setelah hasil dibuka, dan bukti reproduksibilitas sudah memadai?

**Rekomendasi Eksekutor:** terima kebijakan sebagai tata kelola awal setelah review Dola, tetapi pertahankan status data sebagai CONCEPTUAL/NOT LOCKED sampai semua gerbang pra-lock lulus dan Owner memberi otorisasi lock yang eksplisit.
