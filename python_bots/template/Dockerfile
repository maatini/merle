# syntax=docker/dockerfile:1
FROM python:3.11-slim AS builder

# uv binary aus offiziellem Image kopieren (sehr klein & schnell)
COPY --from=ghcr.io/astral-sh/uv:0.11 /uv /bin/uv

WORKDIR /app

# Nur die Lockfiles zuerst → bessere Layer-Caching
COPY pyproject.toml uv.lock ./

# System-Pakete nur für Build (Playwright braucht später noch mehr)
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Dependencies installieren (ohne dev) — frozen = exakt wie im Lockfile
RUN uv sync --frozen --no-dev --no-cache

# ─────────────────────────────────────────────────────────────
# Runtime Image (deutlich kleiner)
# ─────────────────────────────────────────────────────────────
FROM python:3.11-slim

WORKDIR /app

# uv für "uv run" im Container (optional, aber praktisch)
COPY --from=ghcr.io/astral-sh/uv:0.11 /uv /bin/uv

# Playwright + Fonts (für Web-Automatisierung)
RUN apt-get update && apt-get install -y --no-install-recommends \
        wget \
        ca-certificates \
        fonts-liberation \
        libglib2.0-0 \
        libnss3 \
        libnspr4 \
        libatk1.0-0 \
        libatk-bridge2.0-0 \
        libcups2 \
        libdrm2 \
        libdbus-1-3 \
        libxkbcommon0 \
        libxcomposite1 \
        libxdamage1 \
        libxfixes3 \
        libxrandr2 \
        libgbm1 \
        libpango-1.0-0 \
        libcairo2 \
        libasound2 \
    && rm -rf /var/lib/apt/lists/* \
    && playwright install --with-deps chromium || true

# Virtuelle Umgebung aus Builder-Stage kopieren
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Quellcode
COPY . .

# Nicht-root User
RUN useradd --create-home --uid 1000 botuser \
    && chown -R botuser:botuser /app
USER botuser

# Healthcheck (kann von Orchestrator genutzt werden)
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import asyncio; from main import main; print('ok')" || exit 1

CMD ["uv", "run", "python", "main.py"]
