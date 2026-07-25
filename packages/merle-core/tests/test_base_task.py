"""
Tests for BaseTask (Phase 2 core class).
"""

import pytest

from merle_core import BaseTask


class ExampleSuccessTask(BaseTask):
    async def execute(self) -> dict:
        self.logger.info("Doing real work...")
        return {"processed": 42, "status": "ok"}


class ExampleFailingTask(BaseTask):
    async def execute(self) -> dict:
        raise ValueError("Something went wrong in the task")


class TestBaseTaskLifecycle:
    """Tests the core lifecycle and hooks of BaseTask."""

    @pytest.mark.asyncio
    async def test_successful_task_lifecycle(self, fake_settings):
        task = ExampleSuccessTask(fake_settings)

        assert task.status == "pending"

        result = await task.run()

        assert task.status == "success"
        assert result == {"processed": 42, "status": "ok"}
        assert task.duration is not None
        assert task.duration > 0

    @pytest.mark.asyncio
    async def test_failing_task_calls_on_failure_hook(self, fake_settings):
        failure_called = False
        last_exception = None

        class FailingTaskWithHook(ExampleFailingTask):
            def _on_failure(self, exception: Exception):
                nonlocal failure_called, last_exception
                failure_called = True
                last_exception = exception

        task = FailingTaskWithHook(fake_settings)

        with pytest.raises(ValueError, match="Something went wrong"):
            await task.run()

        assert task.status == "failed"
        assert failure_called is True
        assert isinstance(last_exception, ValueError)

    @pytest.mark.asyncio
    async def test_get_metrics_after_success(self, fake_settings):
        task = ExampleSuccessTask(fake_settings)
        await task.run()

        metrics = task.get_metrics()

        assert metrics["task"] == "ExampleSuccessTask"
        assert metrics["status"] == "success"
        assert metrics["duration_seconds"] is not None

    @pytest.mark.asyncio
    async def test_task_name_can_be_overridden(self, fake_settings):
        task = ExampleSuccessTask(fake_settings, name="custom_invoice_fetch")
        assert task.name == "custom_invoice_fetch"
