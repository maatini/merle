# Merle Knowledge Base — Navigation für Coding Agents

**Zweck:** Dieses Verzeichnis enthält eine LLM-optimierte Wissensbasis mit Fokus auf **Verantwortlichkeiten** (was gehört wem, was sind Invarianten) und **Abhängigkeiten** (wer ruft wen, welche externen Deps).

**Prinzip: Progressive Disclosure.** Starte hier (`index.md`), folge den Links je nach Fragestellung.

---

## Quick Start für Agenten

| Frage                                | Erster Anlaufpunkt                                                                                                                                    |
| ------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| Was ist Merle überhaupt?             | [`overview.md`](./overview.md)                                                                                                                        |
| Wie hängen die Komponenten zusammen? | [`architecture/components.md`](./architecture/components.md)                                                                                          |
| Wer ist von wem abhängig?            | [`architecture/dependencies.md`](./architecture/dependencies.md)                                                                                      |
| Welche globalen Patterns gibt es?    | [`cross-cutting/shared-patterns.md`](./cross-cutting/shared-patterns.md)                                                                              |
| Was bedeuten die @tags?              | [`cross-cutting/tags.md`](./cross-cutting/tags.md)                                                                                                    |
| Ich muss einen Bot schreiben         | [`modules/bot-template/`](./modules/bot-template/index.md) → [`modules/merle-core/`](./modules/merle-core/index.md)                                   |
| Ich muss merle-core ändern           | [`modules/merle-core/responsibility.md`](./modules/merle-core/responsibility.md) → [`modules/merle-core/gotchas.md`](./modules/merle-core/gotchas.md) |
| Ich muss die CLI erweitern           | [`modules/merle-cli/`](./modules/merle-cli/index.md)                                                                                                  |
| Ich muss die CI/CD anpassen          | [`modules/ci-cd/`](./modules/ci-cd/index.md)                                                                                                          |
| Ich suche ein Referenzbeispiel       | [`modules/examples/`](./modules/examples/index.md)                                                                                                    |
| Ich muss diese KB aktualisieren      | [`maintenance.md`](./maintenance.md)                                                                                                                  |

---

## Verzeichnisstruktur

- **[`overview.md`](./overview.md)** — Projektzweck, Architektur-Zusammenfassung, Tech-Stack, Governance-Prinzipien
- **[`architecture/`](./architecture/index.md)** — Globale Architektur
  - `components.md` — 7 logische Hauptkomponenten + C4-Diagramme
  - `dependencies.md` — Globaler Abhängigkeitsgraph + Mermaid
  - `data-flows.md` — Wichtige Datenflüsse als Sequenzdiagramme (Bot-Generierung, Ausführung, NATS)
  - `decisions.md` — Verweise auf ADRs in `docs/decisions/`
- **[`modules/`](./modules/merle-core/index.md)** — Pro Modul: responsibility, dependencies, interfaces, gotchas
  - `merle-core/` — Gemeinsame Bibliothek (@tag:basebot, @tag:basetask, @tag:retry, @tag:observability, etc.)
  - `merle-cli/` — CLI-Tool (`merle new-bot`, `merle validate`, etc.)
  - `bot-template/` — Copier-Template für neue Bots (@tag:copier-template)
  - `examples/` — Referenz-Bots und Integrationsmuster
  - `ci-cd/` — GitHub Actions Workflows und Quality Gates
- **[`cross-cutting/`](./cross-cutting/index.md)** — Modulübergreifende Konzepte
  - `tags.md` — @tag-Registry
  - `shared-patterns.md` — Wiederverwendbare Patterns
- **[`maintenance.md`](./maintenance.md)** — Wie und wann diese KB aktualisiert wird

---

## Konventionen

- **Deutsch** für Erklärungen, **Englisch** für Code-Begriffe
- **Mermaid** für alle Diagramme (versionierbar, kein externes Tool nötig)
- **@tag:konzept** für modulübergreifende Verweise
- **Relative Links** zu allen Dateien
- Jede responsibility.md beantwortet: _Was gehört mir? Was sind meine Invarianten? Was sind meine Entry Points?_
- Jede dependencies.md beantwortet: _Wer ruft mich? Wen rufe ich?_
