# ILIS Semantic Engine Contract

**Status:** Draft for V1  
**Contract version:** 1.0

Dokumen ini menetapkan kontrak data antara ILVE dan Semantic Engine.

## 1. Batasan V1

V1 Semantic Engine hanya menangani kalimat pernyataan sederhana dengan satu predikasi utama. Kalimat kompleks, majemuk, bertingkat, tanya, perintah, serta resolusi rujukan lintas kalimat belum menjadi cakupan V1. Input di luar cakupan harus ditandai unsupported atau low_confidence; engine tidak boleh memaksakan interpretasi.

## 2. Alur data

Pipeline mengirimkan dua hal kepada Semantic Engine: (1) teks asli persis seperti diterima, dan (2) hasil ILVE. Teks asli wajib dipertahankan. Normalisasi ILVE adalah petunjuk untuk memahami variasi, bukan pengganti teks asli.

## 3. Kontrak input

Bentuk input antarmodul yang dituju:

| Field | Tipe | Wajib | Keterangan |
|---|---|---:|---|
| contract_version | string | Ya | Versi kontrak, 1.0. |
| original_text | string | Ya | Teks asli, termasuk kapitalisasi dan tanda baca. |
| ilve | object | Ya | Hasil pemrosesan ILVE. |
| ilve.normalized_text | string | Ya | Teks hasil normalisasi variasi. |
| ilve.tokens | array of string | Ya | Token hasil ILVE. |
| ilve.variation_hints | array | Ya | Petunjuk variasi; boleh kosong. |

Setiap variation hint minimal memuat surface (bentuk asli), normalized (bentuk normalisasi), dan category (misalnya slang, abbreviation, typo, nonstandard). Adapter pipeline memetakan keluaran aktual ILVE ke kontrak ini. Implementasi ILVE boleh memiliki metadata tambahan.

Contoh input untuk “Gue lagi makan nasi.”:

```json
{
  "contract_version": "1.0",
  "original_text": "Gue lagi makan nasi.",
  "ilve": {
    "normalized_text": "saya lagi makan nasi.",
    "tokens": ["saya", "lagi", "makan", "nasi", "."],
    "variation_hints": [
      {"surface": "Gue", "normalized": "saya", "category": "slang"}
    ]
  }
}
```

Contoh ini adalah ilustrasi kontrak, bukan klaim bahwa keluaran internal ILVE saat ini sudah persis seperti ini.

## 4. Struktur output semantik

Semantic Engine menghasilkan objek dengan dua belas field inti berikut. Semua field harus tersedia pada hasil semantik; gunakan null atau nilai enum yang ditentukan jika informasi tidak tersedia.

| Field | Tipe | Keterangan |
|---|---|---|
| Actor | string atau null | Pelaku/entitas yang menjadi subjek predikasi; gunakan bentuk kanonis bila dapat ditentukan. |
| Predicate | string atau null | Tindakan, keadaan, atau relasi utama; gunakan lema/bentuk kanonis. |
| Patient/Object | string atau null | Entitas yang dikenai tindakan atau objek predikat. |
| Recipient | string atau null | Penerima atau pihak yang memperoleh sesuatu. |
| Location | string atau null | Lokasi yang disebutkan secara eksplisit. |
| Time | string atau null | Keterangan waktu eksplisit; jangan simpulkan dari aspek. |
| Aspect | string | progressive, completed, prospective, habitual, atau unspecified. |
| Negation | string | none, negative, not_yet, atau identity_negative. |
| Modality | string | none, ability, obligation, possibility, desire, atau permission. |
| Intent | string | Jenis tindak tutur; nilai normal V1 adalah assertion. |
| Register | string | formal, informal, slang, atau unknown. |
| Confidence | number | Keyakinan parsing dalam rentang 0.0–1.0, bukan kebenaran faktual isi kalimat. |

### Aturan interpretasi

- Actor adalah peran semantik, bukan otomatis kata pertama.
- Predicate menyatakan inti tindakan/keadaan; “makan” menjadi makan.
- Patient/Object untuk contoh ini adalah “nasi”.
- Recipient hanya diisi jika dinyatakan atau dapat diidentifikasi langsung.
- Location dan Time hanya diisi jika eksplisit dan dapat dikenali.
- Aspect berbeda dari Time. “Lagi” menandai progressive, tetapi tidak menentukan waktu kalender.
- Negation membedakan negasi umum, belum terjadi, dan negasi identitas. Jika tidak ada, gunakan none.
- Modality mencatat kemampuan, kewajiban, kemungkinan, keinginan, atau izin. Jika tidak ada, gunakan none.
- Intent V1 terutama assertion; enum lain tidak berarti jenis kalimat itu sudah didukung.
- Register menggambarkan ragam ujaran, bukan penilaian benar/salah.

## 5. Contoh output JSON

Untuk input “Gue lagi makan nasi.”, hasil yang diharapkan:

```json
{
  "contract_version": "1.0",
  "status": "supported",
  "original_text": "Gue lagi makan nasi.",
  "ilve": {
    "normalized_text": "saya lagi makan nasi.",
    "tokens": ["saya", "lagi", "makan", "nasi", "."],
    "variation_hints": [
      {"surface": "Gue", "normalized": "saya", "category": "slang"}
    ]
  },
  "semantics": {
    "Actor": "saya",
    "Predicate": "makan",
    "Patient/Object": "nasi",
    "Recipient": null,
    "Location": null,
    "Time": null,
    "Aspect": "progressive",
    "Negation": "none",
    "Modality": "none",
    "Intent": "assertion",
    "Register": "slang",
    "Confidence": 0.98
  }
}
```

“Gue” dinormalisasi menjadi aktor kanonis “saya”, tetapi register slang tetap tercatat. “Lagi” menjadi aspek progressive. Tidak ada penerima, lokasi, atau waktu eksplisit. Nilai confidence 0.98 hanya ilustrasi; nilai produksi harus berasal dari mekanisme penilaian engine dan diuji.

## 6. Status output

Output selalu menggunakan pembungkus berikut:

| Field | Tipe | Keterangan |
|---|---|---|
| contract_version | string | Versi kontrak output. |
| status | string | supported, unsupported, atau low_confidence. |
| semantics | object atau null | Objek dua belas field semantik atau null. |

- supported: input sesuai cakupan V1 dan hasil memenuhi ambang keyakinan implementasi.
- low_confidence: input dapat dianalisis, tetapi satu atau lebih bagian tidak jelas. Struktur parsial boleh dikembalikan; field yang tidak diketahui harus null.
- unsupported: struktur di luar cakupan V1 atau tidak dapat diproses secara bertanggung jawab; semantics harus null.

Ambang status ditentukan implementasi, dicatat, dan diuji. Konsumen tidak boleh menganggap confidence tinggi sebagai bukti bahwa isi kalimat benar di dunia nyata.

## 7. Aturan kompatibilitas antar modul

1. Nama dan makna field inti tidak boleh diubah diam-diam.
2. Field wajib harus hadir; gunakan null atau enum yang ditentukan untuk informasi yang tidak tersedia.
3. Hasil semantik adalah interpretasi teks, bukan fakta dunia yang sudah terverifikasi.
4. Semantic Engine tidak menyimpan pengetahuan dunia, memutuskan kebenaran fakta, atau melakukan inferensi; itu tugas modul Knowledge dan Reasoning.
5. Perubahan yang memutus kompatibilitas memerlukan kenaikan versi kontrak dan pembaruan tes integrasi.
6. Teks asli dan petunjuk variasi ILVE harus tetap dapat ditelusuri.

## 8. Kriteria penerimaan V1

- Pipeline mengirim teks asli dan hasil ILVE.
- Semantic Engine menyediakan seluruh dua belas field untuk kalimat sederhana yang didukung.
- Informasi yang tidak disebutkan tidak diisi dengan tebakan.
- Variasi seperti “gue” dapat dipahami tanpa menghilangkan informasi register.
- “Lagi” tidak disalahartikan sebagai waktu kalender.
- Kalimat kompleks yang belum didukung ditandai secara eksplisit.
- Tes otomatis memverifikasi struktur, enum, nullability, dan status.

---

Dokumen ini mendefinisikan kontrak data, bukan klaim bahwa Semantic Engine sudah diimplementasikan. Kemampuan aktual harus dibuktikan melalui kode dan pengujian.
