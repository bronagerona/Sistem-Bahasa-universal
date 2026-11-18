# Contributing to ILIS

Terima kasih sudah tertarik mengembangkan ILIS.

## Prinsip kontribusi

- Jaga modul tetap kecil dan memiliki tanggung jawab jelas.
- Sertakan pengujian untuk setiap perilaku baru.
- Pertahankan teks asli pengguna saat menambahkan normalisasi.
- Dokumentasikan keterbatasan, asumsi, dan sumber data.
- Jangan menambahkan klaim pemahaman semantik jika implementasinya baru berupa
  pencocokan kata atau aturan sederhana.

## Menjalankan tes

Install pytest, lalu jalankan:

```bash
python -m pip install -e ".[dev]"
python -m pytest
```

Untuk saat ini, pytest merupakan dependensi pengembangan yang dipasang terpisah.
