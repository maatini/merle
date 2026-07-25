"""
merle-core — Shared core utilities for Merle RPA bots.

Phase 2: Erweiterte Resilienz, Observability und zentrale Patterns.
"""

# Task Model (available as submodule)
from . import task
from .base_bot import BaseBot
from .base_task import BaseTask
from .exceptions import (
    ElementNotFoundError,
    MerleError,
    PlaywrightError,
    RetryExhaustedError,
    SecretNotFoundError,
    SecretsError,
)
from .http_client import RpaHttpClient
from .logging_config import setup_logging
from .retry import (
    aggressive_retry,
    browser_retry,
    default_http_retry,
    sensitive_operation_retry,
    with_retry,
)
from .task import TaskError, TaskResult, TaskSpec, TaskStatus

__all__ = [
    "BaseBot",
    "BaseTask",
    "ElementNotFoundError",
    "MerleError",
    "PlaywrightError",
    "RetryExhaustedError",
    "RpaHttpClient",
    "SecretNotFoundError",
    "SecretsError",
    "TaskError",
    "TaskResult",
    "TaskSpec",
    "TaskStatus",
    "aggressive_retry",
    "browser_retry",
    "default_http_retry",
    "sensitive_operation_retry",
    "setup_logging",
    "with_retry",
]

# --- Optional submodules (only imported when the corresponding extra is installed) ---

# Observability (extra: "observability")
try:
    from . import observability
    from .observability import configure_observability, get_meter, get_tracer

    _has_observability = True
except ImportError:
    observability = None  # type: ignore[assignment]
    configure_observability = None  # type: ignore[assignment]
    get_tracer = None  # type: ignore[assignment]
    get_meter = None  # type: ignore[assignment]
    _has_observability = False

# Playwright (extra: "playwright")
try:
    from . import playwright

    _has_playwright = True
except ImportError:
    playwright = None  # type: ignore[assignment]
    _has_playwright = False

# Secrets / Azure (extra: "azure")
try:
    from . import secrets

    _has_azure = True
except ImportError:
    secrets = None  # type: ignore[assignment]
    _has_azure = False

# NATS (extra: "nats") — Phase 4 foundation
try:
    from . import nats

    _has_nats = True
except ImportError:
    nats = None  # type: ignore[assignment]
    _has_nats = False

# Data and UiPath modules (always importable, optional dependencies inside)
from . import data, uipath

__all__ += [
    "configure_observability",
    "data",
    "get_meter",
    "get_tracer",
    "nats",
    "observability",
    "playwright",
    "secrets",
    "task",
    "uipath",
]


__version__ = "0.7.0"  # Deploy, Hybrid Gold & Security Hardening
