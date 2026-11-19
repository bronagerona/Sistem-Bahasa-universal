# Catatan Pemeriksaan Tautan Sumber — Pilar D

## Batch 007

Pada review Batch 007, beberapa tautan sumber pada record Pilar D terindikasi tidak aktif atau tidak dapat diakses. Isi fakta Batch 007 **tidak diubah** sebagai tindak lanjut catatan ini.

Sebelum record terkait dipertimbangkan untuk dinaikkan dari `draft` menjadi `verified`, kurator wajib:

1. Memeriksa setiap URL sumber secara langsung.
2. Mengganti tautan yang mati/tidak stabil dengan URL cadangan resmi yang mengarah ke halaman spesifik dan mendukung klaim terkait.
3. Memastikan halaman cadangan benar-benar mendukung nilai, satuan, definisi, dan kualifikasi pada record.
4. Mencatat URL pengganti dan tanggal pemeriksaan pada record atau log sumber yang sesuai.
5. Mempertahankan status `draft` sampai pemeriksaan selesai dan bukti sumber dapat ditelusuri.

Catatan ini tidak menyatakan bahwa seluruh tautan Batch 007 mati, tidak menetapkan URL pengganti, dan tidak mengubah status verifikasi fakta. Pemeriksaan serta penggantian URL merupakan prasyarat sebelum verifikasi manual.

## Status pekerjaan verifikasi — tertunda untuk tahap verifikasi

**Status: BELUM DIKERJAKAN. Dijadwalkan sebagai tugas tahap verifikasi sumber dataset, setelah fase kurasi batch.**

Cakupan tugas tertunda:
- Meninjau semua URL sumber pada lima fakta Batch 007 (fact-0033 sampai fact-0037).
- Mengidentifikasi URL yang mati, dialihkan secara tidak tepat, atau tidak mendukung klaim spesifik.
- Mencari dan mencatat URL cadangan resmi yang relevan untuk setiap sumber bermasalah.
- Memeriksa kecocokan klaim, angka, satuan, dan qualifiers terhadap halaman cadangan.
- Memperbarui referensi sumber dan tanggal pemeriksaan setelah bukti tersedia.
- Mempertahankan `verification_status: draft` sampai pemeriksaan manual selesai dan disetujui.

Tugas ini **tidak termasuk pekerjaan Batch 009** dan tidak boleh dianggap selesai hanya karena catatan ini sudah tercatat. Tidak ada fakta Batch 007 yang diubah pada tahap ini.

## Batasan

Dokumen ini hanya catatan kurasi dataset. Tidak memberi izin integrasi ke ILIS, perubahan kode, skema SQLite, test suite, atau workflow CI.


## Batch 010 — Checklist verifikasi sumber untuk fact-0048 (AU)

**Status: BELUM DIKERJAKAN. Dijadwalkan untuk tahap verifikasi sumber setelah fase kurasi batch.** Batch 010 LULUS review kurator, tetapi kelulusan kurasi tidak berarti sumber atau fakta AU telah diverifikasi secara independen.

Cakupan checklist khusus fact-0048:
1. Buka dan periksa sumber primer IAU, terutama dokumen Resolusi B2 (2012), serta sumber NASA yang dicantumkan pada record.
2. Pastikan definisi satuan astronomi (au/AU) tepat sebesar 149.597.870.700 meter dan kutip konteks definisi resminya.
3. Pastikan satuan, notasi angka, dan konversi meter konsisten; catat jika sumber menggunakan notasi atau pembulatan berbeda.
4. Bedakan nilai definisi AU yang tetap dari jarak Bumi–Matahari aktual/rata-rata yang bersifat konteks astronomi; jangan menyamakan keduanya.
5. Pastikan URL aktif, spesifik, dan benar-benar mendukung klaim. Jika URL NASA tidak relevan atau tidak mendukung definisi numerik, gunakan sumber primer IAU sebagai rujukan utama dan catat URL resmi pengganti.
6. Catat URL yang diperiksa, tanggal pemeriksaan, bagian/dokumen pendukung, serta hasil kecocokan klaim pada fact-0048 atau log sumber.
7. Pertahankan `verification_status: draft` sampai seluruh pemeriksaan manual selesai dan disetujui.

Checklist ini **belum merupakan verifikasi** dan tidak memberi izin mengubah status record sekarang. Tugas ini terpisah dari backlog Batch 007 di atas; backlog Batch 007 (fact-0033 sampai fact-0037) tetap **BELUM DIKERJAKAN** dan tidak digantikan atau ditutup oleh checklist Batch 010.


## ✅ FASE 1 LAPORAN KURASI LENGKAP BATCH 001-018 + DAFTAR BACKLOG VERIFIKASI
### 🟢 Ringkasan
- Batch 001-018 Kurasi SELESAI, SEMUA record tetap DRAFT
- Tahap selanjutnya: Tahap 2 Verifikasi Besar-besaran

### ⏳ Daftar Backlog (Status: BELUM DIKERJAKAN)
#### 🔤 Bahasa & Morfologi (Tugas Kurator)
- Batch 007 fact-0033-0037
- Batch 010 fact-0048 AU IAU
- Batch 013: morfologi mengapa
- Batch 014: apakah / adakah
- Batch 015: di vs pada / dalam
- Batch 016: sudah vs telah / akan / pernah
- Batch 017: seluruh vs semua / setiap
- Batch 018: meN- nasal, di- awalan vs preposisi, ter- polisemi, -kan benefaktif/kausatif

#### 📚 Verifikasi Sumber Pilar D per Batch (Tugas Verifikator)
- Batch 014: USGS
- Batch 015: USGS
- Batch 016: NOAA
- Batch 017: EPA / USFW / CBD / USDA
- Batch 018: USGS Geologi

### 📌 Catatan Penting
- Jangan ubah isi file JSONL dataset sebelum ada perintah resmi Dola
- Semua eval-xxxx final_test tetap konseptual, tidak dipakai tuning
- Belum ada izin integrasi ke ILIS


---

# LAPORAN FASE 2 — VERIFIKASI BESAR-BESARAN
**Tanggal pemeriksaan:** 20 November 2026  
**Branch:** `ilis-v2-development`  
**Cakupan:** seluruh backlog bahasa/morfologi dan sumber Pilar D pada catatan ini.  
**Batas perubahan:** hanya dokumen ini. Tidak ada JSONL atau file lain yang diubah.

## 1. Ringkasan hasil
Total 48 unit pemeriksaan:
- Bahasa/morfologi: 17 unit — **15 TERVERIFIKASI**, **2 PERLU REVISI**.
- Pilar D: 31 fakta — **28 TERVERIFIKASI**, **3 PERLU REVISI**.
- **TOTAL: 43 TERVERIFIKASI, 5 PERLU REVISI.**

Label pada log ini adalah hasil pemeriksaan bukti, bukan perubahan status dataset. Semua record JSONL tetap `verification_status: draft`.

Catatan klasifikasi: fact-0033–0037 (Batch 007) dan fact-0048 (Batch 010) adalah fakta astronomi, bukan tugas bahasa/morfologi. Keenam fakta tersebut diperiksa pada bagian sumber Pilar D.

## 2. BAGIAN 1 — Verifikasi Bahasa dan Morfologi

### Batch 013 — mengapa
- **lex-0067 / pat-0067: TERVERIFIKASI.**
- TBBI mencatat pola `meng- + apa → mengapa` pada Tabel 7.2; §7.2.2.4.3 menjelaskan bahwa mengapa/kenapa menanyakan sebab. Analisis akar dan fungsi tanya sebab sesuai.
- Sumber: [Tata Bahasa Baku Bahasa Indonesia (TBBI), Edisi Keempat, 2017](https://repositori.kemendikdasmen.go.id/16351/1/Tata%20Bahasa%20Baku%20Bahasa%20Ind.pdf), Bab 7.2.2.4.

### Batch 014 — apakah / adakah
- **lex-0070 / pat-0070 (apakah): TERVERIFIKASI.** TBBI §8.2.5.1 menjelaskan `-kah` sebagai partikel klitika yang menegaskan interogatif dan memberi contoh `apa` → `apakah`; fungsi pertanyaan polar sesuai.
- **lex-0071 / pat-0071 (adakah): TERVERIFIKASI.** TBBI memberi contoh `Masih adakah orang ...?`; fungsi menanyakan keberadaan/ketersediaan dan parafrasa `apakah ada` sesuai.
- Sumber: [TBBI Edisi Keempat](https://repositori.kemendikdasmen.go.id/16351/1/Tata%20Bahasa%20Baku%20Bahasa%20Ind.pdf), §8.2.5.1 dan contoh penggunaan `adakah`.

### Batch 015 — di / pada / dalam
- **lex-0073 / pat-0073 (di sebagai preposisi): TERVERIFIKASI.** Preposisi `di` lokasi ditulis terpisah; prefiks pasif `di-` ditulis serangkai. TBBI membedakan keduanya secara eksplisit.
- **lex-0076 / pat-0076 (pada): TERVERIFIKASI.** TBBI Tabel 9.3 mencatat `pada` untuk keterangan tempat dan waktu (misalnya `pada saya`, `pada permukaan`, `pada pukul 05.00`, `pada hari ini`). Pemakaian temporal dan relasi abstrak dalam contoh sesuai; `pada` tidak dapat dipertukarkan bebas dengan `di`.
- **lex-0077 / pat-0077 (dalam): PERLU REVISI.** Pembedaan preposisi (misalnya `dalam laci`, `dalam tiga hari`) dan adjektiva kedalaman (misalnya `kolam itu dalam`) tepat. Namun contoh leksikon `Ia berpikir dalam sebelum menjawab` tidak idiomatis/kurang jelas untuk maksud “berpikir mendalam”. Ganti setelah review kurator, misalnya `Ia berpikir secara mendalam sebelum menjawab` atau `Ia memikirkan persoalan itu dalam-dalam`.
- Sumber: [TBBI Edisi Keempat](https://repositori.kemendikdasmen.go.id/16351/1/Tata%20Bahasa%20Baku%20Bahasa%20Ind.pdf), Tabel 9.3; [Frasa Preposisi dalam Bahasa Indonesia](https://repositori.kemendikdasmen.go.id/2549/1/FRASA%20PREPOSISI%20DALAM%20BAHASA%20INDONESIA.pdf).

### Batch 016 — sudah / telah / pernah / akan
- **lex-0079 / pat-0079 (sudah): TERVERIFIKASI.**
- **lex-0080 / pat-0080 (telah): TERVERIFIKASI.** TBBI menggolongkan keduanya sebagai pemarkah aspektualitas; keduanya dapat bertumpang tindih, tetapi tidak sinonim sempurna dalam semua konstruksi. `Telah` cenderung lebih formal, bukan aturan mutlak.
- **lex-0081 / pat-0081 (pernah): TERVERIFIKASI.** Makna pengalaman sebelum waktu acuan didukung kajian aspek bahasa Indonesia.
- **lex-0082 / pat-0082 (akan): TERVERIFIKASI.** Penanda prospektif dengan kemungkinan nuansa niat/prediksi sesuai konteks; jangan dianggap menjamin peristiwa pasti terjadi.
- Sumber: [TBBI Edisi Keempat](https://repositori.kemendikdasmen.go.id/16351/1/Tata%20Bahasa%20Baku%20Bahasa%20Ind.pdf), Bab 4; Grangé (2010), [Aspect and modality in Indonesian: The case of sudah, telah, pernah and sempat](https://doi.org/10.17510/wacana.v12i2.117).

### Batch 017 — seluruh / semua / setiap
- **lex-0085 / pat-0085 (seluruh): TERVERIFIKASI.**
- **Pembanding semua: TERVERIFIKASI sebagai pembedaan makna, bukan entri JSONL baru.** Rujukan Badan Bahasa menjelaskan bahwa `semua` menonjolkan hitungan setiap anggota, sedangkan `seluruh` menonjolkan keseluruhan sebagai satu kesatuan/kolektif. Dalam sejumlah konteks keduanya dapat saling menggantikan; perbedaannya bukan mutlak.
- **lex-0086 / pat-0086 (setiap): TERVERIFIKASI.** Makna distributif—menerapkan pernyataan pada anggota satu per satu—dan pola umum `setiap + nomina tunggal` sesuai.
- Sumber: [Petunjuk Praktis Berbahasa Indonesia](https://repositori.kemendikdasmen.go.id/3420/1/Petunjuk%20praktis%20berbahasa%20indonesia.pdf), bagian “Semua, seluruh, segala, sekalian, dan segenap”; TBBI Edisi Keempat.

### Batch 018 — meN- / di- / ter- / -kan
- **lex-0088 / pat-0088 (meN- nasal): TERVERIFIKASI.** Contoh `membaca` dari `baca` dan `menulis` dari `tulis` sesuai kaidah morfofonemik prefiks `meng-`; bentuk permukaan menyesuaikan fonem awal pangkal.
- **lex-0089 / pat-0089 (di- pasif vs preposisi): TERVERIFIKASI.** `ditulis` adalah prefiks pasif serangkai; `di sekolah` adalah preposisi terpisah.
- **lex-0091 / pat-0091 (ter-): PERLU REVISI.** TBBI menguraikan beberapa fungsi verba `ter-`: perfektif/pasif-like, ketidaksengajaan, serta ketaksanggupan/ketakmampuan. TBBI juga menegaskan bahwa nuansa ketidaksengajaan pada contoh seperti `terjatuh` tidak semata-mata berasal dari prefiks; sifat perbuatan/leksem ikut menentukan. Rumusan pola “ter- menandai peristiwa yang tidak disengaja” terlalu kuat jika dipahami sebagai makna afiks otomatis. Perlu dirumuskan ulang sebagai salah satu tafsir konstruksi/leksem tertentu.
- **lex-0092 / pat-0092 (-kan benefaktif/kausatif): TERVERIFIKASI.** TBBI memberi contoh benefaktif `mengambilkan tamu air minum` dan fungsi kausatif pada kelompok verba ber-`-kan`. Fungsi harus ditentukan dari pangkal dan konstruksi; tidak semua kata berakhiran `-kan` benefaktif.
- Sumber utama: [TBBI Edisi Keempat](https://repositori.kemendikdasmen.go.id/16351/1/Tata%20Bahasa%20Baku%20Bahasa%20Ind.pdf), Bab 4 §4.1.3.3.3–§4.1.3.3.6 dan §4.2.2.3–§4.2.2.5.

## 3. BAGIAN 2 — Verifikasi Sumber Pilar D
Tanggal pemeriksaan halaman: 20 November 2026. Status menilai kecocokan klaim dan qualifiers dengan sumber resmi spesifik.

### Batch 007 — astronomi
- **fact-0033 (rotasi sideris Merkurius sekitar 58,6 hari): PERLU REVISI.** NASA NSSDC mencantumkan 1.407,6 jam, setara sekitar 58,65 hari; NASA Mercury Facts membulatkan menjadi 59 hari. Nilai `58,6` perlu diselaraskan dengan presisi sumber (misalnya sekitar 58,65 hari atau sekitar 59 hari), bukan memotong 58,65 menjadi 58,6 tanpa penjelasan. Sumber: [NASA NSSDC Mercury Fact Sheet](https://nssdc.gsfc.nasa.gov/planetary/factsheet/mercuryfact.html); [NASA Mercury Facts](https://science.nasa.gov/mercury/facts/).
- **fact-0034 (orbit Merkurius sekitar 88 hari): TERVERIFIKASI.** NSSDC mencantumkan periode orbit sideris 87,969 hari; pembulatan menjadi 88 hari tepat. Sumber: [NASA NSSDC Mercury Fact Sheet](https://nssdc.gsfc.nasa.gov/planetary/factsheet/mercuryfact.html).
- **fact-0035 (orbit sideris Bulan 27,3 hari vs siklus fase 29,5 hari): TERVERIFIKASI.** NASA menjelaskan kedua periode tersebut secara eksplisit. Sumber: [NASA Top Moon Questions](https://science.nasa.gov/moon/top-moon-questions/); [NASA Moon Phases](https://science.nasa.gov/moon/moon-phases/).
- **fact-0036 (Bulan satu-satunya satelit alami Bumi): TERVERIFIKASI.** NASA menyatakan secara eksplisit bahwa Bulan adalah satu-satunya satelit alami Bumi. Sumber: [NASA Moon Facts](https://science.nasa.gov/moon/facts/).
- **fact-0037 (tahun Mars sekitar 687 hari Bumi): TERVERIFIKASI.** NASA mencantumkan 669,6 sol atau 687 hari Bumi; qualifier membedakannya dari hari Matahari Mars. Sumber: [NASA Mars Facts](https://science.nasa.gov/mars/facts/).

### Batch 010 — astronomi
- **fact-0048 (definisi satuan astronomi 149.597.870.700 meter): PERLU REVISI.** Nilai tepat benar menurut IAU Resolution B2 (2012), tetapi simbol resmi yang direkomendasikan IAU adalah `au` (huruf kecil), sedangkan subject record menggunakan `AU`. Tautan NASA yang dicantumkan pada record juga terlalu umum dan bukan sumber spesifik definisi numerik. Pada revisi data berikutnya, gunakan `au` dan utamakan sumber primer IAU; nilai 149.597.870.700 m tetap benar. Sumber: [IAU Resolution B2 (2012), PDF resmi](https://www.iau.org/static/resolutions/IAU2012_English.pdf).

### Batch 014 — hidrologi
- **fact-0068 (transpirasi): TERVERIFIKASI.** USGS mendefinisikan pelepasan uap air dari daun melalui stomata dan membedakannya dari evaporasi. [USGS Evapotranspiration and the Water Cycle](https://www.usgs.gov/water-science-school/science/evapotranspiration-and-water-cycle).
- **fact-0069 (limpasan permukaan): TERVERIFIKASI.** USGS mendukung aliran limpasan di permukaan dan faktor meteorologi, tanah, vegetasi, serta topografi. [USGS Surface Runoff and the Water Cycle](https://www.usgs.gov/water-science-school/science/surface-runoff-and-water-cycle).
- **fact-0070 (air tanah): TERVERIFIKASI.** USGS menjelaskan air tanah tersimpan pada pori, rekahan, dan ruang antarpartikel di zona jenuh. [USGS Groundwater Storage and the Water Cycle](https://www.usgs.gov/water-science-school/science/groundwater-storage-and-water-cycle).
- **fact-0071 (akuifer): TERVERIFIKASI.** USGS menjelaskan formasi pembawa air dan peran porositas/permeabilitas. [USGS Aquifers and Groundwater](https://www.usgs.gov/water-science-school/science/aquifers-and-groundwater).
- **fact-0072 (DAS): TERVERIFIKASI.** USGS mendefinisikan watershed sebagai wilayah daratan yang mengalirkan air menuju sungai, danau, atau titik keluaran; batasnya berkaitan dengan punggung topografi. [USGS Watersheds and Drainage Basins](https://www.usgs.gov/water-science-school/science/watersheds-and-drainage-basins).

### Batch 015 — hidrologi
- **fact-0073 (pengisian ulang air tanah): TERVERIFIKASI.** USGS menjelaskan infiltrasi yang mencapai zona jenuh dan mengisi ulang akuifer; tidak semua infiltrasi otomatis menjadi recharge. [USGS Infiltration and the Water Cycle](https://www.usgs.gov/water-science-school/science/infiltration-and-water-cycle); [USGS Groundwater Storage and the Water Cycle](https://www.usgs.gov/water-science-school/science/groundwater-storage-and-water-cycle).
- **fact-0074 (muka air tanah): PERLU REVISI.** Sumber edukatif USGS menyebut permukaan atas zona jenuh sebagai water table. Namun publikasi teknis USGS mengingatkan bahwa menyamakannya secara universal dengan puncak zona jenuh dapat terlalu sederhana; definisi hidrogeologi perlu dikualifikasi sebagai permukaan tekanan atmosfer pada akuifer tak tertekan. Tambahkan konteks tersebut pada revisi data mendatang. Sumber: [USGS Aquifers and Groundwater](https://www.usgs.gov/water-science-school/science/aquifers-and-groundwater); [USGS The Water Table (2010)](https://pubs.usgs.gov/publication/70041610).
- **fact-0075 (mata air): TERVERIFIKASI.** USGS mendefinisikan spring sebagai tempat air tanah muncul ke permukaan; debit bergantung pada kondisi geologi/hidrologi. [USGS Springs and the Water Cycle](https://www.usgs.gov/water-science-school/science/springs-and-water-cycle).
- **fact-0076 (debit aliran sungai): TERVERIFIKASI.** USGS mendefinisikan discharge sebagai volume air yang melewati titik/penampang per satuan waktu. [USGS How Streamflow is Measured](https://www.usgs.gov/water-science-school/science/how-streamflow-measured).
- **fact-0077 (kualitas air): TERVERIFIKASI.** USGS mendefinisikannya sebagai kesesuaian air untuk penggunaan tertentu berdasarkan karakteristik fisik, kimia, dan biologis. [USGS Water Quality](https://www.usgs.gov/water-science-school/water-quality).

### Batch 016 — atmosfer
- **fact-0078 (uap air): TERVERIFIKASI.** NOAA menjelaskan fase gas air di atmosfer dan sumbernya, termasuk evaporasi serta transpirasi. [NOAA What Is Humidity?](https://www.nesdis.noaa.gov/about/k-12-education/atmosphere/what-humidity).
- **fact-0079 (kelembapan relatif): TERVERIFIKASI.** NOAA menjelaskan perbandingan uap air aktual dengan kapasitas maksimum udara pada suhu saat itu; 100% berarti jenuh, bukan otomatis hujan. [NOAA What Is Humidity?](https://www.nesdis.noaa.gov/about/k-12-education/atmosphere/what-humidity).
- **fact-0080 (tekanan udara): TERVERIFIKASI.** NOAA/NWS mendukung definisi tekanan sebagai gaya per satuan luas/berat kolom udara di atas lokasi. [NOAA Air Pressure](https://www.noaa.gov/jetstream/atmosphere/air-pressure); [NWS Basic Weather Education](https://www.weather.gov/crp/weather_education).
- **fact-0081 (angin): TERVERIFIKASI.** NOAA menjelaskan gaya gradien tekanan dari tinggi ke rendah dan pengaruh Coriolis serta gesekan terhadap aliran nyata. [NOAA Origin of Wind](https://www.noaa.gov/jetstream/synoptic/origin-of-wind).
- **fact-0082 (awan): TERVERIFIKASI.** NOAA mendukung pembentukan awan melalui pendinginan dan kondensasi uap air pada inti kondensasi menjadi tetes air dan/atau kristal es. [NOAA How Clouds Form](https://www.noaa.gov/jetstream/clouds/how-clouds-form); [NOAA Clouds](https://www.nesdis.noaa.gov/our-environment/clouds).

### Batch 017 — ekologi
- **fact-0083 (ekosistem): TERVERIFIKASI.** EPA mendefinisikan ekosistem sebagai komunitas organisme hidup bersama komponen nonhidup yang berinteraksi; batas ekosistem tidak selalu tegas. [US EPA Ecological Condition](https://www.epa.gov/report-environment/ecological-condition).
- **fact-0084 (habitat): TERVERIFIKASI.** USFWS mendukung kebutuhan habitat berupa makanan, air, tempat berlindung, dan ruang; USFWS juga memberi contoh perubahan pemakaian habitat sepanjang siklus hidup pada spesies tertentu. [USFWS Junior Refuge Manager Booklet](https://www.fws.gov/sites/default/files/documents/JuniorRefugeManagerBooklet_Reelfoot.pdf); [USFWS Threats to Birds: Habitat Impacts](https://www.fws.gov/story/threats-birds-habitat-impacts).
- **fact-0085 (keanekaragaman hayati): TERVERIFIKASI.** CBD mendefinisikan variasi kehidupan dalam spesies, antarspesies, dan ekosistem; ringkasan tiga tingkat gen, spesies, ekosistem konsisten. [CBD Convention Text, Article 2](https://www.cbd.int/convention/articles/default.shtml?a=cbd-02).
- **fact-0086 (penyerbukan): TERVERIFIKASI.** USDA Forest Service menjelaskan transfer serbuk sari dari antera ke stigma dan agen penyerbuk berupa angin, air, atau hewan; penyerbukan berbeda dari pembuahan. [USDA Forest Service Pollinator-Friendly BMPs, Glossary](https://www.fs.usda.gov/wildflowers/pollinators/BMPs/documents/PollinatorFriendlyBMPsFederalLands05152015.pdf).
- **fact-0087 (rantai makanan): TERVERIFIKASI.** NPS menjelaskan perpindahan energi antarorganisme; materi NPS tentang daur materi juga mendukung perpindahan materi melalui rantai makanan dan peran dekomposer. [NPS Food Chain](https://www.nps.gov/teachers/classrooms/food-chain.htm); [NPS Matter in Motion](https://www.nps.gov/teachers/classrooms/matter-in-motion.htm).

### Batch 018 — geologi
- **fact-0088 (siklus batuan): TERVERIFIKASI.** USGS menggambarkan hubungan batuan beku, sedimen/batuan sedimen, dan metamorf melalui jalur proses yang beragam, bukan satu urutan wajib. [USGS Bulletin 2195 — The Rock Cycle](https://pubs.usgs.gov/bul/2195/b2195.pdf); [USGS Open-File Report 94-636](https://pubs.usgs.gov/of/1994/0636/report.pdf).
- **fact-0089 (batuan beku): TERVERIFIKASI.** USGS mendukung pembentukan saat magma/lava mendingin, mengkristal, dan membeku; magma di bawah permukaan dibedakan dari lava di permukaan. [USGS What Are Igneous Rocks?](https://www.usgs.gov/faqs/what-are-igneous-rocks).
- **fact-0090 (batuan sedimen): TERVERIFIKASI.** USGS mendukung pembentukan dari material hasil pelapukan/organisme, pengendapan, pemadatan/penyemenan, serta presipitasi kimia pada sebagian jenis. [USGS What Are Sedimentary Rocks?](https://www.usgs.gov/faqs/what-are-sedimentary-rocks).
- **fact-0091 (batuan metamorf): TERVERIFIKASI.** USGS menjelaskan perubahan batuan asal oleh panas, tekanan, dan fluida; metamorfisme tidak berarti batuan melebur seluruhnya. [USGS What Are Metamorphic Rocks?](https://www.usgs.gov/faqs/what-are-metamorphic-rocks).
- **fact-0092 (lempeng tektonik): TERVERIFIKASI.** USGS menjelaskan lempeng litosfer bergerak relatif satu sama lain di atas astenosfer/mantel yang dapat mengalir perlahan pada skala waktu geologi; jenis batas lempeng dan kaitannya dengan gempa didukung glosarium USGS. [USGS Are Tectonic Plates Floating on Magma?](https://www.usgs.gov/faqs/are-tectonic-plates-floating-magma); [USGS Earthquake Hazards Glossary](https://www.usgs.gov/glossary/earthquake-hazards-program).

## 4. Daftar tindak lanjut PERLU REVISI
Perubahan dataset tidak diizinkan dan tidak dilakukan. Lima temuan yang perlu dibawa ke usulan revisi tersendiri:
1. **lex-0077:** ganti contoh `Ia berpikir dalam sebelum menjawab` dengan contoh yang idiomatis; pertahankan pembedaan preposisi/adjektiva.
2. **pat-0091 / lex-0091:** rumuskan ulang deskripsi `ter-`; makna tidak sengaja tidak otomatis berasal dari prefiks saja.
3. **fact-0033:** selaraskan presisi rotasi sideris Merkurius dengan sumber (sekitar 58,65 hari dari 1.407,6 jam, atau sekitar 59 hari dalam pembulatan NASA).
4. **fact-0048:** gunakan simbol IAU `au` dan sumber primer IAU; nilai 149.597.870.700 m benar.
5. **fact-0074:** tambahkan kualifikasi hidrogeologi untuk definisi muka air tanah, khususnya konteks akuifer tak tertekan/permukaan tekanan atmosfer.

## 5. Status dan batas izin setelah verifikasi
- Hasil audit: **43 TERVERIFIKASI; 5 PERLU REVISI** dari 48 unit pemeriksaan.
- **Seluruh record JSONL Batch 001–018 tetap DRAFT.** Status TERVERIFIKASI dalam log ini tidak mengubah field `verification_status` pada dataset.
- Tidak ada file JSONL yang diedit.
- `SCHEMA_TEMPORARY.md`, `docs/ilis_project_state.md`, kode ILIS, tes, workflow CI, SQLite, dan `tests/beta_suite.py` tidak disentuh.
- Tidak ada integrasi dataset ke ILIS.
- Lima item PERLU REVISI menunggu instruksi/persetujuan tersendiri sebelum perubahan dataset dilakukan.
