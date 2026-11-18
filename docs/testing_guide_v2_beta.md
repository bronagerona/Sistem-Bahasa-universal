# Panduan Penguji ILIS v2.0-beta + Template Laporan Temuan

**Repositori:** `bronagerona/Sistem-Bahasa-universal`  
**Branch acuan:** `ilis-v2-development`  
**Versi yang diuji:** `v2.0-beta`  
**Jenis dokumen:** Panduan pengujian real-world dan formulir laporan  
**Catatan:** Dokumen ini tidak mengubah atau mendefinisikan ulang perilaku kode ILIS.

---

## 1. Pengantar untuk tester

Terima kasih sudah membantu menguji ILIS (Indonesian Language Intelligence System) v2.0-beta. Tujuan pengujian ini adalah melihat bagaimana ILIS berperilaku saat menerima bahasa Indonesia yang digunakan sehari-hari, bukan hanya kalimat contoh yang rapi.

ILIS dirancang sebagai sistem pemrosesan bahasa yang **deterministik dan bukan LLM**. Sistem menggunakan komponen dan aturan internal untuk memahami masukan, mengolah konteks/pengetahuan, melakukan inferensi, lalu menyusun respons. Karena itu, ILIS tidak memiliki kemampuan generatif terbuka seperti model bahasa besar; hasilnya bergantung pada kemampuan dan cakupan aturan serta data yang tersedia.

### Fitur yang menjadi fokus pengujian

- **Semantic Engine:** mengurai masukan menjadi informasi semantik terstruktur, termasuk jenis masukan seperti pernyataan, pertanyaan, dan perintah.
- **Reasoning Engine:** menarik kesimpulan dari informasi semantik dan pengetahuan yang tersedia, serta membawa tingkat keyakinan dan ketidakpastian.
- **Language Generator:** menyusun respons dan mendukung variasi register seperti formal, informal, dan gaul pada skenario yang telah didukung.
- **Chatbot pipeline:** menghubungkan pemrosesan semantik, konteks, penalaran, dan pembangkitan bahasa melalui antarmuka chatbot.
- **Memory dan Knowledge:** menyediakan working memory untuk konteks aktif serta penyimpanan pengetahuan/episodik. SQLite bersifat opsional; mode in-memory tetap tersedia sebagai pilihan default.
- **Pengujian end-to-end:** versi beta ini telah memiliki rangkaian tes otomatis untuk alur chatbot. Pengujian real-world melengkapi tes otomatis, bukan menggantikannya.

### Batasan yang sudah diketahui

1. ILIS **bukan LLM** dan tidak boleh diasumsikan mampu menjawab semua topik atau membuat respons bebas untuk masukan yang belum didukung.
2. Cakupan utama adalah variasi bahasa Indonesia. Bahasa daerah, campur kode yang kompleks, istilah khusus, dan konteks budaya yang tidak tercakup dapat menghasilkan pemahaman yang keliru atau tidak didukung.
3. Ejaan tidak baku, singkatan, typo, slang, dan kalimat ambigu belum tentu dikenali secara konsisten. Catat bentuk masukan persis seperti yang diketik.
4. Penalaran hanya dapat menggunakan aturan dan pengetahuan yang tersedia. Kesimpulan yang tampak masuk akal bagi manusia belum tentu dapat ditarik ILIS.
5. Skor confidence merupakan sinyal internal, bukan jaminan bahwa jawaban benar secara faktual.
6. Respons untuk perintah, misalnya permintaan membunyikan lonceng, dapat berupa **pengakuan/acknowledgement**. Itu tidak berarti ILIS benar-benar menjalankan aksi eksternal di game atau perangkat.
7. SQLite adalah opsi persistensi untuk data Knowledge dan Episodic. Working Memory tetap berada di memori proses; jangan menganggap seluruh konteks percakapan otomatis tersimpan permanen.
8. Data SQLite pada versi ini disimpan tanpa enkripsi aplikasi dan belum memiliki kebijakan retensi otomatis. Gunakan data uji, bukan informasi pribadi atau rahasia.
9. Register yang tidak dikenali atau tidak tersedia dapat dinormalisasi ke formal. Catat bila hasilnya terasa tidak sesuai dengan permintaan.
10. Pengujian ini bukan sertifikasi keamanan, privasi, atau kesiapan produksi.

### Prinsip pengujian

- Uji dengan kalimat alami. Jangan memperbaiki typo atau slang sebelum mengirimkannya.
- Catat input dan output secara persis, termasuk tanda baca dan kapitalisasi.
- Bedakan **bug** (perilaku menyimpang dari perilaku yang diharapkan/didokumentasikan) dengan **saran V2.1** (kemampuan baru atau peningkatan yang belum dijanjikan di beta).
- Jika memungkinkan, ulangi skenario yang sama dan catat apakah hasilnya konsisten.
- Jangan memasukkan kata sandi, data pribadi, atau informasi rahasia ke sistem uji.

---

## 2. Daftar skenario uji coba

Untuk setiap skenario, isi template pada bagian 3. Tester boleh menambahkan variasi sendiri. Contoh input di bawah adalah titik awal, bukan daftar kalimat yang harus dijawab dengan satu redaksi tertentu.

### A. Chatbot — alur percakapan dasar

| ID | Input / langkah uji | Yang diamati |
|---|---|---|
| CB-01 | Tanyakan: “Apakah api bisa membakar kayu?” | Apakah dikenali sebagai pertanyaan; jawaban relevan; ketidakpastian tidak dihilangkan. |
| CB-02 | Berikan pernyataan sederhana tentang fakta yang didukung sistem. | Apakah sistem menangani pernyataan tanpa mengubahnya menjadi pertanyaan/perintah. |
| CB-03 | Tanyakan hal di luar cakupan yang diketahui. | Apakah sistem menghindari kesimpulan yang dibuat-buat dan menunjukkan keterbatasan/ketidakpastian. |
| CB-04 | Kirim kalimat ambigu dengan dua kemungkinan makna. | Apakah respons terlalu cepat memilih satu makna; apakah ketidakpastian tercermin. |
| CB-05 | Kirim perintah: “Bunyikan lonceng.” | Apakah respons berupa acknowledgement yang wajar; jangan menilai aksi eksternal sebagai berhasil kecuali integrasi game memang membuktikannya. |

### B. NPC Game — respons karakter dan aksi

Gunakan ILIS melalui integrasi NPC/game yang tersedia pada lingkungan pengujian. Jika belum ada integrasi game, uji respons teksnya saja dan tandai bahwa aksi game tidak diuji.

| ID | Input / langkah uji | Yang diamati |
|---|---|---|
| NPC-01 | Pemain menyapa NPC dengan bahasa santai. | Respons terasa sesuai sebagai dialog NPC dan tidak terlalu kaku. |
| NPC-02 | Pemain memberi instruksi singkat, misalnya “ikut aku”. | Apakah maksud perintah dikenali; pisahkan respons teks dari aksi NPC yang benar-benar terjadi. |
| NPC-03 | Pemain bertanya tentang objek/karakter yang dikenal dalam skenario. | Apakah NPC menjawab berdasarkan konteks/pengetahuan yang tersedia. |
| NPC-04 | Pemain memberi perintah yang tidak didukung integrasi. | Apakah sistem memberi acknowledgement/penolakan yang jelas tanpa mengklaim aksi telah dilakukan. |
| NPC-05 | Ulangi dialog dengan register berbeda (formal, santai, gaul). | Konsistensi karakter, kesesuaian register, dan keterbacaan dialog. |

### C. Variasi Bahasa Indonesia

| ID | Input / langkah uji | Yang diamati |
|---|---|---|
| VB-01 | Formal: “Apakah Anda dapat membantu saya?” | Pengenalan maksud dan respons formal. |
| VB-02 | Santai: “Bisa bantu gue?” | Apakah maksud tetap dikenali meskipun pilihan kata santai. |
| VB-03 | Gaul: “Bro, ini gimana sih?” | Apakah sistem menangani slang yang digunakan tanpa mengarang makna. |
| VB-04 | Singkatan: “gw gk ngerti, hrs gmna?” | Bagian yang dikenali dan bagian yang gagal dipahami. |
| VB-05 | Tidak baku/typo: “aku pngen nanya soal lonceng” | Apakah typo mengganggu klasifikasi maksud atau respons. |
| VB-06 | Campuran istilah Indonesia dan istilah asing/daerah. | Catat bagian yang tidak dikenali; jangan menganggap dukungan bahasa lain sudah dijamin. |
| VB-07 | Minta jawaban dalam register formal, informal, lalu gaul. | Apakah register keluaran mengikuti permintaan dan tetap mempertahankan makna. |

### D. Multi-turn — konteks antar-giliran

Mulai sesi baru bila tersedia. Kirim pesan secara berurutan tanpa mengulang seluruh konteks, lalu periksa apakah giliran berikutnya ditafsirkan dengan benar.

| ID | Urutan input / langkah uji | Yang diamati |
|---|---|---|
| MT-01 | “Ada naga di cerita ini.” → “Naga itu takut apa?” | Apakah referensi “naga itu” terhubung dengan konteks sebelumnya jika pengetahuan yang diperlukan tersedia. |
| MT-02 | Berikan satu fakta, lalu tanyakan “Kenapa begitu?” | Apakah pertanyaan lanjutan merujuk pada fakta yang tepat. |
| MT-03 | Berikan dua fakta yang saling bertentangan, lalu tanyakan kesimpulannya. | Apakah konflik/ketidakpastian ditangani, bukan dipastikan secara sembarang. |
| MT-04 | Ganti topik setelah beberapa giliran, lalu gunakan kata “itu”. | Apakah sistem keliru memakai konteks lama. |
| MT-05 | Ulangi skenario dalam sesi baru. | Apakah konteks sesi lama tidak dianggap tersedia tanpa mekanisme persistensi yang sesuai. |

### E. SQLite Persistensi

Lakukan bagian ini hanya jika tester memiliki akses ke konfigurasi SQLite dan dapat memulai ulang proses/aplikasi. Jangan mengubah atau menghapus database penting.

| ID | Langkah uji | Yang diamati |
|---|---|---|
| SQL-01 | Jalankan ILIS dengan mode in-memory. Simpan/masukkan pengetahuan uji, lalu mulai ulang proses. | Pastikan tester memahami bahwa mode in-memory tidak ditujukan untuk mempertahankan data setelah proses berhenti. |
| SQL-02 | Jalankan ILIS dengan SQLite aktif dan simpan satu fakta uji. | Apakah operasi penyimpanan selesai tanpa error. |
| SQL-03 | Mulai ulang proses dengan database uji yang sama, lalu tanyakan fakta yang disimpan. | Apakah data Knowledge yang didukung muncul kembali. |
| SQL-04 | Simpan data episodik uji, mulai ulang, lalu periksa kembali sesuai antarmuka yang tersedia. | Apakah data episodik yang dipersistenkan dapat dimuat kembali. |
| SQL-05 | Tutup koneksi/provider dua kali jika antarmuka pengujian memungkinkan. | Apakah penutupan berulang ditangani tanpa crash. |
| SQL-06 | Uji path database yang tidak valid pada salinan/lingkungan uji. | Apakah error ditangani secara jelas dan tidak meninggalkan proses dalam keadaan rusak. |
| SQL-07 | Bandingkan Working Memory sebelum dan sesudah restart. | Pastikan tidak mengasumsikan Working Memory ikut dipersistenkan; catat perilaku aktual. |

---

## 3. Template laporan hasil pengujian

Salin tabel berikut untuk setiap skenario yang diuji. Gunakan satu baris per percobaan agar hasil yang berbeda tidak tercampur.

### Identitas pengujian

| Kolom | Isian |
|---|---|
| ID laporan | |
| Nama tester / alias | |
| Tanggal dan waktu (zona waktu) | |
| Versi / branch | ILIS v2.0-beta / ilis-v2-development |
| Lingkungan (OS, perangkat, aplikasi/integrasi) | |
| Mode penyimpanan | In-memory / SQLite / Tidak diketahui |
| ID skenario | |
| Status | Lulus / Bug / Saran peningkatan V2.1 / Tidak dapat diuji |

### Catatan hasil per percobaan

| No. | Teks input persis | Output ILIS persis | Perilaku yang diharapkan | Perilaku aktual / kejanggalan | Status (Lulus / Bug / Saran V2.1) |
|---|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |

### Detail temuan (isi jika status Bug atau Saran V2.1)

| Kolom | Isian |
|---|---|
| Judul singkat temuan | |
| Jenis | Bug / Saran peningkatan V2.1 |
| Tingkat dampak | Kritis / Tinggi / Sedang / Rendah |
| Langkah reproduksi | 1. … 2. … 3. … |
| Hasil yang diharapkan | |
| Hasil aktual | |
| Frekuensi | Selalu / Sering / Kadang-kadang / Sekali |
| Bukti tambahan (screenshot/log, bila aman) | |
| Dugaan area terkait (opsional) | Chatbot / Semantic / Reasoning / Generator / Memory / SQLite / Integrasi NPC / Tidak diketahui |
| Saran perbaikan (opsional) | |

### Panduan memilih status

- **Lulus:** hasil sesuai tujuan skenario dan tidak ditemukan perilaku janggal yang material.
- **Bug:** perilaku menyimpang, crash/error, kehilangan data yang seharusnya dipersistenkan, salah klasifikasi yang dapat direproduksi, atau klaim aksi yang tidak benar.
- **Saran peningkatan V2.1:** sistem berfungsi sesuai batasan beta, tetapi tester mengusulkan dukungan baru, cakupan bahasa lebih luas, respons lebih alami, atau fitur tambahan.
- **Tidak dapat diuji:** lingkungan, akses, integrasi, atau prasyarat tidak tersedia. Jelaskan alasannya.

---

## 4. Hal yang PERLU DILAPORKAN

Setiap laporan Bug atau Saran V2.1 sebaiknya menyertakan:

1. **Teks input persis** — salin apa adanya, termasuk typo, singkatan, emoji, tanda baca, kapitalisasi, dan spasi yang relevan.
2. **Output ILIS persis** — jangan diringkas atau diperbaiki. Jika output panjang, sertakan bagian lengkap yang relevan.
3. **Perilaku yang tidak wajar** — jelaskan apa yang terasa salah: maksud tidak dikenali, jawaban tidak nyambung, konteks tertukar, kesimpulan terlalu yakin, register keliru, respons berulang, error, atau data tidak tersimpan.
4. **Konteks percakapan** — untuk kasus multi-turn, sertakan seluruh urutan pesan sejak awal sesi yang relevan, bukan hanya pesan terakhir.
5. **Kondisi pengujian** — versi, branch, mode in-memory/SQLite, perangkat/OS, integrasi yang digunakan, serta apakah proses baru saja dimulai ulang.
6. **Langkah reproduksi** — tuliskan urutan yang bisa diikuti tester lain.
7. **Frekuensi dan dampak** — apakah terjadi setiap kali atau hanya sesekali, serta seberapa mengganggu hasilnya.
8. **Bukti** — screenshot atau log yang relevan bila tersedia. Samarkan token, kata sandi, alamat, identitas, dan data sensitif.
9. **Perbedaan harapan dan kenyataan** — jelaskan hasil yang diharapkan dan hasil yang benar-benar terjadi.

### Contoh format laporan singkat

> **ID:** VB-04  
> **Input:** “gw gk ngerti, hrs gmna?”  
> **Output ILIS:** [tempel output persis]  
> **Harapan:** ILIS mengenali bahwa pengguna meminta arahan atau meminta penjelasan.  
> **Aktual:** [jelaskan respons yang terjadi]  
> **Status:** Bug atau Saran peningkatan V2.1  
> **Reproduksi:** [apakah terjadi lagi saat input dikirim ulang]

### Privasi dan keamanan saat menguji

- Gunakan nama, fakta, dan data fiktif.
- Jangan mengirim kredensial, data pribadi, rahasia perusahaan, atau percakapan privat.
- Hapus atau samarkan informasi sensitif dari screenshot/log sebelum membagikan laporan.
- Jangan menguji pada database produksi atau menghapus data yang bukan milik tester.

---

## 5. Penutup

Laporan yang paling membantu bukan hanya menyebut “jawabannya salah”, tetapi menunjukkan **input persis, output persis, konteks, dan langkah untuk mengulanginya**. Temuan yang jelas membantu memisahkan masalah implementasi (bug) dari peluang pengembangan fitur untuk ILIS V2.1.

Terima kasih telah menguji ILIS v2.0-beta dan membantu meningkatkan kualitas sistem.
