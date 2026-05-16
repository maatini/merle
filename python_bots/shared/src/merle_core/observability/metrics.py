"""
OpenTelemetry Metrics für Merle-Bots.

Stellt gängige Metriken (Counter, Histogram) für Bots und Tasks bereit.
"""

from __future__ import annotations

from typing import Any

from opentelemetry import metrics
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter

_meter_provider: MeterProvider | None = None


def init_metrics(
    *,
    service_name: str,
    otlp_endpoint: str | None = None,
    resource_attributes: dict[str, Any] | None = None,
) -> MeterProvider:
    """
    Initialisiert den globalen MeterProvider.
    """
    global _meter_provider

    if _meter_provider is not None:
        return _meter_provider

    resource = Resource.create({
        "service.name": service_name,
        **(resource_attributes or {}),
    })

    readers = []

    if otlp_endpoint:
        exporter = OTLPMetricExporter(endpoint=otlp_endpoint, insecure=True)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=15000)
        readers.append(reader)
    else:
        # Für lokale Entwicklung: Console
        from opentelemetry.sdk.metrics.export import ConsoleMetricExporter
        reader = PeriodicExportingMetricReader(ConsoleMetricExporter(), export_interval_millis=30000)
        readers.append(reader)

    provider = MeterProvider(resource=resource, metric_readers=readers)
    metrics.set_meter_provider(provider)
    _meter_provider = provider

    return provider


def get_meter(name: str) -> metrics.Meter:
    """Gibt einen benannten Meter zurück."""
    return metrics.get_meter(name)


# ─────────────────────────────────────────────────────────────
# Praktische Helper für typische Merle-Metriken
# ─────────────────────────────────────────────────────────────

def create_bot_metrics(meter: metrics.Meter) -> dict[str, Any]:
    """
    Erzeugt die Standard-Metriken, die die meisten Merle-Bots brauchen.
    """
    return {
        "bot_executions_total": meter.create_counter(
            name="bot_executions_total",
            description="Anzahl der Bot-Ausführungen",
            unit="1",
        ),
        "bot_duration_seconds": meter.create_histogram(
            name="bot_duration_seconds",
            description="Ausführungsdauer eines Bots",
            unit="s",
        ),
        "task_executions_total": meter.create_counter(
            name="task_executions_total",
            description="Anzahl der Task-Ausführungen",
            unit="1",
        ),
        "task_duration_seconds": meter.create_histogram(
            name="task_duration_seconds",
            description="Ausführungsdauer eines Tasks",
            unit="s",
        ),
        "errors_total": meter.create_counter(
            name="errors_total",
            description="Anzahl aufgetretener Fehler",
            unit="1",
        ),
    }
