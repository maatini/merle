# Architekturentscheidungen (ADRs)

Alle ADRs liegen in `docs/decisions/`. Diese Seite verlinkt nur — **keine Duplizierung**.

| ADR                                                                             | Titel                      | Status         | Kernentscheidung                                                         |
| ------------------------------------------------------------------------------- | -------------------------- | -------------- | ------------------------------------------------------------------------ |
| [0001](./../../decisions/0001-python-first-strategie.md)                        | Python-First Strategie     | Accepted       | 80-90% Python, UiPath nur bei nachgewiesenem Vorteil                     |
| [0002](./../../decisions/0002-verbindliche-template-architektur.md)             | Template-Architektur       | Accepted       | Jeder Bot aus Template; loguru/tenacity/pydantic-settings standardisiert |
| [0003](./../../decisions/0003-integration-python-uipath.md)                     | Python↔UiPath Integration | Accepted       | Lose Kopplung via NATS, nicht synchrones Ping-Pong                       |
| [0004](./../../decisions/0004-copier-bot-scaffolding.md)                        | Copier Scaffolding         | Accepted       | Copier statt manuellem `cp -r`; Feature-Flags; `copier update`           |
| [0005](./../../decisions/0005-merle-core-v02-architecture.md)                   | merle-core v0.2            | Accepted       | Modulare Struktur; OTEL nativ; Regel 10 (merle-core-Pflicht)             |
| [0006](./../../decisions/0006-nats-orchestration-foundation.md)                 | NATS Orchestrierung        | Accepted       | NATS+JetStream als Kommunikations-Backbone (Phase 4)                     |
| [0007](./../../decisions/0007-lightpanda-als-optionale-browser-engine.md)       | Lightpanda Browser         | Accepted       | CDP-kompatible Zig-Engine; 10-16× weniger RAM; kein Screenshot/PDF       |
| [0008](./../../decisions/0008-repository-visibility-and-internal-governance.md) | Repository Visibility      | **Superseded** | Ursprünglich: private-only. Ersetzt durch 0009                           |
| [0009](./../../decisions/0009-repository-public-source-available.md)            | Public Source-Available    | Accepted       | Repository öffentlich; Proprietary License behält alle Rechte            |

## Wie neue ADRs entstehen

1. Technologieentscheidung fällen (mit Entscheidungsmatrix falls Python-vs-UiPath)
2. ADR im Template-Format in `docs/decisions/` anlegen (fortlaufende Nummer)
3. In `mkdocs.yml` unter `nav → Entscheidungen (ADRs)` eintragen
4. Diese Seite aktualisieren (Zeile in Tabelle ergänzen)
