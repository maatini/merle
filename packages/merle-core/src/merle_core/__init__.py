"""
merle-core — Shared core utilities for Merle RPA bots.

Phase 2: Erweiterte Resilienz, Observability und zentrale Patterns.
"""

from .base_bot import BaseBot
from .base_task import BaseTask
from .http_client import RpaHttpClient
from .logging_config import setup_logging
from .exceptions import (
    MerleError,
    RetryExhaustedError,
    PlaywrightError,
    ElementNotFoundError,
    SecretsError,
    SecretNotFoundError,
)
from .retry import (
    with_retry,
    default_http_retry,
    browser_retry,
    sensitive_operation_retry,
    aggressive_retry,
)
from .task import TaskSpec, TaskResult, TaskStatus, TaskError

# Task Model (available as submodule)
from . import task

__all__ = [
    "BaseBot",
    "BaseTask",
    "RpaHttpClient",
    "setup_logging",
    # Task Model (Phase 4)
    "TaskSpec",
    "TaskResult",
    "TaskStatus",
    "TaskError",
    # Exceptions
    "MerleError",
    "RetryExhaustedError",
    "PlaywrightError",
    "ElementNotFoundError",
    "SecretsError",
    "SecretNotFoundError",
    # Retry
    "with_retry",
    "default_http_retry",
    "browser_retry",
    "sensitive_operation_retry",
    "aggressive_retry",
]

# --- Optional submodules (only imported when the corresponding extra is installed) ---

# Observability (extra: "observability")
try:
    from . import observability
    from .observability import configure_observability, get_tracer, get_meter

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
from . import data
from . import uipath

__all__ += [
    "configure_observability",
    "get_tracer",
    "get_meter",
    "observability",
    "playwright",
    "secrets",
    "nats",
    "task",
    "data",
    "uipath",
]


__version__ = "0.7.0"  # Deploy, Hybrid Gold & Security Hardening
