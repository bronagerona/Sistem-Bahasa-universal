# ILIS V1 — Laporan Beta Testing & Evaluasi Resmi

**Versi:** ILIS V1  
**Branch evaluasi:** `ilis-foundation`  
**Metode:** audit kontrak + pengujian otomatis end-to-end melalui `ILISCore()`  
**Kebijakan:** tanpa LLM, model AI, machine learning, embedding, atau layanan AI eksternal.

## 1. Ringkasan eksekutif

ILIS V1 telah mengintegrasikan tokenizer/variation pipeline, Semantic Engine,
Knowledge Engine, Reasoning Engine, Context & Memory Engine, Learning Engine,
Language Generator, serta adapter chatbot dan game. Beta suite menguji
orkestrasi antarmodul, keluaran yang didukung, perilaku unknown, pemisahan
memori, hipotesis pembelajaran, dan pelestarian ketidakpastian.

**Penting tentang skor:** skor di bawah adalah *rating kesiapan/kematangan
berdasarkan cakupan implementasi dan batasan yang terdokumentasi* (skala 1–5),
bukan persentase akurasi empiris atau klaim benchmark populasi. Dataset V1
masih kecil dan sengaja berisi kasus penerimaan serta kasus di luar cakupan.
Waktu CI juga bukan benchmark performa perangkat produksi.

## 2. Scorecard V1

| Area penilaian | Skor / 5 | Evaluasi |
|---|---:|---|
| Akurasi Semantic Engine | 2.5 | Kontrak 12 field dan beberapa pola deklaratif sederhana diuji; cakupan sintaksis terbatas. |
| Ketahanan typo / slang | 2.0 | Variasi leksikal yang terdaftar seperti gue, gak, dan udh dikenali; typo bebas dan slang luas belum didukung. |
| Ketepatan Reasoning | 1.5 | Satu aturan risiko terbakar teruji; bukan reasoning umum. |
| Konsistensi Memory / Context | 3.5 | Session isolation, Working/Episodic Memory, provenance dan lifecycle diuji; semua masih in-memory. |
| Kesetiaan makna Language Generator | 2.5 | Register dan ketidakpastian dipertahankan pada pola burn-risk; cakupan makna/domain terbatas. |
| Kecepatan pemrosesan | Belum diukur | Suite merekam durasi satu jalur end-to-end tanpa ambang; belum ada benchmark berulang, p50/p95, beban serentak, atau perangkat target. |

Skor bukan hasil pengukuran akurasi terhadap korpus representatif. Untuk
menghasilkan metrik akurasi yang sah, V2 perlu dataset berlabel yang lebih
besar, pemisahan data pengembangan/evaluasi, dan penilaian per field semantik.

## 3. Dataset beta dan cakupan pengujian

Dataset executable tersedia di `tests/beta_suite.py` sebagai
`BETA_DATASET`. Kasus mencakup:

| ID | Input / skenario | Hasil yang diuji |
|---|---|---|
| CHAT-001 | Api menyentuh rumah kayu | Adapter fallback, inferensi risiko, register formal, metadata |
| CHAT-002 | Gue lagi makan nasi. | Semantic supported, peran semantik, register slang |
| CHAT-003 | Apakah naga takut lonceng? | Pertanyaan di luar cakupan ditandai unsupported |
| GAME-001 | Naga takut lonceng | Episode tersimpan, dialog NPC berstatus hipotesis |
| GAME-002 | Pemain membuka gerbang kuno | Episode tersimpan, reasoning unknown |
| MEM-001 | Dua sesi berbeda | Isolasi Working/Episodic Memory |
| LEARN-001 | Saya makan nasi. | Klaim baru disimpan sebagai hypothesis, bukan verified |
| GEN-001 | Inferensi risiko terbakar | Bahasa kemungkinan tidak dihilangkan |
| PERF-001 | Chatbot end-to-end | Durasi jalur dicatat tanpa ambang hardware-spesifik |

Jalankan:

```bash
python -m pip install -e ".[dev]"
python -m pytest
python -m pytest tests/beta_suite.py -v
```

Suite menggunakan `ILISCore()` dan adapter publik. Kasus yang belum didukung
diharapkan menghasilkan `unsupported`, `low_confidence`, atau `unknown`,
bukan dipaksakan menjadi kesimpulan.

## 4. Daftar bug dan gap yang diketahui

Daftar ini memisahkan bug implementasi yang terkonfirmasi dari gap kemampuan
yang memang menjadi batas V1. Tidak ada bug baru yang diklaim hanya dari
asumsi; item berikut adalah perilaku terbatas yang harus diperbaiki atau
diperjelas pada V2.

1. **Semantic coverage gap:** pola kalimat tertentu yang secara intuitif
   sederhana, misalnya `Api menyentuh rumah kayu`, belum diparse oleh
   Semantic Engine V1. Chatbot adapter memakai fallback khusus untuk contoh
   penerimaan itu dan mengembalikan status semantik asli secara transparan.
2. **Generator domain gap:** parser kesimpulan otomatis Generator hanya
   mengenali pola risiko terbakar V1. Domain lain perlu memberikan
   `reasoning_result["meaning"]` terstruktur.
3. **Game rule gap:** `Naga takut lonceng` adalah aturan interpretasi lokal
   adapter game dengan confidence heuristik 0.48, bukan aturan Reasoning
   Engine umum atau fakta terverifikasi. Event lain yang tak dikenal hanya
   disimpan dan menghasilkan unknown.
4. **Variation coverage gap:** daftar variasi eksplisit tidak setara dengan
   koreksi typo umum. Typo baru, slang regional, singkatan baru, dan variasi
   ambigu belum ditangani secara luas.
5. **Conflict granularity gap:** deteksi konflik Knowledge Engine hanya
   mencocokkan subject + relation yang sama dengan object berbeda; tidak
   menyelesaikan konflik atau memilih klaim benar.
6. **Persistence gap:** Knowledge, Working, dan Episodic Memory berbasis
   in-memory; restart proses menghilangkan data.
7. **Benchmark gap:** belum ada baseline latency, throughput, p50/p95,
   konsumsi memori, atau pengujian concurrency pada perangkat target.

## 5. Seluruh batasan resmi ILIS V1

### 5.1 Language / tokenizer / variation
- Pemrosesan variasi bergantung pada aturan/leksikon eksplisit; bukan
  koreksi typo bebas atau pemahaman semua variasi bahasa Indonesia.
- Kemiripan ejaan tidak dianggap bukti kesamaan makna.
- Variasi yang tidak dikenal tidak boleh dinormalisasi dengan tebakan.
- Cakupan dialek/variasi regional dan campur bahasa tidak dijamin.

### 5.2 Semantic Engine
- Hanya kalimat pernyataan sederhana dengan satu predikasi utama.
- Kalimat majemuk, kompleks, bertingkat, tanya, perintah, dan resolusi rujukan
  lintas kalimat belum didukung.
- Hasil di luar cakupan harus `unsupported` atau `low_confidence`; field
  yang tidak diketahui tidak boleh ditebak.
- Confidence adalah keyakinan parsing, bukan kebenaran fakta.
- Pola `Api menyentuh rumah kayu` belum dikenali Semantic Engine; Fase 7
  memakai fallback adapter khusus.

### 5.3 Knowledge Engine
- Store konsep, relasi, fakta, dan provenance hanya in-memory.
- Tidak ada pemeriksaan kebenaran otomatis, inferensi umum, atau resolusi
  konflik otomatis.
- Deteksi konflik hanya konflik langsung pada subject + relation sama
  dengan object berbeda.
- Status `verified` adalah label eksplisit, bukan hasil verifikasi otomatis.
- Ingesti semantik yang diterima disimpan sebagai hypothesis, bukan verified.

### 5.4 Reasoning Engine
- Hanya satu aturan inferensi: risiko terbakar dari relasi
  `can_burn` dan `made_of` pada material yang sama.
- Bukan penalaran umum, perencanaan, simulasi fisika, atau prediksi dunia nyata.
- Confidence 0.72 / 0.48 / 0.0 adalah skor heuristik tetap, bukan probabilitas
  terkalibrasi.
- Konflik relevan menghentikan inferensi; data/provenance hilang menghasilkan
  unknown.
- Kesimpulan dari premis verified tetap bukan kepastian kejadian dunia nyata.

### 5.5 Context & Memory
- Semua store V1 in-memory; data hilang saat proses berhenti.
- Working Memory tidak memiliki batas token atau pemangkasan otomatis.
- Episodic Memory menyimpan deskripsi dan metadata pemanggil; belum
  mengekstrak event bebas secara otomatis.
- Event episodik tidak otomatis menjadi fakta atau premis reasoning.
- Long-Term Memory adalah referensi ke Knowledge Engine, bukan database
  persisten terpisah.

### 5.6 Learning Engine
- Pembelajaran deterministik berbasis aturan, bukan pembelajaran model.
- Klaim baru menjadi hypothesis; tidak ada promosi otomatis menjadi verified.
- Konfirmasi harus eksplisit dan hipotesis yang konflik tidak dapat langsung
  dikonfirmasi.
- Semantic ingestion bergantung pada hasil supported dan assertion positif
  dengan subject/relation/object lengkap.
- Fallback negasi pembakaran hanya mengenali pola terbatas
  `<benda> [tidak] [bisa] dibakar`.
- Episode tanpa atribut terstruktur hanya menjadi catatan pengalaman;
  bukan fakta hasil ekstraksi bebas.
- Tidak ada verifikasi fakta otomatis, resolusi konflik, atau generalisasi
  bebas.

### 5.7 Language Generator
- Komposisi deterministik dan aturan eksplisit, bukan generator bahasa umum.
- Parser otomatis hanya mengenali pola kesimpulan burn-risk V1.
- Domain lain sebaiknya mengirim representasi `meaning` terstruktur.
- Variasi bahasa/register dan typo belum mencakup seluruh Bahasa Indonesia.
- Context hanya memasok metadata register dan referen eksplisit; generator
  tidak menyimpulkan fakta baru dari riwayat percakapan.
- Ketidakpastian dipertahankan pada jenis reasoning yang didukung, tetapi
  kesetiaan semantik di luar konstruksi yang diuji belum terjamin.

### 5.8 Interface / adapters
- Chatbot memiliki fallback eksplisit untuk pola `Api menyentuh rumah kayu`;
  pola lain yang tidak didukung menghasilkan jawaban unknown yang berhati-hati.
- Semantic status untuk contoh fallback tetap status asli Semantic Engine,
  bukan dipalsukan sebagai supported.
- Game adapter memiliki interpretasi lokal khusus `Naga takut lonceng`;
  confidence 0.48 adalah heuristik, dan output bukan fakta terverifikasi.
- Reasoning Engine inti tetap hanya memiliki aturan burn-risk; event game
  umum belum menjadi aturan reasoning.
- Adapter tidak mengubah event bebas menjadi fakta terverifikasi dan tidak
  melakukan auto-confirm Learning Engine.

### 5.9 Non-functional
- Tidak ada LLM, model AI, machine learning, embedding, atau layanan AI
  eksternal dalam implementasi V1.
- Belum ada benchmark performa formal, pengujian beban, concurrency,
  batas penggunaan memori, atau SLA.
- Klaim setara LLM atau pemahaman bahasa universal tidak didukung evaluasi V1.

## 6. Kesimpulan dan kriteria kelulusan beta

ILIS V1 layak diperlakukan sebagai fondasi deterministik eksperimental untuk
alur chatbot/game yang sempit dan dapat diaudit. V1 belum layak diposisikan
sebagai chatbot serbaguna atau reasoning engine umum.

Kriteria kelulusan teknis suite: seluruh test proyek dan beta suite lulus.
Kriteria kelulusan produk yang lebih luas memerlukan dataset berlabel,
review manusia, benchmark performa, serta pengujian domain game tambahan.
