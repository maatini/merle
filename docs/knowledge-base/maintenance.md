# Maintenance — KB aktuell halten

## Wann aktualisieren?

| Ereignis                           | Was tun?                                                                                                                                                                                                  |
| ---------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Neue ADR**                       | `architecture/decisions.md` → Zeile in Tabelle ergänzen. Falls relevant: `@tag` in `cross-cutting/tags.md` hinzufügen.                                                                                    |
| **Neues merle-core-Modul**         | `modules/merle-core/index.md` → Dateitabelle ergänzen. Neues File in `modules/merle-core/responsibility.md` (neue Sektion). `interfaces.md` ergänzen. `dependencies.md` → Outbound-Tabelle aktualisieren. |
| **Neuer CLI-Befehl**               | `modules/merle-cli/responsibility.md` → Neue Befehl-Sektion. `interfaces.md` → Signatur-Tabelle.                                                                                                          |
| **Template-Änderung**              | `modules/bot-template/responsibility.md` → Betroffene Jinja-Datei aktualisieren. Falls neue Feature-Flags: `interfaces.md` → Variablen-Tabelle.                                                           |
| **Neues Example**                  | `modules/examples/index.md` → Zeile in Tabelle. `responsibility.md` → Neue Sektion.                                                                                                                       |
| **CI/CD-Änderung**                 | `modules/ci-cd/responsibility.md` → Workflow-Sektion aktualisieren. `dependencies.md` → Trigger/Jobs/Actions aktualisieren.                                                                               |
| **Neues Shared Pattern**           | `cross-cutting/shared-patterns.md` → Neue Sektion.                                                                                                                                                        |
| **Neues Cross-Cutting-Konzept**    | `cross-cutting/tags.md` → Neue Zeile in @Tag-Tabelle.                                                                                                                                                     |
| **Neue Hauptkomponente**           | `architecture/components.md` → Neue Sektion + C4-Diagramm aktualisieren.                                                                                                                                  |
| **Abhängigkeitsänderung (extern)** | `architecture/dependencies.md` → Tabelle(n) aktualisieren.                                                                                                                                                |
| **Gotcha entdeckt**                | `gotchas.md` des betroffenen Moduls → Neue Sektion.                                                                                                                                                       |
| **Breaking Change**                | Alle betroffenen `responsibility.md` + `interfaces.md` + `gotchas.md` aktualisieren. `architecture/decisions.md` → ggf. neue ADR verlinken.                                                               |

## Konventionen

1. **Mermaid vor ASCII**: Alle Diagramme als Mermaid — sie sind versionierbar, werden von GitHub/MkDocs gerendert und sind lesbar im Diff.
2. **Tabellen vor Prosa**: Strukturierte Daten (Dependencies, Interfaces, Flags) immer in Tabellen. Fließtext nur für Kontext.
3. **@tags konsequent nutzen**: Jedes modulübergreifende Konzept bekommt einen Tag. Neue Tags in `cross-cutting/tags.md` registrieren.
4. **Relative Links**: Alle Links zu anderen KB-Dateien sind relativ (`./overview.md`, `../architecture/dependencies.md`). Links zu externen Docs: `../../decisions/0001-python-first-strategie.md`.
5. **Keine Duplizierung**: ADRs, Governance-Regeln, Strategie-Docs liegen in `docs/` und werden **verlinkt**, nicht kopiert. Die KB ist eine ergänzende Sicht für Agenten, kein Ersatz für die vollständige Doku.
6. **Ground Truth = Source Code**: Wenn KB und Source divergieren, gewinnt der Source Code. KB dann aktualisieren.

## Datei-Längenlimits (Richtwerte)

| Datei               | Max. Zeilen | Bei Überschreitung                              |
| ------------------- | ----------- | ----------------------------------------------- |
| `index.md`          | 60          | In Sub-Indexes aufteilen                        |
| `responsibility.md` | 300         | Modul weiter in Submodule zerlegen              |
| `dependencies.md`   | 150         | Komplexe Graphen in Mermaid, Tabellen straffen  |
| `interfaces.md`     | 200         | Nur Public API, keine Interna                   |
| `gotchas.md`        | 150         | Nur häufig getroffene Fallstricke, keine Trivia |

## Nicht tun

- ❌ Prosa-Wände schreiben (Agenten scannen, sie lesen nicht)
- ❌ ADRs duplizieren (verlinken!)
- ❌ Source-Code in die KB kopieren (wird stale)
- ❌ Speculative Informationen (nur was im Code existiert)
- ❌ Veraltete Informationen lassen (lieber löschen als "deprecated"-Markierungen)
