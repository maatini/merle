# ADR-0006: NATS als Grundlage für die zukünftige Orchestrierung (Phase 4)

**Status:** Accepted (Minimal Approach)  
**Datum:** 2026-05

## Kontext

Nachdem in Phase 2 ein starkes `merle-core` mit Resilienz und Observability geschaffen wurde, stellt sich die Frage, wie zukünftig **viele kleine, entkoppelte Tasks** orchestriert werden sollen.

Bisherige Ansätze (monolithische Bots + Prefect) stoßen bei sehr granularen, hochskalierbaren oder heterogenen Workloads an Grenzen.

## Entscheidung

Wir führen **NATS + JetStream** als zentrale Kommunikations- und Orchestrierungsschicht ein.

In Phase 4 (A1) bauen wir bewusst nur das **Fundament**:

- Ein flexibles Task-Modell (`TaskSpec` / `TaskResult`)
- Einen einfachen NATS-Client in `merle-core`
- Unterstützung für Publish/Subscribe und Request/Reply
- Kein voller Orchestrator (kommt in späteren Phasen)

## Begründung

- **NATS** ist extrem leichtgewichtig, hochperformant und cloud-native.
- Bietet nativ **Request/Reply**, was für RPA-Tasks sehr nützlich ist.
- JetStream ermöglicht persistente, zuverlässige Queues und State.
- Gute Integration mit bestehenden Tools (Cobra-NATS, NATS-Monitoring).
- Passt perfekt zur Vision von granularen, event-getriebenen Tasks.

## Konsequenzen

### Positiv
- Starke Entkopplung zwischen Tasks
- Gute Skalierbarkeit (horizontal)
- Natürliche Unterstützung für Retry, Dead Letter Queues, etc. (über JetStream)
- Gute Observability (Traces + Metrics können über NATS transportiert werden)

### Negativ / Risiken
- Erhöhte Komplexität im Vergleich zu monolithischen Bots
- Lernkurve für das Team (Event-Driven Thinking)
- NATS muss betrieben werden (auch wenn es sehr wartungsarm ist)

## Nächste Schritte (nach Phase 4)

- ADR für vollwertigen Orchestrator
- Worker-Framework
- Task State Management über NATS KV
- Integration mit Cobra-NATS als visuellem Monitoring-Tool

---

**Entscheidungsträger:** Merle RPA-Hybrid-Architekt
**Review:** Engineering Team
