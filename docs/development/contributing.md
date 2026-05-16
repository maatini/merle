# Contributing Guidelines

Willkommen! Wir freuen uns über Beiträge zum Merle-Framework.

## Grundsätze

- **Python-First** — Alle Änderungen müssen die Python-First-Strategie respektieren.
- **Template-Konformität** — Neue Features müssen mit dem aktuellen Copier-Template und `merle-core` kompatibel sein.
- **Governance** — Jede größere Änderung sollte in einem ADR dokumentiert werden.

## Workflow

1. Issue anlegen (falls nicht schon vorhanden)
2. Feature-Branch von `main` erstellen
3. Änderungen + Tests
4. Pull Request gegen `main`
5. Review durch mindestens einen Maintainer + RPA-Hybrid-Architekten

## Code-Qualität

- Ruff + mypy (strict) müssen durchlaufen
- Pre-commit Hooks sind verpflichtend
- Jede neue Funktionalität braucht grundlegende Tests

---

**Hinweis**: Für AI-gestützte Entwicklung bitte die Regeln in [AGENTS.md](../../AGENTS.md) beachten.