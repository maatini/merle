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

__all__ = [
    "BaseBot",
    "BaseTask",                    # Neu in v0.2
    "RpaHttpClient",
    "setup_logging",
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

# Observability (optional, via extra "observability")
from . import observability
from .observability import configure_observability, get_tracer, get_meter

# Playwright (optional, via extra "playwright")
from . import playwright

# Secrets (optional, via extra "azure") - available as submodule
# from merle_core import secrets

__all__ += [
    "configure_observability",
    "get_tracer",
    "get_meter",
    "observability",
    "playwright",
    "secrets",   # available as submodule
]

__version__ = "0.2.0"
