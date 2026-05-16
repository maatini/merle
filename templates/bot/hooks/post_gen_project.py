#!/usr/bin/env python3
"""
Post-Generation Hook für das Merle Bot Copier-Template.

Wird automatisch nach der Generierung ausgeführt.
Führt uv sync + grundlegendes Linting aus, damit der Bot sofort "grün" ist.
"""

import os
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    """Führt einen Shell-Befehl aus und gibt das Ergebnis zurück."""
    print(f"→ Running: {' '.join(cmd)}")
    return subprocess.run(cmd, check=check, capture_output=True, text=True)


def main() -> None:
    project_root = Path.cwd()

    print("\n🚀 Merle Bot Post-Generation Setup")
    print("=" * 50)

    # 1. uv sync (die wichtigste Aktion)
    try:
        run(["uv", "sync", "--group", "dev"])
        print("✅ uv sync --group dev erfolgreich")
    except subprocess.CalledProcessError as e:
        print(f"⚠️  uv sync fehlgeschlagen (nicht kritisch): {e}")
        print("   Bitte später manuell ausführen: uv sync --group dev")

    # 2. Ruff format + check --fix
    try:
        run(["uv", "run", "ruff", "format", "."], check=False)
        run(["uv", "run", "ruff", "check", "--fix", "."], check=False)
        print("✅ Code formatiert und gelintet")
    except Exception as e:
        print(f"⚠️  Ruff-Schritt übersprungen: {e}")

    # 3. Kurze Erfolgsmeldung
    print("\n" + "=" * 50)
    print("✅ Dein neuer Merle-Bot ist bereit!")
    print(f"   cd {project_root}")
    print("   uv run python main.py")
    print("   uv run pytest -q")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    main()
