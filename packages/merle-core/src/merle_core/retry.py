"""
Zentrale Retry-Policies und Dekoratoren für Merle-Bots.

Bietet vordefinierte, bewährte Policies für verschiedene Szenarien:
- HTTP / API Calls
- Browser-Automatisierung (Playwright)
- Datenbank- / Queue-Operationen
- Sensitive Operationen (weniger aggressive Retries)

Verwendung:
    from merle_core.retry import with_retry, default_http_retry

    @with_retry(policy=default_http_retry)
    async def call_external_api(...):
        ...
"""

from __future__ import annotations

import asyncio
import functools
import inspect
from typing import Any, Callable, TypeVar

from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
    RetryCallState,
)
from loguru import logger

from .exceptions import RetryExhaustedError

T = TypeVar("T")


# ─────────────────────────────────────────────────────────────
# Vordefinierte Policies
# ─────────────────────────────────────────────────────────────


def _log_retry(retry_state: RetryCallState) -> None:
    """Loggt jeden Retry-Versuch strukturiert."""
    if retry_state.outcome is None:
        return
    exc = retry_state.outcome.exception()
    if exc:
        logger.warning(
            "Retry attempt {attempt} failed for {fn} | error={error}",
            attempt=retry_state.attempt_number,
            fn=retry_state.fn.__name__ if retry_state.fn else "unknown",
            error=str(exc),
        )


# HTTP / API Calls (schnell, viele Retries)
default_http_retry = retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=2, max=30),
    retry=retry_if_exception_type((ConnectionError, TimeoutError)),
    before_sleep=_log_retry,
    reraise=True,
)

# Browser / Playwright (langsamer, weniger Retries + längere Wartezeit)
browser_retry = retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=2, min=4, max=60),
    retry=retry_if_exception_type((TimeoutError,)),
    before_sleep=_log_retry,
    reraise=True,
)

# Sensitive Operationen (z.B. Finanztransaktionen, kritische Queue-Items)
sensitive_operation_retry = retry(
    stop=stop_after_attempt(2),
    wait=wait_exponential(multiplier=5, min=10, max=120),
    retry=retry_if_exception_type((ConnectionError,)),
    before_sleep=_log_retry,
    reraise=True,
)

# Aggressive Policy (viele Versuche, kurze Intervalle) – nur für unkritische Jobs
aggressive_retry = retry(
    stop=stop_after_attempt(8),
    wait=wait_exponential(multiplier=0.5, min=1, max=15),
    retry=retry_if_exception_type(Exception),
    before_sleep=_log_retry,
    reraise=True,
)


# ─────────────────────────────────────────────────────────────
# Dekorator-Factory
# ─────────────────────────────────────────────────────────────


def with_retry(
    policy: Any = default_http_retry,
    *,
    operation_name: str | None = None,
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Dekorator, der eine Tenacity-Policy mit Merle-spezifischem Error-Handling kombiniert.

    Args:
        policy: Eine der vordefinierten Policies oder eine eigene tenacity retry-Instanz
        operation_name: Optionaler Name für bessere Fehlermeldungen
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        # Apply tenacity to the original function first so retries see the real
        # exception types (and async functions stay awaitable).
        retried = policy(func)  # type: ignore[untyped-decorator]
        op_name = operation_name or func.__name__

        def _wrap_exhausted(exc: Exception) -> RetryExhaustedError:
            return RetryExhaustedError(
                operation=op_name,
                attempts=getattr(policy, "stop", "unknown"),  # type: ignore[arg-type]
                last_error=exc,
            )

        if inspect.iscoroutinefunction(func) or asyncio.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> T:
                try:
                    return await retried(*args, **kwargs)  # type: ignore[misc]
                except RetryExhaustedError:
                    raise
                except Exception as exc:
                    raise _wrap_exhausted(exc) from exc

            return async_wrapper  # type: ignore[return-value]

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            try:
                return retried(*args, **kwargs)  # type: ignore[return-value]
            except RetryExhaustedError:
                raise
            except Exception as exc:
                raise _wrap_exhausted(exc) from exc

        return wrapper  # type: ignore[return-value]

    return decorator


# ─────────────────────────────────────────────────────────────
# Hilfsfunktion für manuelle Nutzung
# ─────────────────────────────────────────────────────────────


async def retry_with_policy(
    func: Callable[..., Any],
    *args: Any,
    policy: Any = default_http_retry,
    operation_name: str | None = None,
    **kwargs: Any,
) -> Any:
    """Führt eine async Funktion mit einer Retry-Policy aus."""
    decorated = with_retry(policy=policy, operation_name=operation_name)(func)
    return await decorated(*args, **kwargs)
