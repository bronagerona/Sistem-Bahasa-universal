# Penanganan Pertanyaan Identitas di ChatbotAdapter

## Tujuan

Pertanyaan tentang identitas dan kemampuan chatbot ILIS ditangani pada lapisan integrasi `ChatbotAdapter`, bukan di Semantic Engine, Reasoning Engine, Language Generator, atau ILIS Core. Penanganan ini deterministik dan tidak menggunakan LLM.

## Deteksi intent

Adapter mencocokkan teks yang telah dinormalisasi (case-folding dan perapian spasi) dengan frasa berikut:

- `siapa kamu`
- `apa yang bisa kamu lakukan`
- `kemampuanmu`
- `jelaskan kemampuanmu`

Pencocokan tidak bergantung pada posisi frasa. Karena itu, pesan gabungan seperti `Halo siapa kamu? Jelaskan apa yang bisa kamu lakukan` dikenali sebagai pertanyaan identitas/kemampuan.

## Aturan berdasarkan persona

- **Mode A (`chatbot_ilis`)**: adapter mengembalikan jawaban identitas dan kemampuan ILIS yang statis. Teks kemampuan diteruskan melalui `PersonaRenderer` sehingga identitas Mode A tetap konsisten. Register jawaban ini formal.
- **Mode B (`application`)**: deteksi identitas ILIS tidak mengambil alih. Pesan diteruskan ke alur ILIS Core normal dan identitas aplikasi tetap dikelola oleh persona yang dikonfigurasi.
- **Mode C (`character`)**: sama seperti Mode B; alur Core normal tetap berjalan dan identitas NPC tidak diganti menjadi identitas ILIS.

## Batas arsitektur

Rute khusus Mode A tidak menjalankan Semantic, Reasoning, atau Language Generator karena jawaban sudah ditentukan oleh adapter. Pada hasil rute ini, `semantic_result`, `reasoning_result`, dan `generation` bernilai `None`; metadata menandai `response_type: identity_intent`. Session tetap divalidasi agar perilaku untuk ID sesi yang tidak dikenal tidak berubah.

Implementasi ini tidak mengubah:

- kontrak Semantic (12 field);
- kontrak Reasoning (6 key) maupun logika inti Semantic/Reasoning;
- PersonaRenderer dan profil persona;
- SQLite atau skema penyimpanannya;
- `GameEngineAdapter`.

## Pengujian

`tests/test_identity_intent.py` mencakup empat frasa deteksi, skenario pesan gabungan Run #15, serta verifikasi bahwa Mode B dan Mode C tetap menggunakan alur Core normal.
