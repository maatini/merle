# Merle CLI — Kommandozeilen-Tool

**Paket:** `tools/merle/` | **Binary:** `merle` | **Version:** 0.4.0

Die Merle CLI ist das primäre Entwicklerwerkzeug. Sie wrappt @tag:copier-template, führt Qualitäts-Checks durch und dient als Einstiegspunkt für alle Entwickler-Interaktionen.

## Befehlsübersicht

| Befehl                         | Zweck                                       | Datei     |
| ------------------------------ | ------------------------------------------- | --------- |
| `merle new-bot <name> [opts]`  | @tag:copier-template — Neuen Bot generieren | `main.py` |
| `merle validate [--strict]`    | Governance + Code-Qualität prüfen           | `main.py` |
| `merle docs [--serve/--build]` | Dokumentation serven/bauen                  | `main.py` |
| `merle info`                   | Framework-Status anzeigen                   | `main.py` |
| `merle version`                | Version ausgeben                            | `main.py` |

## Dateien

| Datei                        | Zweck                                                                                      |
| ---------------------------- | ------------------------------------------------------------------------------------------ |
| `merle/main.py` (293 Zeilen) | **Die gesamte CLI-Implementierung.** Alle 5 Commands + 4 Helper-Funktionen in einer Datei. |
| `merle/__init__.py`          | Leer (Package-Marker)                                                                      |
| `pyproject.toml`             | Package-Metadaten + Dependencies + Entry Point                                             |

## Wichtige Links

- **[`responsibility.md`](./responsibility.md)** — Was jeder Befehl tut, Invarianten, Seiteneffekte
- **[`dependencies.md`](./dependencies.md)** — Coupling zu Copier, Template, Repo-Struktur
- **[`interfaces.md`](./interfaces.md)** — CLI-Signaturen, Exit-Codes, Env-Variablen
- **[`gotchas.md`](./gotchas.md)** — Repo-Root-Auflösung, `unsafe=True`, Copier-Import-Fallback
