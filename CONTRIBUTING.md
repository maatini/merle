# Contributing to Merle

Vielen Dank, dass du zum Merle Framework beitragen möchtest!

## Grundprinzipien

- **Python-First** — Neue Funktionen werden primär in Python umgesetzt.
- **Template & Core zuerst** — Änderungen am `templates/bot/` und `merle-core` haben höchste Priorität.
- **Kleine, reviewbare PRs** — Große Refactorings bitte vorher als Issue oder ADR diskutieren.
- **Tests & Docs** — Jede neue Funktion braucht Tests und Dokumentation.

## Entwicklungsumgebung

```bash
git clone <repo>
cd merle
uv sync --group dev --all-packages
```

Wichtige Befehle:

```bash
# Neuen Bot zum Testen erzeugen
merle new-bot test_bot --playwright

# Docs lokal starten (MkDocs Material)
uv run mkdocs serve
```

## Pull Request Prozess

1. Branch von `develop` oder `main` erstellen
2. Feature implementieren + Tests schreiben
3. `uv run ruff check --fix . && uv run ruff format .`
4. `uv run pytest`
5. PR erstellen mit guter Beschreibung + Screenshots (falls UI-relevant)

## Commit Messages

Verwende Conventional Commits:

- `feat(core): add BaseTask self-healing hooks`
- `fix(playwright): improve failure artifact naming`
- `docs(architecture): add C4 diagrams`
- `chore(template): update to merle-core 0.2`

## Code of Conduct

Wir behandeln uns respektvoll. Keine tolerierbaren Verhaltensweisen.

---

Bei Fragen: Öffne gerne ein Issue oder schreibe im internen `#rpa-engineering` Channel.
