# DAFTAR DASAR TAHAP 04 — WACANA & VARIASI BAHASA

**Acuan utama:** `docs/TAHAP_04_WACANA_DAN_VARIASI_BAHASA.md`  
**Dasar acuan:** `docs/DAFTAR_DASAR_TAHAP_01.md`, `docs/DAFTAR_DASAR_TAHAP_02.md`, dan `docs/DAFTAR_DASAR_TAHAP_03.md`  
**Branch:** `ilis-v2-development`  
**Status:** Daftar Referensi — BELUM DIMUAT KE DATASET AKTIF  
**Cakupan:** kesinambungan percakapan, giliran bicara, pengelolaan topik, klarifikasi dan koreksi, variasi ragam bahasa, serta prinsip komunikasi  
**Batas perubahan:** hanya dokumen ini; tidak mengubah dataset JSONL, kode, konfigurasi runtime, atau branch `main`.

---

## 1 — Wacana: Percakapan Berkesinambungan

Wacana adalah rangkaian ujaran yang saling berhubungan. Makna sebuah jawaban sering bergantung pada giliran bicara sebelumnya. Karena itu, percakapan perlu dipahami sebagai satu alur, bukan kumpulan kalimat yang berdiri sendiri.

### A. Giliran Bicara dan Pergantian Peran

Peserta percakapan bergantian menjadi penutur dan pendengar. Ungkapan tertentu membantu seseorang mengambil giliran, memberi kesempatan kepada orang lain, atau mengakhiri percakapan.

**1. Mengambil giliran bicara**

Fungsi: memberi tanda bahwa penutur ingin mulai menyampaikan pendapat, menanggapi, atau menambahkan informasi.

| Ungkapan | Contoh pemakaian |
|---|---|
| “Menurut saya …” | “Menurut saya, kita sebaiknya mulai dari bagian yang paling mudah.” |
| “Kalau begitu …” | “Kalau begitu, saya ingin mengusulkan cara lain.” |
| “Boleh saya menambahkan?” | “Boleh saya menambahkan? Ada satu hal yang belum dibahas.” |

Contoh tambahan yang juga wajar: “Saya ingin menanggapi sedikit.” Ungkapan mengambil giliran tidak otomatis berarti penutur menolak pendapat sebelumnya.

**2. Memberi giliran bicara**

Fungsi: mempersilakan lawan bicara menyampaikan pendapat, menjawab, atau melanjutkan cerita.

| Ungkapan | Contoh pemakaian |
|---|---|
| “Bagaimana menurutmu?” | “Itu pendapat saya. Bagaimana menurutmu?” |
| “Kamu ada pendapat lain?” | “Kita sudah mendengar dua usulan. Kamu ada pendapat lain?” |
| “Silakan, saya dengarkan.” | “Kalau kamu ingin menjelaskan lebih lanjut, silakan, saya dengarkan.” |

Memberi giliran tidak berarti memaksa orang lain berbicara. Lawan bicara boleh belum memiliki pendapat atau memilih untuk tidak menanggapi.

**3. Menutup percakapan**

Fungsi: memberi tanda bahwa percakapan atau bagian percakapan akan diakhiri, ditunda, atau dilanjutkan pada kesempatan lain.

| Ungkapan | Contoh pemakaian |
|---|---|
| “Sudah dulu ya.” | “Saya harus melanjutkan pekerjaan. Sudah dulu ya.” |
| “Sampai ketemu nanti.” | “Terima kasih sudah datang. Sampai ketemu nanti.” |
| “Kita lanjutkan lain waktu.” | “Sepertinya waktunya sudah habis. Kita lanjutkan lain waktu.” |

Penutup dapat menandai akhir percakapan, tetapi tidak selalu berarti hubungan atau topiknya selesai untuk selamanya. “Kita lanjutkan lain waktu” justru menunjukkan kemungkinan percakapan diteruskan kemudian.

**Hal yang perlu diperhatikan:**
- Giliran bicara tidak selalu berganti secara kaku. Dalam percakapan akrab, peserta kadang menyahut atau berbicara hampir bersamaan.
- Jeda tidak otomatis berarti percakapan sudah selesai. Penutur mungkin sedang berpikir atau belum menyelesaikan ucapannya.
- Sistem tidak boleh menganggap setiap pertanyaan sebagai undangan untuk mengambil alih seluruh percakapan.
- Jika pengguna masih melanjutkan penjelasan, beri ruang dan jangan buru-buru menutup topik.

### B. Menjaga Kesinambungan Topik

Menjaga kesinambungan topik berarti menghubungkan ujaran terbaru dengan hal yang relevan dari percakapan sebelumnya.

| Ungkapan | Fungsi | Contoh |
|---|---|---|
| “Tadi kamu bilang …” | Mengacu pada informasi yang disampaikan sebelumnya | “Tadi kamu bilang ingin berangkat pagi. Apakah rencananya masih sama?” |
| “Mengenai hal itu …” | Melanjutkan topik yang sedang dibahas | “Mengenai hal itu, saya ingin memastikan satu bagian.” |
| “Jadi maksudmu adalah …, benar begitu?” | Merangkum untuk memastikan pemahaman | “Jadi maksudmu jadwalnya belum ditetapkan, benar begitu?” |

**Prinsip kesinambungan:**
1. Kenali topik yang sedang aktif dari percakapan yang tersedia.
2. Hubungkan kata ganti, kata penunjuk, atau jawaban singkat dengan rujukan yang paling masuk akal.
3. Pertahankan topik selama belum ada tanda yang cukup bahwa pembicaraan berpindah.
4. Gunakan ringkasan singkat jika perlu memastikan pemahaman.
5. Jika ada beberapa rujukan yang sama-sama mungkin, tanyakan bagian yang belum jelas.

Contoh:

> A: Aku sedang mencari buku untuk tugas.
>
> B: Buku yang tentang sejarah?
>
> A: Iya, yang membahas masa kemerdekaan.
>
> B: Jadi, kamu mencari buku sejarah tentang masa kemerdekaan.

B menghubungkan jawaban A dengan topik sebelumnya. B tidak menambahkan judul atau isi buku yang belum disebutkan.

### C. Mengubah Topik dengan Halus

Perubahan topik adalah perpindahan pembicaraan dari satu hal ke hal lain. Penanda topik membantu lawan bicara mengikuti perpindahan tersebut.

| Penanda | Fungsi | Contoh |
|---|---|---|
| “Ngomong-ngomong …” | Memperkenalkan hal lain secara santai | “Ngomong-ngomong, kamu sudah makan?” |
| “Oh iya, ada satu hal …” | Mengingatkan atau membuka hal lain | “Oh iya, ada satu hal yang ingin saya tanyakan.” |
| “Beralih sedikit ke hal lain …” | Menandai perpindahan topik dengan jelas | “Beralih sedikit ke hal lain, bagaimana perkembangan tugasmu?” |

Contoh:

> A: Besok kita bertemu pukul tiga, ya?
>
> B: Iya, di tempat yang sama?
>
> A: Betul. Ngomong-ngomong, kamu sudah membawa bukunya?
>
> B: Belum, nanti saya bawa.

**Analisis:**
- Topik pertama adalah waktu dan tempat pertemuan.
- “Ngomong-ngomong” menandai bahwa A mulai membicarakan hal lain.
- Topik kedua adalah buku yang perlu dibawa.
- Jawaban B harus dihubungkan dengan pertanyaan tentang buku, bukan pertanyaan tentang waktu atau tempat.

**Catatan kehati-hatian:**
- Perubahan topik tanpa penanda dapat membingungkan, terutama jika hubungan antara topik lama dan topik baru tidak jelas.
- Namun, tidak setiap perubahan topik harus memakai ungkapan khusus. Isi ujaran dan konteks juga dapat menunjukkan perpindahan.
- Jangan menyimpulkan perubahan topik hanya dari satu kata yang kebetulan muncul.
- Jika hubungan ujaran baru dengan pembicaraan sebelumnya tidak jelas, tanyakan atau tanggapi bagian yang benar-benar dipahami.

### D. Klarifikasi dan Koreksi dalam Percakapan

Klarifikasi meminta informasi tambahan ketika maksud belum jelas. Koreksi memperbaiki ucapan sendiri atau pemahaman lawan bicara.

| Bentuk | Fungsi | Contoh |
|---|---|---|
| Meminta penjelasan | Meminta pengulangan atau rincian yang belum dipahami | “Maaf, bisa diulang bagian itu?” |
| Memperbaiki diri sendiri | Mengganti atau memperjelas ucapan sendiri | “Eh, maksud saya bukan itu, melainkan bagian yang sebelumnya.” |
| Memperbaiki pemahaman | Memberi tahu bahwa tafsiran lawan bicara tidak sesuai | “Bukan itu maksudku. Maksudku adalah jadwalnya yang perlu diubah.” |
| Memastikan pemahaman | Memeriksa apakah ringkasan sudah tepat | “Jadi yang kamu maksud hari Jumat, benar begitu?” |

**Prinsip:**
- Koreksi dari penutur merupakan informasi baru tentang maksud yang ingin disampaikan.
- Jika pengguna berkata “Bukan itu maksudku”, sistem harus meninjau kembali tafsiran sebelumnya.
- Jangan mempertahankan tafsiran lama setelah penutur secara jelas memperbaikinya.
- Tanyakan bagian yang memang belum jelas; jangan meminta pengguna mengulang seluruh percakapan tanpa kebutuhan.
- Koreksi satu bagian tidak otomatis membatalkan semua informasi lain yang sudah benar.

---

## 2 — Variasi Bahasa

Bahasa Indonesia digunakan dalam beragam situasi. Bentuk baku, sehari-hari, formal, santai, lisan, dan tulisan memiliki fungsi masing-masing. Sistem perlu mengenali variasi tersebut tanpa menganggap semua ujaran harus berbentuk resmi.

### A. Baku dan Tidak Baku / Sehari-hari

| Situasi | Bentuk baku | Bentuk sehari-hari |
|---|---|---|
| Salam | “Selamat pagi.” | “Pagi.” / “Hai.” |
| Menanyakan kabar | “Apa kabar?” | “Gimana kabarnya?” |
| Terima kasih | “Terima kasih.” | “Makasih.” / “Makasih ya.” |
| Meminta maaf | “Saya minta maaf.” | “Maaf ya.” |
| Berpamitan | “Saya pamit dulu.” | “Aku duluan, ya.” / “Sampai ketemu.” |

**Catatan:**
- Bentuk baku lazim digunakan dalam dokumen resmi, pendidikan, dan situasi yang menuntut ragam standar.
- Bentuk sehari-hari lazim digunakan dalam percakapan informal.
- Bentuk sehari-hari bukan otomatis bahasa yang salah. Bentuk tersebut merupakan variasi pemakaian yang sesuai dengan konteks tertentu.
- Tidak semua pasangan merupakan pengganti kata demi kata. Misalnya, “Pagi” adalah salam singkat yang lazim, sedangkan “Selamat pagi” lebih lengkap.
- Sistem harus memahami maksud ujaran informal tanpa mengharuskan pengguna mengubahnya menjadi bentuk baku.

### B. Ragam Formal dan Santai

| Aspek | Formal | Santai |
|---|---|---|
| Kata ganti orang | Saya — Anda; atau sapaan yang sesuai seperti Bapak/Ibu | Aku — Kamu |
| Susunan kalimat | Cenderung lengkap dan tertata | Dapat lebih pendek dan ringkas |
| Pilihan kata | Lebih resmi dan netral | Lebih akrab dan sehari-hari |
| Contoh meminta bantuan | “Bisakah Anda membantu saya memeriksa dokumen ini?” | “Bisa bantu aku cek dokumen ini?” |
| Contoh menyampaikan rencana | “Saya akan mengirimkan hasilnya setelah pemeriksaan selesai.” | “Aku kirim hasilnya kalau sudah selesai dicek.” |

**Contoh kalimat lengkap:**

- Formal: “Selamat siang. Apakah Anda bersedia menjelaskan kembali bagian yang belum saya pahami?”
- Santai: “Siang. Bisa jelasin lagi bagian yang belum aku paham?”

**Catatan pemilihan ragam:**
- Ragam formal sesuai untuk situasi resmi, pelayanan, komunikasi profesional, atau ketika hubungan belum akrab.
- Ragam santai sesuai untuk percakapan akrab atau situasi informal.
- “Anda” tidak selalu menjadi sapaan paling alami. Dalam situasi tertentu, “Bapak”, “Ibu”, jabatan, atau nama lebih sesuai.
- Sistem sebaiknya mengikuti ragam yang digunakan pengguna secara wajar, tetapi tetap menjaga kesopanan.
- Jangan menyimpulkan kedekatan hubungan, usia, jabatan, atau status sosial hanya dari satu kata ganti.

### C. Bahasa Lisan dan Tulisan

**Ciri bahasa lisan:**
- Sering menggunakan kalimat pendek atau tidak lengkap.
- Dapat mengandung jeda, pengulangan, perubahan susunan kalimat, dan perbaikan spontan.
- Dapat menggunakan partikel penegas atau nuansa seperti “lah”, “dong”, “nih”, “sih”, “kok”, dan “deh”.
- Makna dapat dibantu oleh intonasi, ekspresi, situasi, dan gerak tubuh.

**Ciri bahasa tulisan:**
- Umumnya lebih terstruktur dan dapat diperiksa sebelum disampaikan.
- Dalam konteks resmi, biasanya menggunakan ejaan dan tanda baca baku.
- Dalam percakapan digital, tulisan dapat meniru bahasa lisan dan memakai bentuk ringkas.

| Bentuk percakapan/lisan | Bentuk tulisan lebih baku |
|---|---|
| “Aku lagi di jalan.” | “Saya sedang dalam perjalanan.” |
| “Nanti aku kabarin, ya.” | “Nanti saya akan memberi kabar.” |
| “Gimana kalau besok?” | “Bagaimana jika besok?” |
| “Aku nggak tahu.” | “Saya tidak tahu.” |

**Partikel dalam percakapan:**

| Partikel | Contoh | Catatan fungsi |
|---|---|---|
| -lah / lah | “Tenanglah.” | Dapat memberi penegasan atau nuansa tertentu; fungsi bergantung pada susunan dan konteks. |
| dong | “Bantu sebentar, dong.” | Dapat melunakkan permintaan atau memberi penekanan akrab. |
| nih | “Ini nih yang saya cari.” | Dapat menarik perhatian pada sesuatu yang ditunjuk atau dibicarakan. |
| sih | “Bagus sih, tetapi agak mahal.” | Dapat memberi penekanan atau membatasi/menyeimbangkan pernyataan. |

**Peringatan:**
- Partikel tidak selalu memiliki padanan satu kata dalam ragam baku.
- Maknanya dapat berubah menurut posisi, intonasi, dan konteks.
- Tidak ada ragam lisan atau tulisan yang selalu lebih benar. Ketepatan ditentukan oleh tujuan, situasi, dan pembaca atau pendengar.
- Sistem tidak boleh menganggap partikel informal sebagai gangguan atau menghapus nuansanya secara otomatis.

### D. Ungkapan Umum Sehari-hari

| Kata/ungkapan sehari-hari | Padanan baku atau catatan pemakaian |
|---|---|
| “Gimana?” | “Bagaimana?” |
| “Gak tahu” / “Nggak tahu” | “Tidak tahu.” Bentuk informal yang lazim dalam percakapan. |
| “Lagi di jalan” | “Sedang dalam perjalanan.” |
| “Nanti dulu ya” | Meminta penundaan untuk saat ini; belum tentu menolak. |
| “Bentar” | “Sebentar.” |
| “Makasih” | “Terima kasih.” |
| “Udah” | “Sudah.” |
| “Kayaknya” | “Sepertinya.” |
| “Gak apa-apa” | “Tidak apa-apa.” |

**Batas cakupan:**
- Daftar ini berisi ungkapan umum, bukan seluruh slang atau variasi daerah.
- Bentuk informal dapat memiliki variasi ejaan, misalnya “gak”, “nggak”, dan “enggak”.
- Ungkapan yang sama dapat memiliki fungsi berbeda menurut konteks. “Nanti dulu ya” biasanya meminta penundaan, bukan otomatis menolak.
- Jika menemukan istilah lokal atau istilah kelompok yang belum dipahami, sistem sebaiknya meminta penjelasan daripada mengarang artinya.
- Bentuk sehari-hari merupakan ragam bahasa, bukan bukti bahwa penutur tidak menguasai bahasa Indonesia.

---

## 3 — Contoh Percakapan Utuh dan Analisis

Contoh berikut memperlihatkan hubungan antargiliran, pilihan ragam, dan cara memahami topik. Nama atau situasi dalam contoh hanya berfungsi sebagai ilustrasi.

### Percakapan 1 — Sapaan, Tanya Kabar, dan Penutup

> A: Halo, selamat pagi!
>
> B: Pagi. Apa kabar?
>
> A: Baik, terima kasih. Kamu sendiri?
>
> B: Aku juga baik, makasih.
>
> A: Syukurlah. Aku lanjut kerja dulu, ya.
>
> B: Oke. Sampai ketemu nanti.

**Analisis:**
- Alur percakapan: sapaan → pertanyaan kabar → jawaban → pertanyaan balik → jawaban → penutup.
- “Kamu sendiri?” merujuk pada pertanyaan kabar sebelumnya.
- “Aku juga baik” adalah jawaban yang lengkap dalam konteks, walaupun singkat.
- “Aku lanjut kerja dulu” memberi alasan untuk mengakhiri percakapan saat itu.
- Ragam yang digunakan santai dan tetap sopan.
- “Sampai ketemu nanti” menutup percakapan tanpa menyatakan bahwa mereka tidak akan berbicara lagi.

### Percakapan 2 — Meminta Tolong dan Berterima Kasih

> A: Bisa tolong ambilkan buku di meja itu?
>
> B: Tentu. Buku yang sampul biru?
>
> A: Iya, yang biru. Terima kasih.
>
> B: Sama-sama. Ini bukunya.
>
> A: Terima kasih sudah membantu.
>
> B: Dengan senang hati.

**Analisis:**
- “Bisa tolong …?” berfungsi sebagai permintaan bantuan yang sopan, bukan semata-mata pertanyaan tentang kemampuan.
- B meminta klarifikasi karena ada kemungkinan lebih dari satu buku.
- “Iya, yang biru” mengonfirmasi rujukan yang dimaksud.
- “Sama-sama” dan “Dengan senang hati” merupakan tanggapan lazim terhadap ucapan terima kasih.
- Sistem tidak boleh menebak buku yang dimaksud sebelum cirinya cukup jelas.

### Percakapan 3 — Mengubah Topik dengan Penanda

> A: Jadi, tugas yang kemarin sudah selesai?
>
> B: Sudah. Tinggal saya periksa sekali lagi.
>
> A: Bagus. Ngomong-ngomong, kamu jadi ikut makan siang?
>
> B: Jadi. Kita berangkat jam dua belas?
>
> A: Iya, kalau kamu sudah siap.
>
> B: Oke, nanti aku kabari.

**Analisis:**
- Topik pertama adalah penyelesaian tugas.
- “Ngomong-ngomong” menandai perpindahan ke topik makan siang.
- Jawaban B tentang jam dua belas harus dihubungkan dengan rencana makan siang, bukan tugas.
- “Nanti aku kabari” menyatakan bahwa B akan memberi informasi kemudian; tidak menetapkan waktu pasti untuk kabar tersebut.
- Percakapan tetap berkesinambungan karena topik baru diperkenalkan dengan jelas.

---

## 4 — Prinsip Percakapan yang Baik

Prinsip berikut menjadi pedoman komunikasi, bukan klaim bahwa sistem sudah otomatis mampu menjalankan semuanya.

1. **Dengarkan dan pahami sebelum menjawab.** Perhatikan ujaran terbaru serta konteks percakapan yang benar-benar tersedia.
2. **Jika tidak paham, bertanya; jangan menebak.** Minta klarifikasi pada bagian yang paling menentukan makna.
3. **Hubungkan jawaban dengan topik yang tepat.** Jangan membawa informasi dari topik lama jika pengguna sudah berpindah topik.
4. **Setuju atau tidak setuju dengan alasan.** Jangan sekadar menyetujui semua pernyataan. Jelaskan alasan yang relevan dan bedakan fakta dari pendapat.
5. **Jika dikoreksi, perbarui pemahaman.** Jangan mempertahankan tafsiran yang sudah dinyatakan keliru oleh penutur.
6. **Sesuaikan ragam bahasa dengan situasi.** Gunakan bahasa formal atau santai secara wajar tanpa merendahkan ragam lain.
7. **Jaga giliran bicara.** Jangan menganggap jeda sebagai akhir atau terus mengambil alih percakapan.
8. **Jujur tentang batas pengetahuan.** “Saya belum tahu soal itu” lebih baik daripada memberikan jawaban yang dibuat-buat.
9. **Jangan mengarang konteks yang hilang.** Rujukan, maksud, emosi, atau keputusan yang belum jelas harus tetap dinyatakan belum pasti.
10. **Jaga kesantunan tanpa mengubah maksud.** Bahasa sopan tidak boleh membuat penolakan berubah menjadi persetujuan atau dugaan berubah menjadi fakta.

---

## 5 — Verifikasi Mandiri dan Batas Penggunaan

Pemeriksaan ini menilai kelengkapan dokumen terhadap tugas Tahap 4. Ini bukan validasi ahli eksternal, bukan pengujian runtime, dan bukan bukti bahwa ILIS telah menguasai seluruh variasi percakapan.

| Pemeriksaan | Hasil | Catatan |
|---|---|---|
| Mengambil giliran bicara dijelaskan dengan tiga contoh | ✅ | Termasuk “Menurut saya”, “Kalau begitu”, dan permintaan menambahkan pendapat |
| Memberi giliran bicara dijelaskan dengan tiga contoh | ✅ | Termasuk pertanyaan pendapat dan mempersilakan lawan bicara |
| Menutup percakapan dijelaskan dengan tiga contoh | ✅ | Penutup tidak dianggap selalu sebagai akhir permanen |
| Kesinambungan topik dijelaskan | ✅ | Menghubungkan ujaran dengan konteks sebelumnya |
| Perubahan topik dan penandanya dijelaskan | ✅ | Termasuk risiko perpindahan tanpa penanda yang jelas |
| Klarifikasi dan koreksi dijelaskan | ✅ | Meminta penjelasan, memperbaiki diri, dan memperbaiki pemahaman |
| Tabel baku dan sehari-hari tersedia | ✅ | Salam, kabar, terima kasih, maaf, dan pamitan |
| Tabel formal dan santai tersedia | ✅ | Kata ganti, ciri kalimat, serta contoh kalimat lengkap |
| Bahasa lisan dan tulisan dibedakan | ✅ | Termasuk partikel lah, dong, nih, dan sih |
| Ungkapan sehari-hari dan padanannya tersedia | ✅ | Gimana, gak tahu, lagi di jalan, dan nanti dulu |
| Tiga contoh percakapan utuh beserta analisis | ✅ | Sapaan, permintaan bantuan, dan perubahan topik |
| Prinsip percakapan yang baik tercakup | ✅ | Mendengarkan, klarifikasi, koreksi, alasan, dan kejujuran |
| Ragam informal dijelaskan sebagai variasi, bukan otomatis kesalahan | ✅ | Ketepatan bergantung pada situasi |
| Tidak memasukkan pengetahuan umum/ensiklopedis | ✅ | Isi berfokus pada bahasa dan percakapan |
| Siap menjadi dataset aktif | ❌ | Belum melalui audit evaluator, konversi skema, atau pengujian |

### Batas Aktivasi

- Dokumen ini **hanya daftar referensi Tahap 4**, bukan dataset.
- Tidak ada perubahan pada file JSONL, kode, mesin inti, atau konfigurasi runtime.
- Tidak ada perluasan basis pengetahuan umum atau fakta ensiklopedis.
- Tidak ada klaim bahwa seluruh kemampuan wacana dan variasi bahasa sudah diimplementasikan atau diuji pada runtime.
- Contoh percakapan merupakan bahan pembelajaran konseptual, bukan kasus evaluasi resmi.
- Setiap pemanfaatan lebih lanjut memerlukan audit Dola dan persetujuan terpisah sesuai tata kelola proyek.

**Kesimpulan:** Tahap 4 menyatukan pemahaman bahasa dari tahap sebelumnya ke dalam percakapan yang berkesinambungan dan ragam pemakaian yang berbeda. Prinsip utamanya adalah **mengikuti alur percakapan, menghormati cara orang berbahasa, memperbarui pemahaman saat dikoreksi, dan tidak mengarang hal yang belum jelas.**
