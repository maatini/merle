"""
Task-Modell für Merle (Phase 4 – NATS Orchestrierung).

Dieses Modell ist bewusst einfach und flexibel gehalten (A1-Variante),
damit es schnell einsetzbar ist und später bei Bedarf erweitert werden kann.

Kern-Idee:
- Ein Task wird durch ein TaskSpec beschrieben.
- Das Ergebnis wird als TaskResult zurückgegeben.
- Alles ist serialisierbar (für NATS / JSON).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class TaskStatus(str, Enum):
    """Mögliche Zustände einer Task."""

    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"
    RETRYING = "retrying"


@dataclass
class TaskError:
    """Standardisierte Fehlerrepräsentation einer Task."""

    type: str
    message: str
    details: dict[str, Any] | None = None
    traceback: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": self.type,
            "message": self.message,
            "details": self.details or {},
            "traceback": self.traceback,
        }

    @classmethod
    def from_exception(cls, exc: Exception) -> TaskError:
        return cls(
            type=exc.__class__.__name__,
            message=str(exc),
            details=getattr(exc, "details", None),
        )


@dataclass
class TaskSpec:
    """
    Beschreibt eine auszuführende Task.

    Attributes:
        task_id: Eindeutige ID der Task (wird meist vom Orchestrator vergeben)
        task_type: Art der Task (z.B. "web_scrape", "excel_process", "pdf_extract")
        payload: Die eigentlichen Eingabedaten (flexibel als dict)
        metadata: Zusätzliche Metadaten (z.B. priority, timeout, source_bot, etc.)
        retry_policy: Name einer Retry-Policy aus merle_core.retry (optional)
        created_at: Zeitpunkt der Erstellung
    """

    task_id: str
    task_type: str
    payload: dict[str, Any]
    metadata: dict[str, Any] = field(default_factory=dict)
    retry_policy: str | None = None
    created_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "task_type": self.task_type,
            "payload": self.payload,
            "metadata": self.metadata,
            "retry_policy": self.retry_policy,
            "created_at": self.created_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> TaskSpec:
        return cls(
            task_id=data["task_id"],
            task_type=data["task_type"],
            payload=data.get("payload", {}),
            metadata=data.get("metadata", {}),
            retry_policy=data.get("retry_policy"),
            created_at=datetime.fromisoformat(data["created_at"]) if "created_at" in data else datetime.utcnow(),
        )


@dataclass
class TaskResult:
    """
    Ergebnis einer ausgeführten Task.

    Attributes:
        task_id: ID der ursprünglichen Task
        status: Erfolgs- oder Fehlerstatus
        result: Die eigentlichen Ergebnisdaten (flexibel)
        error: Fehlerinformationen (falls status == FAILED)
        metadata: Zusätzliche Metadaten (z.B. duration, worker_id, etc.)
        completed_at: Zeitpunkt der Fertigstellung
    """

    task_id: str
    status: TaskStatus
    result: dict[str, Any] | None = None
    error: TaskError | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    completed_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "status": self.status.value,
            "result": self.result,
            "error": self.error.to_dict() if self.error else None,
            "metadata": self.metadata,
            "completed_at": self.completed_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> TaskResult:
        error = None
        if data.get("error"):
            error = TaskError(
                type=data["error"]["type"],
                message=data["error"]["message"],
                details=data["error"].get("details"),
                traceback=data["error"].get("traceback"),
            )

        return cls(
            task_id=data["task_id"],
            status=TaskStatus(data["status"]),
            result=data.get("result"),
            error=error,
            metadata=data.get("metadata", {}),
            completed_at=datetime.fromisoformat(data["completed_at"]) if "completed_at" in data else datetime.utcnow(),
        )

    @classmethod
    def success(cls, task_id: str, result: dict[str, Any], **metadata: Any) -> TaskResult:
        return cls(
            task_id=task_id,
            status=TaskStatus.SUCCESS,
            result=result,
            metadata=metadata,
        )

    @classmethod
    def failure(cls, task_id: str, error: TaskError, **metadata: Any) -> TaskResult:
        return cls(
            task_id=task_id,
            status=TaskStatus.FAILED,
            error=error,
            metadata=metadata,
        )
