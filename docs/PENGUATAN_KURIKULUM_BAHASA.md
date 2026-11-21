# DOKUMEN PENGUATAN KURIKULUM PEMAHAMAN BAHASA INDONESIA ILIS
**Target Lokasi:** `docs/PENGUATAN_KURIKULUM_BAHASA.md`  
**Branch:** `ilis-v2-development`  
**Status:** Dokumen Penguatan & Rujukan Pra-Implementasi (Non-Kode, Non-Dataset)

---

## 1. Maksud & Urgensi Dokumen Penguatan
Dokumen ini disusun saat fase dokumentasi kurikulum (`docs/KURIKULUM_PEMAHAMAN_BAHASA.md` serta `docs/TAHAP_01_FONDASI_DASAR.md` hingga `docs/TAHAP_04_WACANA_DAN_VARIASI_BAHASA.md`) telah selesai dan **belum ada implementasi kode atau perubahan dataset yang berjalan**.

Tujuannya adalah mengunci prinsip, urutan kerja, dan batasan tegas sebelum implementasi dimulai, agar pengembangan tidak melenceng ke pengayaan pengetahuan umum yang prematur atau melompati fondasi bahasa dasar.

---

## 2. Penguncian Prioritas Utama
1. **Bahasa & Pemahaman Maksud di Atas Pengetahuan Umum:** Fokus utama fase ini adalah kemampuan ILIS mengenali bentuk bahasa, struktur kalimat, konteks, maksud penutur, dan alur percakapan bahasa Indonesia sehari-hari.
2. **Penundaan Pengetahuan Umum:** Penambahan dan perluasan data pengetahuan umum (termasuk sisa 10% dari penutupan 18 *batch* sebelumnya) ditunda dan dipisahkan dari jalur implementasi bahasa hingga fondasi bahasa terbentuk kuat.
3. **Paham Maksud > Hafal Aturan Kaku:** Aturan tata bahasa dan istilah linguistik baku digunakan sebagai kerangka acuan yang jelas, namun target akhirnya adalah ketepatan memahami maksud di balik ujaran manusia.

---

## 3. Aturan Urutan Tahapan (Anti-Loncat Tahap)
Implementasi dan pengujian wajib mengikuti urutan bertahap tanpa melompat:
* **Tahap 1 (`TAHAP_01_FONDASI_DASAR.md`):** Fonologi & ejaan dasar, 11 kelas kata dengan istilah baku, serta kata dasar berfrekuensi tinggi.
* **Tahap 2 (`TAHAP_02_KATA_DAN_KALIMAT.md`):** Morfologi dasar (prefiks, sufiks, konfiks, reduplikasi, perubahan bunyi), frasa, pola kalimat dasar (termasuk S-P-O-K), serta aktif/pasif.
* **Tahap 3 (`TAHAP_03_MAKSUD_DAN_KONTEKS.md`):** Bentuk vs maksud sebenarnya, deiksis & rujukan, kalimat tidak lengkap/parsial, negasi (*tidak, bukan, belum, jangan*), aspek waktu, dan modalitas.
* **Tahap 4 (`TAHAP_04_WACANA_DAN_VARIASI_BAHASA.md`):** Giliran bicara, kesinambungan & perpindahan topik, klarifikasi/koreksi, serta variasi bahasa (baku/tidak baku, formal/santai, lisan/tulisan, ungkapan umum).

**Syarat Naik Tahap:** Setiap tahap harus melalui evaluasi dan uji yang memadai sebelum memulai implementasi tahap berikutnya.

---

## 4. Pagar Pengaman Eksekusi (Guardrails)
* **Jangan ubah dataset yang ada** dan **jangan ubah kode mesin inti** hanya karena menyusun atau memperkuat dokumen perencanaan.
* **Tetap gunakan istilah linguistik baku** (*Nomina, Verba, Adjektiva, Adverbia, Pronomina, Numeralia, Preposisi, Konjungsi, Interjeksi, Artikula, Partikel*) sebagai acuan utama.
* **Utamakan kejujuran batas pemahaman:** Lebih baik mengenali ketidakjelasan, membutuhkan konteks/klarifikasi, atau menyatakan belum tahu daripada menebak maksud atau fakta secara asal.
* **Evaluasi manual tetap dijaga:** Pengujian dan kontrol langsung pada *playground* tetap dilakukan secara bertahap dan terukur.

---

## 5. Penutup
Dokumen ini menjadi pengingat bersama bagi seluruh penyusunan rencana dan implementasi berikutnya di `ilis-v2-development`: **bangun fondasi bahasa tahap demi tahap, jaga batas cakupan, dan dahulukan pemahaman maksud percakapan.**
