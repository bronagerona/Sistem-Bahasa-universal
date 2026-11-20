# Laporan Observasi Final-Test ILIS

> **Status:** OBSERVASI DOKUMENTER — EKSEKUSI 18 KASUS BELUM DAPAT DILAKUKAN  
> **Tanggal:** 20 November 2026  
> **Branch sumber:** `ilis-v2-development`  
> **Basis kode/data yang diperiksa:** `46b69d19a4595611033c0a6149877fe2f8b4aa47`  
> **Sasaran laporan:** `docs/audit_448/final_test_evaluation_report.md`  
> **Batas perubahan:** hanya dokumen laporan ini; tidak mengubah JSONL, kode runtime, tes, workflow, SQLite, atau `main`.

## 1. Ringkasan Eksekutif

Inventaris Final-Test berisi 18 kasus: `eval-0010`, `eval-0015`, dan `eval-0020` sampai `eval-0095` dengan interval lima. Semua kasus berada di kelompok `regression`, tersebar di 18 batch Evaluation.

**Hasil eksekusi aktual: 0 dari 18 kasus berhasil dijalankan terhadap runtime ILIS dalam pekerjaan ini.** Karena tidak ada keluaran runtime yang diperoleh, tidak ada kasus yang dapat dinilai PASS atau FAIL. Semua 18 kasus berstatus **NOT RUN / BELUM TERUJI**.

Persentase kelulusan Final-Test **belum dapat dihitung**. Angka 0/18 (0%) hanya menyatakan tidak ada kasus yang memperoleh status lulus terverifikasi dalam observasi ini; angka tersebut **bukan** bukti bahwa sistem gagal pada 18 kasus. Persentase pass yang sah memerlukan eksekusi aktual dan penilaian terhadap rubrik yang ditetapkan.

## 2. Metode dan Batas Eksekusi

### Sumber yang diperiksa

- `docs/audit_448/evaluation_audit.md`
- `docs/audit_448/final_audit_448_and_revision_plan.md`
- `docs/audit_448/final_test_lock_policy.md`
- 18 file `data/indonesian/evaluation/batch_001.jsonl` sampai `batch_018.jsonl`
- `.github/workflows/tests.yml`
- `src/ilis/interfaces/chatbot_adapter.py`, `src/ilis/cli.py`, dan `tests/test_e2e_chatbot.py`

### Mengapa eksekusi tidak dapat diklaim

1. Semua 18 record menyebut kasus sebagai konseptual, bukan tes otomatis yang telah dijalankan.
2. Workflow `Tests` menjalankan `pytest -ra` pada tes yang sudah ada. Workflow tersebut tidak memuat atau mengeksekusi record Final-Test dari 18 file JSONL.
3. Workflow mendukung pemicu manual, tetapi jalur konektor GitHub yang tersedia pada sesi ini hanya menyediakan pembacaan resource dan tidak menyediakan aksi untuk mengirim `workflow_dispatch`.
4. Tidak tersedia sesi runtime ILIS yang dapat dipanggil langsung dari percakapan ini. Percobaan memperoleh salinan repo melalui jaringan dari lingkungan eksekusi terisolasi juga gagal karena host GitHub tidak dapat dijangkau.
5. Tidak dibuat runner baru, tidak diubah workflow, dan tidak dibuat tes otomatis ad hoc, sesuai batas observasi dan larangan mengubah komponen selain laporan.

Dengan demikian, pemeriksaan isi prompt dan expected behavior di bawah adalah **analisis statis**, bukan hasil eksekusi chatbot. Riwayat CI umum atau eksperimen Playground A–E tidak dipakai sebagai pengganti hasil per kasus Final-Test.

## 3. Hasil per Kasus

| ID | Input yang diperiksa | Perilaku yang diharapkan | Hasil aktual |
|---|---|---|---|
| eval-0010 | Halo, apa kabar? | Sapaan alami sesuai hotfix Greeting; tidak menambahkan prefix identitas pada sapaan biasa. | **NOT RUN** — tidak ada keluaran runtime. |
| eval-0015 | Hai! | Mengenali sapaan satu token; respons alami, `reasoning_type: greeting`, kontrak Semantic 12 dan Reasoning 6 tetap terjaga, tanpa prefix identitas. | **NOT RUN** — tidak ada keluaran runtime. |
| eval-0020 | Turn 1: Aku sedang mencari buku sejarah. Turn 2: Ngomong-ngomong, apa fungsi akar tumbuhan? Turn 3: Kembali ke buku tadi, aku butuh untuk tugas sekolah. | Memulihkan referen/topik buku setelah percakapan menyimpang ke topik lain. | **NOT RUN** — tidak ada keluaran multi-turn. |
| eval-0025 | Turn 1: Saya akan mengirim laporan setelah rapat. Turn 2: Rapat belum berlangsung. Turn 3: Jadi laporan sudah dikirim? | Tidak menyimpulkan laporan telah dikirim; mempertahankan syarat temporal bahwa pengiriman direncanakan setelah rapat. | **NOT RUN** — tidak ada keluaran multi-turn. |
| eval-0030 | Turn 1: Mungkin rapat berlangsung besok. Turn 2: Belum ada konfirmasi jadwal. Turn 3: Jadi rapat sudah dipastikan besok? | Mempertahankan modalitas kemungkinan dan status belum terkonfirmasi; tidak menaikkan perkiraan menjadi kepastian. | **NOT RUN** — tidak ada keluaran multi-turn. |
| eval-0035 | Turn 1: Budi mengatakan bahwa rapat dipindahkan. Turn 2: Belum ada pengumuman resmi. Turn 3: Jadi rapat memang sudah dipindahkan? | Mempertahankan atribusi kepada Budi dan status belum terverifikasi; tidak mengubah laporan menjadi fakta resmi. | **NOT RUN** — tidak ada keluaran multi-turn. |
| eval-0040 | Turn 1: Merkurius berotasi sekitar 58,6 hari. Turn 2: Jadi satu hari Matahari di Merkurius juga 58,6 hari? Turn 3: Bukankah orbitnya sekitar 88 hari? | Membedakan rotasi sideris, hari Matahari, dan periode orbit; tidak mencampuradukkan ketiganya. | **NOT RUN** — tidak ada keluaran multi-turn. |
| eval-0045 | Turn 1: Kami kadang-kadang berolahraga. Turn 2: Jadi kami berolahraga setiap hari? Turn 3: Biasanya pada akhir pekan. | Membedakan frekuensi sesekali, habitual, dan setiap hari; memperbarui interpretasi dari turn berikutnya. | **NOT RUN** — tidak ada keluaran multi-turn. |
| eval-0050 | Turn 1: Kami menunggu selama satu jam. Turn 2: Acara berlangsung hingga pukul sembilan. Turn 3: Paket sudah sampai. Turn 4: Apakah semua kata penanda itu menyatakan durasi? | Membedakan durasi `selama`, batas akhir `hingga`, dan predikat tiba `sampai`. | **NOT RUN** — tidak ada keluaran multi-turn. |
| eval-0055 | Turn 1: Saya belum selesai. Turn 2: Dia bukan dokter. Turn 3: Jangan masuk. Turn 4: Kami datang tanpa mobil. Turn 5: Apakah semua kalimat itu menyatakan hal yang sama? | Membedakan negasi temporal/aspektual `belum`, penyangkalan identitas `bukan`, larangan `jangan`, dan ketiadaan penyerta `tanpa`. | **NOT RUN** — tidak ada keluaran multi-turn. |
| eval-0060 | Turn 1: Peserta wajib mendaftar. Turn 2: Dia mampu berenang. Turn 3: Pelanggan berhak bertanya. Turn 4: Laporan seharusnya selesai. Turn 5: Apakah kelima pernyataan menyatakan jenis modalitas yang sama? | Membedakan kewajiban, kemampuan, hak, dan ekspektasi/norma. | **NOT RUN** — tidak ada keluaran multi-turn. |
| eval-0065 | Turn 1: Saya sedang belajar. Turn 2: Kita akan bekerja bersama. Turn 3: Kami akan menghubungi Anda. Apakah semua pronomina memiliki referen dan cakupan kelompok yang sama? | Membedakan penutur tunggal, kelompok inklusif, kelompok eksklusif, dan lawan bicara. | **NOT RUN** — tidak ada keluaran multi-turn. |
| eval-0070 | Turn 1: Siapa yang datang? Turn 2: Kapan mereka tiba? Turn 3: Di mana mereka bertemu? Turn 4: Mengapa mereka pergi? Turn 5: Berapa orang yang tersisa? | Membedakan target orang, waktu, lokasi, sebab, dan jumlah sambil menjaga referen lintas giliran. | **NOT RUN** — tidak ada keluaran multi-turn. |
| eval-0075 | Turn 1: Apakah ruang tersedia? Turn 2: Adakah pilihan lain? Turn 3: Berapa jumlahnya? Turn 4: Bagaimana cara memesannya? | Membedakan pertanyaan polar, keberadaan, jumlah, dan metode serta menjaga konteks. | **NOT RUN** — tidak ada keluaran multi-turn. |
| eval-0080 | Turn 1: Buku ada di meja. Turn 2: Saya pindahkan ke lemari. Turn 3: Buku itu berasal dari perpustakaan. Turn 4: Saya menyimpannya dalam kotak. | Membedakan lokasi, tujuan, asal, dan interior/lingkup serta menjaga referen buku. | **NOT RUN** — tidak ada keluaran multi-turn. |
| eval-0085 | Turn 1: Saya sedang menyiapkan bahan. Turn 2: Saya sudah mengirim draf. Turn 3: Saya pernah memakai format itu. Turn 4: Besok saya akan memperbaikinya. | Membedakan progresif, tercapai, pengalaman, dan prospektif; menjaga urutan waktu tanpa menyimpulkan kepastian berlebihan. | **NOT RUN** — tidak ada keluaran multi-turn. |
| eval-0090 | Turn 1: Banyak peserta datang. Turn 2: Setiap peserta mendapat nomor. Turn 3: Sebagian peserta pulang. Turn 4: Seluruh acara selesai. | Membedakan kuantitas tak tentu, distribusi individual, cakupan parsial, dan cakupan total; tidak mengarang angka. | **NOT RUN** — tidak ada keluaran multi-turn. |
| eval-0095 | Kasus konseptual: bedakan membaca, ditulis, berjalan, terjatuh, dan membawakan berdasarkan pelaku, pasien, valensi, dan fungsi afiks. | Menganalisis perbedaan morfologi dan suara/valensi secara tepat. | **NOT RUN** — tidak ada keluaran runtime. |

### Rekap status

| Status | Jumlah |
|---|---:|
| PASS terverifikasi | 0 |
| FAIL terverifikasi | 0 |
| NOT RUN / belum teruji | 18 |
| **Total** | **18** |

- **Execution coverage:** 0/18 = 0%.
- **Verified pass rate:** belum dapat dihitung (tidak ada kasus yang dieksekusi).
- **Verified fail rate:** belum dapat dihitung (tidak ada kasus yang dieksekusi).

Tidak tepat menyatakan sistem lulus 0% ataupun gagal 100%. Yang dapat dinyatakan adalah **cakupan eksekusi Final-Test pada observasi ini 0%**.

## 4. Kasus yang Perlu Diperhatikan

Karena tidak ada keluaran aktual, daftar berikut adalah risiko desain/penilaian yang perlu diperhatikan saat eksekusi nanti, bukan daftar bug yang telah terbukti.

1. **eval-0010 dan eval-0015 — greeting.** Periksa respons alami, jenis reasoning greeting, dan ketiadaan prefix identitas. Keduanya satu keluarga regression greeting dengan pemicu leksikal berbeda, bukan dua kategori kemampuan independen.
2. **eval-0020 — pemulihan topik setelah interupsi.** Perlu rubrik yang jelas untuk menentukan apakah sistem benar-benar merujuk buku sejarah, bukan sekadar menghasilkan respons relevan secara umum.
3. **eval-0025, eval-0030, eval-0035 — status temporal, modalitas, dan atribusi.** Rubrik harus membedakan rencana dari kejadian aktual, kemungkinan dari kepastian, serta laporan seseorang dari fakta yang telah diverifikasi.
4. **eval-0040 — presisi angka astronomi.** Input memakai sekitar 58,6 hari untuk rotasi Merkurius. Record Knowledge `fact-0033` pada versi saat ini telah diperjelas menjadi sekitar 58,65 hari. Nilai 58,6 tetap merupakan pendekatan kasar yang pernah digunakan, tetapi rubrik sebaiknya menilai pembedaan rotasi sideris/hari Matahari/orbit dan konsistensi presisi secara terpisah.
5. **eval-0055 — negasi.** BL-ILIS-002 sudah diimplementasikan sebagai modul terisolasi dan diuji pada 205 anotasi, tetapi belum dihubungkan ke runtime produksi. Karena itu, hasil modul tersebut tidak boleh diasumsikan otomatis tercermin pada respons chatbot untuk kasus ini.
6. **eval-0060 sampai eval-0095 — cakupan konsep luas.** Banyak kasus menggabungkan beberapa konsep dalam satu rangkaian multi-turn. Rubrik perlu menyebut unsur mana yang wajib benar agar penilaian tidak bergantung pada kesan umum terhadap jawaban.
7. **Semua kasus multi-turn.** Jalankan setiap rangkaian dengan satu instance chatbot dan satu session yang sama, urutan turn dipertahankan, tanpa menyuntikkan expected behavior ke konteks sistem. Catat keluaran setiap turn, bukan hanya jawaban akhir.

## 5. Kesimpulan Kualitas dan Kesiapan Staging

**Belum ada dasar empiris dari Final-Test ini untuk menyatakan hasil sistem sudah cukup baik atau menghitung tingkat kelulusannya.** Ini bukan vonis bahwa ILIS gagal; ini berarti evaluasi yang diminta belum benar-benar dieksekusi.

Berdasarkan audit Evaluation yang sudah ada dan kebijakan Final-Test:

- 18 kasus masih berstatus DRAFT dan konseptual.
- Seluruh 18 kasus hanya mewakili kelompok regression; bukan holdout seimbang untuk Lexicon, Sentence Patterns, Multi-turn, dan Knowledge.
- Split Development/Validation/Final-Test masih terkonfounded oleh kelompok.
- Expected behavior masih berupa deskripsi bahasa alami; rubrik operasional PASS/FAIL belum ditetapkan untuk semua kasus.
- Audit lintas-pilar belum menyeluruh.
- Final-Test masih **CONCEPTUAL — NOT LOCKED**; label `split: final_test` tidak dengan sendirinya mengunci data.
- BL-ILIS-002 telah diuji sebagai modul terisolasi, tetapi belum terhubung ke runtime produksi.
- Tidak ada otorisasi staging yang dihasilkan oleh laporan observasi ini.

**Rekomendasi: jangan lanjut ke staging berdasarkan hasil Final-Test saat ini.** Sebelum staging dipertimbangkan, diperlukan runner yang mengeksekusi seluruh kasus pada versi kode yang dibekukan, rubrik yang dapat dinilai, pencatatan output per turn, audit independensi/lintas-pilar, serta penyelesaian prasyarat penguncian sesuai kebijakan dan persetujuan Owner.

Jika nanti eksekusi dijalankan di GitHub Actions, catat secara eksplisit bahwa itu adalah runner jarak jauh GitHub Actions, bukan staging lokal milik Owner.

## 6. Jaminan Ruang Lingkup Perubahan

- Tidak ada file JSONL yang diubah.
- Tidak ada record, input, expected behavior, split, atau verification status yang diubah.
- Tidak ada kode runtime, tes, workflow, konfigurasi, atau SQLite yang diubah.
- Tidak ada perubahan pada branch `main`.
- Dokumen ini hanya melaporkan inventaris, analisis statis, keterbatasan eksekusi, dan rekomendasi.

**Status akhir laporan:** 18/18 kasus telah diinventarisasi dan dibandingkan secara statis dengan expected behavior; 0/18 benar-benar dieksekusi. Final-Test belum menghasilkan persentase kelulusan yang sah dan belum dapat menjadi dasar persetujuan staging.
