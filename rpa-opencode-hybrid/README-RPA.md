# RPA OpenCode Hybrid

**Angepasste OpenCode-IDE für hybride RPA-Entwicklung**

Dies ist ein Fork von [OpenCode](https://github.com/anomalyco/opencode), angepasst und optimiert
für das [RPA Hybrid Development Kit](../). Der Fork erweitert OpenCode um:
- Einen dedizierten **RPA-Hybrid-Architekt** Agent
- RPA-spezifische **Skills** für Prozessanalyse, Bot-Generierung und Governance
- Ein **MCP-Tool** (`rpa-context`) für On-Demand-Kit-Dokumentation
- Custom **Commands** (`/rpa-new-bot`, `/rpa-validate`)

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

## Verwendung

1. Öffne das RPA Hybrid Development Kit mit OpenCode:
   ```bash
   cd rpa-opencode-hybrid
   opencode ../  # Öffnet das Kit als Workspace
   ```

2. Wähle den `rpa-hybrid` Agent aus (falls nicht automatisch als Default)

3. Nutze die Commands:
   - `/rpa-new-bot` — Neuen Bot erstellen
   - `/rpa-validate` — Governance prüfen

4. Bei Bedarf Skills laden:
   - `load_skill rpa-process-analyzer` — Prozess analysieren
   - `load_skill rpa-bot-generator` — Bot generieren
   - `load_skill governance-validator` — Validieren

## Struktur der Erweiterungen

```
.opencode/
├── agent/
│   └── rpa-hybrid.md           # Custom Primary Agent
├── skills/
│   ├── rpa-process-analyzer/
│   │   └── SKILL.md
│   ├── rpa-bot-generator/
│   │   └── SKILL.md
│   └── governance-validator/
│       └── SKILL.md
├── tool/
│   └── rpa-context.ts          # MCP-Tool für Kit-Kontext
├── command/
│   ├── rpa-new-bot.md
│   └── rpa-validate.md
└── opencode.jsonc              # Permissions & Tool-Konfiguration
```

## Upstream

Dieser Fork basiert auf [anomalyco/opencode](https://github.com/anomalyco/opencode).
Die Anpassungen sind nicht-invasiv — alle OpenCode-Features bleiben vollständig erhalten.
