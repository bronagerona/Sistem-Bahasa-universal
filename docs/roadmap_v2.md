# ILIS V2 — Roadmap Perbaikan & Penambahan Fitur

**Status:** usulan rencana setelah evaluasi beta V1  
**Prinsip tetap:** deterministic-first, tanpa LLM/model AI sebagai inti,
modular, provenance-aware, dan backward-compatible sejauh mungkin.

## Tujuan V2

Memperluas cakupan bahasa Indonesia dan domain reasoning secara terukur,
meningkatkan kesetiaan makna generator, memperkuat memori, serta membangun
evaluasi yang dapat direproduksi. Setiap fitur harus memiliki dataset,
aturan penerimaan, dan tes regresi sebelum digabungkan.

## Tahap 1 — Semantic Engine V2

- Perluas parser dari pola satu predikasi ke struktur kalimat yang lebih kaya:
  frasa preposisional, argumen opsional, kalimat pasif sederhana, dan
  beberapa pola klausa yang aman.
- Tambahkan pemrosesan pertanyaan dan perintah secara eksplisit dengan Intent
  yang jelas; jangan memaksakan semuanya menjadi assertion.
- Tingkatkan resolusi variasi melalui kamus alias terkurasi, normalisasi
  typo berbasis aturan dan jarak edit yang dibatasi, serta confidence per
  field.
- Pertahankan teks asli, variasi surface, dan provenance normalisasi.
- Tetapkan ambang abstain: input ambigu/di luar cakupan harus low_confidence
  atau unsupported.
- Pertahankan kontrak V1 atau naikkan contract version jika perubahan
  struktural memang memutus kompatibilitas.

**Deliverable:** semantic corpus berlabel, parser V2, matriks per-field
precision/recall, dan tes regresi slang/typo.

## Tahap 2 — Reasoning Engine V2

- Bangun registry aturan dengan ID, versi, domain, prasyarat, dan jejak
  evidence yang eksplisit.
- Tambahkan aturan domain bertahap: properti objek, sebab-akibat sederhana,
  keadaan karakter/NPC, kepemilikan, lokasi, dan perubahan state game.
- Pisahkan fakta observasi, aturan dunia game, hipotesis, dan kesimpulan.
- Tambahkan resolusi konflik berbasis kebijakan eksplisit; jangan memilih
  fakta secara diam-diam.
- Batasi kedalaman inferensi, deteksi siklus, dan sediakan penjelasan
  langkah-per-langkah.
- Confidence tetap heuristik sampai tersedia kalibrasi berbasis dataset.

**Deliverable:** rule pack V2, regression suite per domain, conflict policy,
dan audit evidence untuk setiap inferensi.

## Tahap 3 — Language Generator V2

- Perluas input utama menjadi semantic frame/meaning graph generik, bukan
  parser khusus satu jenis kesimpulan.
- Tambahkan konstruksi kalimat untuk assertion, negation, question,
  command, modality, tense/aspect, recipient, location, dan time.
- Tingkatkan pilihan leksikal serta variasi formal, informal, slang, dan
  bentuk ringkas tanpa mengubah proposisi.
- Terapkan semantic round-trip checks: makna hasil kalimat harus cocok dengan
  meaning input pada subset grammar yang didukung.
- Sediakan strategi abstain/fallback saat meaning belum dapat direalisasikan.
- Uji variasi output agar tidak repetitif tetapi tetap setia pada makna.

**Deliverable:** grammar realization V2, generator berbasis semantic frame,
dan tes kesetiaan makna per register.

## Tahap 4 — Persistensi Memory ke Disk

- Rancang backend storage interface agar MemoryStore/KnowledgeStore dapat
  memakai adapter in-memory atau disk.
- Mulai dari SQLite untuk sesi, Working/Episodic Memory, konsep, relasi,
  fakta, provenance, dan hypothesis tracker.
- Terapkan schema versioning, migrasi, transaksi, indeks, dan pemulihan
  setelah restart.
- Definisikan kebijakan retensi, penghapusan sesi, ekspor/impor, dan backup.
- Pastikan isolasi sesi serta integritas referensi episode/fakta tetap terjaga.
- Tambahkan tes restart: tulis data, tutup proses/instance, buat instance baru,
  lalu verifikasi data dapat dibaca.

**Deliverable:** persistence adapter SQLite, migrasi schema, dokumentasi
backup/retensi, dan tes restart.

## Tahap 5 — Beta dataset, benchmark, dan quality gates

- Perbesar dataset dengan contoh formal, santai, gaul, singkatan, typo,
  kalimat ambigu, negatif, modal, pertanyaan, perintah, dan multi-klausa.
- Pisahkan train-free rule development fixtures dari held-out evaluation set;
  tidak ada training model.
- Ukur semantic exact-match dan per-field accuracy, variation normalization
  precision/recall, reasoning conclusion/evidence accuracy, memory
  consistency, generator meaning preservation, serta latency p50/p95.
- Jalankan benchmark di hardware yang dicatat dan gunakan batas regresi
  yang tidak bergantung pada runner CI yang berubah-ubah.
- Setiap bug beta menjadi regression test.

## Tahap 6 — Interface & Developer Experience

- Ganti fallback phrase khusus dengan routing berbasis semantic frame dan
  registry aturan yang terdokumentasi.
- Sediakan API konsisten untuk chatbot, NPC, event ingestion, dan response
  metadata.
- Tambahkan konfigurasi rule pack per genre game tanpa mencampur fakta game
  dengan pengetahuan umum.
- Tambahkan observability: trace ID, rule ID, provenance, latency per tahap,
  serta alasan abstain.
- Jaga kompatibilitas API dan dokumentasikan perubahan.

## Urutan prioritas yang disarankan

1. Semantic V2 + dataset evaluasi (mengurangi fallback phrase khusus).
2. Reasoning V2 rule registry dan rule pack game.
3. Generator V2 berbasis meaning frame.
4. SQLite persistence dan migrasi.
5. Benchmark performa, regression gates, dan API hardening.

## Definition of Done V2

- Seluruh tes V1 tetap lulus atau perubahan kontrak dimigrasikan dengan tes.
- Dataset evaluasi memiliki label dan prosedur review yang terdokumentasi.
- Setiap kesimpulan reasoning dapat ditelusuri ke premis, rule ID, dan
  provenance.
- Generator mempertahankan proposisi, negasi, modalitas, dan ketidakpastian
  pada subset grammar yang dinyatakan didukung.
- Data memori bertahan setelah restart melalui backend disk dan lulus tes
  migrasi.
- Benchmark melaporkan hasil aktual beserta hardware, ukuran dataset, dan
  metodologi.
- Tidak ada komponen LLM/model AI yang ditambahkan sebagai inti ILIS.
