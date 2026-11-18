# ILIS — Indonesian Language Intelligence System

ILIS adalah sistem pemrosesan dan kecerdasan bahasa Indonesia yang dikembangkan **tanpa LLM sebagai inti**. ILIS dirancang sebagai sistem modular dan deterministik: pemahaman, representasi makna, pengetahuan, penalaran, memori, pembelajaran, dan generasi bahasa dibangun melalui komponen yang eksplisit serta dapat diuji.

Visi ILIS adalah menyediakan fondasi bahasa dan makna yang dapat digunakan untuk chatbot, NPC, dan berbagai genre game—bukan sekadar kumpulan template kalimat.

## Status

**✅ Rilis ILIS V1.0 Prototype Sudah Tersedia**

- Rilis: [ILIS V1.0 Prototype](https://github.com/bronagerona/Sistem-Bahasa-universal/releases/tag/v1.0-prototype)
- Branch integrasi: `main`
- Validasi rilis: GitHub Actions — **92 pengujian lulus**.

V1.0 Prototype merupakan fondasi sistem yang sudah berjalan dan terintegrasi. Rilis ini bukan klaim bahwa ILIS telah menyamai kemampuan LLM atau memiliki pemahaman bahasa umum.

## Cakupan bahasa V1

ILIS V1 menargetkan variasi bahasa Indonesia berikut:
- formal dan baku;
- santai dan percakapan sehari-hari;
- gaul/slang;
- singkatan;
- bentuk tidak baku;
- variasi ejaan dan typo.

Bahasa daerah dan pencampuran lintas bahasa belum menjadi cakupan yang dijamin pada V1.

## Modul yang sudah berjalan di V1

1. **Language Foundation** — tokenizer dan ILVE sebagai fondasi pemrosesan bahasa.
2. **Semantic Engine V1** — pemrosesan dan representasi semantik.
3. **Concept & Knowledge Engine V1** — struktur konsep dan pengetahuan.
4. **Reasoning Engine V1** — penalaran berbasis mekanisme dan aturan yang tersedia.
5. **Context & Memory Engine V1** — pengelolaan konteks serta memori.
6. **Learning Engine V1** — mekanisme pembelajaran dalam batas desain V1.
7. **Language Generator V1** — pembentukan keluaran bahasa.
8. **Interface** — Chatbot Adapter dan Game Adapter.
9. **Beta Test Suite & Evaluasi** — rangkaian pengujian untuk memeriksa perilaku dan kemampuan sistem.

## Prinsip desain

1. **Meaning-first:** memisahkan bentuk permukaan kalimat dari representasi maknanya.
2. **Dynamic construction:** membangun pemahaman dan keluaran dari struktur, bukan hanya mengambil kalimat template.
3. **Modular:** setiap subsistem memiliki tanggung jawab dan batas yang jelas.
4. **Deterministik dan dapat diuji:** perilaku inti dirancang agar dapat ditelusuri serta diuji.
5. **Evidence-aware:** membedakan fakta, dugaan, sumber, dan tingkat keyakinan sesuai dukungan implementasi.
6. **No LLM as the core:** LLM bukan mesin utama ILIS. Visi ini merupakan prinsip arsitektur, bukan sekadar opsi konfigurasi.

## Batasan ILIS V1

V1.0 adalah prototype yang sudah terintegrasi, tetapi kemampuannya masih memiliki batasan:

- Cakupan semantik dan pola pemahaman masih terbatas; belum setara pemahaman bahasa umum.
- Normalisasi slang, singkatan, bentuk tidak baku, dan typo masih bergantung pada aturan serta leksikon yang tersedia.
- Penalaran masih terbatas pada aturan dan pola yang diimplementasikan.
- Penyimpanan memori masih berbasis proses/in-memory dan belum menyediakan persistensi penuh.
- Pembelajaran V1 tidak berarti sistem belajar bebas seperti manusia atau melakukan pembaruan model bahasa.
- Generator bahasa masih memiliki keterbatasan variasi dan konstruksi keluaran.
- Sebagian fallback adapter masih spesifik terhadap frasa atau pola tertentu.
- Belum tersedia benchmark formal untuk performa, beban, dan konkurensi.
- ILIS tidak menjamin verifikasi kebenaran fakta secara mandiri.
- Bahasa daerah dan code-mixing lintas bahasa belum dijamin.

Karena itu, ILIS V1 **belum setara LLM dan belum mengklaim kecerdasan atau pemahaman universal**. Kemampuan yang belum didukung implementasi harus diperlakukan sebagai pekerjaan pengembangan berikutnya.

## Roadmap V2

Arah pengembangan berikutnya mencakup:

- memperluas cakupan semantik dan normalisasi typo/slang;
- memperkuat registry aturan dan penalaran untuk domain game;
- mengembangkan generator berbasis semantic frame agar konstruksi bahasa lebih fleksibel;
- menambahkan persistensi memori, termasuk opsi SQLite;
- memperluas dataset, skenario, dan benchmark evaluasi;
- meningkatkan observability, provenance, serta kualitas adapter;
- memperluas pengujian integrasi dan evaluasi performa.

Roadmap ini adalah sasaran pengembangan, bukan daftar kemampuan yang sudah tersedia di V1.

## Pengembangan

Proyek menggunakan Python. Untuk instruksi instalasi, pengujian, arsitektur, dan kontribusi, lihat dokumentasi di repository:

- [Dokumentasi arsitektur](docs/architecture.md)
- [Panduan kontribusi](CONTRIBUTING.md)

