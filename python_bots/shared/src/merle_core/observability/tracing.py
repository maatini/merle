"""
OpenTelemetry Tracing Setup für Merle.

Bietet einen einfachen Weg, einen Tracer zu erhalten und Spans zu erstellen.
"""

from __future__ import annotations

from typing import Any

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

_tracer_provider: TracerProvider | None = None


def init_tracing(
    *,
    service_name: str,
    service_version: str = "0.2.0",
    otlp_endpoint: str | None = None,
    resource_attributes: dict[str, Any] | None = None,
) -> TracerProvider:
    """
    Initialisiert den globalen OpenTelemetry TracerProvider.

    Wird normalerweise über `configure_observability()` aufgerufen.
    """
    global _tracer_provider

    if _tracer_provider is not None:
        return _tracer_provider

    resource = Resource.create({
        "service.name": service_name,
        "service.version": service_version,
        **(resource_attributes or {}),
    })

    provider = TracerProvider(resource=resource)

    if otlp_endpoint:
        exporter = OTLPSpanExporter(endpoint=otlp_endpoint, insecure=True)
        processor = BatchSpanProcessor(exporter)
        provider.add_span_processor(processor)
    else:
        # Fallback: Console Exporter für lokale Entwicklung
        from opentelemetry.sdk.trace.export import ConsoleSpanExporter
        processor = BatchSpanProcessor(ConsoleSpanExporter())
        provider.add_span_processor(processor)

    trace.set_tracer_provider(provider)
    _tracer_provider = provider

    return provider


def get_tracer(name: str) -> trace.Tracer:
    """Gibt einen benannten Tracer zurück."""
    return trace.get_tracer(name)
