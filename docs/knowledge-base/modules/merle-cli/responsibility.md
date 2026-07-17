# Merle CLI — Verantwortlichkeiten

**Source:** `tools/merle/merle/main.py` (293 Zeilen, alle Commands + Helpers in einer Datei)  
**Framework:** Typer (`typer.Typer` app) + Rich (Tabellen, Panels, Farben)

## Architektur

Die CLI ist eine Single-File-Typer-App. Es gibt **keine** Trennung in Subcommands, Plugins oder Module — bewusst einfach gehalten.

```python
app = typer.Typer(
    name="merle",
    help="Merle RPA Framework CLI — Python-first hybrid RPA toolchain",
)
```

---

## 1. `merle new-bot <NAME> [OPTIONS]` — Bot-Generierung

**Owns:** @tag:copier-template — den einzigen, offiziellen Weg, neue Bots zu erstellen.

| Aspekt            | Details                                                                                                                                                        |
| ----------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Eingabe**       | `name` (snake_case), optionale Feature-Flags                                                                                                                   |
| **Ausgabe**       | Generierter Bot unter `python_bots/<name>/` oder standalone                                                                                                    |
| **Seiteneffekte** | `uv sync`, `ruff format`, `ruff check --fix` via Post-Generation-Hook                                                                                          |
| **Invarianten**   | Template `templates/bot/` muss existieren. `browser_engine` muss `"chromium"` oder `"lightpanda"` sein. `unsafe=True` für Copier (sonst läuft der Hook nicht). |
| **Aufruf von**    | RPA-Entwickler (Mensch)                                                                                                                                        |

**Mapping CLI-Flags → Template-Variablen:**

| CLI-Flag                     | Template-Variable                 | Typ  |
| ---------------------------- | --------------------------------- | ---- |
| `name`                       | `bot_name`                        | str  |
| `--description` / `-d`       | `bot_description`                 | str  |
| `--playwright` / `-p`        | `include_playwright`              | bool |
| `--browser-engine` / `-b`    | `browser_engine`                  | str  |
| `--lightpanda`               | `browser_engine` = `"lightpanda"` | str  |
| `--pandas`                   | `include_pandas`                  | bool |
| `--pdf`                      | `include_pdf`                     | bool |
| `--uipath`                   | `include_uipath_orchestrator`     | bool |
| `--basebot` / `--no-basebot` | `use_base_bot_class`              | bool |
| `--location`                 | `location`                        | str  |

**Ablauf:**

1. `_get_template_path()` → `templates/bot/`
2. Validiere Template existiert
3. Validiere `browser_engine`
4. Baue `answers` dict
5. `copier.run_copy(template_path, target_dir, data=answers, overwrite=False, unsafe=True)`
6. Bei Copier-Fehler: zeige manuellen Fallback-Befehl

---

## 2. `merle validate [--strict] [--core-only]` — Qualitätsprüfung

**Owns:** Governance-Validierung. Zentraler Befehl für CI und Entwickler, um zu prüfen ob das Repository konform ist.

| Aspekt          | Details                                                                                                               |
| --------------- | --------------------------------------------------------------------------------------------------------------------- |
| **Eingabe**     | `--strict` (exit 1 bei Fehlern), `--core-only` (nur mypy auf merle-core)                                              |
| **Ausgabe**     | Rich-Tabelle mit Prüfergebnissen (✅/❌), optional non-zero Exit-Code                                                 |
| **Prüft**       | Ruff Lint + Format, mypy (strict), Template-Integrität (copier.yml + hook existieren), Visibility-Reminder (ADR-0009) |
| **Invarianten** | Läuft immer vom Repo-Root aus. `_run()` wrappt `subprocess.run` mit Logging.                                          |

**Prüfschritte im Detail:**

1. `ruff check .` — Lint-Fehler
2. `ruff format --check .` — Format-Abweichungen
3. `mypy packages/merle-core/src/merle_core` (mit `--strict` wird das volle strict-Flag übergeben)
4. Template-Integrität: `templates/bot/copier.yml` + `templates/bot/hooks/post_gen_project.py` vorhanden?
5. Visibility: Hinweis auf ADR-0009

---

## 3. `merle docs [--serve/--build] [--port] [--strict]` — Dokumentation

**Owns:** Dokumentations-Workflow. Wrappt MkDocs.

| Aspekt          | Details                                                                                            |
| --------------- | -------------------------------------------------------------------------------------------------- |
| **Eingabe**     | `--serve` (default, Port 8000), `--build` (statisch nach `site/`), `--strict` (MkDocs strict mode) |
| **Invarianten** | `--build` löscht `site/` vorher komplett (Policy: `site/` nie committen).                          |
| **Aufruf von**  | Entwickler, CI (docs.yml)                                                                          |

---

## 4. `merle info` — Framework-Status

**Owns:** Informationsanzeige. Single Source of Truth für Versionen und Pfade im CLI-Kontext.

**Zeigt an:**

- CLI-Version (via `importlib.metadata.version("merle-cli")`)
- Status + Pfade: merle-core, Template, CLI, Docs, ADRs, Examples, Governance
- Philosophy-Panel: "Python-First • Template-First • Governance"

---

## 5. `merle version` — Version

**Owns:** Versionsstring. Einfachste Ausgabe.

Zeigt: `merle CLI v<version> | Merle Framework v0.4.0 (Professional Foundation)`

---

## Interne Helper (privat, in `main.py`)

| Funktion                | Zweck                                                                | Annahmen                                          |
| ----------------------- | -------------------------------------------------------------------- | ------------------------------------------------- |
| `_get_repo_root()`      | Repo-Root via `Path(__file__).resolve().parent.parent.parent.parent` | CLI liegt in `tools/merle/merle/` → 4 Ebenen hoch |
| `_get_template_path()`  | `_get_repo_root() / "templates" / "bot"`                             | Template liegt immer im Repo-Root                 |
| `_run(cmd, cwd, check)` | `subprocess.run` Wrapper mit Rich-dimmed Logging                     | Shell-Commands, kein async                        |
| `_get_version()`        | `importlib.metadata.version("merle-cli")` mit Fallback `"0.2.0-dev"` | Package muss installiert sein                     |

---

## Was die CLI **nicht** besitzt

- **Keine** Bot-Ausführung (das machen die generierten Bots selbst)
- **Keine** Template-Dateien (die liegen in `templates/bot/`)
- **Keine** merle-core-Logik (die CLI importiert merle-core **nicht**)
- **Keine** Docker-Builds (das macht `just docker-bot <bot>`)
- **Keine** NATS-Verwaltung (Placeholder `merle nats-up` existiert nicht)

## Design-Entscheidungen

1. **Single-File-CLI**: Bewusst einfach. Keine Subcommand-Module, keine Plugin-Architektur. Bei >500 Zeilen aufteilen.
2. **Kein merle-core-Import**: Die CLI ist unabhängig von merle-core. Sie ruft Copier auf, das den Code generiert, der dann merle-core importiert — aber sie selbst nicht.
3. **`unsafe=True`**: Ohne diesen Copier-Flag läuft `post_gen_project.py` nicht. Security-Risiko minimal, da der Hook nur `uv sync` + `ruff` ausführt und die CLI nur von vertrauenswürdigen Entwicklern aufgerufen wird.
