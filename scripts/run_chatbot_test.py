"""Run one deterministic ILIS V2 chatbot message in GitHub Actions.

The message is supplied through ILIS_TEST_MESSAGE so workflow inputs are never
interpolated into a shell command.
"""
from __future__ import annotations

import html
import json
import os
import sys

from ilis.interfaces import ILISCore


def main() -> int:
    message = os.environ.get("ILIS_TEST_MESSAGE", "")
    if not message.strip():
        print("ERROR: ILIS_TEST_MESSAGE must not be empty.", file=sys.stderr)
        return 2

    core = ILISCore()
    session_id = core.create_session(metadata={"source": "github_actions_playground"})
    try:
        result = core.chatbot().respond(message, session_id)
        answer = result["answer"]
        metadata = result["metadata"]
        print("INPUT:")
        print(message)
        print("\nILIS ANSWER:")
        print(answer)
        print("\nMETADATA:")
        print(json.dumps(metadata, ensure_ascii=False, indent=2))

        summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
        if summary_path:
            summary = (
                "<h2>Hasil uji chatbot ILIS V2</h2>"
                f"<h3>Pesan kamu</h3><pre>{html.escape(message)}</pre>"
                f"<h3>Jawaban ILIS</h3><pre>{html.escape(str(answer))}</pre>"
                f"<h3>Informasi hasil</h3><pre>{html.escape(json.dumps(metadata, ensure_ascii=False, indent=2))}</pre>"
                "<p>Catatan: ILIS berjalan secara deterministik tanpa LLM. "
                "Hasil ini adalah keluaran prototipe V2 pada branch pengembangan.</p>"
            )
            with open(summary_path, "a", encoding="utf-8") as summary_file:
                summary_file.write(summary + "\n")
        return 0
    finally:
        core.close()


if __name__ == "__main__":
    raise SystemExit(main())
