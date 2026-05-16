# Architektur-Entscheidungen (ADRs)

Dieses Verzeichnis enthält alle **Architecture Decision Records** des Merle-Frameworks.

Jede größere technische oder strategische Entscheidung wird hier dokumentiert — inklusive Kontext, Alternativen und Begründung.

## Aktuelle ADRs

| # | Titel | Status | Datum |
|---|-------|--------|-------|
| [0001](0001-python-first-strategie.md) | Python-First Strategie | Accepted | 2025 |
| [0002](0002-verbindliche-template-architektur.md) | Verbindliche Template-Architektur | Accepted | 2025 |
| [0003](0003-integration-python-uipath.md) | Integration Python ↔ UiPath | Accepted | 2025 |
| [0004](0004-copier-bot-scaffolding.md) | Copier-basiertes Bot-Scaffolding | Accepted | 2026 |
| [0005](0005-merle-core-v02-architecture.md) | merle-core v0.2 Architektur | Accepted | 2026 |
| [0006](0006-nats-orchestration-foundation.md) | NATS als Grundlage für Orchestrierung (Phase 4) | Accepted | 2026 |
| [0007](0007-lightpanda-als-optionale-browser-engine.md) | Lightpanda als optionale Browser-Engine | Accepted | 2026-05-17 |
| [0008](0008-repository-visibility-and-internal-governance.md) | Repository Visibility & Internal Governance | Accepted | 2026-05-16 |

## Warum ADRs?

- Nachvollziehbarkeit von Architekturentscheidungen
- Vermeidung von "Das haben wir schon immer so gemacht"
- Hilft neuen Teammitgliedern und dem RPA-Hybrid-Architekten bei Reviews
- Wird vom `governance-validator` und OpenCode-Agenten aktiv genutzt

---

**Merke**: Jede Entscheidung für oder gegen UiPath **muss** in einem ADR dokumentiert werden (siehe Regel 10).