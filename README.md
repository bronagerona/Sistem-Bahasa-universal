# ILIS — Indonesian Language Intelligence System

ILIS adalah sistem pemrosesan dan kecerdasan bahasa Indonesia yang dikembangkan **tanpa LLM sebagai inti**. ILIS dirancang sebagai sistem modular dan deterministik: pemahaman, representasi makna, pengetahuan, penalaran, memori, pembelajaran, dan generasi bahasa dibangun melalui komponen yang eksplisit serta dapat diuji.

Visi ILIS adalah menyediakan fondasi bahasa dan makna yang dapat digunakan untuk chatbot, NPC, dan berbagai genre game—bukan sekadar kumpulan template kalimat.

## Status

**✅ ILIS V1.0 Prototype tersedia**

- Rilis V1: [ILIS V1.0 Prototype](https://github.com/bronagerona/Sistem-Bahasa-universal/releases/tag/v1.0-prototype)
- Baseline rilis V1 berada di branch `main`.
- Branch `ilis-v2-development` memuat pengembangan V2 Alpha.

**🧪 ILIS V2.0-alpha — tahap benchmark dan evaluasi**

V2 memperluas pemrosesan pertanyaan dan perintah sederhana, penalaran berbasis bukti untuk skenario api–kayu–rumah dan naga–lonceng, variasi keluaran generator, serta persistensi SQLite opsional. Mode in-memory tetap menjadi default.

V2 masih alpha: cakupan bahasa dan aturan terbatas, confidence score belum terkalibrasi sebagai probabilitas, dan sistem belum setara LLM atau mengklaim pemahaman bahasa universal. Status rilis final alpha mengikuti hasil GitHub Actions pada branch pengembangan.

Dokumen evaluasi: [Laporan Evaluasi V2 Alpha](docs/v2_alpha_evaluation_report.md).  
Rencana berikutnya: [Roadmap V3](docs/v3_roadmap.md).

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

ILIS masih prototype/alpha. Semantik, penalaran, generator, dan adapter dibatasi implementasi pola, kosakata, fakta, dan aturan yang tersedia. Sistem tidak menjamin kebenaran fakta dunia, tidak melakukan pembelajaran bebas seperti manusia, dan belum menyediakan pemahaman bahasa umum setara LLM.

## Pengujian dan pengembangan

Instalasi dan tes:

```bash
python -m pip install -e ".[dev]"
python -m pytest
```

Untuk rincian arsitektur, kontrak, benchmark, dan kontribusi, lihat dokumentasi di direktori `docs/` serta [Panduan kontribusi](CONTRIBUTING.md).
