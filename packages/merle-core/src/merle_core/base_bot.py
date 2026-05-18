"""
BaseBot — Die zentrale Basisklasse für Merle RPA-Bots (Phase 2+).

Erweiterungen gegenüber v0.1:
- Automatisches Timing + Metriken
- Erweiterte Lifecycle-Hooks (_on_success, _on_failure)
- Bessere Integration mit BaseTask
- Vorbereitung für Observability (Metrics / Tracing)
"""

from __future__ import annotations

import time
from abc import ABC, abstractmethod
from typing import Any

from loguru import logger


class BaseBot(ABC):
    """
    Abstrakte Basisklasse für alle Merle RPA-Bots.

    Jeder Bot sollte von dieser Klasse erben und `execute()` implementieren.
    Die `run()`-Methode übernimmt standardisiertes Logging, Timing und Error-Handling.
    """

    def __init__(self, settings: Any, *, name: str | None = None) -> None:
        """
        Initialize BaseBot.

        Args:
            settings: Pydantic-settings or any config object. Should ideally have
                      a `bot_name` attribute (enforced by governance).
            name: Optional explicit bot name. Takes precedence over settings.bot_name.
        """
        self.settings = settings
        bot_name = name or getattr(settings, "bot_name", None) or self.__class__.__name__
        self.name = bot_name
        self.logger = logger.bind(bot=self.name)
        self._start_time: float | None = None
        self._duration: float | None = None
        self._status: str = "pending"

    @abstractmethod
    async def execute(self) -> dict[str, Any]:
        """Hauptlogik des Bots. Muss in der Subklasse implementiert werden."""
        ...

    async def run(self) -> dict[str, Any]:
        """
        Öffentliche Einstiegsmethode mit vollständigem Lifecycle-Management.
        In der Regel nicht überschreiben.
        """
        self._start_time = time.perf_counter()
        self._status = "running"

        self.logger.info(
            "Bot {} startet (env={})",
            self.name,
            getattr(self.settings, "environment", "unknown"),
        )

        # Optional: OTEL Metrics (wenn configure_observability() aufgerufen wurde)
        _record_bot_start(self.settings.bot_name)

        try:
            result = await self.execute()
            self._status = "success"
            self._duration = time.perf_counter() - self._start_time

            self.logger.info(
                "Bot {} erfolgreich beendet in {:.2f}s",
                self.name,
                self._duration,
            )
            _record_bot_success(self.name, self._duration)
            self._on_success(result)
            return result

        except Exception as exc:
            self._status = "failed"
            self._duration = time.perf_counter() - self._start_time if self._start_time else 0
            self.logger.exception("Bot {} fehlgeschlagen nach {:.2f}s", self.name, self._duration)
            _record_bot_failure(self.name, self._duration)
            self._on_failure(exc)
            raise

    def _on_success(self, result: dict[str, Any]) -> None:
        """Hook nach erfolgreicher Ausführung. Kann für Post-Processing oder Metrics überschrieben werden."""
        pass

    def _on_failure(self, exception: Exception) -> None:
        """Hook bei Fehlern. Geeignet für Self-Healing, Fallback oder Alerting."""
        pass

    def health_check(self) -> dict[str, Any]:
        """Erweiterter Health-Check mit aktuellen Metriken."""
        return {
            "status": "healthy" if self._status != "failed" else "unhealthy",
            "bot": self.name,
            "environment": getattr(self.settings, "environment", "unknown"),
            "last_run_status": self._status,
            "last_run_duration": round(self._duration, 3) if self._duration else None,
        }

    def get_metrics(self) -> dict[str, Any]:
        """Liefert Metriken der letzten Bot-Ausführung."""
        return {
            "bot": self.name,
            "status": self._status,
            "duration_seconds": round(self._duration, 3) if self._duration is not None else None,
        }

    @property
    def duration(self) -> float | None:
        """Dauer der letzten Ausführung in Sekunden."""
        return self._duration

    @property
    def status(self) -> str:
        """Aktueller oder letzter Ausführungsstatus."""
        return self._status


# ─────────────────────────────────────────────────────────────
# Leichte OTEL-Integration (wird nur aktiv, wenn observability konfiguriert ist)
# ─────────────────────────────────────────────────────────────


def _record_bot_start(bot_name: str) -> None:
    try:
        from .observability.metrics import get_meter

        meter = get_meter("merle_core.base_bot")
        counter = meter.create_counter("bot_executions_total", unit="1")
        counter.add(1, {"bot": bot_name, "status": "started"})
    except Exception:
        pass  # Observability nicht aktiviert oder nicht installiert


def _record_bot_success(bot_name: str, duration: float) -> None:
    try:
        from .observability.metrics import get_meter

        meter = get_meter("merle_core.base_bot")
        counter = meter.create_counter("bot_executions_total", unit="1")
        histogram = meter.create_histogram("bot_duration_seconds", unit="s")
        counter.add(1, {"bot": bot_name, "status": "success"})
        histogram.record(duration, {"bot": bot_name})
    except Exception:
        pass


def _record_bot_failure(bot_name: str, duration: float) -> None:
    try:
        from .observability.metrics import get_meter

        meter = get_meter("merle_core.base_bot")
        counter = meter.create_counter("bot_executions_total", unit="1")
        error_counter = meter.create_counter("errors_total", unit="1")
        histogram = meter.create_histogram("bot_duration_seconds", unit="s")

        counter.add(1, {"bot": bot_name, "status": "failed"})
        error_counter.add(1, {"bot": bot_name, "error_type": "exception"})
        histogram.record(duration, {"bot": bot_name})
    except Exception:
        pass
