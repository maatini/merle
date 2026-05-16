# Architektur von Merle

## C4 Context Diagram (Level 1)

```mermaid
C4Context
    title System Context - Merle RPA Platform

    Person(developer, "RPA Developer", "Entwickelt und betreibt Python-Bots")
    Person(business, "Fachabteilung", "Definiert Prozesse und prüft Ergebnisse")

    System(merle, "Merle Platform", "Python-First RPA Lifecycle Engine")
    System(uipath, "UiPath Orchestrator", "Enterprise Orchestrierung (optional)")

    System_Ext(azure, "Azure (Key Vault, AKS, Monitor)", "Cloud Services")
    System_Ext(targets, "Zielsysteme", "SAP, Webportale, Datenbanken, E-Mail...")

    Rel(developer, merle, "Entwickelt und deployed Bots")
    Rel(business, merle, "Nimmt Ergebnisse entgegen")
    Rel(merle, uipath, "Queue-Items, Jobs (hybrid)")
    Rel(merle, azure, "Secrets, Observability, Hosting")
    Rel(merle, targets, "Automatisiert Prozesse")
```

## C4 Container Diagram (Level 2)

```mermaid
C4Container
    title Merle - Container Architecture

    Container_Boundary(merle, "Merle Platform") {
        Container(template, "Copier Template", "Python + uv", "Standardisiertes Bot-Gerüst")
        Container(merle_core, "merle-core", "Python Library", "BaseBot, BaseTask, Retry, Observability, Playwright, Secrets")
        Container(examples, "Example Bots", "Python", "Web, Excel, UiPath-Hybrid Beispiele")
    }

    ContainerDb(keyvault, "Azure Key Vault", "Secrets")
    Container(otel, "OpenTelemetry (Loki + Tempo + Prometheus)", "Observability")
    Container(uipath, "UiPath Orchestrator", "Queue + Jobs")

    Rel(template, merle_core, "verwendet")
    Rel(examples, merle_core, "verwendet")
    Rel(merle_core, keyvault, "Secrets")
    Rel(merle_core, otel, "Traces + Metrics + Logs")
    Rel(examples, uipath, "Queue Items (hybrid)")
```

## Aktueller Stand: Prefect vs. NATS

| Aspekt                    | Prefect 3 (aktuell)          | NATS + JetStream (Vision)              | Status |
|---------------------------|------------------------------|----------------------------------------|--------|
| Orchestrierung            | Zentraler Server             | Dezentral, hochskalierbar              | Phase 4 geplant |
| State Management          | Prefect DB                   | NATS KV + Streams                      | - |
| UI / Transparenz          | Prefect UI                   | Cobra-NATS + BPMNinja                  | - |
| Self-Healing              | Begrenzt                     | Stark (Retry + Circuit Breaker)        | Schon in merle-core |
| Multi-Tenant / Isolation  | Gut                          | Exzellent (Streams + Consumers)        | - |
| Kosten / Betrieb          | Server notwendig             | Leichtgewichtig (kann in AKS laufen)   | - |

**Aktuelle Empfehlung (2026):**
- Für **komplexe Workflows** mit vielen Abhängigkeiten → Prefect 3
- Für **hochskalierbare, event-getriebene RPA** → NATS (Zielarchitektur)

---

## Technologie-Stack (2026)

- **Core**: Python 3.11+, uv, pydantic-settings
- **Resilienz**: tenacity, merle-core retry policies
- **Observability**: OpenTelemetry (OTLP) + loguru
- **Web**: Playwright (via merle-core wrapper)
- **Daten**: pandas, openpyxl, pdfplumber
- **Secrets**: Azure Key Vault
- **Container**: Docker (non-root, uv-basiert)
- **Orchestrierung**: Prefect 3 (heute) → NATS (Ziel)