import { tool } from "@opencode-ai/plugin"
import { readFile } from "node:fs/promises"
import { join } from "node:path"
import { execSync } from "node:child_process"

/**
 * Merle RPA Context Loader — Lädt relevante Dokumentation aus dem
 * Merle Framework (Python-First RPA) basierend auf einem Topic.
 * Funktioniert sowohl bei Projekt-Root als auch bei globaler ~/.opencode Installation.
 */
export default tool({
  description: `Lade Merle RPA-Dokumentation zu einem bestimmten Thema.

Verfügbare Topics:
- "strategy" → Python-First Strategie
- "decision-matrix" → Entscheidungsmatrix (Python vs. UiPath)
- "governance" → Governance-Regeln (inkl. Rule 10)
- "project-structure" → Repository-Struktur & Konventionen
- "architecture" → Architektur (C4 + NATS Vision)
- "secrets" → Secrets Management
- "merle_core" → merle-core v0.3 (BaseTask, NATS, Observability, Playwright...)
- "examples" → Offizielle Beispiele
- "dev-guide" → Entwicklungsleitfaden
- "agent-rules" → Agent-Regeln (CLAUDE.md)
- "template" → Template-Struktur & Best Practices
- "all" → Alle Docs im Überblick

Nutze dieses Tool, wenn du Merle-Framework-Dokumentation brauchst (z.B. vor Bot-Erstellung oder Review).`,
  args: {
    topic: tool.schema
      .enum([
        "strategy",
        "decision-matrix",
        "governance",
        "project-structure",
        "dev-guide",
        "secrets",
        "architecture",
        "agent-rules",
        "merle_core",
        "examples",
        "template",
        "all",
      ])
      .describe("Welches Thema soll geladen werden?"),
  },
  async execute(args) {
    // Robust workspace detection: prefer OPENCODE_WORKSPACE, then git root, then cwd
    let workspace = process.env.OPENCODE_WORKSPACE
    if (!workspace) {
      try {
        workspace = execSync("git rev-parse --show-toplevel", { encoding: "utf8", stdio: ["pipe", "pipe", "ignore"] }).trim()
      } catch {
        workspace = process.cwd()
      }
    }

    const topicMap: Record<string, { file: string; label: string }> = {
      strategy: { file: "docs/concepts/strategie.md", label: "Python-First Strategie" },
      "decision-matrix": {
        file: "docs/concepts/entscheidungsmatrix.md",
        label: "Entscheidungsmatrix",
      },
      governance: { file: "docs/concepts/governance.md", label: "Governance-Regeln" },
      "project-structure": {
        file: "docs/concepts/projektstruktur.md",
        label: "Projektstruktur",
      },
      "dev-guide": {
        file: "docs/concepts/entwicklungsleitfaden.md",
        label: "Entwicklungsleitfaden",
      },
      secrets: { file: "docs/concepts/secrets-management.md", label: "Secrets Management" },
      architecture: { file: "docs/concepts/architecture.md", label: "Architektur (C4 + NATS)" },
      "agent-rules": { file: "agent/CLAUDE.md", label: "Agent-Regeln" },
      merle_core: { file: "packages/merle-core/README.md", label: "merle-core v0.3" },
      examples: { file: "examples/README.md", label: "Offizielle Beispiele" },
    }

    try {
      if (args.topic === "all") {
        const summaries: string[] = []
        for (const [key, { label }] of Object.entries(topicMap)) {
          summaries.push(`- **${key}**: ${label}`)
        }
        summaries.push("- **template**: templates/bot/ (Copier) + merle new-bot — verbindliches Template")

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
        return `# Template-Struktur (Merle Standard)

**Empfohlener Weg (Phase 3+):** Verwende immer den Copier-Template + Merle CLI:

\`\`\`bash
merle new-bot <bot_name> --playwright --pandas
# oder
copier copy templates/bot python_bots/<bot_name>
\`\`\`

Das moderne Template liegt unter \`templates/bot/\` und erzeugt:

\`\`\`
python_bots/<bot_name>/
├── main.py              # Einstiegspunkt (configure_observability + Task-Orchestrierung)
├── config.py            # pydantic-settings + AzureKeyVaultSettings
├── tasks/               # Geschäftslogik als BaseTask-Klassen
│   ├── __init__.py
│   └── <domain>_<action>_task.py
├── tests/               # pytest + pytest-playwright
│   ├── __init__.py
│   ├── conftest.py
│   └── test_*.py
├── requirements.txt
├── Dockerfile           # Linux-Container (uv-basiert)
├── pyproject.toml       # uv + mypy + ruff
├── .env.example
├── .gitignore
└── README.md
\`\`\`

**Wichtige Merle-Core-Features (Rule 10):**
- Erbt von \`BaseTask\` (nicht plain classes)
- \`configure_observability(service_name=...)\` in \`main.py\`
- \`@with_retry\` aus \`merle_core.retry\`
- Loguru + OpenTelemetry über \`merle_core\`
- NATS/JetStream Support (Phase 4)

**Legacy-Template** (nur noch für sehr alte Bots): \`python_bots/template/\`
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
      return `Fehler beim Laden von "${args.topic}": ${message}\n\nStelle sicher, dass du im Merle-Repository arbeitest (AGENTS.md vorhanden) oder die .opencode-Erweiterungen global installiert sind.`
    }
  },
})
