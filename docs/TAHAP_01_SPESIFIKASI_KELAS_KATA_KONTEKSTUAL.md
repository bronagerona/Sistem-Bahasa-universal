# SPESIFIKASI AWAL — DISAMBIGUASI KELAS KATA BERDASARKAN KONTEKS TAHAP 1

**Status:** DRAF UNTUK EVALUASI — BELUM DISETUJUI, BELUM DIIMPLEMENTASIKAN  
**Jalur:** B — pengenalan kelas kata berdasarkan konteks  
**Cakupan awal yang diusulkan:** Disambiguasi terbatas entri `dekat` (adjektiva/preposisi)  
**Acuan:** `docs/RENCANA_PENGEMBANGAN_RUNTIME_TAHAP_01.md`, `docs/IMPLEMENTASI_TAHAP_01.md`, `data/reference/tahap_01_fondasi/kata_dasar.json`, PR #50–#54.

---

## 1. Keputusan cakupan: jangan mengklaim classifier umum

Modul saat ini memiliki `lookup_word()` yang mengembalikan kelas dari entri referensi. Itu bukan klasifikasi fungsi kata dalam kalimat.

Audit terhadap referensi aktual menemukan:
- `dekat` memiliki dua kelas: `adjektiva` dan `preposisi`, dengan catatan bahwa konteks menentukan fungsinya.
- `jalan` hanya tercatat sebagai `nomina` pada referensi saat ini. Contoh `Mereka jalan ke pasar.` tidak boleh dipakai untuk mengajarkan keluaran `verba` karena kelas verba belum tersedia pada entri tersebut.
- Karena itu, paket awal ini **tidak** mengklaim menyelesaikan klasifikasi 11 kelas kata atau semua kata ambigu. Ia hanya menguji apakah dua kelas yang sudah tercantum untuk `dekat` dapat dibedakan pada pola struktural yang sangat terbatas.

Tidak ada perubahan atau penambahan data referensi dalam pekerjaan ini.

Ini BUKAN pemilah kelas kata umum. Hanya penentuan antara 2 pilihan yang sudah diketahui untuk kata `dekat` saja. Tidak berlaku untuk kata lain.

## 2. Tujuan dan non-tujuan

### Tujuan
1. Menerima kalimat/potongan teks dan satu rentang token sasaran yang eksplisit.
2. Mengambil kandidat kelas dari referensi kata, bukan mengarang kelas baru.
3. Menyempitkan kandidat `dekat` hanya pada pola yang memiliki bukti struktural eksplisit dan kasus uji yang disetujui.
4. Mengembalikan alternatif atau ketidakpastian bila pola tidak cukup kuat.
5. Menyertakan bukti yang benar-benar ditemukan agar keputusan dapat diaudit.

### Bukan tujuan
- Bukan parser sintaksis umum, POS tagger umum, atau model probabilistik.
- Tidak menganalisis imbuhan, morfologi, klausa kompleks, makna tersirat, pragmatik, atau pengetahuan dunia.
- Tidak menyimpulkan kelas kata dari posisi saja.
- Tidak menambah/mengubah entri JSON.
- Tidak mengubah Semantic 12, Reasoning 6, KnowledgeEngine, ChatbotAdapter, playground, workflow, atau `main`.
- Tidak mengintegrasikan classifier ke alur chatbot.

## 3. Kontrak masukan yang diusulkan

Fungsi konseptual: `classify_word_in_context(text, target_span)`.

- `text`: string asli, dipertahankan persis.
- `target_span.start`: indeks awal inklusif.
- `target_span.end`: indeks akhir eksklusif.
- Rentang harus menunjuk tepat satu token kata yang ada di teks. Indeks memakai offset Unicode code point Python, bukan offset byte.
- Pemanggil wajib memberikan rentang eksplisit. Sistem tidak boleh memilih kemunculan pertama secara diam-diam jika token berulang.
- Jika rentang di luar batas, kosong, atau tidak menunjuk token yang valid, masukan ditolak dengan kesalahan input yang jelas.
- Jika kata sasaran tidak tercantum di referensi, status hasil adalah `unknown`, bukan kelas hasil tebakan.

Contoh: untuk `"Rumah itu dekat."`, rentang harus menunjuk hanya token `dekat`.

## 4. Kontrak keluaran yang diusulkan

Setiap hasil memuat:
- `input`: teks asli, tidak berubah;
- `target`: token yang ditunjuk rentang;
- `target_span`: rentang awal-inklusif/akhir-eksklusif;
- `classes`: kelas yang masih didukung;
- `status`: `classified`, `ambiguous`, `needs_context`, atau `unknown`;
- `evidence`: daftar petunjuk struktural yang benar-benar cocok;
- `explanation`: alasan singkat dalam bahasa Indonesia;
- `reference_match`: kelas kandidat yang tercatat pada referensi.

Arti status:
- `classified`: satu kelas didukung oleh pola eksplisit yang telah disetujui dan diuji.
- `ambiguous`: lebih dari satu kelas referensi masih masuk akal.
- `needs_context`: teks/rentang tidak memberi bukti cukup untuk memutuskan.
- `unknown`: token tidak ditemukan dalam referensi yang tersedia.

Tidak ada skor probabilitas atau ranking tersembunyi. Kelas alternatif tidak boleh dihapus hanya karena satu kelas terasa lebih lazim.

## 5. Batas penyempitan kelas (K-1) — aturan operasional

1. Kandidat awal harus berasal dari `lookup_word()` / referensi kata.
2. Penyempitan hanya diizinkan untuk pola yang disebutkan secara eksplisit di spesifikasi ini dan memiliki contoh positif, negatif, serta batas yang telah disetujui.
3. Petunjuk posisi saja bukan bukti yang cukup.
4. Jika pola tidak cocok persis atau ada lebih dari satu analisis wajar, pertahankan kelas kandidat dan gunakan `ambiguous` atau `needs_context`.
5. Setiap hasil `classified` wajib menyebut bukti struktural yang memicunya.
6. Jangan gunakan skor angka, probabilitas, frekuensi korpus yang tidak tersedia, atau pengetahuan dunia.

## 6. Pola awal yang diusulkan untuk `dekat`

Pola berikut adalah hipotesis terbatas untuk dievaluasi, bukan aturan bahasa universal.

### B-DEKAT-ADJ-01 — predikat adjektiva dengan penguat eksplisit
Bentuk seperti `Rumah itu sangat dekat.`:
- sasaran `dekat` didahului penguat `sangat`;
- berada sebagai predikat setelah subjek sederhana;
- tidak diikuti objek nominal yang diperkenalkan langsung oleh `dekat`.

Keluaran yang diusulkan: `classified` → [`adjektiva`].

### B-DEKAT-ADJ-02 — predikat adjektiva sederhana di akhir klausa
Bentuk seperti `Rumah itu dekat.`:
- subjek sederhana diikuti `dekat` sebagai predikat;
- sasaran diikuti akhir teks atau tanda akhir kalimat;
- tidak ada frasa nominal yang menjadi pelengkap langsung setelah `dekat`.

Keluaran yang diusulkan: `classified` → [`adjektiva`].

### B-DEKAT-PRE-01 — `dekat` langsung diikuti frasa nominal
Bentuk seperti `Mereka tinggal dekat sekolah.` atau `Kami duduk dekat pintu.`:
- sasaran `dekat` langsung diikuti satu nomina yang terdaftar pada referensi;
- pola kalimat sederhana memiliki predikat sebelum sasaran;
- tidak ada tanda bahwa kata setelah sasaran merupakan awal kalimat baru.

Keluaran yang diusulkan: `classified` → [`preposisi`].

**Batas penting:** pola ini hanya boleh diterapkan pada contoh konstruksi yang benar-benar diuji. Jangan menggeneralisasi ke frasa kompleks, nama diri, atau token setelah `dekat` yang tidak dikenal. Jika bukti objek nominal tidak dapat dipastikan dari referensi dan pola sederhana, kembalikan `needs_context`.

### Tidak didukung
- Fragmen `dekat rumah` tanpa kalimat lengkap.
- Token `dekat` berdiri sendiri.
- `Rumah dekat` tanpa konteks tambahan.
- `Dia dekat dengan saya` sampai konstruksi `dekat dengan` memiliki evaluasi tersendiri.
- Kalimat majemuk/kompleks dan pola yang tidak disebutkan di atas.

## 7. Paket kasus uji kandidat

Kunci di bawah adalah **usulan untuk evaluator**, belum boleh dianggap sebagai kebenaran final sebelum ditinjau.

| ID | Kalimat | Sasaran | Hasil usulan | Alasan/petunjuk |
|---|---|---|---|---|
| B-DEKAT-001 | Rumah itu dekat. | dekat | classified: adjektiva | Predikat adjektiva pada klausa sederhana |
| B-DEKAT-002 | Rumah itu sangat dekat. | dekat | needs_context | `sangat` belum terdaftar; posisi sebelum sasaran tidak cukup menjadi bukti kelas kata |
| B-DEKAT-003 | Gedung itu cukup dekat. | dekat | needs_context | Penguat `cukup` belum disetujui sebagai pola |
| B-DEKAT-004 | Mereka tinggal dekat sekolah. | dekat | needs_context | `sekolah` belum terdaftar; kelas kata unsur setelah `dekat` tidak dapat diverifikasi |
| B-DEKAT-005 | Kami duduk dekat pintu. | dekat | classified: preposisi | Diikuti nomina sasaran `pintu` |
| B-DEKAT-006 | Kantor berada dekat stasiun. | dekat | needs_context | Pola verba `berada` belum disetujui |
| B-DEKAT-007 | Dekat rumah itu ada taman. | Dekat | needs_context | Posisi awal dan struktur berbeda |
| B-DEKAT-008 | dekat rumah | dekat | needs_context | Fragmen tanpa konteks kalimat |
| B-DEKAT-009 | dekat | dekat | needs_context | Token tunggal |
| B-DEKAT-010 | Rumah dekat. | dekat | needs_context | Struktur terlalu minim untuk pola awal |
| B-DEKAT-011 | Dia dekat dengan saya. | dekat | needs_context | Konstruksi `dekat dengan` belum ditinjau |
| B-DEKAT-012 | Rumah itu dekat dan nyaman. | dekat | needs_context | Koordinasi predikat belum menjadi pola awal |
| B-DEKAT-013 | Rumah itu dekat sekolah. | dekat | needs_context | `sekolah` belum terdaftar; kelas kata unsur setelah `dekat` tidak dapat diverifikasi |
| B-DEKAT-014 | Rumah itu sangat dekat sekolah. | dekat | needs_context | Dua analisis mungkin; jangan paksa |
| B-DEKAT-015 | Rumah itu dekat sekolah dan pasar. | dekat | needs_context | Frasa nominal koordinatif belum didukung |
| B-DEKAT-016 | Mereka tinggal dekat sekolah; rumahnya jauh. | dekat | needs_context | Klausa majemuk di luar pola awal |

### Revisi kunci berdasarkan audit referensi aktual

Pemeriksaan ulang terhadap `data/reference/tahap_01_fondasi/kata_dasar.json` menetapkan bahwa `pintu` tercatat sebagai nomina, sedangkan `sekolah` dan `sangat` belum tercantum. Karena komponen pola yang tidak terdaftar tidak dapat dipakai sebagai bukti kelas kata, kunci kasus berikut direvisi:

- **B-DEKAT-002** menjadi `needs_context`: `sangat` tidak boleh diperlakukan sebagai fitur leksikal atau bukti kelas kata. Posisi sebelum sasaran saja tidak cukup.
- **B-DEKAT-004** menjadi `needs_context`: kelas kata `sekolah` tidak tersedia dalam referensi.
- **B-DEKAT-013** menjadi `needs_context`: alasan yang sama dengan B-DEKAT-004.
- **B-DEKAT-005** tetap `classified: preposisi`: `pintu` tercatat sebagai nomina dan pola sederhana yang disetujui dapat diuji.

Kasus lain tetap sesuai kunci sebelumnya. Revisi ini hanya mengubah kunci dan alasan uji; tidak menambah kosakata, tidak mengubah JSON, dan tidak memperluas cakupan classifier.

**Prinsip bukti:** jika salah satu unsur yang diperlukan oleh pola belum terdaftar atau tidak dapat diverifikasi dari referensi, pola tersebut tidak boleh menghasilkan `classified`. Gunakan `needs_context`; jangan menebak dan jangan membuat daftar leksikal tersembunyi.

### Kasus kontrol kontrak
1. Token tidak ada di referensi → `unknown`.
2. Token referensi unambiguous seperti `buku` tidak boleh diklaim sebagai hasil analisis kontekstual oleh pola `dekat`; hasil tetap dibatasi pada dukungan referensi atau `needs_context` sesuai kontrak final.
3. Token sasaran muncul dua kali, tetapi rentang menunjuk kemunculan kedua → hanya kemunculan kedua yang dianalisis.
4. Rentang salah atau menunjuk sebagian token → input ditolak, bukan diperbaiki diam-diam.
5. Teks dengan emoji/karakter multibyte sebelum sasaran → span harus tetap menunjuk token yang tepat.
6. Huruf kapital pada awal kalimat tidak mengubah pencocokan token, tetapi bentuk asli pada keluaran harus dipertahankan.

## 8. Pertanyaan yang wajib diputuskan evaluator

1. Apakah B-DEKAT-ADJ-01 dan B-DEKAT-ADJ-02 benar-benar memberi bukti struktural cukup untuk `adjektiva`, atau keduanya harus tetap `needs_context`?
2. Apakah B-DEKAT-PRE-01 dapat dibatasi aman dengan daftar nomina referensi dan pola kalimat sederhana, atau memerlukan anotasi manual per contoh?
3. Apakah kasus 003, 006, 007, 012, 014, 015, dan 016 tepat dikunci sebagai `needs_context`?
4. Apakah kontrak rentang eksplisit lebih aman daripada pencarian otomatis token sasaran?
5. Apakah `classified` sebaiknya hanya dipakai untuk pola yang telah disetujui, dan tidak untuk kelas tunggal yang sekadar berasal dari lookup kamus?
6. Apakah ada risiko bahwa pola awal melampaui batas Tahap 1 atau diam-diam menjadi parser sintaksis?

## 9. Gerbang sebelum implementasi

Tidak ada kode ditulis sampai:
- evaluator menyetujui atau merevisi pola dan kunci kasus;
- kontrak masukan rentang dan keluaran disepakati;
- contoh positif, negatif, dan ambigu dinilai memadai;
- ketidaksesuaian data referensi (termasuk entri `jalan` yang saat ini hanya nomina) tetap ditangani tanpa mengarang atau menambahkan kelas.

Jika diterima, implementasi berikutnya harus berada pada branch/PR terpisah, hanya modul classifier terisolasi dan tesnya. Tidak mengubah JSON, pemeriksa EJA-04, Semantic 12, Reasoning 6, KnowledgeEngine, ChatbotAdapter, playground, workflow, atau `main`.

---

**Kesimpulan:** Jalur B dimulai sebagai eksperimen disambiguasi satu entri ambigu (`dekat`), bukan classifier 11 kelas. Lebih baik kemampuan kecil dengan bukti yang dapat diaudit daripada label luas yang tampak pintar tetapi menebak.
