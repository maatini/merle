"""
Merle-spezifische Exception-Hierarchie.

Ziel: Klare, unterscheidbare Fehlertypen für besseres Error-Handling,
Retry-Policies und Observability.
"""

from __future__ import annotations

from typing import Any


class MerleError(Exception):
    """Basis-Exception für alle Merle-spezifischen Fehler."""

    def __init__(self, message: str, *, details: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.details = details or {}


# ─────────────────────────────────────────────────────────────
# Retry & Resilience
# ─────────────────────────────────────────────────────────────


class RetryExhaustedError(MerleError):
    """Alle Retry-Versuche sind fehlgeschlagen."""

    def __init__(self, operation: str, attempts: int, last_error: Exception) -> None:
        super().__init__(
            f"Retry exhausted after {attempts} attempts for operation '{operation}'",
            details={"operation": operation, "attempts": attempts, "last_error": str(last_error)},
        )
        self.operation = operation
        self.attempts = attempts
        self.last_error = last_error


class CircuitBreakerOpenError(MerleError):
    """Circuit Breaker ist offen – Operation wird nicht ausgeführt."""


# ─────────────────────────────────────────────────────────────
# Playwright / Browser
# ─────────────────────────────────────────────────────────────


class PlaywrightError(MerleError):
    """Basis-Exception für alle Playwright-bezogenen Fehler."""


class BrowserLaunchError(PlaywrightError):
    """Browser konnte nicht gestartet werden (Proxy, Stealth, Ressourcen)."""


class ElementNotFoundError(PlaywrightError):
    """Ein erwartetes Element wurde nicht gefunden (Selector, Timeout)."""

    def __init__(self, selector: str, page_url: str | None = None) -> None:
        super().__init__(f"Element not found: {selector}")
        self.selector = selector
        self.page_url = page_url


class ScreenshotFailedError(PlaywrightError):
    """Screenshot konnte nicht erstellt werden."""


# ─────────────────────────────────────────────────────────────
# Datenverarbeitung (Excel, PDF, Email)
# ─────────────────────────────────────────────────────────────


class DataProcessingError(MerleError):
    """Fehler bei der Verarbeitung von Excel, PDF oder E-Mails."""


class ExcelError(DataProcessingError):
    pass


class PdfError(DataProcessingError):
    pass


# ─────────────────────────────────────────────────────────────
# UiPath / Orchestrator
# ─────────────────────────────────────────────────────────────


class UiPathError(MerleError):
    """Fehler bei der Kommunikation mit UiPath Orchestrator."""


class QueueItemError(UiPathError):
    """Fehler beim Hinzufügen, Abrufen oder Aktualisieren eines Queue-Items."""


# ─────────────────────────────────────────────────────────────
# Secrets & Konfiguration
# ─────────────────────────────────────────────────────────────


class SecretsError(MerleError):
    """Fehler beim Zugriff auf Secrets (Key Vault, .env, etc.)."""


class SecretNotFoundError(SecretsError):
    """Ein benötigtes Secret wurde nicht gefunden."""


# ─────────────────────────────────────────────────────────────
# Allgemeine Business-Fehler
# ─────────────────────────────────────────────────────────────


class BusinessRuleViolation(MerleError):
    """Eine Geschäftsregel wurde verletzt (z.B. ungültiger Status)."""
