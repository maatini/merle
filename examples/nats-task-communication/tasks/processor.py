"""
Consumer-side helpers: turn a TaskSpec into a TaskResult (pure, no NATS I/O).
"""

from __future__ import annotations

from typing import Any

from merle_core import TaskResult, TaskSpec


def handle_scrape_spec(spec: TaskSpec) -> TaskResult:
    """
    Simulate processing of a web_scrape TaskSpec.

    Pure function — unit-testable without a NATS server.
    """
    url = spec.payload.get("url", "")
    selectors = spec.payload.get("selectors") or []
    records = max(1, len(selectors)) * 6  # deterministic mock metric

    return TaskResult.success(
        task_id=spec.task_id,
        result={
            "processed": True,
            "records": records,
            "url": url,
            "selectors": selectors,
        },
        processor="data-processor-bot",
    )


def build_success_result(
    task_id: str,
    *,
    records: int = 12,
    extra: dict[str, Any] | None = None,
) -> TaskResult:
    """Convenience constructor used by live NATS reply path."""
    result: dict[str, Any] = {"processed": True, "records": records}
    if extra:
        result.update(extra)
    return TaskResult.success(
        task_id=task_id,
        result=result,
        processor="data-processor-bot",
    )
