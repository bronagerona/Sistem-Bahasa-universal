# KURIKULUM PEMAHAMAN BAHASA INDONESIA ILIS

**Target Lokasi:** `docs/KURIKULUM_PEMAHAMAN_BAHASA.md`  
**Branch:** `ilis-v2-development`  
**Status:** Dokumen Rancangan & Peta Arah (Non-Implementasi)

## Bagian 1 — Pendahuluan

### Tujuan Kurikulum

Kurikulum ini disusun sebagai peta pembelajaran bahasa Indonesia bagi ILIS pada fase Pengembangan Percakapan Sehari-hari. Tujuan utama dari kurikulum ini adalah membekali sistem agar mampu memahami maksud penutur manusia secara utuh dan kontekstual, bukan sekadar menghafal daftar aturan tata bahasa yang kaku atau mencocokkan kata secara mekanis.

### Prinsip Utama

- **Bertahap dan Terukur:** Pembelajaran disusun dari unit bahasa paling dasar (bunyi, ejaan, kelas kata) menuju struktur yang kompleks (pragmatik, wacana, variasi ragam bicara).
- **Prioritas Kebutuhan Percakapan:** Materi yang berdampak langsung pada kelancaran dialog sehari-hari—terutama pemahaman konteks, rujukan giliran bicara, dan maksud tersirat—mendapatkan bobot prioritas lebih tinggi dibandingkan detail teoretis yang jarang muncul dalam interaksi manusia.
- **Kejujuran Epistemik:** Sistem tetap mempertahankan prinsip untuk mengenali batas pemahamannya (membedakan antara makna yang pasti, ambigu, atau memerlukan klarifikasi) alih-alih menebak maksud penutur secara serampangan.

### Batasan Dokumen

Dokumen ini bersifat sebagai rancangan konseptual dan peta arah (roadmap) semata. Penyusunan dokumen ini tidak mengubah dataset yang sudah ada, tidak memodifikasi kode mesin saat ini, dan belum merupakan tahap implementasi teknis langsung.

## Bagian 2 — 8 Bidang Lengkap Bahasa Indonesia

Berikut adalah delapan bidang kajian bahasa Indonesia yang menjadi kerangka referensi ILIS, dilengkapi dengan istilah linguistik baku serta contoh penggunaan nyata dalam bahasa Indonesia sehari-hari.

### 1. Fonologi dan Ejaan

- **Tujuan:** Memastikan sistem mengenali representasi tulisan dari bunyi bahasa Indonesia yang baku serta mampu menoleransi atau menormalisasi variasi penulisan umum dalam teks percakapan.
- **Ruang Lingkup:** Sistem bunyi (vokal, konsonan, diftong, kluster), pemenggalan suku kata, penggunaan huruf kapital, tanda baca (titik, koma, tanda tanya, tanda seru), penulisan kata depan vs awalan, serta penulisan unsur serapan sesuai Ejaan Bahasa Indonesia yang Disempurnakan (EYD).
- **Contoh Nyata:**
  - Perbedaan makna akibat tanda baca: "Dia makan, Nak." (sapaan) vs "Dia makan nak." (tidak bermakna/keliru).
  - Penulisan baku vs tidak baku: apotek (baku) vs apotik (tidak baku); di rumah (preposisi dipisah) vs dimakan (prefiks digabung).

### 2. Kelas Kata (Kategori Sintaksis)

- **Tujuan:** Memberikan kemampuan pada sistem untuk mengidentifikasi fungsi dan kategori gramatikal setiap kata dalam kalimat sebagai dasar analisis struktur dan makna.
- **Ruang Lingkup:** Sebelas kelas kata baku dalam tata bahasa Indonesia:
  - **Nomina** (kata yang mengacu pada benda, manusia, konsep, atau hal): kopi, motor, Jakarta, kejujuran.
  - **Verba** (kata yang menyatakan perbuatan, tindakan, proses, atau keadaan): makan, berjalan, tidur, berpikir.
  - **Adjektiva** (kata yang menerangkan sifat atau keadaan nomina): panas, cepat, ramai, bingung.
  - **Adverbia** (kata yang memberi keterangan pada verba, adjektiva, atau kalimat): sangat, sudah, belum, sering, besok.
  - **Pronomina** (kata yang menggantikan nomina atau frasa nominal): saya, kamu, dia, mereka, ini, itu, siapa.
  - **Numeralia** (kata yang menyatakan jumlah, urutan, atau himpunan): satu, dua, ketiga, banyak, beberapa.
  - **Preposisi** (kata yang menandai hubungan makna di depan nomina/frasa): di, ke, dari, untuk, dengan, pada.
  - **Konjungsi** (kata penghubung antarkata, antarfrasa, antarklausa, atau antarkalimat): dan, atau, tetapi, karena, jika, padahal.
  - **Interjeksi** (kata seru yang mengungkapkan perasaan atau seruan spontan): wah, aduh, loh, nah, astaga.
  - **Artikula** (kata yang membatasi atau mendampingi nomina tertentu): si, sang, para, kaum.
  - **Partikel** (unsur penegas, penanya, atau pembentuk nuansa yang melekat atau mendampingi kata): -lah, -kah, -tah, pun.

### 3. Morfologi

- **Tujuan:** Memahami proses pembentukan kata dari bentuk dasar menjadi kata turunan serta perubahan makna dan kelas kata yang menyertainya.
- **Ruang Lingkup:**
  - **Prefiks (Awalan):** Imbuhan yang diletakkan di awal kata dasar.  
    Contoh: meN- + baca → membaca (verba aktif); di- + ambil → diambil (verba pasif); ter- + tidur → tertidur (ketidaksengajaan).
  - **Sufiks (Akhiran):** Imbuhan yang diletakkan di akhir kata dasar.  
    Contoh: ambil + -kan → ambilkan (benefaktif/perintah); makan + -an → makanan (nomina hasil/objek).
  - **Infiks (Sisipan):** Imbuhan yang disisipkan di tengah kata dasar.  
    Contoh: gigi + -er- → gerigi; tunjuk + -el- → telunjuk.
  - **Konfiks (Imbuhan Terbelah):** Gabungan awalan dan akhiran yang melekat secara bersamaan sebagai satu kesatuan makna.  
    Contoh: ke-...-an + hujan → kehujanan (tertimpa keadaan); peN-...-an + kirim → pengiriman (proses).
  - **Reduplikasi (Pengulangan):** Pengulangan satuan gramatikal, baik seluruhnya maupun sebagian, untuk menyatakan jamak, intensitas, atau kesalingan.  
    Contoh: buku-buku (jamak), bolak-balik (berulang-ulang), tolong-menolong (saling).
  - **Pemajemukan (Komposisi):** Penggabungan dua morfem dasar atau lebih yang menimbulkan satu makna baru yang padu.  
    Contoh: rumah sakit, kambing hitam, kereta api, tanggung jawab.

### 4. Sintaksis

- **Tujuan:** Memahami aturan penggabungan kata menjadi satuan yang lebih besar (frasa, klausa, kalimat) sehingga sistem mampu membedakan subjek pelaku, tindakan, objek, dan keterangan.
- **Ruang Lingkup:**
  - **Frasa:** Gabungan dua kata atau lebih yang bersifat nonpredikatif (tidak memiliki subjek-predikat), seperti kopi hitam panas (frasa nominal) atau sedang menunggu (frasa verbal).
  - **Klausa:** Satuan gramatikal yang memiliki unsur predikat dan berpotensi menjadi kalimat.
  - **Fungsi Sintaksis (S-P-O-K):** Subjek (S), Predikat (P), Objek (O), Pelengkap (Pel), dan Keterangan (K).  
    Contoh: Dia (S) menyeduh (P) kopi (O) di dapur (K).
  - **Jenis Kalimat Berdasarkan Tujuan Komunikasi:** Kalimat deklaratif (berita), interogatif (tanya), imperatif (perintah/permintaan), larangan, dan penyangkalan (negasi).

### 5. Semantik

- **Tujuan:** Memahami makna kata, frasa, dan kalimat secara harfiah maupun kias, serta mengidentifikasi hubungan dan potensi kerancuan makna.
- **Ruang Lingkup:**
  - **Sinonim:** Kesamaan atau kemiripan makna (melihat — menengok — memandang).
  - **Antonim:** Perlawanan makna (panas >< dingin; datang >< pergi).
  - **Makna Denotatif vs Konotatif:** Denotatif adalah makna lugas/apa adanya (kursi = tempat duduk); konotatif adalah makna tambahan/nilai rasa (kursi = jabatan).
  - **Polisemi:** Satu kata yang memiliki lebih dari satu makna yang masih saling berkaitan (kepala = bagian tubuh, kepala = pemimpin/ketua).
  - **Ambiguitas:** Ketaksaan makna akibat struktur frasa atau kalimat yang dapat ditafsirkan lebih dari satu cara (lukisan ibu = lukisan milik ibu, lukisan tentang ibu, atau lukisan karya ibu).

### 6. Pragmatik

- **Tujuan:** Memahami maksud sebenarnya dari penutur berdasarkan situasi, hubungan antarpenutur, dan konteks di luar struktur kalimat harfiah.
- **Ruang Lingkup:**
  - **Tindak Tutur (Bentuk vs Maksud):** Ketidaksesuaian antara bentuk kalimat sintaksis dan fungsi komunikatifnya (misalnya kalimat tanya yang berfungsi sebagai perintah halus).
  - **Implikatur (Makna Tersirat):** Pesan yang disampaikan secara tidak langsung tanpa diucapkan secara eksplisit.
  - **Prinsip Kesantunan:** Penggunaan penanda kesantunan (tolong, maaf, permisi, silakan) dan penghalusan penolakan agar interaksi tetap harmonis.
  - **Deiksis:** Kata yang rujukannya berpindah-pindah tergantung siapa yang berbicara, kapan, dan di mana (saya, kamu, sini, sana, sekarang, tadi).

### 7. Wacana & Percakapan

- **Tujuan:** Mengelola keterpaduan antarkalimat dan antargiliran bicara dalam interaksi panjang (multi-turn) agar percakapan terasa nyambung dan utuh.
- **Ruang Lingkup:**
  - **Konteks Percakapan:** Mempertahankan topik aktif dan riwayat informasi dari giliran sebelumnya.
  - **Rujukan (Anafora & Katafora):** Menautkan pronomina atau frasa penunjuk (itu, dia, hal tersebut, yang tadi) ke entitas yang sudah atau akan disebutkan.
  - **Elipsis (Pelesapan):** Penghilangan unsur kalimat yang sudah diketahui bersama dari konteks ("Mau kopi?" → "Mau." — melesapkan subjek dan objek).
  - **Giliran Bicara (Turn-Taking):** Mekanisme membuka percakapan, merespons, menyela, mengalihkan topik, mengklarifikasi, dan mengoreksi kesalahpahaman.
  - **Kohesi dan Koherensi:** Keterkaitan bentuk kebahasaan dan kepaduan logika makna antarbagian wacana.

### 8. Variasi Bahasa

- **Tujuan:** Memampukan sistem mengenali berbagai ragam bahasa Indonesia yang digunakan manusia sesuai situasi sosial, media komunikasi, dan tingkat keakraban.
- **Ruang Lingkup:**
  - **Baku vs Tidak Baku:** Perbedaan kesesuaian dengan kaidah standar (tidak vs nggak/gak; bagaimana vs gimana; sudah vs udah).
  - **Formal vs Informal:** Ragam resmi (surat dinas, presentasi) vs ragam santai (obrolan teman, keluarga).
  - **Lisan vs Tulisan:** Ragam lisan cenderung singkat, bergantung pada konteks situasi, dan banyak menggunakan partikel (sih, kok, deh, dong, ya), sedangkan ragam tulisan lebih lengkap secara sintaksis.
  - **Gaul / Slang / Kosakata Sehari-hari:** Ungkapan populer dalam percakapan urban (baper, santai aja, gas, gaskeun, mager, capek deh).

## Bagian 3 — Pembagian Tahap Pembelajaran

Pembelajaran bahasa Indonesia bagi ILIS dibagi ke dalam empat tahap berurutan. Setiap tahap menjadi prasyarat bagi tahap berikutnya.

### 🟢 TAHAP 1: Fondasi Dasar

- **Cakupan Materi:**
  - Pengenalan fonologi dasar, tanda baca utama (., ?, !, ,), dan normalisasi ejaan baku vs variasi penulisan umum.
  - Pengenalan lengkap 11 kelas kata menggunakan istilah linguistik baku (Nomina, Verba, Adjektiva, Adverbia, Pronomina, Numeralia, Preposisi, Konjungsi, Interjeksi, Artikula, Partikel).
  - Inventarisasi kata dasar berfrekuensi tinggi beserta makna leksikal dasarnya.
- **Tujuan Tahap:** Sistem mampu mengenali batas kata, menormalisasi variasi ejaan ringan, serta mengklasifikasikan kelas kata dan makna dasar setiap leksikon dengan akurat.

### 🟡 TAHAP 2: Pembentukan Kata & Kalimat Sederhana

- **Cakupan Materi:**
  - Morfologi dasar: membedakan fungsi dan perubahan makna akibat prefiks (meN-, di-, ber-, ter-), sufiks (-kan, -i, -an), dan konfiks (ke-...-an, peN-...-an), serta reduplikasi dasar.
  - Struktur frasa dan pola kalimat dasar S-P-O-K (membedakan pelaku, tindakan, sasaran, dan keterangan tempat/waktu).
  - Klasifikasi jenis kalimat secara sintaksis: kalimat deklaratif (berita), interogatif (tanya), imperatif (perintah), larangan (jangan), dan penyangkalan (tidak, bukan).
  - Semantik dasar: pengenalan sinonim umum, antonim dasar, dan makna denotatif yang lugas.
- **Tujuan Tahap:** Sistem memahami bagaimana kata dibentuk dan bagaimana kata-kata tersebut menyusun struktur kalimat tunggal yang utuh dan bermakna jelas.

### 🟠 TAHAP 3: Memahami Maksud & Konteks

- **Cakupan Materi:**
  - Pragmatik inti: membedakan bentuk gramatikal kalimat dengan maksud komunikatif sebenarnya:
    - "Bisa tolong…?" → bentuk interogatif, maksud permintaan bantuan.
    - "Nanti dulu" → frasa adverbial waktu, maksud penundaan atau penolakan halus.
    - "Belum" → adverbia negasi, maksud penyangkalan yang terikat pada rentang waktu hingga saat ini (berimplikasi masih mungkin terjadi di masa depan).
  - Pemahaman kalimat tidak lengkap (elipsis) dan penautan rujukan (anafora) ke giliran percakapan sebelumnya.
  - Penguasaan nuansa negasi (tidak untuk verba/adjektiva vs bukan untuk nomina), penanda waktu (sudah, sedang, akan, baru saja, tadi), dan modalitas (harus, boleh, bisa, mungkin, ingin).
- **Tujuan Tahap:** Sistem mampu menangkap apa yang sebenarnya dimaksudkan oleh penutur, bukan sekadar memproses kata-kata yang diucapkan secara harfiah.

### 🔴 TAHAP 4: Percakapan Utuh & Variasi Bahasa

- **Cakupan Materi:**
  - Pengelolaan wacana multi-turn: menjaga kesinambungan topik, mendeteksi perpindahan topik ("Ngomong-ngomong..."), menangani permintaan klarifikasi ("Maksudnya gimana?"), dan memproses koreksi pengguna ("Bukan itu maksudku...").
  - Pemahaman variasi bahasa: menjembatani ragam percakapan santai/informal/lisan (termasuk partikel ekspresif seperti sih, kok, deh, dong dan bentuk tidak baku) ke representasi makna yang dipahami sistem.
  - Pembacaan makna tersirat (implikatur), tingkat kesantunan, serta penanda nuansa emosi dalam bicara (ragu-ragu, terburu-buru, kesal, antusias, atau pasrah).
- **Tujuan Tahap:** Sistem mampu mengikuti alur percakapan alami antarmanusia dari awal hingga akhir secara luwes, kontekstual, dan responsif.

## Bagian 4 — Prioritas Khusus untuk ILIS

### Mengapa Pragmatik dan Wacana Mendapat Prioritas Utama?

Dalam percakapan manusia sehari-hari, komunikasi jarang berlangsung dalam bentuk kalimat baku yang lengkap dan harfiah. Manusia berbicara secara ekonomis (menghilangkan kata yang dianggap sudah dimengerti lawan bicara) dan tidak langsung (menyampaikan permintaan, penolakan, atau perasaan secara tersirat demi menjaga kesantunan).

Jika ILIS hanya mengandalkan sintaksis dan semantik harfiah tanpa Pragmatik dan Wacana:

- Sistem akan gagal mengenali bahwa pertanyaan seperti "Ada pulpen nggak?" adalah permintaan meminjam pulpen, bukan sekadar survei kepemilikan alat tulis.
- Sistem akan kehilangan jejak pada giliran bicara kedua atau ketiga ketika penutur hanya mengucapkan frasa singkat seperti "Yang itu aja" atau "Kenapa emangnya?".
- Sistem akan kaku menghadapi ragam lisan sehari-hari yang penuh dengan elipsis dan partikel nuansa.

Oleh karena itu, Pragmatik dan Wacana menjadi kunci utama yang mengubah ILIS dari sekadar mesin pencocok aturan menjadi sistem yang benar-benar memahami maksud percakapan manusia.

### Daftar 24 Contoh Kalimat Nyata Sehari-hari yang Mengandalkan Konteks & Maksud Tersirat

| No | Kalimat Sehari-hari | Bentuk Literal | Maksud Sebenarnya / Fungsi Pragmatis | Aspek Kunci |
|---:|---|---|---|---|
| 1 | "Bisa ambilkan?" | Kalimat tanya kemampuan | Permintaan tolong agar lawan bicara mengambilkan sesuatu | Tindak tutur tidak langsung |
| 2 | "Nanti saja." | Frasa keterangan waktu | Penundaan tindakan atau penolakan halus untuk saat ini | Implikatur penundaan |
| 3 | "Yang tadi itu." | Frasa penunjuk tanpa predikat | Merujuk kembali pada topik/objek yang dibahas pada giliran sebelumnya | Anafora & elipsis |
| 4 | "Aku juga." | Pronomina + adverbia | Menyatakan kesamaan pengalaman, pendapat, atau keinginan dengan lawan bicara | Elipsis & kohesi |
| 5 | "Bukan begitu maksudku." | Kalimat penyangkalan | Koreksi atas kesalahpahaman interpretasi dari giliran sebelumnya | Perbaikan wacana (repair) |
| 6 | "Ya terserah." | Partikel + adjektiva | Penyerahan keputusan, sering kali disertai nada pasrah atau kurang antusias | Nuansa emosi & kesantunan |
| 7 | "Belum." | Adverbia negasi | Menyatakan suatu peristiwa belum terjadi hingga saat ini, namun berpotensi terjadi nanti | Negasi terikat waktu |
| 8 | "Emang kenapa?" | Kalimat tanya alasan | Meminta penjelasan lebih lanjut atau menantang relevansi pernyataan sebelumnya | Giliran bicara & nuansa |
| 9 | "Panas banget ya hari ini." | Pernyataan cuaca | Basa-basi pembuka obrolan atau kode halus agar menyalakan pendingin/kipas | Implikatur percakapan |
| 10 | "Mau ke mana?" | Pertanyaan arah/tujuan | Sapaan ramah saat berpapasan (tidak selalu menuntut jawaban detail lokasi) | Fungsi fatis / kesantunan |
| 11 | "Boleh juga tuh." | Pernyataan izin/kemungkinan | Persetujuan antusias terhadap usulan atau ide lawan bicara | Modalitas & ragam lisan |
| 12 | "Nggak usah repot-repot." | Kalimat larangan | Penolakan sopan atas tawaran bantuan atau pemberian | Prinsip kesantunan |
| 13 | "Tunggu sebentar ya." | Perintah menunggu | Permintaan jeda waktu singkat sebelum melanjutkan aktivitas/pembicaraan | Manajemen giliran bicara |
| 14 | "Gimana jadinya?" | Kalimat tanya proses | Menanyakan kepastian akhir dari rencana yang sudah dibahas sebelumnya | Konteks wacana |
| 15 | "Kayaknya sih gitu." | Pernyataan dugaan | Persetujuan ragu-ragu; penutur tidak 100% yakin dengan faktanya | Modalitas epistemik |
| 16 | "Udah makan?" | Pertanyaan status aktivitas | Bentuk perhatian sosial atau ajakan makan bersama secara tidak langsung | Tindak tutur & budaya |
| 17 | "Lagi di jalan nih." | Keterangan lokasi | Pemberitahuan bahwa penutur sedang menuju lokasi dan belum bisa fokus penuh | Konteks situasi & deiksis |
| 18 | "Yang mana dulu?" | Pertanyaan pilihan | Meminta penentuan prioritas dari beberapa opsi yang muncul sebelumnya | Elipsis & penentuan urutan |
| 19 | "Maksudnya?" | Pertanyaan makna | Permintaan klarifikasi karena pernyataan sebelumnya dianggap kurang jelas/ambigu | Klarifikasi wacana |
| 20 | "Oh, pantesan." | Interjeksi + konjungsi | Menunjukkan pemahaman baru setelah mendapat informasi penyebab dari lawan bicara | Koherensi & penerimaan info |
| 21 | "Bentar, aku cek dulu." | Keterangan waktu + tindakan | Penundaan singkat untuk memverifikasi data sebelum memberi jawaban pasti | Manajemen giliran & status |
| 22 | "Nggak apa-apa kok." | Penyangkalan masalah | Menenangkan lawan bicara, meskipun dalam konteks tertentu bisa menyiratkan kecewa | Implikatur & nuansa emosi |
| 23 | "Terus?" | Konjungsi + tanda tanya | Mendorong lawan bicara melanjutkan cerita atau menanyakan konsekuensi berikutnya | Pemeliharaan giliran bicara |
| 24 | "Yaudah deh, gas." | Interjeksi + partikel + slang | Keputusan akhir untuk menyetujui dan segera menjalankan rencana | Variasi bahasa & penutup topik |

## Bagian 5 — Catatan Penting

- **Peta Arah, Bukan Daftar Tugas Mendesak:** Dokumen ini berfungsi sebagai kompas jangka panjang bagi pengembangan kemampuan bahasa ILIS. Tidak seluruh poin di dalamnya harus dikejar secara terburu-buru dalam satu waktu.
- **Selektivitas Dataset:** Tidak semua materi linguistik dalam kurikulum ini perlu langsung dimasukkan ke dalam dataset. Penambahan pola dan kaidah dilakukan secara selektif sesuai kebutuhan nyata yang ditemui saat pengujian percakapan.
- **Gerbang Uji Bertahap (Quality Gate):** Setiap tahap pembelajaran (Tahap 1 hingga Tahap 4) harus diuji dan dipastikan berjalan stabil terlebih dahulu sebelum melangkah ke tahap berikutnya, agar tidak terjadi penumpukan aturan yang saling bertabrakan.
- **Pemisahan dari Dataset Pengetahuan Umum:** Pengisian dan pengembangan dataset pengetahuan umum (DRAFT) tetap ditunda dan dipisahkan secara tegas dari kurikulum pemahaman bahasa ini, sehingga fokus sistem saat ini murni pada ketajaman memahami struktur dan maksud bahasa manusia.
