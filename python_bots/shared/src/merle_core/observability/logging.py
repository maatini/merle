"""
Loguru Integration mit OpenTelemetry.

Fügt automatisch Trace-ID und Span-ID zu allen Loguru-Logs hinzu,
wenn ein aktiver Span vorhanden ist.
"""

from __future__ import annotations

from loguru import logger
from opentelemetry import trace


def _otel_sink(message: str) -> None:
    """
    Custom Loguru Sink, der Trace-Kontext injiziert.
    """
    record = message.record

    span = trace.get_current_span()
    if span and span.is_recording():
        ctx = span.get_span_context()
        record["extra"]["trace_id"] = format(ctx.trace_id, "032x")
        record["extra"]["span_id"] = format(ctx.span_id, "016x")
    else:
        record["extra"].setdefault("trace_id", "")
        record["extra"].setdefault("span_id", "")

    # Standard-Format mit Trace-Kontext
    logger.opt(depth=6).log(
        record["level"].name,
        "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | "
        "trace={extra[trace_id]} span={extra[span_id]} | "
        "{name}:{function}:{line} - {message}",
        **record,
    )


def configure_loguru_otel_sink() -> None:
    """
    Aktiviert den OTEL-fähigen Loguru-Sink.

    Entfernt vorherige Handler und ersetzt sie durch einen, der
    Trace-Kontext automatisch mitloggt.
    """
    logger.remove()

    logger.add(
        _otel_sink,
        level="INFO",
        serialize=False,
        backtrace=True,
        diagnose=False,
    )

    # Optional: separater JSON-Handler für Produktion (kann später erweitert werden)
    logger.add(
        "logs/bot_{time:YYYY-MM-DD}.json",
        level="INFO",
        format="{time} {level} {message} {extra}",
        serialize=True,
        rotation="10 MB",
        retention="30 days",
    )
