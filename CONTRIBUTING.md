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
   uv run pytest packages/merle-core -q
   ```
4. Bei Template-Änderungen: Einen Test-Bot mit `merle new-bot` oder Copier generieren und prüfen
5. PR mit guter Beschreibung + Referenz zu Issue/ADR erstellen

**Wichtige Regel:** Änderungen an `templates/bot/` oder `merle-core` haben höchste Priorität und müssen besonders sorgfältig getestet werden.

## Commit Messages (Conventional Commits + Commitizen)

**Verpflichtend:** Conventional Commits (enforced by pre-commit hook + commitizen).

Beispiele:

- `feat(core): add self-healing retry hooks to BaseTask`
- `fix(template): correct playwright extra in generated pyproject.toml.jinja`
- `docs(adr): add ADR-0008 for repository visibility`
- `chore(ci): add Trivy + Bandit to matrix`
- `refactor(shared): move merle-core to packages/ (breaking change — major version)`

**Lokale DX:**

```bash
uv sync --group dev
uv run pre-commit install
# Interaktiv (empfohlen):
uv run cz commit
# Oder normal commit (Hook validiert Message):
git commit -m "feat(cli): add merle validate command"
```

Commitizen + pre-commit Hook sorgen für:

- Konsistente Messages
- Automatische SemVer-Bumps (`uv run cz bump`)
- Automatisches CHANGELOG-Update

Nach einem Version-Bump **immer** den Workspace-Lockfile synchronisieren und mit committen
(sonst schlägt CI bei `uv lock --check` fehl):

```bash
uv run cz bump
uv lock
git add uv.lock && git commit --amend --no-edit
# Tag nur force-moven, wenn er noch nicht gepusht wurde:
git tag -f "v$(uv run cz version -p)"
```

Siehe `pyproject.toml` → `[tool.commitizen]` und `.pre-commit-config.yaml`.

## Code of Conduct

Wir behandeln uns respektvoll. Keine tolerierbaren Verhaltensweisen.

---

Bei Fragen: Öffne gerne ein Issue oder schreibe im internen `#rpa-engineering` Channel.
