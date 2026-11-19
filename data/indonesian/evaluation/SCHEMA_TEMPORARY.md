# SCHEMA TEMPORARY — Pilar E (Evaluasi Dataset)

> Status: **SCHEMA TEMPORARY**
> Versi: 0.1
> Cakupan: catatan skema sementara untuk sampel evaluasi dataset pengayaan bahasa Indonesia ILIS.
> Batas: bukan spesifikasi tes otomatis ILIS dan bukan izin mengubah kode, test suite, CI/workflow, SQLite, atau baseline V3.1-Beta.

## Field record evaluasi

Setiap record pada `sample.jsonl` menggunakan field berikut:

- `evaluation_id`: ID unik kasus evaluasi.
- `test_group`: kelompok yang diuji, misalnya `lexicon`, `sentence_patterns`, `multi_turn`, `knowledge`, atau `regression`.
- `target_ref`: ID record dataset atau perilaku baseline yang menjadi sasaran.
- `input`: masukan/kasus yang dievaluasi.
- `expected_behavior`: perilaku atau hasil yang diharapkan.
- `metric_name`: nama metrik yang diamati.
- `split`: pemisahan sementara `development`, `validation`, atau `final_test`.
- `leakage_risk_note`: catatan risiko kebocoran data dan pencegahannya.
- `source`: asal kasus dan hubungan dengan data sampel.
- `verification_status`: status peninjauan record.

## Catatan penggunaan

1. Nama field dan pembagian split ini bersifat sementara untuk menguji keterbacaan serta kelengkapan skema.
2. Record pada split berbeda tidak boleh berupa salinan atau parafrasa dekat yang menyebabkan kebocoran.
3. Kasus `final_test` tidak boleh digunakan untuk tuning atau penyusunan contoh pengembangan.
4. Kasus regresi baseline pada sampel ini bersifat dokumentasi konseptual; tidak dijalankan sebagai tes dan tidak mengubah test suite.
5. Skema final baru ditetapkan setelah review evaluator dan persetujuan Pemilik Proyek.
6. Tidak ada hubungan langsung ke runner tes, kode ILIS, database SQLite, atau workflow CI pada tahap ini.
