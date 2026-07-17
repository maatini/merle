# CI/CD — Verantwortlichkeiten

## `ci.yml` — Haupt-Pipeline

**Owns:** Zentrale Qualitätsgates für alle Code-Änderungen.

| Job                 | Zweck                                   | Wichtige Details                                                                                                                 |
| ------------------- | --------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| **Quality**         | Lint + Type-Check + Test + CLI-Validate | Matrix-Strategie über Python 3.11 + 3.12. Ruff, mypy, pytest, `merle validate`. Alles derzeit `\|\| true`.                       |
| **Security**        | SAST + Vuln-Scan + Secrets-Detection    | Bandit (Python SAST), Trivy (Filesystem-Scan CRITICAL+HIGH), TruffleHog. Alles `continue-on-error`.                              |
| **Pre-commit**      | Format-Enforcement                      | Führt `pre-commit run --all-files` aus + Prettier-Check auf geänderten Non-Python-Dateien. Commitizen-Check via pre-commit Hook. |
| **Docker Template** | Template-Validierung                    | Generiert Test-Bot aus Template, baut Docker-Image im Monorepo-Modus. Fast Smoke-Test.                                           |

**Intended als Required Status Checks** für Branch Protection auf `main` — aber derzeit alle non-fatal.

---

## `docker-build.yml` — Docker-Validierung

**Owns:** Sicherstellen, dass das @tag:copier-template korrekte Docker-Images produziert.

| Aspekt          | Details                                                                                                   |
| --------------- | --------------------------------------------------------------------------------------------------------- |
| **Trigger**     | Push/PR mit Änderungen an `templates/bot/**`, `.dockerignore`; `workflow_dispatch`                        |
| **Job**         | `build-generated-bot`: Copier → Bot generieren → Docker Build mit Buildx + GHA-Caching → Image existiert? |
| **Geplant**     | Publish-Job (GHCR + SBOM + cosign sign) — auskommentiert, Phase 3+                                        |
| **Build-Modus** | Immer Monorepo (Build-Kontext = Repo-Root)                                                                |

---

## `docs.yml` — Dokumentation

**Owns:** MkDocs-Build + Deployment auf GitHub Pages.

| Aspekt         | Details                                                                                                 |
| -------------- | ------------------------------------------------------------------------------------------------------- |
| **Trigger**    | Push → `main` mit Änderungen an `docs/**`, `mkdocs.yml`, `AGENTS.md`, `README*.md`; `workflow_dispatch` |
| **Build-Job**  | Installiert `mkdocs-material` + `mkdocs-awesome-pages-plugin`, `mkdocs build --strict`                  |
| **Deploy-Job** | `deploy-pages` Action. `continue-on-error` (Pages möglicherweise nicht aktiviert).                      |
| **Output**     | `site/` → GitHub Pages (Artifact-Upload)                                                                |

---

## Weitere GitHub-Konfiguration

| Datei                    | Zweck                                                                                                                                                                       |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `dependabot.yml`         | Weekly Updates: GitHub Actions (Montags), Python/pip. Ignoriert Major-Ruff/Mypy-Bumps.                                                                                      |
| `CODEOWNERS`             | 6 Ownership-Zonen: merle-architects (root/docs/ADRs), merle-core-maintainers, merle-template-maintainers, merle-platform (CI/Devbox), merle-opencode-hybrid, merle-examples |
| `PULL_REQUEST_TEMPLATE/` | Leer (Platzhalter)                                                                                                                                                          |
| `ISSUE_TEMPLATE/`        | Bug-Report + Feature-Request + Config                                                                                                                                       |

---

## Pre-commit Hooks (`.pre-commit-config.yaml`)

| Hook           | Stage         | Zweck                                 |
| -------------- | ------------- | ------------------------------------- |
| **Ruff**       | `pre-commit`  | Lint mit Auto-Fix + Format-Check      |
| **Prettier**   | `pre-commit`  | Formatiert YAML, Markdown, JSON, TOML |
| **Commitizen** | `commit-msg`  | Erzwingt Conventional Commits         |
| **Mypy**       | (deaktiviert) | Läuft stattdessen in CI               |

## Was CI/CD **nicht** besitzt

- **Keine** Deployment-Pipeline für Bots (Bots werden manuell deployed)
- **Keine** Integration-Tests mit echten externen Systemen
- **Keine** Performance-Tests
- **Keine** NATS-Infrastructure-Tests (Phase 4)
- **Kein** `release.yml` — Releases sind derzeit manuell (Commitizen bump)
