"""
Mocked tests for the observability module.
"""

from merle_core.observability import configure_observability, get_meter, get_tracer


def test_configure_observability_does_not_crash_without_otlp():
    """Should work even without a real OTEL collector (falls back to console)."""
    configure_observability(
        service_name="test-bot",
        enable_tracing=True,
        enable_metrics=True,
    )


def test_get_tracer_returns_tracer():
    tracer = get_tracer("test.module")
    assert tracer is not None


def test_get_meter_returns_meter():
    meter = get_meter("test.module")
    assert meter is not None


def test_configure_observability_does_not_crash_and_enables_tracing():
    """Integration-style test: configure_observability should work without crashing
    and make get_tracer / get_meter return valid objects."""
    # Reset global state
    import merle_core.observability.metrics as metrics_mod
    import merle_core.observability.tracing as tracing_mod

    tracing_mod._tracer_provider = None  # type: ignore[attr-defined]
    metrics_mod._meter_provider = None  # type: ignore[attr-defined]

    # Should not raise
    configure_observability(
        service_name="test-bot",
        service_version="0.2.0",
        enable_tracing=True,
        enable_metrics=True,
    )

    tracer = get_tracer("test.module")
    meter = get_meter("test.module")

    assert tracer is not None
    assert meter is not None
