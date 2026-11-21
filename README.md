# ILIS — Indonesian Language Intelligence System

ILIS adalah sistem pemrosesan dan kecerdasan bahasa Indonesia yang dikembangkan **tanpa LLM sebagai inti**. ILIS dirancang sebagai sistem modular dan deterministik: pemahaman, representasi makna, pengetahuan, penalaran, memori, pembelajaran, dan generasi bahasa dibangun melalui komponen yang eksplisit serta dapat diuji.

Visi ILIS adalah menyediakan fondasi bahasa dan makna yang dapat digunakan untuk chatbot, NPC, dan berbagai genre game—bukan sekadar kumpulan template kalimat.

## Status

**✅ ILIS V1.0 Prototype tersedia**

- Rilis V1: [ILIS V1.0 Prototype](https://github.com/bronagerona/Sistem-Bahasa-universal/releases/tag/v1.0-prototype)
- Baseline rilis V1 berada di branch `main`.

**🧪 ILIS V2.2-beta — Beta Candidate**

- Rilis beta: [ILIS V2.2-beta](https://github.com/bronagerona/Sistem-Bahasa-universal/releases/tag/v2.2-beta)
- Branch pengembangan: `ilis-v2-development`.
- V2.2 menambahkan percakapan multi-turn dengan SessionManager in-memory, konteks percakapan terbatas, dan reset sesi.
- Riwayat percakapan belum persisten dan hilang ketika proses/aplikasi dimulai ulang.

**🧪 ILIS V3.1 — Beta Candidate / Pre-release (belum diterbitkan)**

- Catatan rilis: [ILIS V3.1 — Catatan Rilis](docs/v3.1_release_notes.md).
- Dokumentasi arsitektur: [V3 Concept Engine Architecture](docs/v3_concept_engine_architecture.md).
- Panduan developer: [V3 Concept Engine Developer Guide](docs/v3_concept_engine_developer_guide.md).
- V3 menambahkan Concept Engine sebagai fallback setelah lookup fakta persis pada KnowledgeEngine lama.
- V3.1 memperbaiki penanganan assertion agar pernyataan literal tidak berubah menjadi inferensi faktual yang tidak didukung, serta membatasi awalan identitas Mode A hanya untuk Identity Intent.
- Validasi pasca-merge: regresi lengkap **313 passed + 1 xfailed**; enam skenario smoke test eksplisit **6/6 passed**. [Lihat hasil GitHub Actions](https://github.com/bronagerona/Sistem-Bahasa-universal/actions/runs/44447366943).
- Satu XFAIL adalah tes beta lama `tests/beta_suite.py::test_beta_chatbot_full_pipeline_and_register`, yang masih mengharapkan inferensi kebakaran dari pernyataan “Api menyentuh rumah kayu”. Tes tetap dijalankan; perilaku baru yang disengaja adalah mengakui pernyataan tanpa menyimpulkan kebakaran.
- **V3.1 masih berstatus Beta Candidate / pre-release; belum diterbitkan sebagai tag atau GitHub Release.** Hasil tes yang lulus tidak menjamin bebas bug atau kesiapan produksi.
- Sebagian besar seed ConceptStore produksi masih berstatus PARTIAL. Data KNOWN terverifikasi penuh saat ini hanya tersedia pada fixture pengujian terisolasi, bukan seed produksi.
- Multi-turn tetap menggunakan penyimpanan in-memory; riwayat percakapan hilang saat aplikasi atau proses dimulai ulang.

## Cakupan bahasa

ILIS menargetkan variasi bahasa Indonesia formal, santai, gaul/slang, singkatan, bentuk tidak baku, dan variasi ejaan/typo. Dukungan setiap variasi bergantung pada pola dan leksikon yang tersedia; bahasa daerah dan code-mixing lintas bahasa belum dijamin.

## Modul utama

1. **Language Foundation** — tokenizer dan ILVE sebagai fondasi pemrosesan bahasa.
2. **Semantic Engine** — representasi semantik eksplisit dengan kontrak teruji.
3. **Concept & Knowledge Engine** — konsep, relasi, fakta, dan provenance.
4. **Reasoning Engine** — penalaran deterministik berbasis aturan dan bukti.
5. **Context & Memory Engine** — konteks percakapan dan memori episodik.
6. **Learning Engine** — mekanisme pembelajaran dalam batas desain implementasi.
7. **Language Generator** — konstruksi keluaran bahasa berdasarkan makna dan reasoning.
8. **Interface** — Chatbot Adapter dan Game Adapter.
9. **Storage V2** — opsi persistensi SQLite untuk fakta, provenance, sesi, dan memori episodik.

## Prinsip desain

- **Meaning-first:** memisahkan bentuk permukaan kalimat dari representasi makna.
- **Dynamic construction:** membangun keluaran dari struktur dan aturan, bukan hanya mengambil template.
- **Modular:** setiap subsistem memiliki tanggung jawab dan batas yang jelas.
- **Deterministik dan dapat diuji:** perilaku inti dapat ditelusuri serta diuji.
- **Evidence-aware:** membedakan fakta, dugaan, sumber, dan tingkat keyakinan.
- **No LLM as the core:** LLM bukan mesin utama ILIS.

## Batasan

ILIS masih dalam tahap pengembangan beta. Semantik, penalaran, generator, dan adapter dibatasi implementasi pola, kosakata, fakta, dan aturan yang tersedia. Sistem tidak menjamin kebenaran fakta dunia, tidak melakukan pembelajaran bebas seperti manusia, dan belum menyediakan pemahaman bahasa umum setara LLM. Hasil pengujian otomatis menunjukkan skenario yang diuji lulus, bukan jaminan bebas bug atau kesiapan produksi.

## Pengujian dan pengembangan

Instalasi dan tes:

```bash
python -m pip install -e ".[dev]"
python -m pytest
```

Untuk rincian arsitektur, kontrak, benchmark, dan kontribusi, lihat dokumentasi di direktori `docs/` serta [Panduan kontribusi](CONTRIBUTING.md).
