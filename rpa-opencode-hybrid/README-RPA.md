# Merle OpenCode Hybrid (Advanced / Fork Development)

> **Für die tägliche RPA-Arbeit nicht verwenden!**  
> Die empfohlene Integration ist die leichte `.opencode/`-Konfiguration direkt im Merle-Root (`../.opencode/`).  
> Einfach `opencode` im Merle-Hauptverzeichnis starten — der RPA-Hybrid-Architekt ist dann automatisch aktiv.

Dieses Verzeichnis enthält einen **vollständigen Fork** von [OpenCode](https://github.com/anomalyco/opencode). Es ist nur relevant, wenn du selbst am OpenCode-Core arbeiten oder einen angepassten Build erstellen möchtest.

Der Fork erweitert OpenCode um die Merle-spezifischen RPA-Erweiterungen (die jedoch mittlerweile primär im Root unter `.opencode/` gepflegt werden).

## Enthaltene Erweiterungen

### Primary Agent: `rpa-hybrid`
- Vollständiger System-Prompt mit Python-First-Strategie
- 10 Governance-Regeln tief integriert
- Entscheidungsmatrix für Python vs. UiPath
- Kennt alle Kit-Pfade und Ressourcen

### Skills
| Skill | Zweck |
|-------|-------|
| `rpa-process-analyzer` | Analysiert Prozesse und empfiehlt Python oder UiPath mit Begründung |
| `rpa-bot-generator` | Generiert neue Bots strikt nach Template und Qualitätsregeln |
| `governance-validator` | Validiert Code auf Einhaltung aller 10 Governance-Regeln |

### MCP-Tool: `rpa-context`
Lädt Kit-Dokumentation on-demand: Strategie, Entscheidungsmatrix, Governance, Template u.v.m.

### Commands
| Command | Beschreibung |
|---------|-------------|
| `/rpa-new-bot` | Neuen Bot aus Template erstellen |
| `/rpa-validate` | Governance-Validierung eines Bots |

### Permissions
Feingranulare Berechtigungen:
- `allow` für Bot-Code, Tests, Konfiguration
- `ask` für kritische Änderungen (config.py, Dockerfile)
- Shell-Zugriff auf Bot- und Docs-Verzeichnisse

## Verwendung (nur für Fork-Entwicklung)

```bash
cd rpa-opencode-hybrid
opencode ../          # Merle als Workspace mit diesem Fork öffnen
# oder
opencode .            # Direkt im Fork arbeiten (für OpenCode-Core-Änderungen)
```

**Empfohlener Weg für die tägliche Merle-Arbeit:**  
Im Merle-Root einfach `opencode` ausführen. Die RPA-Erweiterungen leben dort unter `.opencode/` als leichte, versionierte Projekt-Konfiguration und benötigen diesen Fork nicht mehr (siehe `../.opencode/` und `../README.md`).

## Struktur der Erweiterungen (im Fork)

Die RPA-Erweiterungen liegen auch hier noch unter `.opencode/`, dienen aber primär als Referenz oder für Tests gegen den Fork. Die **kanonische Version** befindet sich im Merle-Root unter `../.opencode/`.

```
.opencode/
├── agent/rpa-hybrid.md
├── skills/rpa-*/SKILL.md
├── tool/rpa-context.ts
├── command/rpa-*.md
└── opencode.jsonc
```

## Upstream & Strategie

Dieser Fork basiert auf [anomalyco/opencode](https://github.com/anomalyco/opencode).

**Wichtige Architektur-Entscheidung (2026):**  
Die Merle-spezifischen RPA-Erweiterungen (Persona, Skills, Tool, Commands) wurden aus dem schweren Fork in eine **leichte, projekt-lokale `.opencode/`-Konfiguration** im Merle-Root verschoben. Dadurch profitieren alle Entwickler sofort von der RPA-Hybrid-Architekt-Persona, ohne den großen Fork klonen zu müssen.

Das Verzeichnis `rpa-opencode-hybrid/` bleibt nur für folgende seltene Fälle erhalten:
- Entwicklung von Patches am OpenCode-Core
- Erstellung angepasster Builds / Tauri-Pakete
- Experimente mit neuen OpenCode-Plugin-APIs

Für den Normalfall: `opencode` im Merle-Root starten.
