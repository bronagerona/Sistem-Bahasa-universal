# Roadmap ILIS V3

**Status:** rencana pengembangan; bukan komitmen bahwa fitur telah tersedia.  
**Prasyarat:** evaluasi V2 Alpha dan umpan balik penggunaan nyata.

## Prinsip arah V3

- Tetap tanpa LLM/model AI sebagai inti.
- Mempertahankan kontrak antarmodul dan kompatibilitas API yang sudah stabil.
- Memperluas kemampuan melalui data, aturan, struktur makna, dan pengujian yang dapat ditelusuri.
- Mengutamakan kualitas dan cakupan terukur daripada klaim kecerdasan umum.

## Tahap 1 — Dataset bahasa dan cakupan semantik

- Bangun korpus evaluasi bahasa Indonesia yang berlisensi/bersumber jelas, dianotasi untuk intent, aktor, predikat, objek, negasi, aspek, modalitas, waktu, lokasi, dan register.
- Perluas cakupan pertanyaan, perintah, elipsis, kalimat majemuk, referensi pronomina, dan variasi ejaan.
- Susun matriks coverage formal, santai, slang, singkatan, bentuk tidak baku, serta typo.
- Ukur precision, recall, exact-field accuracy, dan tingkat fallback per kategori.

## Tahap 2 — Semantic representation dan dialog

- Kembangkan semantic frame dan representasi multi-klausa tanpa mengubah kontrak lama secara diam-diam.
- Tambahkan resolusi referensi dan konteks dialog secara eksplisit.
- Bedakan pertanyaan klarifikasi, permintaan tindakan, koreksi, dan tindak lanjut.
- Definisikan perilaku saat informasi tidak lengkap atau saling bertentangan.

## Tahap 3 — Knowledge dan reasoning

- Rancang registry aturan yang dapat diberi versi, domain, prasyarat, dan provenance.
- Tambahkan dukungan negasi, aturan pengecualian, konflik, dan rantai inferensi yang dapat dijelaskan.
- Sediakan mekanisme validasi fakta dan kebijakan kepercayaan sumber.
- Buat dataset benchmark reasoning per domain; hindari menganggap contoh aturan sebagai pengetahuan universal.

## Tahap 4 — Generator dan interaksi

- Perluas konstruksi kalimat berbasis semantic frame, bukan daftar respons statis.
- Tingkatkan konsistensi register, koherensi antar-kalimat, dan pengungkapan ketidakpastian.
- Sediakan action contract untuk NPC/game adapter agar perintah bahasa tidak langsung menjalankan aksi tanpa validasi aplikasi.
- Evaluasi keluaran dengan rubrik keterpahaman, kesetiaan makna, dan variasi.

## Tahap 5 — Persistensi dan operasional

- Tambahkan migrasi skema SQLite yang terversi dan uji kompatibilitas.
- Evaluasi transaksi, konkurensi, backup/restore, dan batas ukuran data.
- Tetapkan observability untuk jejak input, semantic frame, aturan yang aktif, evidence, dan output.
- Pertahankan mode in-memory sederhana untuk penggunaan ringan dan pengujian.

## Tahap 6 — Kualitas rilis

- Jalankan tes unit, integrasi, benchmark korpus, regresi, dan uji performa di CI.
- Tetapkan baseline dan ambang kualitas yang dapat diulang.
- Dokumentasikan perubahan API, batasan, serta prosedur upgrade.
- Rilis bertahap: alpha → beta → kandidat stabil, dengan gerbang kualitas eksplisit.

## Risiko dan hal yang tidak dijanjikan

- Sistem berbasis aturan tetap memerlukan cakupan leksikon, pola, fakta, dan domain yang dirawat.
- Kualitas tidak otomatis meningkat hanya dengan menambah jumlah aturan; konflik dan interaksi ant aturan harus diuji.
- V3 tidak menjanjikan kesetaraan dengan LLM, pemahaman universal, atau pembelajaran bebas tanpa batas.
