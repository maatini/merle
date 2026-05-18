# =============================================================================
# Merle — Justfile (Modern DX for RPA Engineers)
# =============================================================================
# Usage:
#   just --list
#   just new-bot invoice_processor --playwright --pandas
#   just lint
#   just test
#   just docker
#
# Requirements: just (https://github.com/casey/just), uv, Docker (optional)
# Inside Devbox: just is available via `devbox run just ...` or after `direnv allow`.
# =============================================================================

set shell := ["bash", "-cu"]
set dotenv-load := true

# Default recipe
default:
    @just --list

# ─────────────────────────────────────────────────────────────────────────────
# Setup & Environment
# ─────────────────────────────────────────────────────────────────────────────

# Full development environment setup (uv + pre-commit + merle CLI)
setup:
    uv sync --group dev --all-packages
    uv run pre-commit install --install-hooks
    @echo "✅ Merle development environment ready"
    @echo "   Try: just new-bot my_bot --playwright"

# Install only runtime deps (no dev tools)
install:
    uv sync --all-packages

# Update lockfile + sync (after changing pyproject.toml)
lock:
    uv lock
    uv sync --group dev --all-packages

# ─────────────────────────────────────────────────────────────────────────────
# Bot Generation (Copier + merle CLI)
# ─────────────────────────────────────────────────────────────────────────────

# Create a new Merle bot from the official Copier template
# Example: just new-bot invoice_processor --playwright --pandas
new-bot NAME *FLAGS:
    @echo "🤖 Creating new Merle bot: {{NAME}}"
    uv run merle new-bot {{NAME}} {{FLAGS}}
    @echo ""
    @echo "Next steps:"
    @echo "  cd python_bots/{{NAME}}"
    @echo "  uv run python main.py"

# Alternative: direct copier (bypasses merle CLI)
copier-bot NAME:
    copier copy templates/bot python_bots/{{NAME}}

# ─────────────────────────────────────────────────────────────────────────────
# Quality & Linting (matches CI)
# ─────────────────────────────────────────────────────────────────────────────

# Run all linters (Ruff + format check)
lint:
    uv run ruff check .
    uv run ruff format --check .

# Auto-fix + format
fmt:
    uv run ruff check --fix .
    uv run ruff format .

# Type check merle-core (strict)
mypy:
    uv run mypy packages/merle-core/src/merle_core --strict

# Run pre-commit on all files (same as CI)
pre-commit:
    uv run pre-commit run --all-files

# ─────────────────────────────────────────────────────────────────────────────
# Testing
# ─────────────────────────────────────────────────────────────────────────────

# Run all tests (merle-core + template skeleton + examples)
test *ARGS:
    uv run pytest -q {{ARGS}}

# Test only merle-core
test-core *ARGS:
    uv run pytest packages/merle-core -q {{ARGS}}

# Test with coverage
test-cov:
    uv run pytest --cov=merle_core --cov-report=term-missing packages/merle-core

# ─────────────────────────────────────────────────────────────────────────────
# Docker (Template + Examples)
# ─────────────────────────────────────────────────────────────────────────────

# Build the official bot template image (for validation / Trivy scan)
# NOTE: Legacy template (python_bots/template/) was removed in PR 1
docker-template:
    @echo "❌ Legacy template (python_bots/template/) wurde in PR 1 entfernt."
    @echo "   Verwende stattdessen: just new-bot <name>  oder  uv run merle new-bot <name>"
    @exit 1

# Build a specific generated bot (after copier)
docker-bot BOT:
    docker build -t merle-{{BOT}}:latest python_bots/{{BOT}}

# Run Trivy scan locally on the template (requires aquasecurity/trivy image or binary)
trivy-template:
    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
        aquasecurity/trivy:latest image --severity CRITICAL merle-bot-template:latest || true

# ─────────────────────────────────────────────────────────────────────────────
# Documentation
# ─────────────────────────────────────────────────────────────────────────────

# Serve docs locally (MkDocs)
docs:
    uv run mkdocs serve -a localhost:8000

# Build static docs site (always clean first to avoid committing generated artifacts)
docs-build:
    rm -rf site/
    uv run mkdocs build --strict
    @echo "✅ Docs built to site/ (never commit this directory!)"

# ─────────────────────────────────────────────────────────────────────────────
# CI Simulation (local)
# ─────────────────────────────────────────────────────────────────────────────

# Run the full local CI pipeline (what GitHub Actions does)
ci: lint mypy test pre-commit
    @echo "✅ Local CI simulation passed"

# Validate that the lockfile is up-to-date (CI check)
lock-check:
    uv lock --check

# ─────────────────────────────────────────────────────────────────────────────
# Maintenance & Release Helpers
# ─────────────────────────────────────────────────────────────────────────────

# Show current versions of key tools
versions:
    @echo "Python: $(python --version)"
    @echo "uv:     $(uv --version)"
    @echo "Ruff:   $(uv run ruff --version)"
    @echo "Mypy:   $(uv run mypy --version)"
    @echo "Copier: $(uv run copier --version 2>/dev/null || echo 'not installed via uv')"

# Clean Python caches (safe)
clean:
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
    find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
    find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
    @echo "🧹 Python caches cleaned"

# Remove all generated test bots (use with caution)
clean-test-bots:
    find python_bots -maxdepth 1 -type d -name "test_*" -o -name "tmp_*" | xargs rm -rf 2>/dev/null || true
    @echo "🗑️  Test bots removed"

# ─────────────────────────────────────────────────────────────────────────────
# Vision / Future (NATS, Orchestration)
# ─────────────────────────────────────────────────────────────────────────────

# Placeholder for NATS development environment (Phase 5+)
nats-up:
    @echo "🚀 NATS + JetStream development environment (not yet implemented)"
    @echo "   See docs/decisions/0006-nats-orchestration-foundation.md"

# Placeholder for full example orchestration
orchestrate-example:
    @echo "See examples/nats-task-communication/ for current PoC"
