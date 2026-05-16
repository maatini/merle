# Merle Roadmap

**Status:** Living Document  
**Last Updated:** 2026-05-16 (Professional Foundation v0.2)  
**Owner:** Merle RPA-Hybrid-Architekt + Platform Team

---

## Vision (unchanged since initial design)

Merle evolves into a **highly scalable, intelligent, cost-efficient Enterprise RPA Orchestration Platform** with:

- Fine-grained, independently executable and versioned **Tasks / Teil-Tasks**
- **NATS (JetStream)** as the durable, cloud-native backbone for all task storage, status, and routing
- Central **Orchestrator** that schedules tasks across heterogeneous workers (Docker, K8s, on-prem, cloud, GPU nodes) based on declared requirements and priorities
- Support for **multiple executor types**: pure Python, Playwright, Prefect flows, UiPath (via API/Scope), and future **KI/LLM agents + Vision models**
- **BPMN-grade transparency** and auditability (via BPMNinja integration)
- Strong **governance** and **Python-first** default (UiPath only on proven architectural need)

---

## Current State (v0.2 – Professional Foundation) ✅

| Layer                    | Component                          | Maturity | Notes |
|--------------------------|------------------------------------|----------|-------|
| **Core**                 | `merle-core` (0.2.0)               | ✅ Good  | BaseBot, BaseTask, tenacity retry, OTel observability, Azure secrets, NATS client, Playwright stealth wrapper, self-healing hooks |
| **Scaffolding**          | Copier Template + `merle` CLI      | ✅ Good  | Feature flags, post-gen hooks, `merle new-bot`, governance enforcement |
| **DX & Tooling**         | uv workspace, Devbox, justfile, pre-commit | ✅ Good | CI (Ruff + mypy + pytest + Trivy), CODEOWNERS, issue/PR templates |
| **Agent & Governance**   | `.opencode/` + AGENTS.md           | ✅ Excellent | rpa-hybrid agent, governance-validator skill, rpa-bot-generator, binding rules |
| **Documentation**        | `docs/`, ADRs (0001–0006), visuals | ✅ Strong | Entscheidungsmatrix, Architektur, secrets, NATS foundation ADR |
| **Examples**             | `examples/`, `integration_examples/` | 🟡 Growing | Web, Excel, NATS task comm, UiPath hybrid |
| **Docker Story**         | Template Dockerfile + Trivy        | 🟡 Partial | Works but path-dep on merle-core still limits full independence (known issue) |

**Milestone achieved:** Merle is now a **professional, reviewable, internal-enterprise-ready RPA framework**. No longer "just a good first push".

---

## Near-Term (v0.3 – DX, Hardening & Real Examples) — Q2/Q3 2026

**Goals:**
- At least 3–4 **production-grade reference bots** in `examples/` (Invoice processing with PDF+Excel+Mail, SAP GUI via Playwright or rpaframework, Document classification with KI fallback, HR onboarding with HITL)
- `merle-core` observability & self-healing patterns hardened (Phase 2 plan in `docs/plans/phase2-merle-core-observability.md`)
- Docker template for generated bots works **without** workspace path dependencies (multi-stage + proper wheel publishing of merle-core or vendoring strategy)
- Expanded test coverage + property-based testing for resilience patterns
- `docs/ROADMAP.md` + visual C4 diagrams + architecture decision records fully bilingual or English-primary
- `just` + Devbox experience polished (one-command `just demo` that spins up a full example)

**Non-goals for v0.3:** Full NATS orchestrator, Prefect 3 production patterns (those move to v0.4).

---

## Orchestration Foundation (v0.4 – NATS Backbone) — Q3/Q4 2026

**Key Deliverables (see ADR-0006 and `docs/decisions/0006-nats-orchestration-foundation.md`):**

- Stable `merle_core.nats` client with JetStream, durable consumers, request-reply patterns
- **Task decomposition model** (`Task`, `TaskSpec`, `TaskResult`, priority, resource requirements, executor type)
- Reference **Orchestrator PoC** (Python service that pulls from NATS subjects, routes to workers, handles retries + dead-letter)
- Worker runtime that can execute:
  - Python functions / `BaseTask` subclasses
  - Prefect 3 flows (optional)
  - UiPath jobs via Orchestrator API (when justified)
- Cobra-NATS UI integration for visibility into streams, consumers, and task history
- First **resource-aware scheduler** prototype (GPU / RAM / UiPath license tags)

**Success Criteria:**
- A complex business process can be split into 5–12 granular tasks that run on different workers with automatic retry, priority, and observability.
- Task execution history is queryable and visualizable.

---

## Intelligence Layer (v0.5+ – KI Executors & Self-Healing)

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
- Commercial packaging options (if Antigravity decides to productize parts of Merle)

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
- [docs/concepts/governance.md](concepts/governance.md) — The 10 Governance Rules
- [docs/decisions/0005-merle-core-v02-architecture.md](decisions/0005-merle-core-v02-architecture.md)
- [docs/decisions/0006-nats-orchestration-foundation.md](decisions/0006-nats-orchestration-foundation.md)
- [docs/plans/phase2-merle-core-observability.md](plans/phase2-merle-core-observability.md)
- [AGENTS.md](../AGENTS.md) — Binding rules for all AI agents working on Merle

---

**This roadmap is intentionally ambitious but grounded.**  
Every phase builds on the previous one while preserving the core promise: **most RPA work stays in clean, testable, Linux-native Python**, with UiPath and KI as powerful, justified tools in a well-governed hybrid platform.
