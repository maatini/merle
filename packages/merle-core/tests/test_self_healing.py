"""
Advanced Self-Healing Pattern Tests (Phase 2).

Demonstrates how BaseTask + retry can be combined for resilient behavior.
"""

import pytest
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_none

from merle_core import BaseTask
from merle_core.exceptions import RetryExhaustedError
from merle_core.retry import with_retry

# Deterministic, no-wait policy so recovery tests are fast and non-flaky.
fast_connection_retry = retry(
    stop=stop_after_attempt(5),
    wait=wait_none(),
    retry=retry_if_exception_type((ConnectionError, TimeoutError)),
    reraise=True,
)


class UnstableExternalServiceTask(BaseTask):
    """
    Simuliert einen instabilen externen Service.
    Nach 2 Fehlversuchen wird der Aufruf erfolgreich.
    """

    def __init__(self, settings, max_failures: int = 2):
        super().__init__(settings, name="UnstableExternalServiceTask")
        self.attempt = 0
        self.max_failures = max_failures

    @with_retry(policy=fast_connection_retry)
    async def execute(self) -> dict:
        self.attempt += 1
        if self.attempt <= self.max_failures:
            self.logger.warning("External service failed (attempt {})", self.attempt)
            raise ConnectionError("Temporary network issue")
        return {"status": "recovered", "attempts": self.attempt}


class TestSelfHealingPatterns:
    """Tests that show realistic Self-Healing behavior using our framework."""

    @pytest.mark.asyncio
    async def test_task_recovers_after_temporary_failures(self, fake_settings):
        task = UnstableExternalServiceTask(fake_settings, max_failures=2)

        result = await task.run()

        assert result["status"] == "recovered"
        assert result["attempts"] == 3
        assert task.status == "success"
        assert task.attempt == 3

    @pytest.mark.asyncio
    async def test_on_failure_hook_can_trigger_fallback(self, fake_settings):
        """
        Zeigt ein klassisches Self-Healing Pattern:
        Bei endgültigem Fehler wird ein Fallback-Mechanismus getriggert.
        """
        fallback_executed = False

        class TaskWithFallback(UnstableExternalServiceTask):
            def __init__(self, settings):
                super().__init__(settings, max_failures=10)  # Immer fehlschlagen

            def _on_failure(self, exception: Exception):
                nonlocal fallback_executed
                fallback_executed = True
                self.logger.info("Fallback-Mechanismus aktiviert")

        task = TaskWithFallback(fake_settings)

        with pytest.raises(RetryExhaustedError):
            await task.run()

        assert fallback_executed is True
        assert task.status == "failed"
