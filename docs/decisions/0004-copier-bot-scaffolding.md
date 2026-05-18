# ADR-0004: Einführung von Copier als offizielles Bot-Scaffolding-Tool

**Status:** Akzeptiert  
**Datum:** 2026-05-16  
**Entscheidungsträger:** Merle RPA-Hybrid-Architekt + Engineering-Team

---

## Kontext

Bis Phase 0 wurde ein neuer Python-Bot ausschließlich durch manuelles `cp -r python_bots/template/ python_bots/<name>/` erzeugt (siehe ADR-0002).

Dies führt zu mehreren Problemen:

- Vergessene oder falsch angepasste Dateien (`pyproject.toml`, `.env.example`, Dockerfile)
- Keine einfache Möglichkeit, optionale Features (Playwright, pandas, UiPath-Orchestrator) sauber einzuschalten
- Hoher manueller Aufwand und Inkonsistenz
- Der `rpa-bot-generator` Skill muss viele manuelle Schritte dokumentieren

Ziel von Phase 1 ist eine **exzellente Developer Experience**, bei der ein vollständig konformer Bot in unter 90 Sekunden entsteht.

## Entscheidung

Wir führen **Copier** als offizielles Scaffolding-Tool ein.

- Das kanonische Template lebt ab sofort unter `templates/bot/`
- Copier übernimmt:
  - Interaktive / parametrisierte Generierung
  - Bedingte Abhängigkeiten (Feature-Flags)
  - Post-Generation-Hooks (automatisches `uv sync`, Linting, pre-commit)
  - Langfristig auch Updates bestehender Bots (`copier update`)
- Zusätzlich wird eine kleine **Typer-CLI** (`merle new-bot`) als Komfortschicht bereitgestellt.

Der bisherige manuelle Copy-Prozess wird als **deprecated** markiert.

## Rationale

- **Copier** ist 2026 der moderne Standard (besser als Cookiecutter): Unterstützt Updates, Konflikt-Handling, starke Validierung und Python-Hooks.
- Feature-Flags erlauben schlanke Bots (kein Playwright in reinen API-Bots).
- Post-Hooks garantieren, dass jeder generierte Bot sofort `uv run ruff check . && pytest` besteht.
- Die Kombination aus Copier + `merle` CLI bietet sowohl Power-User als auch normale Entwickler eine hervorragende Experience.
- Passt perfekt zur bestehenden uv + Workspace-Strategie (Phase 0).

## Konsequenzen

### Positiv

- Drastisch reduzierte Einstiegshürde
- Garantierte Governance-Konformität ab Sekunde 1
- Feature-Flags verhindern unnötig schwere Bots
- Vorbereitung auf zukünftige Template-Updates ohne manuelles Mergen

### Negativ / Risiken

- Neue Abhängigkeit: `copier` (und optional `typer`)
- Jinja-Templating muss gepflegt werden
- Bestehende Bots müssen manuell migriert werden (Phase 2)

### Migration

- ADR-0002 wird auf "Superseded" gesetzt
- `python_bots/template/` bleibt für 4–6 Wochen als Fallback bestehen (mit deutlichem Deprecation-Hinweis)
- Danach wird es entfernt oder als reiner Snapshot markiert
- Der `rpa-bot-generator` Skill im OpenCode-Bereich wird auf die neue `merle` CLI / Copier umgestellt

## Umsetzung

Siehe Phase-1-Plan und `templates/bot/copier.yml`.

## Referenzen

- ADR-0002 (verbindliche Template-Architektur) – superseded
- `templates/bot/copier.yml`
- `tools/merle/` (CLI)
- `docs/concepts/governance.md` (wird aktualisiert)
