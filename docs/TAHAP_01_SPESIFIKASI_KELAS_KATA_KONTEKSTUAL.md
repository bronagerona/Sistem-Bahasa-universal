# SPESIFIKASI AWAL — DISAMBIGUASI KELAS KATA BERDASARKAN KONTEKS TAHAP 1

**Status:** DISETUJUI SEBAGAI SPESIFIKASI TERBATAS — implementasi awal PR #57 telah digabungkan  
**Jalur:** B — pengenalan kelas kata berdasarkan konteks  
**Cakupan yang disetujui:** Disambiguasi terbatas entri `dekat` (adjektiva/preposisi), sesuai implementasi PR #57  
**Acuan:** `docs/RENCANA_PENGEMBANGAN_RUNTIME_TAHAP_01.md`, `docs/IMPLEMENTASI_TAHAP_01.md`, `data/reference/tahap_01_fondasi/kata_dasar.json`, PR #50–#54.

---

## 1. Keputusan cakupan: jangan mengklaim classifier umum

Modul saat ini memiliki `lookup_word()` yang mengembalikan kelas dari entri referensi. Itu bukan klasifikasi fungsi kata dalam kalimat.

Audit terhadap referensi aktual menemukan:
- `dekat` memiliki dua kelas: `adjektiva` dan `preposisi`, dengan catatan bahwa konteks menentukan fungsinya.
- `jalan` hanya tercatat sebagai `nomina` pada referensi saat ini. Contoh `Mereka jalan ke pasar.` tidak boleh dipakai untuk mengajarkan keluaran `verba` karena kelas verba belum tersedia pada entri tersebut.
- Karena itu, paket awal ini **tidak** mengklaim menyelesaikan klasifikasi 11 kelas kata atau semua kata ambigu. Ia hanya menguji apakah dua kelas yang sudah tercantum untuk `dekat` dapat dibedakan pada pola struktural yang sangat terbatas.

Tidak ada perubahan entri atau penambahan data leksikal dalam pekerjaan spesifikasi ini. Catatan metadata jumlah artikula diperbarui terpisah sesuai keputusan audit Tahap 1.

**Pengecualian batas Tahap 1:** pola struktural pada kata `dekat` adalah pengecualian yang sangat terbatas. Hanya dua pola khusus untuk satu kata ini yang diizinkan; pola tersebut tidak menjadi pola umum untuk kata lain dan bukan parser frasa/klausa.

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

**Catatan implementasi:** classifier PR #57 saat ini menggunakan `classified`, `needs_context`, dan `unknown` sesuai pola terbatasnya. Status `ambiguous` tetap didefinisikan untuk kasus ketika dua atau lebih kelas terdaftar masih sama-sama masuk akal tanpa bukti pembeda, tetapi belum dikeluarkan oleh implementasi saat ini. Pemakaian operasionalnya dicatat sebagai penyempurnaan non-mendesak ketika ada kasus konkret yang memenuhi definisi tersebut.

Tidak ada skor probabilitas atau ranking tersembunyi. Kelas alternatif tidak boleh dihapus hanya karena satu kelas terasa lebih lazim.

## 5. Batas penyempitan kelas (K-1) — aturan operasional

1. Kandidat awal harus berasal dari `lookup_word()` / referensi kata.
2. Penyempitan hanya diizinkan untuk pola yang disebutkan secara eksplisit di spesifikasi ini dan memiliki contoh positif, negatif, serta batas yang telah disetujui.
3. Petunjuk posisi saja bukan bukti yang cukup.
4. Jika pola tidak cocok persis atau ada lebih dari satu analisis wajar, pertahankan kelas kandidat dan gunakan `ambiguous` atau `needs_context`.
5. Setiap hasil `classified` wajib menyebut bukti struktural yang memicunya.
6. Jangan gunakan skor angka, probabilitas, frekuensi korpus yang tidak tersedia, atau pengetahuan dunia.

## 6. Pola awal yang diusulkan untuk `dekat`

Pola berikut adalah pola yang telah disetujui dan diimplementasikan secara terbatas; bukan aturan bahasa universal.

### B-DEKAT-ADJ-01 — predikat adjektiva dengan penguat eksplisit
**[TIDAK DIDUKUNG — `needs_context`, lihat keputusan penyelarasan PR #56]**

Contoh `Rumah itu sangat dekat.` tidak boleh menghasilkan `classified`: `sangat` belum terdaftar pada referensi kata. Posisi sebelum `dekat` saja tidak cukup menjadi bukti kelas kata. Pola ini dicatat sebagai hipotesis yang tidak didukung oleh referensi aktual saat ini.

### B-DEKAT-ADJ-02 — predikat adjektiva sederhana di akhir klausa
Bentuk seperti `Rumah itu dekat.`:
- subjek sederhana diikuti `dekat` sebagai predikat;
- sasaran diikuti akhir teks atau tanda akhir kalimat;
- tidak ada frasa nominal yang menjadi pelengkap langsung setelah `dekat`.

Keluaran yang diusulkan: `classified` → [`adjektiva`].

### B-DEKAT-PRE-01 — `dekat` langsung diikuti nomina terdaftar
**[DIDUKUNG SECARA TERBATAS hanya untuk contoh yang seluruh komponennya terdaftar dan pola spesifiknya diuji]**

- `Kami duduk dekat pintu.` → `classified: preposisi`; `pintu` tercatat sebagai nomina dan pola ini diuji pada PR #57.
- `Mereka tinggal dekat sekolah.` → **[TIDAK DIDUKUNG — `needs_context`, lihat PR #56]**; `sekolah` belum terdaftar sebagai nomina pada referensi.

Jangan memperlakukan pola ini sebagai aturan universal untuk semua nomina atau semua konstruksi setelah `dekat`.

**Batas penting:** pola ini hanya boleh diterapkan pada contoh konstruksi yang benar-benar diuji. Jangan menggeneralisasi ke frasa kompleks, nama diri, atau token setelah `dekat` yang tidak dikenal. Jika bukti objek nominal tidak dapat dipastikan dari referensi dan pola sederhana, kembalikan `needs_context`.

### Tidak didukung
- Fragmen `dekat rumah` tanpa kalimat lengkap.
- Token `dekat` berdiri sendiri.
- `Rumah dekat` tanpa konteks tambahan.
- `Dia dekat dengan saya` sampai konstruksi `dekat dengan` memiliki evaluasi tersendiri.
- Kalimat majemuk/kompleks dan pola yang tidak disebutkan di atas.

## 7. Paket kasus uji yang disetujui

Kunci di bawah adalah **kunci yang telah diselaraskan dengan referensi aktual dan keputusan evaluator**. Kasus yang tidak didukung tetap dipertahankan sebagai `needs_context`.

| ID | Kalimat | Sasaran | Hasil yang diharapkan | Alasan/petunjuk |
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

## 8. Catatan evaluasi desain (keputusan sudah ditetapkan)

Keputusan evaluator telah diterapkan sebelum implementasi PR #57:
1. Pola adjektiva sederhana `Rumah itu dekat.` didukung; pola dengan `sangat` tidak didukung karena `sangat` belum terdaftar.
2. Pola preposisi didukung hanya untuk konstruksi yang unsur terkaitnya terdaftar dan contoh spesifiknya diuji; `dekat sekolah` tidak didukung karena `sekolah` belum terdaftar.
3. Kasus yang tidak memenuhi pola yang disetujui tetap `needs_context`.
4. Rentang sasaran eksplisit dipertahankan agar kemunculan kata berulang tidak dipilih secara diam-diam.
5. `classified` hanya dihasilkan oleh pola kontekstual yang disetujui; lookup kamus tetap merupakan operasi terpisah.
6. Pola `dekat` dipertahankan sebagai pengecualian Tahap 1 yang sempit, bukan parser sintaksis umum.

## 9. Batas implementasi yang berlaku

Implementasi terbatas telah dilakukan pada PR #57. Batas yang tetap berlaku:
- hanya kata `dekat` dan dua pola yang disetujui;
- rentang sasaran diberikan secara eksplisit;
- unsur pola harus dapat diverifikasi dari referensi;
- kasus di luar pola tetap `needs_context`, sedangkan kata yang tidak terdaftar tetap `unknown`;
- tidak ada classifier umum, parser sintaksis, atau penambahan kelas/kosakata tersembunyi;
- tidak mengubah pemeriksa EJA-04, Semantic 12, Reasoning 6, KnowledgeEngine, ChatbotAdapter, playground, workflow, atau `main`.

---

**Kesimpulan:** Jalur B tetap berupa disambiguasi satu entri ambigu (`dekat`), bukan classifier 11 kelas. Hanya dua pola terbatas yang didukung implementasi PR #57. Contoh dengan `sangat` atau `sekolah` secara eksplisit tidak didukung dan harus menghasilkan `needs_context`. Lebih baik kemampuan kecil dengan bukti yang dapat diaudit daripada label luas yang tampak pintar tetapi menebak.
