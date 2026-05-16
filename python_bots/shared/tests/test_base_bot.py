"""
Tests for BaseBot (enhanced in Phase 2).
"""

import pytest

from merle_core import BaseBot


class ExampleBot(BaseBot):
    async def execute(self) -> dict:
        return {"status": "completed", "items": 123}


class FailingBot(BaseBot):
    async def execute(self) -> dict:
        raise RuntimeError("Bot exploded")


class TestBaseBotLifecycle:
    @pytest.mark.asyncio
    async def test_successful_bot_run(self, fake_settings):
        bot = ExampleBot(fake_settings)

        result = await bot.run()

        assert bot.status == "success"
        assert result["items"] == 123
        assert bot.duration is not None

    @pytest.mark.asyncio
    async def test_failing_bot_updates_status_and_calls_hook(self, fake_settings):
        failure_hook_called = False

        class BotWithHook(FailingBot):
            def _on_failure(self, exception: Exception):
                nonlocal failure_hook_called
                failure_hook_called = True

        bot = BotWithHook(fake_settings)

        with pytest.raises(RuntimeError):
            await bot.run()

        assert bot.status == "failed"
        assert failure_hook_called is True

    @pytest.mark.asyncio
    async def test_health_check_reflects_status(self, fake_settings):
        bot = ExampleBot(fake_settings)
        await bot.run()

        health = bot.health_check()

        assert health["bot"] == "test_invoice_bot"
        assert health["last_run_status"] == "success"
        assert health["last_run_duration"] is not None

    def test_initial_status_is_pending(self, fake_settings):
        bot = ExampleBot(fake_settings)
        assert bot.status == "pending"
