"""
Loguru + OpenTelemetry Integration für Merle.

Professionelle, nicht-invasive Anreicherung von Loguru-Records mit
Trace-ID und Span-ID aus dem aktuellen OpenTelemetry Context.

Diese Implementierung verwendet `logger.patch()`, was die sicherste und
performanteste Variante ist (kein Re-Logging, keine Deadlocks).
"""

from __future__ import annotations

from loguru import logger
from opentelemetry import trace


def _inject_otel_context(record: dict) -> None:
    """Patch-Funktion: Injiziert Trace/Span IDs in jedes Log-Record."""
    span = trace.get_current_span()
    if span and span.is_recording():
        ctx = span.get_span_context()
        record["extra"]["trace_id"] = format(ctx.trace_id, "032x")
        record["extra"]["span_id"] = format(ctx.span_id, "016x")
    else:
        record["extra"].setdefault("trace_id", "")
        record["extra"].setdefault("span_id", "")


def configure_loguru_otel_sink() -> None:
    """
    Konfiguriert Loguru so, dass alle Logs automatisch mit OpenTelemetry
    Trace/Span-Kontext angereichert werden.

    Diese Methode ist idempotent und sicher (auch in Tests und bei
    mehrfachem Aufruf).
    """
    # Entferne bestehende Handler nur, wenn wir noch nicht konfiguriert haben
    # (vermeidet doppeltes Logging und Deadlocks)
    if getattr(logger, "_merle_otel_configured", False):
        return

    # Wende den Patch global an — das ist der professionelle Weg
    logger.configure(patcher=_inject_otel_context)

    # Markiere als konfiguriert (idempotent)
    logger._merle_otel_configured = True  # type: ignore[attr-defined]

    # Hinweis: Das eigentliche Format mit trace/span muss im Logger-Handler
    # oder in der Anwendung selbst gesetzt werden, z.B.:
    # logger.add(sys.stderr, format="{time} | {level} | trace={extra[trace_id]} ...")
    #
    # Für die meisten Merle-Bots reicht der Patch + ein gutes Format in main.py.
