"""
BaseTask — Die neue Standard-Basisklasse für feingranulare Arbeitseinheiten in Merle-Bots.

Jeder komplexere Bot sollte seine Geschäftslogik in mehrere `BaseTask`-Unterklassen aufteilen.
Dies ermöglicht:
- Bessere Testbarkeit
- Feingranulares Retry & Error-Handling
- Automatische Metriken pro Task
- Self-Healing-Hooks
"""

from __future__ import annotations

from abc import ABC, abstractmethod
import time
from typing import Any

from loguru import logger


class BaseTask(ABC):
    """
    Abstrakte Basisklasse für wiederverwendbare Tasks innerhalb eines Bots.

    Ein Task ist eine logisch abgeschlossene Arbeitseinheit (z.B. "Daten aus SAP holen",
    "PDF parsen", "Ergebnis in Queue schreiben").

    Beispiel:
        class FetchInvoicesTask(BaseTask):
            async def execute(self) -> dict[str, Any]:
                ...
    """

    def __init__(self, settings: Any, name: str | None = None) -> None:
        self.settings = settings
        self.name = name or self.__class__.__name__
        self.logger = logger.bind(task=self.name)
        self._start_time: float | None = None
        self._duration: float | None = None
        self._status: str = "pending"

    @abstractmethod
    async def execute(self) -> dict[str, Any]:
        """Enthält die eigentliche Business-Logik des Tasks. Muss überschrieben werden."""
        ...

    async def run(self) -> dict[str, Any]:
        """
        Öffentliche Einstiegsmethode mit Timing, Logging und Error-Handling.
        Sollte in der Regel nicht überschrieben werden.
        """
        self._start_time = time.perf_counter()
        self._status = "running"
        self.logger.info("Task {} startet", self.name)

        _record_task_start(self.name)

        try:
            result = await self.execute()
            self._status = "success"
            self._duration = time.perf_counter() - self._start_time

            self.logger.info(
                "Task {} erfolgreich beendet in {:.2f}s",
                self.name,
                self._duration,
            )
            _record_task_success(self.name, self._duration)
            self._on_success(result)
            return result

        except Exception as exc:
            self._status = "failed"
            self._duration = time.perf_counter() - self._start_time if self._start_time else 0
            self.logger.exception("Task {} fehlgeschlagen nach {:.2f}s", self.name, self._duration)
            _record_task_failure(self.name, self._duration)
            self._on_failure(exc)
            raise

    def _on_success(self, result: dict[str, Any]) -> None:
        """Hook für erfolgreiche Ausführung. Kann überschrieben werden."""
        pass

    def _on_failure(self, exception: Exception) -> None:
        """Hook bei Fehlern. Kann für Self-Healing, Fallback oder Alerting überschrieben werden."""
        pass

    def get_metrics(self) -> dict[str, Any]:
        """Liefert grundlegende Metriken über die letzte Ausführung."""
        return {
            "task": self.name,
            "status": self._status,
            "duration_seconds": round(self._duration, 3) if self._duration is not None else None,
        }

    @property
    def duration(self) -> float | None:
        """Dauer der letzten Ausführung in Sekunden."""
        return self._duration

    @property
    def status(self) -> str:
        """Aktueller oder letzter Status des Tasks."""
        return self._status


# ─────────────────────────────────────────────────────────────
# Leichte OTEL-Integration (wird nur aktiv, wenn configure_observability() aufgerufen wurde)
# ─────────────────────────────────────────────────────────────


def _record_task_start(task_name: str) -> None:
    try:
        from .observability.metrics import get_meter

        meter = get_meter("merle_core.base_task")
        counter = meter.create_counter("task_executions_total", unit="1")
        counter.add(1, {"task": task_name, "status": "started"})
    except Exception:
        pass


def _record_task_success(task_name: str, duration: float) -> None:
    try:
        from .observability.metrics import get_meter

        meter = get_meter("merle_core.base_task")
        counter = meter.create_counter("task_executions_total", unit="1")
        histogram = meter.create_histogram("task_duration_seconds", unit="s")
        counter.add(1, {"task": task_name, "status": "success"})
        histogram.record(duration, {"task": task_name})
    except Exception:
        pass


def _record_task_failure(task_name: str, duration: float) -> None:
    try:
        from .observability.metrics import get_meter

        meter = get_meter("merle_core.base_task")
        counter = meter.create_counter("task_executions_total", unit="1")
        error_counter = meter.create_counter("errors_total", unit="1")
        histogram = meter.create_histogram("task_duration_seconds", unit="s")

        counter.add(1, {"task": task_name, "status": "failed"})
        error_counter.add(1, {"task": task_name})
        histogram.record(duration, {"task": task_name})
    except Exception:
        pass
