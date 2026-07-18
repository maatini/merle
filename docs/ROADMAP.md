# Merle Roadmap

**Status:** Living Document  
**Last Updated:** 2026-07-18 (v0.5.1 — Docs & Truth Hardening)  
**Owner:** Merle RPA-Hybrid-Architekt + Platform Team

---

## Vision (unchanged since initial design)

Merle evolves into a **highly scalable, intelligent, cost-efficient Enterprise RPA Orchestration Platform** with:

- Fine-grained, independently executable and versioned **Tasks / Teil-Tasks**
- **NATS (JetStream)** as the durable, cloud-native backbone for all task storage, status, and routing
- Central **Orchestrator** that schedules tasks across heterogeneous workers (Docker, K8s, on-prem, cloud, GPU nodes) based on declared requirements and priorities
- Support for **multiple executor types**: pure Python, Playwright, optional Prefect flows, UiPath (via API/Scope), and future **KI/LLM agents + Vision models**
- **BPMN-grade transparency** and auditability (via BPMNinja integration)
- Strong **governance** and **Python-first** default (UiPath only on proven architectural need)

---

## Current State (v0.5.1) ✅

| Layer                  | Component                                  | Maturity     | Notes                                                                                                                                                                                      |
| ---------------------- | ------------------------------------------ | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Core**               | `merle-core` (0.5.1)                       | ✅ Good      | BaseBot, BaseTask, tenacity retry, OTel observability (extra), Azure secrets (extra), NATS client (extra), **Playwright wrapper mit Chromium + Lightpanda (ADR-0007)**, self-healing hooks |
| **Scaffolding**        | Copier Template + `merle` CLI              | ✅ Good      | Feature flags, post-gen hooks, `merle new-bot`, governance enforcement                                                                                                                     |
| **DX & Tooling**       | uv workspace, Devbox, justfile, pre-commit | ✅ Good      | CI (Ruff + mypy + pytest + Trivy), CODEOWNERS, issue/PR templates                                                                                                                          |
| **Agent & Governance** | `.opencode/` + AGENTS.md                   | ✅ Excellent | rpa-hybrid agent, governance-validator skill, rpa-bot-generator, binding rules                                                                                                             |
| **Documentation**      | `docs/`, ADRs (0001–0009), visuals         | ✅ Strong    | Entscheidungsmatrix, Architektur, secrets, NATS foundation ADR; Version-SSOT 0.5.1                                                                                                         |
| **Examples**           | `examples/`, `integration_examples/`       | 🟡 Growing   | Web, Excel, NATS task comm, UiPath hybrid, invoice-processing                                                                                                                              |
| **Docker Story**       | Template Dockerfile + Trivy                | 🟡 Partial   | Works but path-dep on merle-core still limits full independence (known issue)                                                                                                              |

**Milestone achieved:** Merle is a **professional, reviewable, internal-enterprise-ready RPA framework**. Stack claims match installed dependencies: Prefect 3 and rpaframework are **roadmap / optional / UiPath-scope**, not default installs.

**Shipped since Professional Foundation (v0.2):** Lightpanda (ADR-0007), NATS + Task model foundation, CLI restructuring, data/uipath modules, version SSOT 0.5.1.

---

## Near-Term (DX, Hardening & Real Examples) — ongoing

**Goals:**

- At least 3–4 **production-grade reference bots** in `examples/` (Invoice processing with PDF+Excel+Mail, SAP GUI via Playwright or optional rpaframework, Document classification with KI fallback, HR onboarding with HITL)
- `merle-core` observability & self-healing patterns hardened (Phase 2 plan in `docs/plans/phase2-merle-core-observability.md`)
- Docker template for generated bots works **without** workspace path dependencies (multi-stage + proper wheel publishing of merle-core or vendoring strategy)
- Expanded test coverage + property-based testing for resilience patterns
- `docs/ROADMAP.md` + visual C4 diagrams + architecture decision records fully bilingual or English-primary
- `just` + Devbox experience polished (one-command `just demo` that spins up a full example)

**Non-goals for this track:** Full NATS orchestrator, Prefect 3 as a productized default (orchestration track below).

---

## Orchestration Foundation (NATS Backbone) — Q3/Q4 2026

**Key Deliverables (see ADR-0006 and `docs/decisions/0006-nats-orchestration-foundation.md`):**

- Stable `merle_core.nats` client with JetStream, durable consumers, request-reply patterns (client foundation already in merle-core)
- **Task decomposition model** (`Task`, `TaskSpec`, `TaskResult`, priority, resource requirements, executor type)
- Reference **Orchestrator PoC** (Python service that pulls from NATS subjects, routes to workers, handles retries + dead-letter)
- Worker runtime that can execute:
  - Python functions / `BaseTask` subclasses
  - Prefect 3 flows (**optional**, not default stack)
  - UiPath jobs via Orchestrator API (when justified)
- Cobra-NATS UI integration for visibility into streams, consumers, and task history
- First **resource-aware scheduler** prototype (GPU / RAM / UiPath license tags)

**Success Criteria:**

- A complex business process can be split into 5–12 granular tasks that run on different workers with automatic retry, priority, and observability.
- Task execution history is queryable and visualizable.

---

## Intelligence Layer (KI Executors & Self-Healing)

- KI-Executor abstraction inside the orchestrator (LLM agent, vision model for document understanding, code-generation agent for self-healing)
- Integration with existing Merle resilience patterns (the KI executor becomes just another `ExecutorType` with special requirements)
- Self-healing at **task level** (not only bot level): on failure, the orchestrator can ask a KI agent to propose a patch or alternative path
- Cost & SLA tracking per task type (critical for the "Ressourcen-Optimierung zur Kosten-Minimierung" vision)
- Optional: Prefect 3 as a higher-level orchestration layer on top of NATS tasks for complex DAGs with human-in-the-loop steps

---

## Governance & Long-Term Platform (2027+)

- Formal **Merle Certification Program** for bots (governance-validator as gate in CI + PR)
- **BPMNinja** deep integration: every NATS-orchestrated process can be exported/visualized as BPMN with full audit trail
- Multi-tenant / multi-customer support patterns (isolation, secrets scoping, quota)
- Commercial packaging options (if the author decides to productize parts of Merle)

---

## How to Track Progress

- All architectural decisions are recorded as **ADRs** in `docs/decisions/`
- Implementation plans live in `docs/plans/`
- The `rpa-hybrid` agent and `governance-validator` skill will enforce roadmap alignment during code generation and review
- Quarterly roadmap reviews are documented in this file

---

## Related Documents

- [docs/concepts/strategie.md](concepts/strategie.md) — Python-First Strategy (binding)
- [docs/concepts/entscheidungsmatrix.md](concepts/entscheidungsmatrix.md) — When to use UiPath (binding)
- [docs/concepts/governance.md](concepts/governance.md) — The 11 Governance Rules
- [docs/decisions/0005-merle-core-v02-architecture.md](decisions/0005-merle-core-v02-architecture.md)
- [docs/decisions/0006-nats-orchestration-foundation.md](decisions/0006-nats-orchestration-foundation.md)
- [docs/plans/phase2-merle-core-observability.md](plans/phase2-merle-core-observability.md)
- [AGENTS.md](../AGENTS.md) — Binding rules for all AI agents working on Merle

---

**This roadmap is intentionally ambitious but grounded.**  
Every phase builds on the previous one while preserving the core promise: **most RPA work stays in clean, testable, Linux-native Python**, with UiPath and KI as powerful, justified tools in a well-governed hybrid platform.
