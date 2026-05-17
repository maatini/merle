# Devbox Development Environment (Standard für Merle)

## Purpose

Stellt die **kanonische, reproduzierbare Entwicklungsumgebung** für das gesamte Merle-Projekt bereit (Python 3.11, uv, pre-commit, Node.js 20, Copier, etc.) mithilfe von [Devbox](https://www.jetify.com/devbox) (Nix-basiert).

**Devbox + direnv ist die offizielle Standard-Entwicklungsumgebung.** Alle Teammitglieder und AI-Agenten (OpenCode, Claude, etc.) **müssen** diese Umgebung standardmäßig verwenden.

## When to Use (Immer!)

- Beim Start jeder lokalen Entwicklungssession (`cd` ins Projektverzeichnis)
- Vor jedem `uv sync`, `ruff`, `pytest`, `merle new-bot`, `pre-commit`, `copier`, `mkdocs` etc.
- Wenn der RPA-Hybrid-Architekt oder ein Sub-Agent Shell-Befehle ausführen soll
- Bei Onboarding neuer Entwickler oder bei CI-ähnlichen lokalen Reproduktionen
- Vor dem Ausführen von `devbox run <script>` (siehe `devbox.json`)

## Aktivierung (Standardmäßig)

### Empfohlener Weg: direnv (automatisch)

```bash
# Einmalig einrichten
brew install direnv devbox   # macOS / entsprechend für Linux/WSL
direnv allow .

# Danach reicht normales `cd` ins Verzeichnis:
cd /Volumes/SSD2TB/work/antigravity/merle
# → Devbox wird automatisch geladen (Python, uv, Node, Copier im PATH)
```

### Alternativer Weg

```bash
devbox shell          # Interaktive Shell mit kompletter Env
# oder
devbox run setup      # Einrichtungsskript (uv sync + pre-commit)
devbox run lint
devbox run test
devbox run new-bot rechnungsverarbeitung --playwright
```

## Verhalten für AI-Agenten (RPA-Hybrid-Architekt & Sub-Agents)

**Verbindliche Regel für alle Agenten:**

1. **Immer zuerst die Devbox-Umgebung prüfen/aktivieren**, bevor Shell-Befehle, `uv`, Python oder Tools ausgeführt werden.
2. Innerhalb von OpenCode / Claude Code etc. **Befehle mit `devbox run <cmd>`** ausführen, wenn keine interaktive `devbox shell` aktiv ist.
   - Beispiel: `devbox run uv sync --group dev --all-packages`
   - Beispiel: `devbox run merle new-bot ...`
   - Beispiel: `devbox run uv run ruff check .`
3. Niemals globale `python`, `uv`, `node` oder `pre-commit` aus dem Host verwenden — immer die Devbox-Versionen (vermeidet Versionskonflikte und "works on my machine").
4. Bei Fehlern wie "uv: command not found", "python version mismatch" oder fehlenden Playwright-System-Abhängigkeiten → sofort auf Devbox umstellen und User anleiten.
5. Die `devbox.json` + `.envrc` + `devbox.lock` sind **Teil der Projekt-Governance** (wie `pyproject.toml` und Template). Änderungen nur nach Review.

## Vorteile für Merle (warum Devbox Standard ist)

- **Reproduzierbar** auf macOS, Linux, WSL — exakt dieselben Tool-Versionen wie in CI (Python 3.11, uv 0.11.8, Node 20).
- **Isoliert** — kein Konflikt mit globalen Python/uv-Installationen oder anderen Projekten.
- **Schnell** — schneller als Docker-Dev-Container, aber mächtiger als reines `uv`.
- **Skripte in `devbox.json`** — `devbox run setup`, `lint`, `test`, `new-bot` als Single-Source-of-Truth.
- Passt perfekt zur **Linux-Container-Strategie** des Projekts und zur Nix-basierten OpenCode-Hybrid-Umgebung (`rpa-opencode-hybrid/nix/`).

## Integrierte Skripte (devbox.json → `devbox run <name>`)

- `setup` — Komplette Einrichtung (uv sync + pre-commit hooks)
- `lint` — Ruff Check + Format
- `test` — pytest -q
- `new-bot` — Kurzbefehl für `uv run merle new-bot`

## References & Files

- `devbox.json` — Pakete, Environment-Variablen, Init-Hooks, `shell.scripts`
- `.envrc` — direnv Integration (`use devbox`) für automatische Aktivierung
- `devbox.lock` — Gesperrte exakte Nix-Pakete (committen!)
- `docs/development/setup.md` — Offizielle Setup-Anleitung (Devbox zuerst)
- `CONTRIBUTING.md` — Entwickler-Workflow
- `uv.lock` + Workspace-Mitglieder (`python_bots/shared`, `tools/merle`)

## Onboarding-Hinweis

Neue Entwickler bekommen nach `git clone` + `direnv allow .` sofort eine funktionierende, versionssichere Umgebung — ohne stundenlanges "Python + uv richtig installieren".

---

**Merle Devbox ist nicht optional. Sie ist der Standard.**
