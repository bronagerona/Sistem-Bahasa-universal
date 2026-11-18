# ILIS — Indonesian Language Intelligence System

ILIS adalah proyek eksperimental untuk membangun sistem pemrosesan dan kecerdasan bahasa Indonesia **tanpa menjadikan LLM sebagai inti**. Machine learning boleh digunakan sebagai komponen pendukung, sementara representasi makna, pengetahuan, penalaran, memori, pembelajaran, dan generasi bahasa dikembangkan sebagai modul yang dapat diuji.

## Visi

Membangun satu fondasi bahasa dan makna yang dapat digunakan oleh chatbot, NPC, dan berbagai genre game.

## Cakupan ILIS V1

V1 berfokus pada bahasa Indonesia:
- formal dan baku;
- santai dan percakapan sehari-hari;
- gaul/slang;
- singkatan;
- bentuk tidak baku;
- variasi ejaan dan typo.

Bahasa daerah dan code-mixing lintas bahasa berada di luar cakupan V1.

## Prinsip desain

1. **Meaning-first:** pisahkan bentuk permukaan kalimat dari representasi maknanya.
2. **Dynamic construction:** bangun pemahaman dan keluaran dari struktur, bukan hanya mengambil kalimat template.
3. **Modular:** pemrosesan bahasa, semantik, pengetahuan, penalaran, pembelajaran, dan generasi memiliki batas yang jelas.
4. **Evidence-aware:** bedakan fakta, dugaan, sumber, dan tingkat keyakinan.
5. **Testable:** setiap kemampuan harus punya contoh, pengujian, dan batasan yang terdokumentasi.
6. **No LLM as the core:** model bahasa besar bukan mesin utama ILIS. ML klasik/statistik dapat dieksplorasi sebagai komponen pendukung.

## Status

**Tahap: fondasi proyek / prototipe awal.** Implementasi pertama sengaja kecil dan transparan. Ia belum merupakan sistem kecerdasan setara LLM, belum memiliki pemahaman bahasa umum, dan belum belajar mandiri dari pengalaman. Kemampuan tersebut adalah sasaran riset bertahap, bukan klaim kemampuan saat ini.

## Struktur awal

```text
src/ilis/
  language/       # tokenisasi dan variasi bahasa
  semantics/      # representasi makna (tahap berikutnya)
  cognition/      # penalaran dan konteks (tahap berikutnya)
  learning/       # pembelajaran (tahap berikutnya)
  generation/     # generasi bahasa (tahap berikutnya)
tests/            # pengujian otomatis
docs/             # desain dan keputusan arsitektur
```

## Menjalankan prototipe

Membutuhkan Python 3.10+.

```bash
python -m pip install -e .
ilis "Gue nggak mau cabut, bro!"
```

Atau tanpa instalasi:

```bash
PYTHONPATH=src python -m ilis "Gue nggak mau cabut, bro!"
```

## Pengembangan

Install dependensi pengembangan dan jalankan tes:

```bash
python -m pip install -e ".[dev]"
python -m pytest
```

Lihat [docs/architecture.md](docs/architecture.md) dan [CONTRIBUTING.md](CONTRIBUTING.md).
