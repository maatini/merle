# Merle Documentation Assets

Dieser Ordner enthält alle visuellen Assets für die Merle-Dokumentation.

## Struktur

```
assets/
├── images/
│   ├── decisions/           # Entscheidungsmatrix, Python vs UiPath
│   ├── governance/          # Governance-Regeln Poster & Visuals
│   ├── onboarding/          # Bot Lifecycle, Schnellstart-Visuals
│   └── architecture/        # C4-Diagramme, NATS-Architektur (exportiert)
└── diagrams/                # (optional) exportierte Mermaid-SVGs
```

## Richtlinien für neue Visuals

- **Mermaid** bevorzugen für alle technischen Architecture-Diagramme und Flows (versioniert, wartbar).
- **Generierte Bilder** (professionell, farbig, mit Icons) für Hero-Visuals, Governance-Poster und Lifecycle-Darstellungen.
- Dateinamen: `kebab-case-beschreibend.jpg` oder `.png`
- Immer mit aussagekräftigem Alt-Text und kurzer Erklärung im Markdown einbinden.
- Stil: Indigo + Cyan auf hellem Hintergrund (passend zum MkDocs Material Theme).

## Generierung neuer Visuals

Die hochwertigen Bilder in diesem Ordner wurden mit dem xAI Imagine Model erstellt.

Beispiel-Prompts für neue Visuals findest du im [Dokumentations-Verbesserungsplan](../plans/07-dokumentation-visualisierung.md).

---

**Stand**: Mai 2026 – Phase 3+ Documentation & Visualization Initiative