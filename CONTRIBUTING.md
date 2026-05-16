# Contributing to Merle

Vielen Dank, dass du zum Merle Framework beitragen möchtest!

## Grundprinzipien

- **Python-First** — Neue Funktionen werden primär in Python umgesetzt.
- **Template & Core zuerst** — Änderungen am `templates/bot/` (Copier) und `merle-core` haben höchste Priorität.
- **Referenz-Beispiel beachten** — Schau dir `examples/invoice-processing/` an — das ist der aktuelle Gold-Standard für Merle-Bots.
- **Kleine, reviewbare PRs** — Große Refactorings bitte vorher als Issue oder ADR diskutieren.
- **Tests & Docs** — Jede neue Funktion braucht Tests und Dokumentation.

## Entwicklungsumgebung (verbindlich: Devbox + direnv)

**Devbox ist der Standard.** Sie stellt reproduzierbare Versionen von Python 3.11, uv, pre-commit, Node 20 und Copier bereit.

```bash
git clone <repo>
cd merle
direnv allow .          # oder: devbox shell
devbox run setup        # uv sync + pre-commit hooks
```

Wichtige Befehle (innerhalb Devbox):

```bash
devbox run new-bot test_bot --playwright     # Neuen Bot generieren
just lint                                    # Ruff + Format Check
just test                                    # Core + Reference Tests
just ci                                      # Full local CI (lint + test + pre-commit)
uv run mkdocs serve
```

Der `justfile` im Root ist der empfohlene Einstieg für alle gängigen Entwickler-Commands.

Siehe `docs/development/setup.md` und Skill `devbox-environment` für Details.

## Pull Request Prozess

1. Branch von `main` erstellen (Feature-Branches: `feature/...` oder `fix/...`)
2. Feature implementieren + Tests schreiben
3. Qualität sicherstellen:
   ```bash
   just lint
   just test
   # oder manuell:
   uv run ruff check --fix . && uv run ruff format .
   uv run pytest python_bots/shared -q
   ```
4. Bei Template-Änderungen: Einen Test-Bot mit `merle new-bot` oder Copier generieren und prüfen
5. PR mit guter Beschreibung + Referenz zu Issue/ADR erstellen

**Wichtige Regel:** Änderungen an `templates/bot/` oder `merle-core` haben höchste Priorität und müssen besonders sorgfältig getestet werden.

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
