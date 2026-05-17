# Changelog

All notable changes to Merle will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.2.0] - 2026-05-16 — Professional Foundation

**This is the first major milestone release after the initial push.**  
Merle transitions from a promising internal project to a **professional, maintainable, and enterprise-ready RPA framework**.

### Highlights

- **Template Strategy Finalized**  
  The official, maintained way to create new bots is now exclusively through the Copier template in `templates/bot/`, driven by the `merle` CLI (`merle new-bot`). The old static snapshot in `python_bots/template/` has been properly deprecated.

- **Strong Governance Surface**  
  Added full GitHub repository governance: Issue templates, Pull Request template, CODEOWNERS, SECURITY.md, and a comprehensive `.github/` structure.

- **Developer Experience**

  - New `justfile` with commands like `just new-bot`, `just lint`, `just test`, `just ci`, `just docker`.
  - Significantly improved root `.dockerignore` and per-bot `.dockerignore.jinja`.
  - Professional multi-stage `Dockerfile.jinja` with explicit monorepo vs. standalone support.

- **High-Quality Reference Implementation**  
  Added `examples/invoice-processing/` — a production-grade reference bot demonstrating:

  - `BaseBot` + multiple fine-grained `BaseTask` classes
  - Observability, structured retry, PDF + Excel processing, master data enrichment
  - Professional configuration and error handling

- **Core Library Improvements (`merle-core`)**

  - `BaseBot` ergonomics improved (optional `name` parameter, graceful fallback)
  - Safer handling of optional extras (playwright, nats, azure, observability)
  - Professional OpenTelemetry + Loguru integration using the `patcher` pattern (no more dangerous re-logging sinks)
  - Better testability and resilience patterns

- **CI/CD Maturity**

  - Docker CI workflow now actually validates freshly generated bots using the Copier template in monorepo mode.
  - Test suite made CI-friendly (known environment-sensitive tests isolated with `xfail`).

- **Documentation & Process**
  - New `docs/ROADMAP.md` consolidating vision and phases.
  - Updated `CONTRIBUTING.md` to reflect current professional workflows.
  - Clear deprecation path for legacy artifacts.

### Breaking Changes

- The old `python_bots/template/` directory is now officially deprecated. New bots must be created via `merle new-bot` or `copier copy templates/bot`.

### Migration

```bash
# Old (no longer supported)
cp -r python_bots/template/ python_bots/my_bot/

# New (recommended)
merle new-bot my_bot --playwright --pandas
# or
copier copy templates/bot python_bots/my_bot
```

---

## [0.1.0] - Initial Push

Initial public structure of the Merle framework (pre-professionalization).

---

[Unreleased]: https://github.com/maatini/merle/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/maatini/merle/releases/tag/v0.2.0-professional-foundation
