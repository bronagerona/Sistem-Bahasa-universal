# Identity & Persona Layer ILIS

**Status:** Dokumen arsitektur dan kebutuhan untuk ILIS V2.1  
**Branch acuan:** `ilis-v2-development`  
**Ruang lingkup:** Desain konseptual; belum menyatakan fitur ini telah diimplementasikan.

## 1. Tujuan dan prinsip utama

ILIS adalah mesin pemrosesan bahasa dan penalaran yang dapat digunakan oleh beragam aplikasi. Identitas yang dilihat pengguna tidak boleh otomatis disamakan dengan identitas ILIS.

**Prinsip inti: ILIS Core adalah mesin otak yang terpisah dari lapisan identitas dan persona.** Core memahami masukan, mengelola konteks/pengetahuan, melakukan penalaran sesuai kemampuan yang tersedia, dan menghasilkan informasi respons. Lapisan di atasnya menentukan siapa yang sedang berbicara, dalam peran apa, dan dengan gaya seperti apa.

Satu ILIS Core dapat melayani banyak aplikasi dan banyak karakter tanpa membuat Core mengaku sebagai setiap karakter tersebut. ILIS tetap deterministik dan non-LLM; lapisan persona bukan alasan untuk menambahkan LLM.

## 2. Arsitektur konseptual

Alur konseptual:

`Pengguna / Pemain → Application Identity → (opsional) Character Identity → ILIS Core → hasil terstruktur → perender respons persona → Pengguna / Pemain`

Urutan pemrosesan internal dapat disesuaikan implementasi. Diagram ini menjelaskan pemisahan tanggung jawab, bukan kontrak API yang sudah tersedia.

### 2.1 ILIS Core — mesin otak

Tanggung jawab:
- Memproses variasi bahasa Indonesia dan mengidentifikasi maksud sesuai cakupan engine.
- Menggunakan konteks, memori, pengetahuan, dan penalaran yang tersedia.
- Menghasilkan hasil semantik/penalaran dan status ketidakpastian.
- Tidak menetapkan identitas produk atau berpura-pura menjadi karakter game.
- Tidak mencampur aturan dunia game atau dialog karakter ke dalam aturan inti bahasa.

Core sebaiknya mengembalikan informasi yang dapat dipakai lapisan aplikasi, bukan memaksakan satu suara/identitas universal. Jika informasi tidak cukup, status ketidakpastian tetap dipertahankan.

### 2.2 Application Identity — identitas aplikasi

Menentukan identitas layanan/aplikasi yang menggunakan ILIS. Contohnya:
- Chatbot ILIS: menyatakan secara transparan bahwa ia adalah ILIS.
- Asisten toko: berbicara sebagai asisten layanan toko, sesuai identitas dan kebijakan aplikasi.
- Game: menetapkan nama aplikasi, dunia, aturan komunikasi, dan apakah dialog harus disampaikan melalui karakter.

Application Identity mengatur konteks penggunaan, kebijakan, bahasa default, dan pemilihan persona. Ia bukan pengganti penalaran Core.

### 2.3 Character Identity — identitas karakter

Lapisan opsional untuk aplikasi yang membutuhkan karakter, terutama NPC game. Konfigurasinya dapat mencakup:
- Nama, peran, latar singkat, dan hubungan karakter dengan pemain.
- Pengetahuan yang boleh diketahui karakter serta batas pengetahuannya.
- Tujuan, sikap, emosi/keadaan dialog, dan gaya bahasa.
- Register (formal, santai, gaul), kosakata, serta batasan konten.
- Konteks dunia game dan status karakter yang diberikan oleh game.

Character Identity harus membatasi respons pada informasi yang tersedia bagi karakter. Karakter tidak boleh mengaku sebagai ILIS hanya karena ILIS Core yang memproses dialognya. Jika persona tidak dikonfigurasi, sistem harus menggunakan perilaku fallback yang dinyatakan aplikasi, bukan mengarang identitas.

## 3. Contoh skenario

### 3.1 Chatbot ILIS

- Application Identity: `ILIS Chatbot`.
- Character Identity: tidak digunakan, kecuali aplikasi sengaja menambahkan persona asisten.
- Pertanyaan: “Siapa kamu?”
- Ekspektasi: “Saya ILIS, sistem pemrosesan dan kecerdasan bahasa Indonesia.” Redaksi dapat berbeda, tetapi identitas layanan harus jelas dan tidak mengklaim kemampuan yang belum tersedia.

### 3.2 NPC game fantasi

- Application Identity: identitas game fantasi.
- Character Identity: penjaga gerbang kerajaan.
- Pertanyaan pemain: “Siapa kamu?”
- Ekspektasi: “Aku penjaga gerbang Kerajaan Arunika.” Jawaban mengikuti lore dan peran karakter; tidak menyebut ILIS.
- Batas: karakter tidak boleh mengetahui lore yang tidak diberikan ke konteks/pengetahuannya.

### 3.3 NPC game horor

- Application Identity: identitas game horor.
- Character Identity: penghuni rumah tua yang misterius.
- Pertanyaan pemain: “Siapa kamu?”
- Ekspektasi: jawaban in-character, misalnya “Aku yang masih tinggal di rumah ini… jangan bangunkan yang di loteng.”
- Batas: suasana horor tidak membenarkan klaim aksi atau pengetahuan yang tidak dimiliki karakter.

### 3.4 NPC game simulasi

- Application Identity: identitas game simulasi, misalnya simulasi toko.
- Character Identity: kasir atau pemilik toko.
- Pertanyaan pemain: “Siapa kamu?”
- Ekspektasi: “Saya penjaga toko ini. Ada yang bisa saya bantu?”
- Batas: transaksi atau aksi dalam game hanya boleh diklaim berhasil jika integrasi game mengonfirmasi aksi tersebut.

## 4. Aturan pemisahan dan fallback

1. Identitas aplikasi menentukan konteks penggunaan; identitas karakter menentukan siapa yang berbicara di dalam konteks itu.
2. ILIS Core tidak otomatis menjadi persona yang tampil ke pengguna.
3. Dalam mode Chatbot ILIS, identitas ILIS harus eksplisit.
4. Dalam mode NPC, identitas dan dialog mengikuti konfigurasi karakter/game; jangan menyisipkan identitas ILIS.
5. Jika Character Identity tidak tersedia, gunakan fallback yang ditetapkan Application Identity dan tandai keterbatasan konfigurasi.
6. Jangan membuat karakter mengaku telah melakukan aksi game tanpa konfirmasi dari integrasi.
7. Ketidakpastian Core harus tetap dihormati. Persona boleh mengubah redaksi, bukan mengubah fakta yang diketahui atau menaikkan confidence secara palsu.
8. Pergantian aplikasi/sesi harus memilih konfigurasi identitas yang tepat dan mencegah persona bocor antar-aplikasi atau antar-karakter.

## 5. Kebutuhan fitur yang diusulkan untuk V2.1

Daftar ini adalah kebutuhan pengembangan, bukan klaim bahwa fitur sudah tersedia.

- **Identity Context:** tipe mode/aplikasi dan identitas aplikasi yang eksplisit pada konteks sesi.
- **Application Profile:** nama, deskripsi, tujuan, bahasa/register default, kebijakan, dan fallback identitas.
- **Character Profile:** ID/nama karakter, peran, latar, sifat, gaya bicara, tujuan, dan batas pengetahuan.
- **Persona Selection:** pemilihan persona berdasarkan aplikasi, karakter aktif, atau konteks game.
- **Persona-aware Response Rendering:** mengubah hasil Core menjadi dialog yang sesuai persona tanpa mengubah makna, evidence, confidence, atau ketidakpastian.
- **Identity Question Handling:** respons “siapa kamu?” dan variasinya mengikuti mode serta profil aktif.
- **Session Isolation:** identitas dan konteks persona terisolasi antar-sesi, aplikasi, dan karakter.
- **Game Context Adapter:** menerima state/lore/aksi dari game melalui antarmuka terdefinisi; Core tidak mengarang state game.
- **Action Acknowledgement Contract:** membedakan dialog pengakuan dari aksi yang benar-benar dieksekusi dan dikonfirmasi.
- **Validation & Fallback:** validasi profil, penanganan profil hilang/tidak lengkap, serta fallback deterministik.
- **Tests & Evaluation:** tes kontrak untuk mode chatbot dan NPC; tes pergantian identitas, kebocoran persona, pertanyaan identitas, konflik persona-konteks, dan preservasi ketidakpastian.
- **Documentation & Examples:** contoh konfigurasi dan integrasi untuk chatbot, NPC fantasi, horor, dan simulasi.

## 6. Kriteria penerimaan awal V2.1

- Pertanyaan identitas pada mode Chatbot ILIS menyebut identitas ILIS secara jelas.
- Pertanyaan identitas pada mode NPC menjawab sesuai Character Identity yang aktif dan tidak menyebut ILIS kecuali lore game memang memerlukannya.
- Dua karakter berbeda dapat memakai Core yang sama dengan identitas dan gaya berbeda.
- Pergantian sesi/karakter tidak membawa persona sebelumnya.
- Persona tidak mengubah hasil fakta, confidence, evidence, atau status ketidakpastian dari Core.
- Sistem tidak mengklaim aksi game berhasil tanpa konfirmasi integrasi.

## 7. Status pada ILIS v2.0-beta

Pada v2.0-beta, Identity & Persona Layer **belum terpasang penuh**. Dokumen ini menetapkan arah arsitektur dan kebutuhan V2.1; ia tidak menjamin konfigurasi mode, profil aplikasi, profil karakter, atau pemilihan persona telah tersedia di kode beta. Karena itu, respons identitas yang belum sesuai mode merupakan keterbatasan yang perlu dicatat sebagai temuan/saran V2.1, kecuali ada kontrak beta lain yang secara eksplisit menjanjikan perilaku tersebut.

---
