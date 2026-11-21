# Panduan Persona pada Adapter ILIS V2.1

Persona adalah lapisan presentasi di luar ILIS Core. Adapter menjalankan alur
Semantic/Reasoning/Language Generator seperti biasa, lalu PersonaRenderer
menambahkan identity reply pada teks akhir. Payload Semantic, Reasoning,
metadata, dan teks mentah Language Generator tidak diubah.

## Chatbot: Mode A (default)

ChatbotAdapter otomatis memakai identitas ILIS jika `persona_config` tidak
diberikan:

```python
from ilis.interfaces import ILISCore
from ilis.interfaces.chatbot_adapter import ChatbotAdapter

core = ILISCore()
session_id = core.create_session()
chatbot = ChatbotAdapter(core)
result = chatbot.respond("Apakah api bisa membakar kayu?", session_id)
print(result["answer"])
```

## Game: Mode B (aplikasi) atau Mode C (NPC)

Game adapter tidak memaksakan identitas default karena setiap game/NPC memiliki
identitas sendiri. Berikan konfigurasi persona saat membuat adapter.

Mode B untuk identitas aplikasi/narator:

```python
from ilis.interfaces.game_adapter import GameEngineAdapter
from ilis.persona import ApplicationProfile, MODE_B, PersonaConfig

persona = PersonaConfig(
    mode=MODE_B,
    application=ApplicationProfile(
        application_id="fantasy-game",
        display_name="Penjaga Dunia",
        role="narator permainan",
        identity_reply="Saya Penjaga Dunia, narator permainan ini.",
    ),
)
game = GameEngineAdapter(core, persona_config=persona)
```

Mode C untuk NPC:

```python
from ilis.interfaces.game_adapter import GameEngineAdapter
from ilis.persona import CharacterProfile, MODE_C, PersonaConfig

npc_persona = PersonaConfig(
    mode=MODE_C,
    character=CharacterProfile(
        character_id="cave-guardian",
        display_name="Penjaga Gua",
        role="penjaga gua",
        identity_reply="Aku Penjaga Gua, pelindung tempat ini.",
    ),
)
game = GameEngineAdapter(core, persona_config=npc_persona)
```

Secara default, Mode C menolak penyebutan ILIS pada identitas maupun teks
jawaban NPC. Gunakan `allow_ilis_reference=True` hanya jika ILIS memang bagian
eksplisit dari lore game. Jika GameEngineAdapter dibuat tanpa `persona_config`,
hasil dialog tetap sama seperti versi sebelumnya.

## Batas arsitektur

- PersonaRenderer hanya dipanggil oleh adapter, bukan ILIS Core.
- Chatbot default menggunakan Mode A; Game menerima Mode B/C dari aplikasi.
- Identity reply ditambahkan sebelum teks mentah; teks mentah tidak ditulis ulang.
- Register sopan/santai tetap diproses Language Generator sebelum rendering persona.
- Semantic 12 field, Reasoning 6 key, SQLite, dan kontrak mesin inti tidak berubah.
