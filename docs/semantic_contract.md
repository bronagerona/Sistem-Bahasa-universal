# ILIS Semantic Engine Contract

**Status:** Kontrak stabil 1.0; kemampuan parser berkembang secara kompatibel.  
**Contract version:** 1.0

Dokumen ini menetapkan kontrak data antara ILVE dan Semantic Engine.

## 1. Cakupan dan kompatibilitas

Kontrak input dan output tetap versi 1.0. Wrapper output tetap memuat `contract_version`, `status`, `semantics`, `original_text`, dan `ilve`. Objek `semantics` tetap memiliki **12 field dengan nama dan urutan yang sama** seperti tabel pada Bagian 4. Tidak ada field baru yang ditambahkan.

V1 mendukung pernyataan sederhana. Perluasan V2 menambahkan pola terbatas untuk pertanyaan sederhana, perintah sederhana, variasi negasi, serta frasa waktu dan lokasi. Penambahan nilai Intent `question` dan `command` menggunakan field Intent yang sudah ada; tidak mengubah bentuk JSON atau versi kontrak.

Parser tetap deterministik, berbasis aturan, dan tidak menggunakan LLM. Kalimat kompleks atau pola yang belum dikenali harus tetap menghasilkan `low_confidence` atau `unsupported`, bukan interpretasi spekulatif.

## 2. Alur data

Pipeline mengirimkan teks asli dan hasil ILVE. Teks asli wajib dipertahankan. Normalisasi ILVE adalah petunjuk untuk memahami variasi, bukan pengganti teks asli.

## 3. Kontrak input

| Field | Tipe | Wajib | Keterangan |
|---|---|---:|---|
| contract_version | string | Ya | Versi kontrak, 1.0. |
| original_text | string | Ya | Teks asli, termasuk kapitalisasi dan tanda baca. |
| ilve | object | Ya | Hasil pemrosesan ILVE. |
| ilve.normalized_text | string | Ya | Teks hasil normalisasi variasi. |
| ilve.tokens | array of string | Ya | Token hasil ILVE. |
| ilve.variation_hints | array | Ya | Petunjuk variasi; boleh kosong. |

Setiap variation hint minimal memuat surface, normalized, dan category.

## 4. Struktur output semantik — tetap 12 field

| Field | Tipe | Keterangan |
|---|---|---|
| Actor | string atau null | Pelaku/entitas subjek; null untuk perintah tanpa pelaku eksplisit. |
| Predicate | string atau null | Tindakan, keadaan, atau relasi utama. |
| Patient/Object | string atau null | Entitas yang dikenai tindakan atau objek predikat. |
| Recipient | string atau null | Penerima yang disebutkan eksplisit. |
| Location | string atau null | Lokasi eksplisit. |
| Time | string atau null | Keterangan waktu eksplisit. |
| Aspect | string | progressive, completed, prospective, habitual, atau unspecified. |
| Negation | string | none, negative, not_yet, atau identity_negative. |
| Modality | string | none, ability, obligation, possibility, desire, atau permission. |
| Intent | string | assertion, question, atau command. |
| Register | string | formal, informal, slang, atau unknown. |
| Confidence | number | Keyakinan parsing 0.0–1.0, bukan kebenaran faktual. |

Field, tipe dasar, wrapper, dan jumlah field ini tidak berubah dari kontrak 1.0. V2 hanya memperluas nilai Intent yang dapat dipakai pada kalimat yang didukung.

## 5. Catatan kemampuan tambahan V2

### Pertanyaan sederhana

Contoh: “Apakah api bisa membakar kayu?”

Untuk pola ini, parser dapat mengembalikan Actor=api, Predicate=membakar, Patient/Object=kayu, Modality=ability, dan Intent=question. Tanda tanya atau penanda tanya yang dikenali menjadi bukti bentuk pertanyaan. Pertanyaan bebas yang belum tercakup tidak otomatis dianggap didukung.

### Perintah sederhana

Contoh: “Bunyikan lonceng”.

Untuk perintah langsung, parser mengembalikan Predicate=bunyikan, Patient/Object=lonceng, Actor=null bila pelaku tidak disebutkan, dan Intent=command. Bentuk perintah dengan penanda seperti “tolong” atau “silakan” juga dikenali jika predikatnya termasuk kosakata aturan.

### Negasi

Variasi seperti “tidak”, “tak”, “gak”, “ga”, “nggak”, “enggak”, “belum”, dan “bukan” dikenali sesuai konteks aturan. Contoh “Api tidak selalu membakar kayu” menghasilkan Negation=negative dan Aspect=habitual. Ini adalah ekstraksi pola permukaan, bukan penalaran kuantifikasi atau klaim kebenaran.

### Waktu dan lokasi

Kosakata waktu diperluas untuk beberapa nama hari, bagian hari, “lusa”, “akhir pekan”, “setiap pagi”, dan frasa umum lain yang terdaftar di implementasi. Lokasi dapat dikenali setelah preposisi seperti “di”, “ke”, “dari”, dan “menuju”. Ekstraksi tetap terbatas pada pola eksplisit.

### Penanganan di luar cakupan

- `supported`: pola dikenali dengan struktur yang cukup.
- `low_confidence`: sebagian struktur dikenali, tetapi peran penting belum jelas.
- `unsupported`: bentuk atau struktur tidak didukung, misalnya kalimat majemuk yang belum ditangani.

Engine tidak boleh mengarang Actor, Predicate, waktu, lokasi, atau relasi yang tidak memiliki bukti tekstual.

## 6. Contoh bentuk output

Wrapper output tidak berubah:

```json
{
  "contract_version": "1.0",
  "status": "supported",
  "original_text": "Apakah api bisa membakar kayu?",
  "ilve": {
    "normalized_text": "apakah api bisa membakar kayu?",
    "tokens": ["apakah", "api", "bisa", "membakar", "kayu", "?"],
    "variation_hints": []
  },
  "semantics": {
    "Actor": "api",
    "Predicate": "membakar",
    "Patient/Object": "kayu",
    "Recipient": null,
    "Location": null,
    "Time": null,
    "Aspect": "unspecified",
    "Negation": "none",
    "Modality": "ability",
    "Intent": "question",
    "Register": "unknown",
    "Confidence": 0.9
  }
}
```

Objek semantics di atas berisi tepat 12 field.

## 7. Aturan kompatibilitas

1. Nama, makna, dan urutan 12 field inti tidak boleh diubah diam-diam.
2. Field wajib harus hadir; gunakan null atau enum yang ditentukan bila informasi tidak tersedia.
3. Hasil semantik adalah interpretasi teks, bukan fakta dunia yang terverifikasi.
4. Semantic Engine tidak menyimpan pengetahuan dunia atau memutuskan kebenaran fakta.
5. Perubahan struktur yang memutus kompatibilitas memerlukan kenaikan versi kontrak dan pembaruan tes integrasi.
6. Teks asli dan petunjuk variasi ILVE harus tetap dapat ditelusuri.

## 8. Kriteria penerimaan V2

- Semua tes V1 tetap lulus.
- Pertanyaan “Apakah api bisa membakar kayu?” dikenali sebagai question.
- Perintah “Bunyikan lonceng” dikenali sebagai command.
- Variasi negasi dan aspek habitual dasar dikenali.
- Frasa waktu/lokasi tambahan diekstrak bila sesuai pola.
- Output tetap tepat 12 field semantik.
- Input di luar cakupan tetap low_confidence atau unsupported.
