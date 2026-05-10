/// <reference path="../env.d.ts" />
import { tool } from "@opencode-ai/plugin"
import { readFile } from "node:fs/promises"
import { join } from "node:path"

/**
 * RPA Context Loader — Lädt relevante Dokumentation aus dem
 * RPA Hybrid Development Kit basierend auf einem Topic.
 */
export default tool({
  description: `Lade RPA-Kit-Dokumentation zu einem bestimmten Thema.

Verfügbare Topics:
- "strategy" → docs/01_Strategie.md (Python-First Strategie)
- "decision-matrix" → docs/02_Wann_Python_vs_UiPath.md (Entscheidungsmatrix)
- "governance" → docs/03_Governance.md (Governance-Regeln)
- "project-structure" → docs/04_Projektstruktur.md (Projektstruktur)
- "dev-guide" → docs/05_Entwicklungsleitfaden.md (Entwicklungsleitfaden)
- "template" → python_bots/template/ (Template-Struktur)
- "agent-rules" → agent/CLAUDE.md (Agent-Regeln)
- "all" → Alle Docs im Überblick

Nutze dieses Tool, wenn du RPA-Kit-Dokumentation brauchst.`,
  args: {
    topic: tool.schema
      .enum([
        "strategy",
        "decision-matrix",
        "governance",
        "project-structure",
        "dev-guide",
        "template",
        "agent-rules",
        "all",
      ])
      .describe("Welches Thema soll geladen werden?"),
  },
  async execute(args) {
    const workspace = process.env.OPENCODE_WORKSPACE || process.cwd()

    const topicMap: Record<string, { file: string; label: string }> = {
      strategy: { file: "docs/01_Strategie.md", label: "Python-First Strategie" },
      "decision-matrix": {
        file: "docs/02_Wann_Python_vs_UiPath.md",
        label: "Entscheidungsmatrix",
      },
      governance: { file: "docs/03_Governance.md", label: "Governance-Regeln" },
      "project-structure": {
        file: "docs/04_Projektstruktur.md",
        label: "Projektstruktur",
      },
      "dev-guide": {
        file: "docs/05_Entwicklungsleitfaden.md",
        label: "Entwicklungsleitfaden",
      },
      "agent-rules": { file: "agent/CLAUDE.md", label: "Agent-Regeln" },
    }

    try {
      if (args.topic === "all") {
        const summaries: string[] = []
        for (const [key, { label }] of Object.entries(topicMap)) {
          summaries.push(`- **${key}**: ${label}`)
        }
        summaries.push("- **template**: python_bots/template/ — Basis-Template")

        return `# RPA Hybrid Development Kit — Übersicht

## Verfügbare Dokumente

${summaries.join("\n")}

Nutze \`load_rpa_context\` mit einem spezifischen Topic, um den vollen Inhalt zu laden.

## Kernprinzipien
- Python-First (80-90 % der Automatisierungen)
- UiPath nur bei nachgewiesenem Vorteil
- Template-basierte Entwicklung
- Linux-Container-fähig
- Strukturiertes Logging & Retry-Mechanismen
- Testgetrieben (>70 % Abdeckung)
`
      }

      if (args.topic === "template") {
        return `# Template-Struktur

Das Basis-Template in \`python_bots/template/\`:

\`\`\`
python_bots/template/
├── main.py              # Einstiegspunkt (asyncio)
├── config.py            # pydantic-settings Konfiguration
├── tasks/               # Geschäftslogik-Module
│   ├── __init__.py
│   └── example_task.py
├── tests/               # Tests
│   ├── __init__.py
│   ├── conftest.py
│   └── test_main.py
├── requirements.txt     # Abhängigkeiten
├── Dockerfile           # Container-Definition
├── .env.example         # Konfigurationsvorlage
├── .gitignore
└── README.md
\`\`\`

## Verwendung
\`\`\`bash
cp -r python_bots/template/ python_bots/<bot_name>/
cd python_bots/<bot_name>/
\`\`\`

## Schlüsselmerkmale
- loguru für strukturiertes Logging
- tenacity für Retry-Mechanismen
- pydantic-settings für Konfiguration
- httpx als async HTTP-Client
- pytest für Testing
- Docker für Container-Deployment
`
      }

      const topic = topicMap[args.topic]
      if (!topic) {
        return `Unbekanntes Topic: ${args.topic}. Nutze "all" für eine Übersicht.`
      }

      const content = await readFile(join(workspace, topic.file), "utf-8")
      return `# ${topic.label}\n\n${content}`
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error)
      return `Fehler beim Laden von "${args.topic}": ${message}\n\nStelle sicher, dass das RPA Hybrid Development Kit im Workspace vorhanden ist.`
    }
  },
})
