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
