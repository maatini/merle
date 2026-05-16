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

## Dokumentation

| Bereich                    | Link |
|---------------------------|------|
| Schnellstart              | [Getting Started](getting-started/quickstart.md) |
| Architektur & Konzepte    | [Architektur](concepts/architecture.md) |
| merle-core (v0.2)         | [merle-core](merle-core/index.md) |
| Beispiele                 | [Beispiele](examples/web.md) |
| Governance & Best Practices | [Governance](concepts/governance.md) |

---

## Status

- **Aktuelle Version**: `merle-core` 0.2 + Copier Template
- **Phase**: 3 – Documentation & Polish
- **Nächstes großes Ziel**: NATS-basierte Orchestrierung (Vision)

---

**Merle** ist ein internes Framework der Antigravity GmbH. Alle Rechte vorbehalten.