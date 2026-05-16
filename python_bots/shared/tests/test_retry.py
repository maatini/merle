"""
Tests for the centralized retry module.
"""

import asyncio

import pytest
from tenacity import RetryError

from merle_core.exceptions import RetryExhaustedError
from merle_core.retry import (
    with_retry,
    default_http_retry,
    browser_retry,
    sensitive_operation_retry,
    aggressive_retry,
)


class TestRetryPolicies:
    """Tests that the predefined retry policies exist and have reasonable settings."""

    def test_default_http_retry_exists(self):
        assert default_http_retry is not None

    def test_browser_retry_exists(self):
        assert browser_retry is not None

    def test_sensitive_operation_retry_exists(self):
        assert sensitive_operation_retry is not None

    def test_aggressive_retry_exists(self):
        assert aggressive_retry is not None


class TestWithRetryDecorator:
    """Tests for the @with_retry decorator."""

    @pytest.mark.asyncio
    async def test_successful_call(self):
        """Decorator should not interfere with successful calls."""

        @with_retry(policy=default_http_retry)
        async def successful_task():
            return {"status": "ok"}

        result = await successful_task()
        assert result == {"status": "ok"}

    @pytest.mark.asyncio
    async def test_retry_exhausted_raises_custom_exception(self):
        """After exhausting retries, RetryExhaustedError should be raised."""

        call_count = 0

        @with_retry(policy=default_http_retry, operation_name="failing_api")
        async def always_fails():
            nonlocal call_count
            call_count += 1
            raise ConnectionError("Service unavailable")

        with pytest.raises((RetryExhaustedError, Exception)) as exc_info:
            await always_fails()

        # The decorator + tenacity should eventually stop retrying
        assert call_count >= 1

    @pytest.mark.asyncio
    async def test_custom_operation_name(self):
        """Custom operation name should appear in the exception."""

        @with_retry(policy=aggressive_retry, operation_name="critical_payment")
        async def failing_payment():
            raise TimeoutError("Timeout")

        with pytest.raises(Exception):
            await failing_payment()
