# TAHAP 04 — WACANA DAN VARIASI BAHASA

**Acuan utama:** `docs/KURIKULUM_PEMAHAMAN_BAHASA.md` — Tahap 4  
**Dasar acuan:** `docs/TAHAP_01_FONDASI_DASAR.md`, `docs/TAHAP_02_KATA_DAN_KALIMAT.md`, dan `docs/TAHAP_03_MAKSUD_DAN_KONTEKS.md`  
**Lokasi:** `docs/TAHAP_04_WACANA_DAN_VARIASI_BAHASA.md`  
**Branch:** `ilis-v2-development`  
**Status:** Dokumen Panduan Konsep (Non-Implementasi)

---

## 1 — Pendahuluan

### Tujuan Tahap 4

Tahap 4 menyatukan kemampuan dari tahap sebelumnya agar ILIS dapat memahami percakapan yang berlangsung dari satu giliran ke giliran berikutnya, bukan hanya memahami kalimat secara terpisah.

- Tahap 1 membantu mengenali bentuk dasar bahasa Indonesia.
- Tahap 2 membantu memahami pembentukan kata dan susunan kalimat.
- Tahap 3 membantu memahami maksud, rujukan, dan konteks sebuah ujaran.
- Tahap 4 membawa semua kemampuan tersebut ke dalam alur percakapan utuh dan ragam bahasa yang berbeda.

Fokusnya bergeser dari **kalimat terpisah** menjadi **percakapan yang berkesinambungan**. Sistem perlu memperhatikan apa yang sudah dibicarakan, siapa yang sedang berbicara, bagaimana topik berkembang, kapan topik berubah, dan ragam bahasa apa yang sedang digunakan.

### Prinsip utama

> Bahasa tidak hanya perlu dipahami dengan benar, tetapi juga digunakan dan ditanggapi secara tepat pada tempatnya.

Tidak ada satu gaya bahasa yang selalu paling tepat untuk semua keadaan. Cara berbicara kepada teman dekat dapat berbeda dari cara berbicara dalam rapat, pelayanan, atau percakapan dengan orang yang baru dikenal.

### Batasan

Dokumen ini adalah panduan pemahaman konsep, bukan bukti bahwa sistem sudah mampu menangani semua percakapan secara otomatis dan sempurna. Contoh-contohnya menjadi bahan belajar dan acuan evaluasi konseptual, bukan otomatis menjadi aturan runtime atau data pengetahuan.

Jika rujukan, maksud, atau suasana percakapan belum cukup jelas, sistem harus mempertahankan ketidakpastian atau meminta klarifikasi. Jangan mengarang konteks yang tidak tersedia.

---

## 2 — Wacana: Percakapan yang Berkesinambungan

Wacana adalah rangkaian ujaran yang saling berhubungan. Makna sebuah jawaban sering baru jelas jika dihubungkan dengan giliran bicara sebelumnya.

Contoh:

> A: Besok jadi bertemu?
>
> B: Jadi. Jam tiga, seperti rencana kemarin.
>
> A: Oke, di tempat yang sama?
>
> B: Iya, di sana.

Jawaban seperti "Jadi", "jam tiga", dan "di sana" tidak berdiri sendiri. Pemahamannya bergantung pada konteks percakapan.

### A. Giliran Bicara dan Pergantian Peran

Dalam percakapan, peserta biasanya bergantian menjadi penutur dan pendengar. Pergantian ini membantu percakapan berjalan dan memberi kesempatan kepada setiap orang untuk menyampaikan maksudnya.

**Mengambil giliran bicara:**
- "Menurut saya, ada cara yang lebih sederhana."
- "Kalau begitu, saya ingin menambahkan sesuatu."
- "Boleh saya menanggapi?"

**Memberi kesempatan kepada lawan bicara:**
- "Bagaimana menurutmu?"
- "Kamu ada pendapat lain?"
- "Silakan, saya dengarkan."

**Menutup atau mengakhiri percakapan:**
- "Sudah dulu ya."
- "Baik, kita lanjutkan lain waktu."
- "Sampai ketemu nanti."

**Hal yang perlu dipahami:**
- Giliran bicara tidak selalu berganti secara kaku. Dalam percakapan akrab, orang kadang menyahut atau berbicara hampir bersamaan.
- Menyela dapat terjadi untuk mengklarifikasi, menunjukkan antusiasme, atau mengingatkan sesuatu. Namun, terlalu sering memotong dapat membuat lawan bicara sulit menyelesaikan maksudnya.
- Ungkapan seperti "terus?", "oh begitu", atau "iya, lalu?" dapat menjadi tanda bahwa pendengar mengikuti cerita dan mempersilakan penutur melanjutkan.
- Sistem tidak boleh menganggap setiap jeda sebagai akhir percakapan. Jeda dapat berarti penutur sedang berpikir atau belum selesai.

### B. Menjaga Kesinambungan Topik

Kesinambungan topik berarti tetap memahami hal yang sedang dibicarakan dan menghubungkan jawaban dengan informasi yang relevan dari giliran sebelumnya.

Contoh penanda kesinambungan:
- "Tadi kamu bilang..."
- "Mengenai hal itu..."
- "Kalau kembali ke rencana tadi..."
- "Jadi, maksudmu adalah..."
- "Seperti yang kita bahas sebelumnya..."

**Prinsip pemahaman:**
1. Kenali topik atau hal yang sedang dibahas.
2. Hubungkan kata ganti, kata penunjuk, atau jawaban singkat dengan konteks yang paling masuk akal.
3. Pertahankan topik selama belum ada tanda yang cukup bahwa pembicaraan berpindah.
4. Jika ada beberapa rujukan yang sama-sama mungkin, jangan memilih secara asal. Minta penjelasan.

Contoh:

> A: Aku sedang mencari buku sejarah untuk tugas.
>
> B: Buku sejarah yang tentang Indonesia?
>
> A: Iya, yang membahas masa kemerdekaan.
>
> B: Oh, berarti kamu mencari buku sejarah Indonesia tentang masa kemerdekaan.

B merangkum informasi untuk memastikan bahwa topik dan maksud A dipahami dengan tepat.

### C. Mengubah Topik dengan Halus

Perubahan topik adalah perpindahan pembicaraan dari satu hal ke hal lain. Penanda perubahan topik membantu lawan bicara memahami bahwa pembicaraan sebelumnya sedang ditinggalkan atau ditunda.

Contoh penanda:
- "Ngomong-ngomong, tadi kamu bilang mau ke mana?"
- "Oh iya, ada satu hal lagi..."
- "Beralih sedikit ke hal lain..."
- "Sebelum lupa, aku mau menanyakan sesuatu."

Contoh:

> A: Jadi besok kita bertemu jam tiga, ya?
>
> B: Iya, di tempat yang sama?
>
> A: Betul. Ngomong-ngomong, kamu sudah membawa bukunya?
>
> B: Wah, aku lupa membawanya. Maaf ya!

Analisis:
- Topik pertama adalah waktu dan tempat pertemuan.
- Ungkapan "Ngomong-ngomong" memberi tanda bahwa A membuka topik lain.
- Topik kedua adalah buku yang perlu dibawa.
- Jawaban B harus dipahami dalam topik baru, bukan sebagai jawaban tentang waktu atau tempat pertemuan.

**Catatan:** Perubahan topik yang tiba-tiba tanpa penanda dapat membingungkan. Namun, tidak semua perpindahan topik harus memakai ungkapan khusus. Konteks, jeda, dan isi ujaran juga dapat menunjukkan perubahan. Sistem sebaiknya tidak menyimpulkan perpindahan topik hanya karena satu kata yang kebetulan muncul.

### D. Klarifikasi dan Koreksi

Klarifikasi dilakukan ketika suatu ujaran belum jelas. Koreksi dilakukan ketika ada bagian pemahaman atau penyampaian yang perlu diperbaiki.

**Meminta penjelasan:**
- "Maaf, saya kurang mengerti maksudnya."
- "Bisa diulang sebentar?"
- "Yang kamu maksud bagian yang mana?"
- "Maksudnya bagaimana?"

**Memperbaiki kesalahpahaman:**
- "Bukan begitu maksud saya. Maksud saya adalah..."
- "Sepertinya ada yang kurang tepat dipahami."
- "Bukan yang itu, tetapi yang sebelumnya."

**Memastikan pemahaman:**
- "Jadi yang kamu maksud adalah ..., benar begitu?"
- "Kalau saya tidak salah menangkap, kamu ingin mengatakan bahwa ..."

**Mengoreksi diri sendiri:**
- "Eh, maksud saya bukan itu."
- "Maaf, saya salah menyebutkan. Seharusnya..."
- "Saya ralat, yang benar adalah..."

**Prinsip pemahaman:**
- Koreksi dari penutur merupakan informasi baru tentang maksud yang ingin disampaikan.
- Jika pengguna berkata "Bukan itu maksudku", sistem harus meninjau kembali interpretasi sebelumnya, bukan terus mempertahankan tafsir yang sudah dibantah.
- Klarifikasi sebaiknya menanyakan bagian yang memang belum jelas, bukan mengulang seluruh percakapan tanpa kebutuhan.
- Koreksi tidak selalu berarti seluruh informasi sebelumnya salah. Perhatikan bagian mana yang secara khusus diperbaiki.

### E. Menangani Kalimat yang Terpotong atau Tidak Lengkap

Dalam percakapan alami, orang sering berhenti di tengah kalimat, mengubah susunan kata, atau melanjutkan maksudnya pada giliran berikutnya.

Contoh:

> A: Jadi maksudnya kalau begini...
>
> B: Kita atur nanti saja?
>
> A: Iya, betul. Kita bicarakan lagi setelah jadwalnya jelas.

Contoh lain:

> A: Tolong ambil yang...
>
> B: Yang di meja?
>
> A: Iya, yang di meja sebelah kanan.

**Hal yang perlu dipahami:**
- Ujaran yang tidak lengkap belum tentu tidak bermakna.
- Pendengar dapat membantu melengkapi maksud berdasarkan konteks yang sudah jelas.
- Jika bagian yang hilang menentukan makna, jangan menebak terlalu jauh. Tanyakan atau tunggu kelanjutannya.
- Sistem tidak perlu memaksa setiap ujaran menjadi kalimat lengkap sebelum dapat memahami maksud umumnya.
- Tanda elipsis (...), jeda, atau kalimat yang terhenti dapat menunjukkan keraguan, jeda berpikir, atau ujaran yang belum selesai; maknanya bergantung pada konteks.

---

## 3 — Variasi Bahasa: Beda Situasi, Beda Cara Bicara

Bahasa Indonesia digunakan dalam berbagai situasi. Bentuk baku, tidak baku, formal, santai, lisan, dan tulisan memiliki fungsi serta konteks pemakaian masing-masing.

**Prinsip penting:** ragam tidak baku atau santai bukan berarti penuturnya tidak memahami bahasa. Bentuk tersebut merupakan variasi pemakaian bahasa. Sistem perlu mengenali maknanya tanpa memaksa semua ujaran mengikuti satu pola formal.

### A. Bahasa Baku dan Tidak Baku

| Situasi | Bentuk baku | Bentuk tidak baku / sehari-hari |
|---|---|---|
| Salam pagi | Selamat pagi | Pagi / Hai |
| Bertanya kabar | Apa kabar? | Gimana kabarnya? / Apa kabar nih? |
| Mengucapkan terima kasih | Terima kasih | Makasih / Makasih ya |
| Meminta maaf | Saya mohon maaf | Maaf ya / Maafkan aku |
| Berpamitan | Saya pamit dulu | Dadah / Sampai ketemu / Aku pergi dulu |
| Menyatakan tidak tahu | Saya tidak tahu | Aku nggak tahu / Gak tahu |

**Catatan:**
- Bentuk baku lazim digunakan dalam tulisan resmi, pendidikan, dokumen, dan situasi yang menuntut ragam standar.
- Bentuk sehari-hari lazim digunakan dalam percakapan informal.
- Bentuk tidak baku dapat memiliki arti yang sama atau hampir sama dengan bentuk bakunya.
- Ejaan seperti "gak", "nggak", dan "enggak" memiliki variasi penulisan dalam percakapan informal. Sistem perlu mengenali variasi yang umum tanpa menganggap semuanya sebagai bentuk ejaan resmi.
- Perbedaan ragam tidak selalu mengubah maksud utama, tetapi dapat memengaruhi kesan akrab, santai, atau resmi.

### B. Ragam Formal dan Santai

| Aspek | Formal / resmi | Santai / akrab |
|---|---|---|
| Kata ganti orang | Saya; Anda atau sapaan yang sesuai | Aku; kamu; kau |
| Menyatakan rencana | Saya akan pergi. | Aku mau pergi. |
| Menawarkan bantuan | Apakah ada yang bisa saya bantu? | Ada yang bisa kubantu? / Bantu apa? |
| Meminta bantuan | Bisakah Anda membantu saya? | Bisa bantu aku? |
| Penutup | Terima kasih atas perhatian Anda. | Makasih ya, sampai ketemu. |

**Pemilihan ragam bergantung pada situasi:**
- Hubungan antara penutur dan lawan bicara.
- Tujuan percakapan.
- Tempat dan suasana komunikasi.
- Kebiasaan atau pilihan sapaan yang digunakan bersama.

Kata "Anda" tidak selalu menjadi pilihan paling alami untuk setiap percakapan formal. Dalam situasi tertentu, sapaan seperti "Bapak", "Ibu", jabatan, atau nama lebih sesuai. Sebaliknya, orang yang baru dikenal pun kadang berbicara santai jika situasinya memang mendukung.

Sistem sebaiknya mengikuti ragam yang sesuai dan menghormati cara pengguna menyapa, tanpa terlalu cepat menilai hubungan atau tingkat keakraban mereka.

### C. Bahasa Lisan dan Tulisan

**Bahasa lisan:**
- Sering memakai kalimat pendek atau tidak lengkap.
- Memiliki jeda, pengulangan, dan perbaikan spontan.
- Dapat memakai partikel penegas atau nuansa seperti "lah", "dong", "nih", "sih", "kok", dan "deh".
- Mengandalkan situasi bersama, intonasi, ekspresi, dan konteks.

**Bahasa tulisan:**
- Umumnya lebih terstruktur dan dapat disunting sebelum dikirim.
- Dalam konteks resmi, biasanya mengikuti ejaan dan tanda baca baku.
- Dalam percakapan digital, tulisan dapat menyerupai bahasa lisan, misalnya "Oke, aku OTW" atau "Nanti aku kabarin".

**Contoh perbedaan:**

| Lisan / percakapan digital | Bentuk lebih baku |
|---|---|
| Aku lagi di jalan. | Saya sedang dalam perjalanan. |
| Nanti aku kabarin, ya. | Nanti saya akan memberi kabar. |
| Gimana kalau besok? | Bagaimana jika besok? |
| Aku nggak tahu. | Saya tidak tahu. |

**Catatan untuk ILIS:** masukan lisan yang ditranskripsikan dan tulisan percakapan sama-sama dapat mengandung bentuk informal. Sistem perlu mengenali bentuk dan maksudnya; jangan otomatis mengubah gaya pengguna atau menganggap bentuk informal sebagai kesalahan pemahaman.

### D. Ungkapan Umum dan Bahasa Gaul yang Umum

Ungkapan sehari-hari merupakan bagian dari variasi bahasa. Bentuknya dapat lebih pendek, lebih akrab, atau berbeda dari bentuk baku, tetapi tetap dapat dipahami dalam konteks.

| Ungkapan sehari-hari | Makna umum |
|---|---|
| Gimana? | Bagaimana? |
| Gak tahu / nggak tahu | Tidak tahu |
| Lagi di jalan | Sedang dalam perjalanan |
| Nanti dulu ya | Ditunda untuk saat ini |
| Bentar | Sebentar |
| Makasih | Terima kasih |
| Udah | Sudah |
| Kayaknya | Sepertinya |
| Gak apa-apa | Tidak apa-apa |

**Batas cakupan tahap ini:**
- Fokus pada ungkapan umum yang banyak dipakai dan maknanya relatif mudah dikenali.
- Belum mencakup seluruh slang daerah, istilah komunitas, bahasa kelompok tertentu, atau ungkapan viral yang berubah cepat.
- Satu ungkapan dapat memiliki makna berbeda menurut konteks. Misalnya, "terserah" dapat berarti menyerahkan pilihan, tetapi dalam situasi tertentu dapat terdengar kurang antusias. Jangan menetapkan satu emosi hanya dari kata itu.
- Jika menemukan istilah yang tidak dikenal atau sangat lokal, sistem sebaiknya meminta penjelasan atau menyatakan belum memahami istilah tersebut.

---

## 4 — Nuansa Komunikasi dan Makna Tersirat yang Sederhana

Percakapan bukan hanya pertukaran informasi. Penutur juga menjaga hubungan, menunjukkan sikap, dan menyesuaikan cara menyampaikan sesuatu.

### A. Kesantunan Dasar

**Meminta bantuan:**
- "Tolong bantu saya sebentar."
- "Boleh minta bantuan?"
- "Bisa tolong ambilkan buku itu?"

Kata "tolong", "boleh", dan "bisa" dapat membuat permintaan terdengar lebih santun. Namun, kesantunan tidak hanya ditentukan oleh satu kata; hubungan, situasi, dan cara penyampaian juga berpengaruh.

**Menolak dengan sopan:**
- "Maaf, kali ini saya belum bisa."
- "Terima kasih tawarannya, tetapi saya tidak bisa ikut."
- "Boleh lain kali? Sekarang saya sedang ada keperluan."

Penolakan dapat disertai alasan atau alternatif jika sesuai. Sistem tidak boleh mengubah penolakan menjadi persetujuan hanya karena penutur memakai kata yang halus.

**Menjawab dengan jujur:**
- "Saya belum yakin, jadi belum bisa memastikannya."
- "Saya belum tahu soal itu."
- "Boleh saya periksa dulu?"

**Mengoreksi dengan halus:**
- "Mungkin maksudnya lebih mendekati..."
- "Sepertinya ada sedikit kekeliruan pada bagian itu."
- "Boleh saya luruskan sedikit?"

### B. Memahami Nuansa Emosi Secara Hati-hati

Beberapa ungkapan dapat memberi petunjuk tentang suasana atau sikap penutur.

| Ungkapan | Kemungkinan nuansa |
|---|---|
| "Aduh, lama banget ya." | Mungkin menunjukkan ketidaksabaran atau keluhan ringan. |
| "Wah, hebat sekali!" | Dapat menunjukkan kekaguman atau pujian. |
| "Yah, sayang sekali." | Dapat menunjukkan kekecewaan. |
| "Asyik, akhirnya selesai!" | Dapat menunjukkan rasa senang atau lega. |
| "Hmm, aku belum yakin." | Dapat menunjukkan keraguan. |

**Peringatan penting:**
- Ungkapan di atas hanya petunjuk, bukan bukti pasti tentang emosi seseorang.
- "Wah, hebat sekali!" bisa tulus, bercanda, atau sarkastis bergantung pada konteks dan cara penyampaian.
- Teks saja sering tidak cukup untuk mengetahui intonasi, ekspresi wajah, atau keadaan batin penutur.
- Jangan menyimpulkan emosi kuat dari satu kalimat. Perhatikan keseluruhan percakapan dan tetap gunakan bahasa yang tidak menghakimi.
- Jika bukti tidak cukup, gunakan ungkapan seperti "mungkin", "terdengar seperti", atau tidak menyimpulkan emosi sama sekali.

### C. Mengetahui Batas Pengetahuan Sendiri

Sistem harus mampu membedakan informasi yang diketahui, dugaan, dan hal yang belum dapat dipastikan.

Contoh jawaban yang jujur:
- "Saya belum tahu pasti soal itu."
- "Itu di luar informasi yang saya miliki saat ini."
- "Maaf, saya belum bisa memastikan jawabannya."
- "Saya perlu informasi tambahan agar tidak salah menjawab."

**Prinsip:** lebih baik jujur belum tahu daripada memberikan jawaban yang dibuat-buat hanya agar terlihat pintar.

Jika konteks percakapan tidak cukup, sistem dapat:
1. Menyebutkan bagian yang belum jelas.
2. Meminta satu klarifikasi yang paling diperlukan.
3. Memisahkan fakta yang diketahui dari dugaan.
4. Tidak mengisi kekosongan dengan informasi yang tidak pernah diberikan.

---

## 5 — Contoh Percakapan Utuh dan Analisisnya

Contoh berikut menunjukkan bagaimana makna dibangun dari beberapa giliran bicara, bukan hanya dari satu kalimat.

### Contoh 1: Percakapan Santai

> A: Halo, pagi!
>
> B: Pagi, gimana kabar kamu?
>
> A: Baik, terima kasih. Kamu sendiri?
>
> B: Juga baik, makasih ya.

**Analisis:**
- Giliran bicara berlangsung bergantian.
- Alurnya: sapaan → pertanyaan kabar → jawaban → pertanyaan balik → jawaban.
- "Kamu sendiri?" dipahami sebagai pertanyaan balik tentang kabar B, bukan pertanyaan yang berdiri sendiri.
- "Juga baik" merupakan jawaban singkat yang maknanya bergantung pada pertanyaan sebelumnya.
- Ragamnya santai, tetapi tetap sopan.

### Contoh 2: Mengubah Topik

> A: Jadi besok kita bertemu jam 3, ya?
>
> B: Iya, di tempat yang sama?
>
> A: Betul. Ngomong-ngomong, kamu sudah bawa bukunya?
>
> B: Wah, aku lupa bawa. Maaf ya!
>
> A: Tidak apa-apa, besok saja juga boleh.

**Analisis:**
- Topik pertama: waktu dan tempat pertemuan.
- "Ngomong-ngomong" menjadi penanda perpindahan ke topik kedua.
- Topik kedua: buku yang perlu dibawa.
- "Aku lupa bawa" merujuk pada buku yang baru saja ditanyakan.
- "Tidak apa-apa" menunjukkan penerimaan atau upaya menenangkan lawan bicara dalam konteks ini.
- Sistem perlu mengikuti topik terbaru tanpa kehilangan informasi bahwa pertemuan berlangsung besok.

### Contoh 3: Meminta Klarifikasi

> A: Saya pikir kita sebaiknya mulai dari yang termudah.
>
> B: Maaf, yang kamu maksud termudah itu yang mana?
>
> A: Maksud saya, langkah pertama yang tidak membutuhkan persiapan rumit.
>
> B: Oh, mengerti. Setuju.

**Analisis:**
- B tidak langsung menebak arti "termudah".
- B meminta klarifikasi secara sopan.
- A menjelaskan maksud yang sebelumnya belum cukup spesifik.
- Setelah mendapat penjelasan, B menyatakan bahwa ia memahami dan setuju.
- Klarifikasi memperbaiki pemahaman tanpa harus mengganti seluruh topik.

### Contoh 4: Ragam Santai dan Ujaran Tidak Lengkap

> A: Besok jadi ikut?
>
> B: Kayaknya bisa, tapi aku...
>
> A: Masih ada urusan?
>
> B: Iya, harus antar adik dulu. Kalau selesai cepat, aku menyusul.
>
> A: Oke, kabari saja nanti.

**Analisis:**
- "Kayaknya" menunjukkan dugaan atau kepastian yang belum penuh.
- B menghentikan kalimat sebelum selesai; A menawarkan kemungkinan maksud berdasarkan konteks.
- B kemudian mengonfirmasi dan melengkapi informasi.
- "Aku menyusul" dipahami dalam konteks rencana kegiatan besok.
- Sistem tidak boleh menganggap B sudah pasti ikut sebelum syaratnya jelas.

### Contoh 5: Koreksi dan Perbaikan Kesalahpahaman

> A: Jadi kamu mau rapatnya dipindah ke hari Jumat?
>
> B: Bukan begitu maksudku. Aku hanya bilang hari Jumat lebih memungkinkan.
>
> A: Oh, jadi belum diputuskan, ya?
>
> B: Betul. Kita tunggu konfirmasi yang lain dulu.

**Analisis:**
- A membuat kesimpulan yang terlalu jauh dari ucapan B.
- B mengoreksi interpretasi A.
- A memperbarui pemahamannya: Jumat baru merupakan pilihan yang memungkinkan, bukan keputusan final.
- "Betul" mengonfirmasi ringkasan A.
- Sistem harus mengikuti koreksi terbaru dan tidak lagi menyatakan bahwa jadwal sudah dipindahkan.

---

## 6 — Latihan Pemahaman Wacana

Latihan ini hanya untuk pembelajaran konsep. **Bukan dataset, bukan kasus evaluasi resmi, dan tidak boleh otomatis dimasukkan ke JSONL.**

### Bagian A — Lanjutkan Percakapan

Lengkapi jawaban yang wajar dan sopan. Jawaban lain yang maknanya sesuai juga dapat diterima.

1. A: Terima kasih banyak atas bantuannya.  
   B: ____________________  
   Contoh jawaban: "Sama-sama." / "Dengan senang hati."

2. A: Maaf, saya belum selesai seperti yang dijanjikan.  
   B: ____________________  
   Contoh jawaban: "Tidak apa-apa, santai saja." / "Baik, kabari saya kalau sudah selesai."

### Bagian B — Kenali Perubahan Topik

Perhatikan kalimat berikut:

> "Saya setuju dengan pendapatmu. Oh ya, kapan kita akan mulai pengerjaannya?"

Bagian yang berfungsi menandai perubahan topik adalah **"Oh ya"**. Pertanyaan tentang kapan pengerjaan dimulai membuka pembicaraan baru setelah pernyataan persetujuan.

### Bagian C — Pilih Ragam yang Sesuai

Kamu sedang berbicara dengan seseorang yang baru pertama kali ditemui dalam situasi resmi.

Pertanyaan: "Siapa nama Anda?"

- a) "Aku Budi, kamu siapa?"
- b) "Nama saya Budi. Boleh saya tahu nama Anda?"

**Contoh jawaban yang paling sesuai: b.** Bentuk tersebut lebih formal dan menjaga kesantunan dalam situasi resmi. Dalam situasi santai, pilihan a juga dapat sesuai jika kedua pihak nyaman menggunakan ragam akrab.

### Bagian D — Pahami Koreksi

> A: Jadi kamu tidak jadi datang?
>
> B: Bukan begitu. Aku terlambat sedikit, tetapi tetap datang.

**Pertanyaan:** Apa yang perlu diperbaiki dari pemahaman A?

**Jawaban:** Bukan berarti B membatalkan kedatangan. B hanya menyatakan akan terlambat. Sistem harus memperbarui pemahamannya berdasarkan koreksi tersebut.

---

## 7 — Catatan Penting dan Kriteria Penyelesaian

### Kriteria Pemahaman Tahap 4

Secara konseptual, Tahap 4 dapat dianggap dipahami apabila sistem mampu menunjukkan perilaku berikut dalam contoh dan pengujian yang sesuai:

- Mengikuti alur percakapan dari satu giliran ke giliran berikutnya.
- Menjaga kesinambungan topik dan mengenali rujukan yang bergantung pada konteks.
- Mengenali penanda perubahan topik tanpa kehilangan konteks yang masih relevan.
- Menangani permintaan klarifikasi, koreksi, dan perbaikan kesalahpahaman.
- Memahami ujaran pendek, elipsis, dan kalimat yang belum lengkap secara hati-hati.
- Mengenali perbedaan ragam baku, tidak baku, formal, santai, lisan, dan tulisan.
- Memahami ungkapan sehari-hari yang umum tanpa menganggap ragam informal sebagai bahasa yang otomatis salah.
- Menyesuaikan kesantunan dan gaya jawaban dengan situasi yang cukup jelas.
- Tidak mengarang maksud, rujukan, emosi, atau fakta ketika bukti percakapan belum memadai.

### Batasan yang Harus Diingat

- Sistem belum tentu dapat menebak emosi tersembunyi atau sarkasme halus tanpa konteks yang jelas.
- Sistem tidak boleh menganggap semua bentuk informal memiliki satu makna tetap.
- Sistem tidak boleh menganggap setiap perubahan topik sebagai perpindahan permanen; topik lama dapat dirujuk kembali.
- Sistem tidak boleh menganggap semua ujaran yang terpotong dapat dilengkapi dengan aman.
- Sistem harus mengakui ketidakpastian dan meminta klarifikasi bila diperlukan.

### Prinsip Utama

> Dengarkan alur percakapan, pahami maksud dan konteksnya, lalu tanggapi dengan tepat.

> Lebih baik jujur belum tahu daripada asal menjawab hanya supaya terlihat pintar.

### Status Dokumen

Dokumen ini merupakan panduan konsep untuk Tahap 4. Penyelesaiannya tidak berarti seluruh kemampuan telah diterapkan atau lulus pengujian runtime.

Dokumen ini **tidak**:
- mengubah dataset JSONL atau status fakta;
- mengubah kode, konfigurasi, atau perilaku runtime;
- menambahkan pola ke dataset;
- menyatakan Tahap 4 telah terimplementasi atau tervalidasi secara teknis.

Implementasi, pemilihan materi dataset, dan pengujian harus dilakukan secara terpisah melalui proses evaluasi dan persetujuan yang berlaku.
