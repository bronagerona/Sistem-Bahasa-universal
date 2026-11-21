# RENCANA PENGEMBANGAN KEMAMPUAN RUNTIME TAHAP 1

**Branch tujuan:** `ilis-v2-development`  
**Status:** Rancangan teknis — BELUM DIIMPLEMENTASIKAN  
**Cakupan:** Pemeriksaan ejaan dasar dan pengenalan kelas kata berdasarkan konteks  
**Acuan:** `docs/IMPLEMENTASI_TAHAP_01.md`, `docs/FORMAT_DATASET.md`, `data/reference/tahap_01_fondasi/aturan_ejaan.json`, `data/reference/tahap_01_fondasi/kata_dasar.json`, serta hasil PR #50 dan PR #51.

---

## 1. Ringkasan Temuan Implementasi Saat Ini

PR #50 menyediakan modul fondasi yang terisolasi dan read-only. PR #51 menambahkan pengujian cakupan terhadap kemampuan yang benar-benar tersedia.

| Area | Kemampuan sekarang | Batas yang terbukti |
|---|---|---|
| Referensi kata | Memuat 152 entri dan 11 kelas kata | Hanya pencarian bentuk yang sama persis; bukan analisis kalimat |
| Bentuk ambigu | Mengembalikan beberapa kelas untuk `dekat` | Belum menentukan kelas berdasarkan konteks |
| Aturan ejaan | Memuat 12 aturan referensi | Aturan masih berupa uraian dan contoh; belum menjadi pola pemeriksaan otomatis |
| Pemeriksaan ejaan | Mengembalikan panduan referensi | Tidak menemukan kesalahan, tidak memberi koreksi, dan tidak mengubah masukan |
| Keamanan data | Membaca ulang JSON setiap operasi | Tidak ada cache atau jalur penulisan dari modul |

**Kesimpulan:** modul awal bekerja sesuai batas yang dinyatakan. PR #51 membuktikan perilaku loader dan API yang ada, bukan membuktikan bahwa pemeriksaan ejaan otomatis atau klasifikasi kelas kata kontekstual sudah tersedia.

---

## 2. Prinsip Pengembangan

1. **Tetap deterministik.** Tidak memakai model bahasa, API eksternal, atau tebakan probabilistik.
2. **Referensi tetap satu sumber kebenaran.** Modul hanya membaca `data/reference`; tidak menulis, mengubah, atau mempromosikan data.
3. **Tidak memaksakan hasil.** Jika bukti tidak cukup, hasil harus `unknown`, `needs_context`, atau status ambigu yang eksplisit.
4. **Pisahkan dua kemampuan.** Pemeriksaan ejaan dan klasifikasi kelas kata dikembangkan serta diuji secara terpisah.
5. **Jangan mengubah maksud penutur.** Sistem tidak boleh mengganti tanda baca atau susunan kalimat jika perubahan itu dapat mengubah fungsi ujaran.
6. **Perluasan bertahap.** Mulai dari aturan dengan bukti bentuk yang jelas. Aturan yang memerlukan pengetahuan konteks atau pengenalan nama diri tetap belum didukung sampai ada data dan pengujian khusus.
7. **Tidak mengintegrasikan ke Semantic 12, Reasoning 6, ChatbotAdapter, KnowledgeEngine, atau playground** dalam pekerjaan rancangan ini.

---

## 3. Jalur A — Pemeriksaan Ejaan Dasar

### 3.1 Masalah yang harus diselesaikan

Dua belas aturan saat ini disimpan sebagai teks penjelasan, contoh benar/salah, dan keterangan. Struktur ini cukup untuk dibaca manusia, tetapi belum cukup untuk dieksekusi sebagai aturan pemeriksaan yang aman.

Tidak semua aturan dapat diperiksa hanya dari bentuk karakter. Contoh:
- Kapitalisasi nama orang/tempat memerlukan identifikasi nama diri.
- `di` terpisah dan awalan `di-` memerlukan pembedaan fungsi.
- Tanda tanya dan tanda seru dapat mengubah maksud; sistem tidak boleh mengganti salah satunya hanya karena contoh acuan.
- Kapitalisasi kata kekerabatan bergantung pada apakah kata itu sapaan/rujukan khusus atau penggunaan umum.

### 3.2 Klasifikasi aturan sebelum implementasi

| Kelompok | Contoh aturan | Penanganan awal |
|---|---|---|
| Pola bentuk yang relatif eksplisit | Spasi pada kata depan dalam contoh yang sudah dikenali | Kandidat pemeriksaan deterministik terbatas |
| Memerlukan konteks tata bahasa | `di rumah` vs `ditulis` | Jangan memberi koreksi otomatis sebelum konteks dan cakupan pola terdefinisi |
| Memerlukan identifikasi entitas | Kapitalisasi nama orang/tempat | Tandai belum didukung tanpa daftar entitas atau anotasi yang sah |
| Memerlukan maksud ujaran | Titik, tanya, seru | Jangan mengganti tanda baca tanpa label maksud yang eksplisit |
| Memerlukan struktur kalimat | Kapitalisasi awal kalimat dan tanda baca akhir | Kandidat pemeriksaan terbatas setelah segmentasi kalimat diuji |
| Memerlukan konteks sosial/referensial | Ayah/Ibu/Kakak/Adik sebagai sapaan atau rujukan khusus | Jangan menebak; gunakan status perlu konteks |

### 3.3 Rancangan keluaran pemeriksa

Setiap temuan nantinya harus memiliki sekurang-kurangnya:
- `rule_id`: identitas aturan yang dirujuk;
- `span`: posisi bagian teks yang diperiksa;
- `observed`: bentuk yang ditemukan;
- `status`: `issue`, `no_issue`, atau `needs_context`;
- `suggestion`: usulan hanya jika koreksi didukung aturan secara jelas; selain itu `null`;
- `explanation`: alasan singkat dalam bahasa Indonesia.

Status keseluruhan tidak boleh menyamakan "tidak ditemukan masalah" dengan "semua ejaan telah dipastikan benar". Pemeriksaan hanya berlaku pada aturan dan pola yang memang didukung.

### 3.4 Prinsip keselamatan koreksi

- Pemeriksa tahap awal sebaiknya **melaporkan temuan terlebih dahulu**, bukan langsung mengubah teks.
- Koreksi otomatis hanya boleh dipertimbangkan untuk pola yang tidak mengubah maksud dan sudah memiliki bukti uji memadai.
- Masukan `Awas?` harus tetap `Awas?` bila maksudnya belum diketahui. Jangan otomatis mengubahnya menjadi `Awas!`.
- Jika aturan membutuhkan konteks yang tidak tersedia, kembalikan `needs_context` tanpa saran koreksi.
- Teks asli harus selalu dipertahankan dalam keluaran.

### 3.5 Tahapan kerja Jalur A

A1. Audit 12 aturan dan kelompokkan menurut tingkat determinisme.  
A2. Susun spesifikasi pola eksekusi hanya untuk aturan yang dapat dibuktikan dari teks.  
A3. Siapkan kasus uji positif, negatif, batas, dan ambigu; setiap kasus memiliki alasan serta keluaran yang diharapkan.  
A4. Evaluasi spesifikasi dan kasus uji sebelum kode ditulis.  
A5. Implementasikan pemeriksa read-only yang melaporkan temuan tanpa mengubah teks.  
A6. Jalankan pengujian otomatis dan uji regresi; catat aturan yang belum didukung secara eksplisit.

---

## 4. Jalur B — Pengenalan Kelas Kata Berdasarkan Konteks

### 4.1 Masalah yang harus diselesaikan

`lookup_word()` saat ini mencari bentuk kata secara persis. Data kata memuat `entri`, `jenis`, `bentuk_dasar`, `imbuhan`, dan `catatan`, tetapi belum menyediakan contoh kalimat beranotasi untuk menentukan fungsi kata dalam pemakaian.

Satu bentuk dapat memiliki lebih dari satu kelas atau fungsi yang bergantung pada konstruksi. Karena itu, hasil pencarian kamus tidak boleh dianggap sebagai hasil klasifikasi konteks.

### 4.2 Rancangan masukan

Klasifikasi kontekstual menerima:
- satu kalimat atau potongan teks;
- satu kata sasaran yang benar-benar muncul di dalam teks;
- posisi kata sasaran, atau cara penentuan posisi yang tidak ambigu.

Jika kata sasaran tidak ditemukan atau muncul beberapa kali tanpa posisi yang ditentukan, sistem harus meminta penentuan sasaran atau mengembalikan status ambigu. Sistem tidak boleh diam-diam memilih kemunculan pertama.

### 4.3 Rancangan keluaran

Setiap hasil klasifikasi setidaknya memuat:
- `token`: kata sasaran;
- `classes`: daftar kelas yang didukung bukti;
- `status`: `classified`, `ambiguous`, `needs_context`, atau `unknown`;
- `evidence`: petunjuk bentuk/konstruksi yang benar-benar ditemukan;
- `explanation`: alasan ringkas;
- `reference_match`: entri referensi yang cocok, jika ada.

Jangan menghasilkan satu label tunggal jika beberapa analisis masih masuk akal. Jangan menyimpulkan kelas kata dari daftar kata tanpa mempertimbangkan fungsi pemakaiannya.

### 4.4 Contoh kebutuhan konteks

| Masukan | Sasaran | Prinsip hasil |
|---|---|---|
| `Rumah itu dekat.` | `dekat` | Uji fungsi sifat dalam predikasi |
| `Mereka tinggal dekat sekolah.` | `dekat` | Uji fungsi relasional/preposisional |
| `Buku itu di meja.` | `di` | Kata depan ditulis sebagai kata terpisah |
| `Buku itu ditulis Rina.` | `ditulis` | Bentuk berimbuhan; berada di luar klasifikasi kata dasar Tahap 1 dan harus ditandai di luar cakupan, bukan dipaksakan menjadi entri `di` |

Contoh di atas adalah kebutuhan rancangan, bukan klaim bahwa classifier sudah mampu menghasilkan label tersebut.

### 4.5 Data uji yang diperlukan

Sebelum implementasi, siapkan korpus uji kecil yang dikurasi manual dengan:
- kalimat lengkap dan kata sasaran yang ditandai;
- label kelas kata yang ditinjau;
- alasan linguistik singkat;
- label alternatif jika konteks masih ambigu;
- kasus kata di luar daftar referensi;
- kasus kata berimbuhan yang memang berada di luar cakupan Tahap 1;
- variasi urutan kata dan contoh sehari-hari yang tetap jelas.

Kasus yang labelnya diperdebatkan tidak boleh dipakai sebagai kunci tunggal sebelum evaluator menyelesaikannya. Data uji harus memisahkan contoh yang jelas dari contoh yang memerlukan konteks lebih luas.

### 4.6 Tahapan kerja Jalur B

B1. Audit entri yang berpotensi memiliki lebih dari satu fungsi, dimulai dari `dekat` dan `di`.  
B2. Susun kumpulan kalimat beranotasi untuk semua kelas kata dengan contoh yang jelas.  
B3. Definisikan cakupan pola dan batas analisis; jangan membangun parser kalimat penuh pada Tahap 1.  
B4. Tetapkan keluaran ambigu/unknown dan aturan untuk kata sasaran yang berulang.  
B5. Evaluasi data uji dan spesifikasi sebelum implementasi.  
B6. Implementasikan classifier terbatas dan uji setiap kelas serta kasus batas secara terpisah.

---

## 5. Gerbang Pengujian dan Kriteria Penerimaan

Kedua jalur dinilai terpisah. Kelulusan satu jalur tidak otomatis meluluskan jalur lainnya.

### Gerbang sebelum kode

- [ ] Spesifikasi perilaku disetujui evaluator.
- [ ] Kasus uji dan kunci jawaban ditinjau.
- [ ] Kasus ambigu memiliki hasil `needs_context`/ambiguous, bukan label paksa.
- [ ] Batas tahap dan batas integrasi tertulis.
- [ ] Tidak ada kebutuhan mengubah data referensi secara diam-diam.

### Gerbang setelah kode

- [ ] Semua tes positif dan negatif yang relevan lulus.
- [ ] Tidak ada kesalahan kritis yang mengubah maksud atau memberi label pasti tanpa bukti.
- [ ] Uji baca ulang dan read-only tetap lulus.
- [ ] Hasil unknown/ambiguous dipertahankan dengan benar.
- [ ] Regresi seluruh tes Tahap 1 tetap lulus.
- [ ] Laporan memisahkan jumlah kasus lulus, gagal, ambigu, dan belum didukung.
- [ ] Evaluator meninjau hasil; Owner memberi persetujuan sebelum integrasi berikutnya.

Ambang angka tidak boleh menggantikan pemeriksaan kesalahan kritis. Satu kesalahan yang mengubah maksud ujaran dapat menjadi alasan menahan kelulusan meskipun persentase umum tinggi.

---

## 6. Batas Perubahan dan Hal yang Tidak Dikerjakan

Rancangan ini **tidak mengizinkan**:
- perubahan pada `data/reference` atau promosi ke `data/runtime`;
- perubahan `Semantic 12`, `Reasoning 6`, KnowledgeEngine, ChatbotAdapter, atau playground;
- integrasi ke chatbot atau perubahan workflow;
- penggunaan LLM/API eksternal untuk menebak kelas kata atau memperbaiki ejaan;
- perluasan ke imbuhan, sintaksis penuh, pragmatik, percakapan, atau pengetahuan umum;
- pengubahan branch `main`.

Setiap implementasi berikutnya harus memiliki tugas, branch, PR, pengujian, evaluasi, dan persetujuan tersendiri.

---

## 7. Rekomendasi Urutan

1. Selesaikan spesifikasi dan paket uji **Jalur A** serta **Jalur B** secara terpisah.
2. Evaluasi keduanya sebelum menulis kode agar kunci uji tidak disesuaikan setelah melihat keluaran program.
3. Implementasikan satu jalur pada satu waktu dalam modul terisolasi.
4. Uji, audit, dan catat keterbatasan setiap jalur.
5. Baru setelah keduanya stabil, evaluasi apakah modul fondasi layak diintegrasikan ke alur ILIS yang lebih luas.

**Prinsip penutup:** sistem harus lebih memilih mengakui batas pengetahuannya daripada memberi koreksi atau label yang tidak didukung bukti.
