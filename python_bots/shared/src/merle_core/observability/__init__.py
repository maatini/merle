"""
merle_core.observability

OpenTelemetry-basiertes Observability-Modul für Merle-Bots.

Ermöglicht einheitliches Tracing, Metrics und strukturierte Logs mit Trace-Kontext.

Verwendung:
    from merle_core.observability import configure_observability, get_tracer, get_meter

    configure_observability(
        service_name="invoice_processor",
        otlp_endpoint="http://otel-collector:4317",
    )

    tracer = get_tracer(__name__)
    meter = get_meter(__name__)
"""

from __future__ import annotations

from typing import Any

from .tracing import get_tracer, init_tracing
from .metrics import get_meter, init_metrics
from .logging import configure_loguru_otel_sink

__all__ = [
    "configure_observability",
    "get_tracer",
    "get_meter",
    "configure_loguru_otel_sink",
]


def configure_observability(
    *,
    service_name: str,
    service_version: str = "0.2.0",
    otlp_endpoint: str | None = None,
    enable_tracing: bool = True,
    enable_metrics: bool = True,
    resource_attributes: dict[str, Any] | None = None,
) -> None:
    """
    Einmalige Initialisierung von Observability für den gesamten Bot.

    Diese Funktion sollte **einmal** am Anfang von `main.py` aufgerufen werden,
    bevor andere Komponenten initialisiert werden.

    Args:
        service_name: Name des Bots (z.B. "invoice_processor")
        service_version: Version des Bots
        otlp_endpoint: OTLP gRPC Endpoint (z.B. "http://localhost:4317")
        enable_tracing: Distributed Tracing aktivieren
        enable_metrics: Metrics aktivieren
        resource_attributes: Zusätzliche Resource-Attribute (env, team, etc.)
    """
    attributes = {
        "service.name": service_name,
        "service.version": service_version,
        "service.namespace": "merle",
        **(resource_attributes or {}),
    }

    if enable_tracing:
        init_tracing(
            service_name=service_name,
            service_version=service_version,
            otlp_endpoint=otlp_endpoint,
            resource_attributes=attributes,
        )

    if enable_metrics:
        init_metrics(
            service_name=service_name,
            otlp_endpoint=otlp_endpoint,
            resource_attributes=attributes,
        )

    # Loguru mit Trace-Kontext anreichern (sehr nützlich)
    configure_loguru_otel_sink()

    from loguru import logger

    logger.info(
        "Observability initialized for service={}",
        service_name,
        extra={"service": service_name, "version": service_version},
    )
