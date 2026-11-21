# Desain Proyek Pengayaan Bahasa Indonesia ILIS

> Versi: v0.1 — revisi berdasarkan review Dola
> Status: Desain disetujui secara prinsip oleh Evaluator (Dola); menunggu keputusan Pemilik Proyek untuk tahap berikutnya
> Target branch: `ilis-v2-development`
> Cakupan dokumen: desain dan persiapan kurasi data saja
> Batas tegas: dokumen ini BUKAN izin untuk mengubah kode, tes, workflow, skema SQLite, atau baseline ILIS V3.1-Beta.

## 1. Latar Belakang

Pengujian internal menunjukkan cakupan bahasa dan pengetahuan ILIS masih terbatas. Beberapa masukan sehari-hari belum dikenali sebagai maksud sosial atau emosional, pertanyaan pengetahuan umum belum memiliki dukungan fakta yang cukup, dan sebagian keluaran membutuhkan evaluasi confidence yang lebih baik.

Pengayaan perlu dilakukan secara terstruktur. Menambah daftar kata saja tidak cukup: ILIS juga membutuhkan variasi bentuk kalimat, contoh dialog yang mempertahankan konteks, sumber pengetahuan yang dapat diverifikasi, serta evaluasi otomatis yang terpisah dari data pengembangan.

## 2. Tujuan

1. Memperluas kosakata bahasa Indonesia dengan makna dan pemakaian yang teranotasi.
2. Mengumpulkan pola kalimat untuk beragam maksud dan bentuk ujaran.
3. Menyusun dialog multi-turn yang mencakup rujukan konteks dan perubahan topik.
4. Menyusun dataset pengetahuan faktual yang memiliki sumber dan status verifikasi.
5. Menyediakan evaluasi otomatis untuk mengukur kualitas data dan perilaku sistem setelah integrasi disetujui secara terpisah.

## 3. Prinsip dan batasan

- V3.1-Beta dipertahankan sebagai baseline; tidak ada perubahan kode produksi, tes, workflow CI/Playground, atau konfigurasi.
- Kontrak Semantic 12 fields dan Reasoning 6 keys tidak diubah oleh proyek desain ini.
- Tidak mengubah KnowledgeEngine, Concept Engine, ChatbotAdapter, PersonaRenderer, multi-turn, skema SQLite, atau `tests/beta_suite.py`.
- Data bahasa, pola kalimat, dialog, dan fakta disimpan sebagai bahan dataset terpisah selama tahap desain dan kurasi.
- Riwayat dialog boleh membantu memahami rujukan percakapan, tetapi tidak boleh diperlakukan sebagai bukti fakta dunia.
- Fakta harus memiliki sumber yang dapat ditelusuri; jika belum cukup bukti, tandai belum terverifikasi dan jangan mengarang.
- Setiap tahap implementasi atau integrasi membutuhkan proposal tersendiri, review Dola, dan persetujuan Pemilik Proyek.

## 4. Pilar A — Kamus Bahasa Indonesia Terstruktur

### Tujuan
Membangun inventaris lema dan bentuk kata yang mencatat makna, kelas kata, variasi bentuk, ragam pemakaian, dan contoh yang tervalidasi.

### Skema entri yang diusulkan
- `entry_id`: ID unik entri.
- `lemma`: bentuk lema/kata dasar yang menjadi entri utama.
- `surface_forms`: variasi bentuk yang ditemukan dalam penggunaan.
- `root`: akar kata, jika dapat ditentukan.
- `affixes`: imbuhan atau proses morfologis yang relevan.
- `part_of_speech`: kelas kata.
- `senses`: daftar makna; setiap makna memiliki ID/sub-ID, definisi, dan konteks penggunaan.
- `synonyms`: sinonim yang sesuai untuk makna tertentu, bukan sekadar kemiripan bentuk.
- `antonyms`: antonim jika memang ada dan relevan.
- `register`: ragam formal, informal, percakapan, slang, atau regional.
- `examples`: contoh kalimat alami untuk setiap makna atau ragam.
- `source`: sumber definisi/contoh.
- `verification_status`: status seperti `draft`, `reviewed`, atau `verified`.
- `conflict_note`: catatan benturan atau tabrakan makna kata, termasuk perbedaan makna antar-konteks, ragam, atau wilayah; isi bila ditemukan konflik dan jelaskan cara membedakannya.
- `notes`: catatan tambahan kurator.

### Aturan kurasi
- Kata polisemi harus memiliki beberapa sense yang dibedakan, bukan dipaksa menjadi satu definisi.
- Bentuk baku, informal, slang, dan regional diberi label ragam yang jelas.
- Hubungan sinonim/antonim harus divalidasi per makna.
- Bentuk yang belum jelas akar atau kelas katanya boleh ditandai belum terverifikasi.
- Contoh buatan diberi label sebagai contoh sintetis dan tidak diklaim sebagai kutipan sumber.

## 5. Pilar B — Dataset Pola Kalimat

### Tujuan
Mencakup variasi struktur ujaran dan maksud komunikatif dalam bahasa Indonesia.

### Cakupan awal
- Pernyataan dan penyangkalan.
- Pertanyaan ya/tidak dan kata tanya (apa, siapa, kapan, di mana, mengapa, bagaimana).
- Permintaan informasi dan permintaan bantuan.
- Perintah, larangan, ajakan, tawaran, dan saran.
- Kemungkinan, kepastian, persetujuan, dan ketidaksetujuan.
- Sapaan, perpisahan, ucapan terima kasih, permintaan maaf.
- Emosi dan keadaan sosial sehari-hari.
- Sebab-akibat, kondisi, perbandingan, dan kalimat majemuk.
- Rujukan implisit dan ungkapan yang bergantung pada konteks.

### Skema pola
- `pattern_id`: ID unik.
- `name`: nama pola.
- `intent`: maksud komunikatif.
- `structure`: deskripsi atau templat struktur.
- `slots`: unsur yang dapat diisi (aktor, tindakan, objek, waktu, dan sebagainya).
- `constraints`: batasan penggunaan dan urutan unsur.
- `positive_examples`: contoh yang sesuai pola.
- `negative_examples`: contoh mirip yang tidak boleh salah diklasifikasikan sebagai pola ini.
- `register`: ragam bahasa.
- `ambiguity_notes`: catatan ambiguitas.
- `source`: sumber contoh atau pola.
- `verification_status`: status peninjauan.

## 6. Pilar C — Dataset Dialog Multi-Turn

### Tujuan
Menyediakan contoh percakapan berurutan untuk menguji pemahaman konteks, rujukan, klarifikasi, dan kesinambungan dialog.

### Skenario awal
- Sapaan dan percakapan ringan.
- Tanya-jawab bertahap.
- Rujukan implisit ke objek atau topik sebelumnya.
- Klarifikasi ketika rujukan ambigu.
- Perubahan topik dan kembali ke topik sebelumnya.
- Koreksi informasi oleh pengguna.
- Persetujuan, penolakan, dan negosiasi.
- Ragam formal dan informal.
- Pertanyaan yang belum memiliki jawaban atau sumber memadai.

### Skema dialog
- `dialogue_id`: ID unik.
- `scenario`: deskripsi skenario.
- `register`: ragam bahasa.
- `turns`: daftar giliran percakapan.
- `context_dependencies`: rujukan giliran terdahulu yang diperlukan.
- `expected_behavior`: perilaku yang diharapkan.
- `annotation_status`: status anotasi.
- `source`: sumber atau keterangan bahwa dialog sintetis.

Setiap giliran dapat memuat `turn_id`, `speaker`, `utterance`, `intent`, anotasi semantik, referensi ke giliran terdahulu, respons yang diharapkan, dan catatan anotator.

### Aturan penting
Konteks percakapan dapat menjelaskan maksud kata seperti “itu”, “yang tadi”, atau “bagaimana kalau yang kedua?”. Namun, konteks tersebut bukan bukti bahwa sebuah klaim faktual benar. Dialog yang memerlukan fakta harus merujuk ke dataset pengetahuan atau sumber tepercaya.

## 7. Pilar D — Dataset Pengetahuan Faktual

### Tujuan
Menyediakan fakta terstruktur yang dapat ditelusuri sumbernya dan dibedakan dari kosakata maupun konteks percakapan.

### Domain awal yang dapat dipertimbangkan
- Alam dan lingkungan.
- Hewan dan tumbuhan.
- Tubuh manusia dan kesehatan umum.
- Bahan dan sifat benda.
- Sains dasar.
- Geografi dan sejarah.
- Teknologi.
- Kehidupan sehari-hari.

### Skema fakta yang diusulkan
- `fact_id`: ID unik fakta.
- `subject`: subjek.
- `predicate`: relasi atau predikat.
- `object`: objek/nilai.
- `category`: kategori domain.
- `qualifiers`: batasan, kondisi, waktu, atau konteks yang diperlukan.
- `source`: referensi sumber yang dapat ditelusuri.
- `source_date`: tanggal sumber atau tanggal akses/publikasi yang relevan.
- `verification_status`: status pemeriksaan.
- `confidence_note`: catatan tingkat kepastian dan batas fakta.
- `conflict_group`: penanda bila ada sumber yang saling bertentangan.

### Aturan kurasi dan peringatan integrasi
- Utamakan sumber tepercaya dan fakta yang dapat diverifikasi.
- Catat batasan konteks, pengecualian, dan tanggal jika fakta dapat berubah.
- Fakta yang bertentangan tidak boleh digabung tanpa penyelesaian; simpan catatan konflik dan minta peninjauan.
- Jika sumber tidak cukup, tandai belum terverifikasi dan sistem harus dapat menahan diri dari jawaban pasti.

**Peringatan kompatibilitas:** Skema fakta Pilar D ini adalah skema dataset konseptual untuk kurasi. Skema tersebut belum tentu langsung cocok dengan struktur SQLite ILIS V3.1-Beta. Pencocokan field, pemetaan, migrasi, atau perubahan database hanya akan dibahas dalam proposal integrasi terpisah pada tahap mendatang, setelah review Dola dan persetujuan Pemilik Proyek. Tidak ada perubahan SQLite yang diizinkan oleh dokumen ini.

## 8. Pilar E — Evaluasi Otomatis

### Kelompok evaluasi
1. **Lexicon:** ketepatan lema, bentuk kata, sense, ragam, dan penanganan ambiguitas.
2. **Sentence patterns:** ketepatan pengenalan pola dan intent.
3. **Multi-turn:** ketepatan resolusi rujukan, kesinambungan konteks, dan permintaan klarifikasi.
4. **Knowledge:** ketepatan fakta, kecukupan sumber, penanganan konflik, dan abstensi saat bukti kurang.
5. **Integration:** perilaku sistem saat dataset kelak diintegrasikan melalui proposal yang disetujui.
6. **Regression:** memastikan perilaku baseline yang sudah disepakati tidak berubah.

### Metrik yang dapat digunakan
- Accuracy, precision, recall, dan F1 untuk klasifikasi.
- Akurasi resolusi rujukan dan deteksi ambiguitas.
- Akurasi faktual dan tingkat jawaban tanpa dukungan.
- Ketepatan abstensi/penahanan jawaban.
- Jumlah regresi terhadap baseline.
- Konsistensi hasil pengujian berulang.

Pisahkan data pengembangan, validasi, dan tes akhir agar contoh tes tidak bocor ke data pengembangan. Target numerik ditentukan setelah sampel awal dan kemampuan anotasi diketahui.

## 9. Organisasi Data yang Diusulkan

Struktur konseptual (belum dibuat atau diisi sebagai bagian dari dokumen ini):

```text
data/indonesian/
  lexicon/
  sentence_patterns/
  dialogues/
  knowledge/
  evaluation/
```

Gunakan JSONL untuk kumpulan record besar dan JSON/YAML untuk konfigurasi atau metadata bila sesuai. Format final ditetapkan setelah sampel kecil menguji kemudahan validasi, pembacaan, dan pemeliharaan.

## 10. Sumber Data, Hak Pakai, dan Anotasi

- Contoh dapat berasal dari penyusunan manual, kamus/referensi yang dapat dipertanggungjawabkan, sumber publik tepercaya, dataset berlisensi, atau dialog sintetis yang ditinjau.
- Periksa lisensi, atribusi, dan hak penggunaan sebelum menyalin atau mengolah dataset eksternal.
- Tandai data sintetis secara eksplisit.
- Simpan provenance: sumber, tanggal, metode pengumpulan, dan penanggung jawab peninjauan.
- Jangan menganggap teks yang ditemukan di internet otomatis bebas digunakan.
- Buat panduan anotasi ringkas agar label intent, sense, register, dan status verifikasi konsisten.

## 11. Tahapan Pelaksanaan yang Diusulkan

0. **Persetujuan desain:** finalisasi dokumen dan batas pekerjaan.
1. **Uji skema dengan sampel kecil:** buat sampel terbatas dari tiap pilar untuk memeriksa kelengkapan field, konsistensi anotasi, dan kemudahan validasi.
2. **Kurasi bahasa:** perluas kamus dan pola kalimat setelah skema sampel dinilai memadai.
3. **Kurasi dialog:** susun skenario multi-turn dan anotasi dependensi konteks.
4. **Kurasi pengetahuan:** kumpulkan fakta dengan sumber dan status verifikasi.
5. **Evaluasi dataset:** siapkan pemisahan data dan pemeriksaan otomatis terhadap kualitas serta konsistensi.
6. **Proposal integrasi terpisah:** evaluasi pemetaan arsitektur dan database tanpa menerapkannya sebelum persetujuan resmi.

Ukuran dataset tidak ditetapkan secara prematur. **Mulai dari sampel dataset kecil untuk menguji skema terlebih dahulu; setelah skema dan proses anotasi terbukti layak, barulah ukuran dataset diperbesar secara bertahap.**

## 12. Kriteria Kesiapan Dataset

Dataset dapat dipertimbangkan siap untuk tahap review berikutnya bila:
- Skema setiap pilar konsisten dan memiliki dokumentasi field.
- Sampel kecil telah diuji dan masalah skema diperbaiki.
- Contoh memiliki anotasi yang jelas dan status verifikasi.
- Sumber dan hak pakai dapat ditelusuri.
- Ambiguitas, konflik makna, dan konflik fakta dicatat.
- Data pengembangan, validasi, dan tes akhir dipisahkan.
- Evaluasi otomatis dapat mendeteksi record tidak lengkap atau tidak konsisten.
- Tidak ada perubahan baseline yang dilakukan secara tidak sengaja.

## 13. Risiko dan Mitigasi

| Risiko | Dampak | Mitigasi |
|---|---|---|
| Makna kata polisemi atau bertabrakan | Salah tafsir dan label leksikal tidak konsisten | Pisahkan sense, gunakan contoh kontekstual, dan isi `conflict_note` untuk mencatat benturan makna |
| Variasi regional bahasa Indonesia | Kata, makna, atau pola ujaran suatu wilayah dapat keliru dianggap berlaku umum atau justru tidak dikenali | Beri label wilayah/ragam bila diketahui, catat sumber dan konteks pemakaian, libatkan peninjau yang memahami variasi tersebut bila memungkinkan, dan jangan menggeneralisasi satu variasi sebagai bentuk nasional |
| Data sintetis terdengar tidak alami | Model belajar pola yang kaku atau tidak mewakili penggunaan nyata | Tinjau manual, variasikan konteks dan register, dan tandai sumber sintetis |
| Fakta tidak akurat atau kedaluwarsa | Jawaban salah atau menyesatkan | Wajibkan sumber, tanggal, status verifikasi, dan kebijakan konflik |
| Kebocoran data evaluasi | Hasil tes tampak lebih baik dari kemampuan sebenarnya | Pisahkan dataset pengembangan, validasi, dan tes akhir |
| Skema dataset tidak cocok dengan arsitektur/database | Integrasi berisiko dan memerlukan perubahan besar | Perlakukan skema sebagai konseptual; lakukan pemetaan hanya dalam proposal integrasi terpisah |
| Perluasan data terlalu cepat | Anotasi tidak konsisten dan kualitas turun | Uji sampel kecil, tetapkan panduan, lalu tambah data bertahap |
| Perubahan tidak sengaja pada baseline Beta | Perilaku V3.1-Beta berubah tanpa persetujuan | Pisahkan pekerjaan desain/kurasi dari kode; review dan persetujuan terpisah sebelum integrasi |

## 14. Hal yang Memerlukan Keputusan pada Tahap Berikutnya

- Ukuran dan prioritas sampel awal untuk setiap pilar.
- Referensi kamus dan sumber pengetahuan yang akan dipakai.
- Cakupan variasi regional dan ragam bahasa.
- Format data final serta alat validasi.
- Target metrik setelah baseline dataset awal tersedia.
- Rencana integrasi teknis, termasuk pemetaan terhadap struktur SQLite, jika dan hanya jika tahap integrasi diajukan secara terpisah.

## 15. Status dan Batas Otorisasi

Desain ini telah disetujui secara prinsip oleh Evaluator (Dola) setelah empat revisi. Persetujuan prinsip tersebut tidak sama dengan persetujuan implementasi. Pekerjaan yang tercakup saat ini hanya desain dan persiapan kurasi dataset. Perubahan kode, tes, workflow, database, maupun baseline ILIS V3.1-Beta tetap dilarang sampai ada proposal terpisah, review Dola, dan persetujuan eksplisit Pemilik Proyek.
