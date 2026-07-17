# Merle CLI — Gotchas & Pitfalls

## `_get_repo_root()` — Harte 4-Ebenen-Annahme

**Problem:** Die CLI berechnet das Repo-Root via `Path(__file__).resolve().parent.parent.parent.parent`. Diese Annahme gilt nur, solange die CLI-Datei in `tools/merle/merle/main.py` liegt.

```python
# tools/merle/merle/main.py (Zeile ~30)
def _get_repo_root():
    return Path(__file__).resolve().parent.parent.parent.parent
    # main.py → merle/ → merle/ → tools/ → repo-root
    #          ↑1        ↑2        ↑3        ↑4
```

**Konsequenz:** Jede Änderung an der Verzeichnisstruktur von `tools/merle/` **bricht die CLI**. Niemals die Tiefe der `main.py` im Dateibaum ändern, ohne `_get_repo_root()` anzupassen.

## Copier: `unsafe=True` ist nötig

**Problem:** `copier.run_copy(..., unsafe=True)` ist erforderlich, damit der Post-Generation-Hook (`hooks/post_gen_project.py`) ausgeführt wird. Ohne diesen Flag wird `uv sync` nicht ausgeführt und der generierte Bot hat nicht-installierte Dependencies.

```python
# Ohne unsafe=True:
copier.run_copy(template_path, target_dir, data=answers)
# → post_gen_project.py wird NICHT ausgeführt
# → Bot hat keine venv, kein ruff-Format, keine installierten Deps

# Mit unsafe=True:
copier.run_copy(template_path, target_dir, data=answers, unsafe=True)
# → post_gen_project.py wird ausgeführt
# → Bot ist sofort lauffähig
```

Das `unsafe` im Namen bezieht sich auf Copiers Sicherheitsmodell (Hooks können beliebigen Code ausführen). Im Merle-Kontext ist der Hook vertrauenswürdig (nur `uv sync` + `ruff`).

## Copier-Import-Fallback: CLI startet ohne Copier

**Problem:** Wenn `copier` nicht installiert ist (z.B. nur `uv sync` ohne `--group dev`), zeigt `merle new-bot` eine Fehlermeldung — aber `merle validate`, `merle docs`, `merle info`, `merle version` funktionieren weiterhin.

```python
try:
    from copier import run_copy
except ImportError:
    run_copy = None  # CLI lebt weiter, nur new-bot ist kaputt
```

Der Entwickler sieht erst beim Aufruf von `merle new-bot` eine Fehlermeldung mit der Anweisung `uv sync --group dev`.

## `merle validate` — Checks sind non-fatal ohne `--strict`

**Problem:** Ohne `--strict` gibt `merle validate` **immer** Exit-Code 0 zurück, selbst wenn Ruff/Mypy Fehler finden. Das ist bewusstes Verhalten für lokale Entwicklung, aber in CI muss `--strict` verwendet werden.

```bash
# Lokal: Zeigt Fehler, aber Exit 0
merle validate

# CI: Zeigt Fehler und Exit 1
merle validate --strict
```

Der CI-Workflow (`ci.yml`) nutzt `merle validate` derzeit **ohne** `--strict` und verlässt sich auf explizite `ruff`/`mypy`-Aufrufe. Das ist inkonsistent und sollte vereinheitlicht werden.

## `merle validate` — mypy nur auf merle-core

**Problem:** `merle validate --core-only` prüft nur `packages/merle-core/src/merle_core`. Generierte Bots werden **nicht** via mypy geprüft. Das ist Absicht (Bots sind zu divers für strict mypy), aber bedeutet dass Bot-Code typ-unsicher sein kann, ohne dass `merle validate` warnt.

## `merle docs --build` löscht `site/` ohne Rückfrage

**Problem:** `merle docs --build` führt `rm -rf site/` vor dem Build aus. Wenn dort Dateien liegen, die nicht von MkDocs generiert wurden, sind sie unwiderruflich weg.

Das ist Policy: `site/` soll niemals manuell bearbeitet oder committet werden. Trotzdem: Vorsicht bei benutzerdefinierten Dateien in `site/`.

## Kein async in der CLI

**Problem:** Die CLI ist komplett synchron (`subprocess.run`, keine `async def`). Das bedeutet:

- `merle new-bot` blockiert den Terminal für die gesamte Dauer von `uv sync` (kann 30+ Sekunden dauern)
- Kein Fortschrittsbalken — nur Typer-Statusmeldungen
- Kein paralleles Ausführen mehrerer Commands möglich

Das ist akzeptabel, da die CLI ein Entwickler-Tool ist und nicht unter hoher Last läuft.

## Version-Diskrepanz

**Problem:** `merle version` zeigt `merle CLI vX.Y.Z | Merle Framework v0.4.0`. Die CLI-Version kommt aus `importlib.metadata.version("merle-cli")`, die Framework-Version ist in `main.py` hartcodiert. Bei Version-Bumps muss beides aktualisiert werden.

Aktuell: `pyproject.toml` sagt `0.4.0`, `egg-info` sagt `0.3.0`. Inkonsistenz nach Upgrade.
