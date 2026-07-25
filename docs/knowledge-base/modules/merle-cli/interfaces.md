# Merle CLI — Interface

## Kommando-Signaturen

### `merle new-bot`

```
merle new-bot NAME [OPTIONS]
```

| Argument | Typ   | Pflicht | Beschreibung           |
| -------- | ----- | ------- | ---------------------- |
| `NAME`   | `str` | ✅      | Bot-Name in snake_case |

| Option                       | Typ           | Default         | Beschreibung                                   |
| ---------------------------- | ------------- | --------------- | ---------------------------------------------- |
| `--description` / `-d`       | `str \| None` | `None`          | Kurzbeschreibung für README                    |
| `--playwright` / `-p`        | `bool`        | `False`         | Playwright-Browser-Automatisierung             |
| `--browser-engine` / `-b`    | `str`         | `"chromium"`    | `"chromium"` oder `"lightpanda"`               |
| `--lightpanda`               | `bool`        | `False`         | Shortcut für `--browser-engine lightpanda`     |
| `--pandas`                   | `bool`        | `False`         | pandas + openpyxl für Excel                    |
| `--pdf`                      | `bool`        | `False`         | pdfplumber für PDF                             |
| `--uipath`                   | `bool`        | `False`         | UiPath Orchestrator Client                     |
| `--basebot` / `--no-basebot` | `bool`        | `True`          | BaseBot-Subklasse generieren                   |
| `--location`                 | `str`         | `"python_bots"` | `"python_bots"` (Monorepo) oder `"standalone"` |

**Exit-Codes:**

- `0` — Bot erfolgreich generiert
- `1` — Fehler (Template nicht gefunden, ungültiger browser_engine, Copier-Fehler)

---

### `merle validate`

```
merle validate [OPTIONS]
```

| Option        | Typ    | Default | Beschreibung                       |
| ------------- | ------ | ------- | ---------------------------------- |
| `--strict`    | `bool` | `False` | Non-zero Exit bei Fehlern          |
| `--core-only` | `bool` | `False` | Nur mypy-Type-Check auf merle-core |

**Exit-Codes:**

- `0` — Alle Checks bestanden (oder `--strict` nicht gesetzt)
- `1` — Fehler bei `--strict`

---

### `merle docs`

```
merle docs [OPTIONS]
```

| Option     | Typ    | Default | Beschreibung                                       |
| ---------- | ------ | ------- | -------------------------------------------------- |
| `--serve`  | `bool` | `True`  | MkDocs Dev-Server starten (exklusiv mit `--build`) |
| `--build`  | `bool` | `False` | Statische Site bauen (löscht `site/` vorher)       |
| `--port`   | `int`  | `8000`  | Port für `--serve`                                 |
| `--strict` | `bool` | `False` | `--strict` an MkDocs weitergeben                   |

---

### `merle info`

```
merle info
```

Keine Argumente. Zeigt Rich-Tabelle mit Framework-Status.

**Exit-Code:** immer `0`

---

### `merle version`

```
merle version
```

Keine Argumente. Gibt eine Zeile aus: `merle CLI vX.Y.Z | Merle Framework v0.4.0 (Professional Foundation)`

**Exit-Code:** immer `0`

---

## Umgebungsvariablen

Die CLI selbst liest **keine** Umgebungsvariablen. Alle Konfiguration erfolgt via CLI-Argumente oder ist hartcodiert (Repo-Pfade).

Die aufgerufenen Subprozesse (`uv`, `ruff`, `mypy`, `mkdocs`) nutzen die Umgebungsvariablen des aufrufenden Shells.

## Interne Helper

```python
def _get_repo_root() -> Path:
    """Repo-Root = 4 Ebenen über dieser Datei (tools/merle/merle/main.py)"""


def _get_template_path() -> Path:
    """_get_repo_root() / "templates" / "bot" """


def _run(cmd: list[str], cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess:
    """Führt Shell-Befehl aus, loggt dimmed, gibt CompletedProcess zurück"""


def _get_version() -> str:
    """Version via importlib.metadata, Fallback '0.2.0-dev'"""
```
