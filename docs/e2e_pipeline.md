# ILIS End-to-End Pipeline V2

Dokumen ini menjelaskan jalur aplikasi chatbot ILIS dari input sampai keluaran bahasa.

## Alur penuh

1. **Input teks** diterima oleh ChatbotAdapter.respond().
2. **ContextEngine** menyimpan pesan dan menjalankan analyze_semantics().
3. **Semantic Engine** menghasilkan wrapper kontrak 1.0 dengan status supported, low_confidence, atau unsupported, serta tepat dua belas field semantik saat status membawa objek semantics.
4. **Reasoning Engine** dipanggil melalui infer_semantic(semantic_result). Fungsi ini memvalidasi kontrak sebelum memproses Intent, lalu menggunakan fakta dan provenance Knowledge Engine.
5. **Language Generator** menerima hasil reasoning dan semantic_result, memilih register, menyusun kalimat, dan mempertahankan uncertainty.
6. **ChatbotAdapter** mengembalikan teks, semantic_result, reasoning_result, dan metadata.

Pola legacy V1 "Api menyentuh rumah kayu" tetap menggunakan aturan infer_burn_risk() setelah jalur infer_semantic() dipanggil, agar perilaku adapter lama tetap kompatibel.

## Penyesuaian confidence Semantic → Reasoning

Untuk jalur semantic yang memiliki nilai Confidence numerik valid:

    confidence_score_akhir =
        confidence_score_reasoning × confidence_semantic

Contoh: skor reasoning 0.72 dan confidence semantic 0.90 menghasilkan skor akhir 0.648.

Penyesuaian ini hanya mengubah angka confidence_score. Nilai reasoning_type tidak dinaikkan atau diturunkan oleh perkalian ini: unknown dan conflicting tetap demikian, sedangkan verified_inference dan hypothetical_inference tetap mencerminkan status fakta/provenance yang mendasarinya.

Jika semantic tidak menyediakan Confidence yang valid, confidence semantic dianggap 0.0. Pengecualian kompatibilitas: pola legacy V1 "Api menyentuh rumah kayu" menggunakan multiplier netral 1.0 karena pola lama tidak menyediakan confidence semantic yang dapat digunakan; ini mempertahankan skor V1 0.72.

## Intent dan fallback

- question: Reasoning mencari fakta yang sesuai atau mengembalikan unknown/conflicting.
- command: Generator memberi acknowledgement perintah.
- assertion: Tidak otomatis dianggap fakta verified.
- low_confidence dan unsupported: menghasilkan reasoning unknown dan jawaban yang menyatakan informasi belum cukup.

Pertanyaan "Apakah lonceng bisa menakuti naga?" dipetakan ke aturan naga-lonceng jika kedua premis Knowledge dan provenance tersedia.

## Register

Register formal, informal, dan slang diteruskan dari Semantic Engine atau metadata sesi. Jika nilai register tidak dikenal atau tidak tersedia, Language Generator menggunakan default formal. Register eksplisit dari pemanggil tetap memiliki prioritas tertinggi.

## Batas acknowledgement perintah

**Acknowledgement perintah bukan bukti bahwa aksi eksternal sudah dieksekusi.** Contoh "Baik, lonceng akan dibunyikan" hanya menyatakan bahwa ILIS mengenali dan merespons perintah. Bunyi lonceng, pemanggilan API, atau aksi di game memerlukan executor/integrasi eksternal yang terpisah dan konfirmasi keberhasilan dari executor tersebut.

## Verifikasi

Tes tests/test_e2e_chatbot.py menjalankan skenario melalui ILISCore.chatbot(), termasuk pertanyaan, perintah, naga-lonceng tiga register, konflik Knowledge, low-confidence, unsupported, dan kompatibilitas pola V1.
