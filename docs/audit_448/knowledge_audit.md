# Audit 448 Record — Pilar D: Knowledge

- **Basis branch:** `ilis-v2-development`
- **Basis SHA:** `544083bffc0e2d2dd757648178e5c6675609b4e8` (setelah merge PR #25)
- **Audit branch:** `audit-448-knowledge`
- **Cakupan:** 90 fakta, 18 file JSONL, `fact-0003`–`fact-0092`.
- **Batas:** dokumentasi audit saja. Tidak mengubah JSONL, kode, tes, workflow, SQLite, atau `main`.
- **Status dataset:** seluruh 90 fakta tetap DRAFT.

## 1. Ringkasan hasil audit

| Status | Jumlah | Dasar |
|---|---:|---|
| PASS | 24 | Memiliki hasil verifikasi sumber terdahulu yang tercatat dalam `source_review_notes.md`; tidak berarti status JSONL berubah menjadi verified. |
| REVISE | 3 | Ada temuan substantif terdahulu yang jelas dan belum boleh dianggap selesai hanya karena catatan sudah ada. |
| REVIEW | 63 | Belum memiliki bukti pemeriksaan spesifik yang cukup dalam log terdahulu, atau pembaruan sumber perlu pemeriksaan ulang. |
| **Total** | **90** | Seluruh record terinventarisasi. |

**PASS/REVISE di laporan audit adalah status hasil telaah, bukan `verification_status` dataset.** Semua JSONL tetap `draft`.

## 2. Validasi inventaris dan struktur

- 18/18 file `data/indonesian/knowledge/batch_001.jsonl` sampai `batch_018.jsonl` berhasil diambil dan diparse.
- 90/90 record terbaca.
- Setiap batch berisi 5 record.
- Rentang ID: `fact-0003` sampai `fact-0092`.
- Semua record memiliki `fact_id`, `subject`, `predicate`, `object`, `source`, dan `verification_status`.
- Seluruh 90 record memiliki `verification_status: draft`.
- 75 record memiliki URL pada field `source`; 15 tidak memiliki URL. Ketiadaan URL tidak otomatis berarti fakta salah, tetapi sumber primer/rujukan spesifik tetap harus dibuktikan sebelum PASS.

Pemeriksaan ini memastikan kelengkapan dasar dan parse JSONL; belum membuktikan ketepatan semua klaim.

## 3. Temuan REVISE yang sudah terdokumentasi

### fact-0033 — periode rotasi sideris Merkurius
- Log sumber terdahulu: nilai 1.407,6 jam setara sekitar 58,65 hari; angka 58,6 perlu diselaraskan dengan presisi atau dinyatakan sebagai pembulatan yang tepat.
- Tindakan: jangan menaikkan status; koreksi data hanya melalui instruksi/otorisasi Owner yang terpisah.
- Rujukan terdahulu: NASA NSSDC Mercury Fact Sheet dan NASA Mercury Facts.

### fact-0048 — satuan astronomi
- Log sumber terdahulu: nilai definisi 149.597.870.700 meter benar menurut IAU Resolution B2 (2012), tetapi simbol yang direkomendasikan IAU adalah `au` (huruf kecil); sumber NASA pada record terlalu umum untuk definisi numerik.
- Tindakan: catat perbedaan simbol dan kebutuhan rujukan primer IAU; jangan mengubah JSONL pada audit ini.

### fact-0074 — muka air tanah
- Log terdahulu menandai perlu kualifikasi: untuk akuifer tak-tertekan, water table adalah permukaan air bertekanan atmosfer. Jangan menggeneralisasi definisi itu ke akuifer tertekan.
- Pemeriksaan ulang halaman USGS FAQ yang sekarang dicantumkan pada record mendukung pembedaan tersebut secara eksplisit: permukaan air akuifer tak-tertekan berada pada tekanan atmosfer; permukaan akuifer tertekan berada di bawah tekanan.
- Halaman publikasi USGS Holzer (2010) tidak berhasil dibaca oleh alat penelusuran pada pemeriksaan ini (403), sehingga bagian teknis pendukungnya belum dapat diverifikasi ulang secara independen.
- Tindakan: tetap REVISE sampai redaksi/qualifier dan dukungan publikasi teknis dinilai memadai oleh reviewer. URL yang tidak dapat dibaca bukan bukti bahwa isinya salah.

## 4. Pemeriksaan ulang fact-0073 sampai fact-0076 (URL PR #21)

### fact-0073 — pengisian ulang air tanah
- URL infiltrasi USGS berhasil dibuka. USGS membedakan air yang hanya masuk ke lapisan tanah dangkal dari sebagian air yang meresap lebih dalam dan mengisi ulang akuifer; halaman juga menyebut faktor yang memengaruhi infiltrasi dan recharge.
- URL Groundwater: What is Groundwater? terhalang pemeriksaan anti-bot saat audit, tetapi halaman infiltrasi yang dapat dibaca mendukung inti klaim dan qualifier bahwa infiltrasi tidak otomatis seluruhnya menjadi recharge.
- **Audit: PASS**, berdasarkan dukungan langsung dari halaman infiltrasi yang dapat diakses dan catatan sumber sebelumnya. Tetap DRAFT pada JSONL.

### fact-0074 — muka air tanah
- URL USGS FAQ berhasil dibuka dan mendukung definisi tekanan atmosfer pada water-table/unconfined aquifer serta membedakannya dari confined aquifer.
- URL publikasi Holzer (2010) gagal dibaca (403). Temuan substantif dan kebutuhan qualifier tetap dicatat.
- **Audit: REVISE**, belum dapat ditutup.

### fact-0075 — mata air
- URL USGS Springs and the Water Cycle berhasil dibuka. USGS menjelaskan spring sebagai tempat air yang bergerak di bawah tanah menemukan bukaan ke permukaan; debit dipengaruhi geologi, tekanan akuifer, area pemasok, curah hujan, dan pengambilan air tanah.
- **Audit: PASS**, klaim dan qualifiers utama sesuai. Tetap DRAFT pada JSONL.

### fact-0076 — debit aliran sungai
- Klaim dasarnya konsisten dengan catatan verifikasi USGS terdahulu: debit/discharge adalah volume air per satuan waktu dan dibedakan dari kecepatan aliran serta tinggi muka air.
- Pada pemeriksaan ulang, URL `How Streamflow is Measured` terkena anti-bot dan URL `Streamgaging Basics` mengembalikan respons 405; isi halaman tidak berhasil diperiksa langsung pada sesi ini.
- **Audit: REVIEW**, bukan karena klaim terbukti salah, melainkan URL baru belum berhasil diverifikasi ulang secara memadai. Perlu reviewer membuka sumber secara langsung atau mencatat sumber resmi alternatif.

## 5. Status per record

| Record | Status audit | Catatan |
|---|---|---|
| fact-0003 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0004 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0005 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0006 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0007 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0008 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0009 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0010 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0011 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0012 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0013 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0014 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0015 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0016 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0017 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0018 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0019 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0020 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0021 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0022 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0023 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0024 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0025 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0026 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0027 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0028 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0029 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0030 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0031 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0032 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0033 | REVISE | Temuan substantif/qualifier tercatat; menunggu tindak lanjut dan review. |
| fact-0034 | PASS | Terverifikasi pada log sumber terdahulu; record tetap DRAFT. |
| fact-0035 | PASS | Terverifikasi pada log sumber terdahulu; record tetap DRAFT. |
| fact-0036 | PASS | Terverifikasi pada log sumber terdahulu; record tetap DRAFT. |
| fact-0037 | PASS | Terverifikasi pada log sumber terdahulu; record tetap DRAFT. |
| fact-0038 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0039 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0040 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0041 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0042 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0043 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0044 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0045 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0046 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0047 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0048 | REVISE | Temuan substantif/qualifier tercatat; menunggu tindak lanjut dan review. |
| fact-0049 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0050 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0051 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0052 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0053 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0054 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0055 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0056 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0057 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0058 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0059 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0060 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0061 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0062 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0063 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0064 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0065 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0066 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0067 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0068 | PASS | Terverifikasi pada log sumber terdahulu; record tetap DRAFT. |
| fact-0069 | PASS | Terverifikasi pada log sumber terdahulu; record tetap DRAFT. |
| fact-0070 | PASS | Terverifikasi pada log sumber terdahulu; record tetap DRAFT. |
| fact-0071 | PASS | Terverifikasi pada log sumber terdahulu; record tetap DRAFT. |
| fact-0072 | PASS | Terverifikasi pada log sumber terdahulu; record tetap DRAFT. |
| fact-0073 | PASS | Terverifikasi pada log sumber terdahulu; record tetap DRAFT. |
| fact-0074 | REVISE | Temuan substantif/qualifier tercatat; menunggu tindak lanjut dan review. |
| fact-0075 | PASS | Terverifikasi pada log sumber terdahulu; record tetap DRAFT. |
| fact-0076 | REVIEW | URL PR #21 belum berhasil diperiksa ulang secara langsung; klaim pernah diverifikasi terdahulu. |
| fact-0077 | PASS | Terverifikasi pada log sumber terdahulu; record tetap DRAFT. |
| fact-0078 | PASS | Terverifikasi pada log sumber terdahulu; record tetap DRAFT. |
| fact-0079 | PASS | Terverifikasi pada log sumber terdahulu; record tetap DRAFT. |
| fact-0080 | PASS | Terverifikasi pada log sumber terdahulu; record tetap DRAFT. |
| fact-0081 | PASS | Terverifikasi pada log sumber terdahulu; record tetap DRAFT. |
| fact-0082 | PASS | Terverifikasi pada log sumber terdahulu; record tetap DRAFT. |
| fact-0083 | PASS | Terverifikasi pada log sumber terdahulu; record tetap DRAFT. |
| fact-0084 | PASS | Terverifikasi pada log sumber terdahulu; record tetap DRAFT. |
| fact-0085 | PASS | Terverifikasi pada log sumber terdahulu; record tetap DRAFT. |
| fact-0086 | PASS | Terverifikasi pada log sumber terdahulu; record tetap DRAFT. |
| fact-0087 | PASS | Terverifikasi pada log sumber terdahulu; record tetap DRAFT. |
| fact-0088 | PASS | Terverifikasi pada log sumber terdahulu; record tetap DRAFT. |
| fact-0089 | PASS | Terverifikasi pada log sumber terdahulu; record tetap DRAFT. |
| fact-0090 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0091 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |
| fact-0092 | REVIEW | Belum ada bukti pemeriksaan spesifik yang cukup pada log audit yang tersedia. |

## 6. Catatan batas audit

1. Untuk 24 PASS, laporan mengacu pada verifikasi terdahulu yang terdokumentasi; bukan klaim bahwa semua 24 sumber dibuka ulang satu per satu pada sesi ini.
2. Untuk 63 REVIEW, jangan menyimpulkan faktanya salah. Bukti yang ada belum cukup untuk PASS.
3. Tiga REVISE merupakan temuan yang sudah ada pada log verifikasi sumber terdahulu.
4. Pemeriksaan ulang fact-0073–0076 mencatat akses aktual URL yang tersedia pada sesi ini; kegagalan anti-bot/HTTP tidak diperlakukan sebagai bukti isi salah.
5. Tidak ada perubahan pada JSONL, `verification_status`, kode, SQLite, atau `main`.
6. Tidak ada staging atau integrasi dataset ke runtime.

## 7. Pekerjaan lanjutan

- Dola meninjau hasil audit Pilar D dan terutama keputusan REVISE/REVIEW.
- Lakukan verifikasi langsung atas URL fact-0076 dan publikasi Holzer untuk fact-0074.
- Audit spesifik sumber untuk 63 REVIEW sebelum status PASS diberikan.
- Audit Evaluasi (90 record) tetap terpisah, dengan pembagian development/validation/locked final-test dan pemeriksaan duplikasi/leakage.
