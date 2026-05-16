"""
Mocked tests for the observability module.
"""

from unittest.mock import patch


from merle_core.observability import configure_observability, get_tracer, get_meter


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


@patch("merle_core.observability.tracing.init_tracing")
def test_configure_calls_init_tracing(mock_init):
    configure_observability(service_name="test-bot", enable_tracing=True)
    mock_init.assert_called()
