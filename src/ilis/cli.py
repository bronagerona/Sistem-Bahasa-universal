"""Command-line interface for the first ILIS prototype."""

from __future__ import annotations

import argparse
import json

from ilis.language.pipeline import inspect_text


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ilis", description="Inspect Indonesian text with the ILIS prototype.")
    parser.add_argument("text", help="Teks bahasa Indonesia yang ingin diperiksa.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    print(json.dumps(inspect_text(args.text), ensure_ascii=False, indent=2))
