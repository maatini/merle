# Entwicklungsumgebung einrichten

**Die offizielle und standardmäßige Entwicklungsumgebung für Merle ist Devbox + direnv.**

Ausführliche Anleitung: → **[docs/development/devbox.md](devbox.md)**

Sie liefert exakt die gleichen Tool-Versionen wie in der CI (Python 3.11, uv 0.11.8, Node 20, Copier, pre-commit) — reproduzierbar auf macOS, Linux und WSL.

## 1. Voraussetzungen (einmalig)

- [Devbox](https://www.jetify.com/devbox) installieren
- [direnv](https://direnv.net) installieren (für automatische Aktivierung beim `cd`)

```bash
# macOS (Homebrew)
brew install devbox direnv

# Danach direnv in die Shell integrieren (zsh/bash/fish — siehe direnv Docs)
```

## 2. Projekt klonen + Devbox aktivieren (Standard)

```bash
git clone https://github.com/maatini/merle.git
cd merle

# Einmalig direnv erlauben → ab jetzt wird Devbox beim Betreten des Verzeichnisses automatisch geladen
direnv allow .

# (Falls du kein direnv nutzt:)
devbox shell
```

Innerhalb der Devbox-Umgebung stehen `python`, `uv`, `pre-commit`, `node`, `copier` und `merle` sofort zur Verfügung (isolierte Versionen).

## 3. Einrichtung der Python-Umgebung

```bash
# Komplette Einrichtung (empfohlen)
devbox run setup
# oder manuell:
uv sync --group dev --all-packages
uv run pre-commit install --install-hooks
```

## 4. Wichtige Befehle (innerhalb Devbox)

```bash
# Neuen Bot erzeugen
devbox run new-bot rechnungsverarbeitung --playwright --pandas
# oder direkt: uv run merle new-bot ...

# Tests
devbox run test
# oder: uv run pytest -q

# Linting + Format
devbox run lint

# Docs lokal
uv run mkdocs serve
```

## OpenCode (empfohlen für KI-gestützte Entwicklung)

```bash
opencode
```

Der **RPA-Hybrid-Architekt** ist automatisch aktiv und **verwendet standardmäßig die Devbox-Umgebung** (Skill `devbox-environment` wird geladen). Alle Shell-Befehle des Agenten laufen über `devbox run ...`.

---

**Nächster Schritt**: Lies den aktualisierten [Schnellstart](../getting-started/quickstart.md).
