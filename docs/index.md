# Merle

**Modular Enterprise RPA Lifecycle Engine**

Python-First Framework für wartbare, testbare und skalierbare RPA-Bots.

80–90 % der Automatisierungen in modernem Python. UiPath nur bei nachgewiesenem Vorteil.

---

## Warum Merle?

- **Python ist der Default** — moderne Stack (Playwright, pandas, Prefect, loguru, tenacity…)
- **Starkes Core-Framework** (`merle-core`) mit Observability, Resilienz und Secrets-Management
- **Template-First** — jeder neue Bot startet mit dem offiziellen Copier-Template
- **Cloud-Native** — Linux-Container-fähig, OpenTelemetry, Azure Key Vault ready
- **Hybride Architektur** — nahtlose Integration mit UiPath wo sinnvoll

---

## Schnellstart

**Neu hier?** → Lies zuerst den **[Junior-Guide für Einsteiger](getting-started/junior-guide.md)** (einfach erklärt, Schritt für Schritt).

```bash
# Neuen Bot erzeugen (empfohlen)
merle new-bot mein_bot --playwright

cd python_bots/mein_bot
uv sync --group dev
uv run python main.py
```

Oder direkt mit Copier:

```bash
copier copy templates/bot python_bots/mein_bot
```

---

## Kern-Visuals (empfohlen zum Einstieg)

Diese drei Diagramme geben dir den besten Überblick über Merle:

| Visual | Beschreibung | Link |
|--------|--------------|------|
| **Python vs. UiPath Entscheidung** | Der zentrale Entscheidungsbaum für alle Automatisierungen | [Entscheidungsmatrix](concepts/entscheidungsmatrix.md) |
| **Die 10 Governance-Regeln** | Visuelle Übersicht aller verbindlichen Regeln | [Governance](concepts/governance.md) |
| **Bot Lifecycle** | Kompletter Weg von der Idee bis zum produktiven Bot in AKS | [Entwicklungsleitfaden](concepts/entwicklungsleitfaden.md) |

---

## Dokumentation

| Bereich                    | Link |
|---------------------------|------|
| Schnellstart              | [Getting Started](getting-started/quickstart.md) |
| Entscheidungsmatrix       | [Python vs. UiPath](concepts/entscheidungsmatrix.md) |
| Governance & Best Practices | [Governance-Regeln](concepts/governance.md) |
| Architektur & NATS Vision | [Architektur](concepts/architecture.md) |
| Entwicklung               | [Entwicklungsleitfaden](concepts/entwicklungsleitfaden.md) |

---

## Status

- **Aktuelle Version**: `merle-core` 0.2 + Copier Template
- **Phase**: 3 – Documentation & Polish
- **Nächstes großes Ziel**: NATS-basierte Orchestrierung (Vision)

---

**Merle** ist ein proprietäres Framework von Martin Richardt. Alle Rechte vorbehalten.