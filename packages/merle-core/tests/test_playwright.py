"""
Mocked tests for the Playwright Robust Wrapper (Chromium + Lightpanda).

Real browser tests are expensive and environment-dependent.
These tests verify the wrapper logic using mocks for both engines.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from merle_core.exceptions import BrowserLaunchError
from merle_core.playwright import BrowserEngine, RobustBrowser, launch_robust_browser
from merle_core.playwright.browser import _wait_for_lightpanda_ready


def test_browser_engine_type():
    """BrowserEngine should only accept valid literal values."""
    assert "chromium" in BrowserEngine.__args__
    assert "lightpanda" in BrowserEngine.__args__
    # Static type checkers will catch invalid values at development time


# ─────────────────────────────────────────────────────────────
# Direct RobustBrowser Unit Tests (for high code coverage)
# ─────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_robust_browser_captures_failure_artifacts_success(
    mock_browser, mock_browser_context, mock_page, tmp_path
):
    """Test that _capture_failure_artifacts works when screenshot_on_failure=True."""
    failure_dir = tmp_path / "failures"

    browser = RobustBrowser(
        mock_browser,
        mock_browser_context,
        screenshot_on_failure=True,
        failure_dir=str(failure_dir),
    )
    browser._pages = [mock_page]

    # Simulate exception during usage
    exc = RuntimeError("Simulated bot crash")
    await browser._capture_failure_artifacts(exc)

    # Should have created failure directory with artifacts
    assert failure_dir.exists()
    assert any(failure_dir.iterdir()), "No failure artifacts were created"
    mock_page.screenshot.assert_called()
    mock_page.content.assert_called()


@pytest.mark.asyncio
async def test_lightpanda_with_proxy_parameter(mock_browser, mock_browser_context, fake_lightpanda_proc):
    """Ensure proxy is correctly passed to new_context when using Lightpanda."""
    fake_lightpanda_module = MagicMock()
    fake_lightpanda_module.serve.return_value = fake_lightpanda_proc

    with (
        patch.dict("sys.modules", {"lightpanda": fake_lightpanda_module}),
        patch("merle_core.playwright.browser.async_playwright") as mock_pw,
        patch("merle_core.playwright.browser._wait_for_lightpanda_ready", new=AsyncMock()),
    ):
        mock_pw.return_value.__aenter__.return_value.chromium.connect_over_cdp = AsyncMock(return_value=mock_browser)

        async with launch_robust_browser(engine="lightpanda", proxy="http://user:pass@proxy:8080") as browser:
            assert isinstance(browser, RobustBrowser)

        # Verify that new_context was called with proxy in context_options
        call_kwargs = mock_browser.new_context.call_args[1]
        assert "proxy" in call_kwargs
        assert call_kwargs["proxy"]["server"] == "http://user:pass@proxy:8080"


@pytest.mark.asyncio
async def test_launch_robust_browser_yields_robust_browser(mock_browser, mock_browser_context):
    """Verify that the context manager returns a RobustBrowser instance."""

    with patch("merle_core.playwright.browser.async_playwright") as mock_pw:
        mock_pw.return_value.__aenter__.return_value.chromium.launch = AsyncMock(return_value=mock_browser)
        mock_browser.new_context = AsyncMock(return_value=mock_browser_context)

        async with launch_robust_browser(headless=True, stealth=False) as browser:
            assert isinstance(browser, RobustBrowser)
            _page = await browser.new_page()
            assert _page is not None


@pytest.mark.asyncio
async def test_robust_browser_captures_failure_artifacts_on_exception(
    mock_browser, mock_browser_context, mock_page, tmp_path
):
    """RobustBrowser.__aexit__ captures artifacts when an exception escapes the CM."""
    failure_dir = tmp_path / "failures"
    browser = RobustBrowser(
        mock_browser,
        mock_browser_context,
        screenshot_on_failure=True,
        failure_dir=str(failure_dir),
    )
    browser._pages = [mock_page]

    with pytest.raises(ValueError, match="Simulated bot failure"):
        async with browser:
            raise ValueError("Simulated bot failure")

    assert any(failure_dir.iterdir()), "No failure artifacts were created"
    mock_page.screenshot.assert_called()
    mock_page.content.assert_called()


# ─────────────────────────────────────────────────────────────
# Lightpanda Engine Tests
# ─────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_launch_robust_browser_lightpanda_path(mock_browser, mock_browser_context, fake_lightpanda_proc):
    """Verify that engine='lightpanda' uses connect_over_cdp and manages the process."""
    fake_lightpanda_module = MagicMock()
    fake_lightpanda_module.serve.return_value = fake_lightpanda_proc

    with (
        patch.dict("sys.modules", {"lightpanda": fake_lightpanda_module}),
        patch("merle_core.playwright.browser.async_playwright") as mock_pw,
        patch("merle_core.playwright.browser._wait_for_lightpanda_ready", new=AsyncMock()),
    ):
        mock_pw.return_value.__aenter__.return_value.chromium.connect_over_cdp = AsyncMock(return_value=mock_browser)

        async with launch_robust_browser(engine="lightpanda") as browser:
            assert isinstance(browser, RobustBrowser)
            _page = await browser.new_page()
            assert _page is not None

        assert fake_lightpanda_proc.terminate_called or fake_lightpanda_proc.kill_called


@pytest.mark.asyncio
async def test_lightpanda_process_cleanup_on_exception(mock_browser, mock_browser_context, fake_lightpanda_proc):
    """Lightpanda process must be killed if an exception occurs inside the context."""
    fake_lightpanda_module = MagicMock()
    fake_lightpanda_module.serve.return_value = fake_lightpanda_proc

    with (
        patch.dict("sys.modules", {"lightpanda": fake_lightpanda_module}),
        patch("merle_core.playwright.browser.async_playwright") as mock_pw,
        patch("merle_core.playwright.browser._wait_for_lightpanda_ready", new=AsyncMock()),
    ):
        mock_pw.return_value.__aenter__.return_value.chromium.connect_over_cdp = AsyncMock(return_value=mock_browser)

        async def _use_browser() -> None:
            async with launch_robust_browser(engine="lightpanda") as browser:
                await browser.new_page()
                raise RuntimeError("Simulated failure in bot logic")

        with pytest.raises(BrowserLaunchError):
            await _use_browser()

        # Process must have been killed during exception handling
        assert fake_lightpanda_proc.kill_called or fake_lightpanda_proc.terminate_called


@pytest.mark.asyncio
async def test_missing_lightpanda_py_raises_clear_error():
    """If lightpanda-py is not installed, a clear error must be raised."""
    with (
        patch("merle_core.playwright.browser.async_playwright") as mock_pw,
        patch("builtins.__import__", side_effect=ImportError("No module named 'lightpanda'")),
    ):
        mock_pw.return_value.__aenter__.return_value.chromium.connect_over_cdp = AsyncMock()

        with pytest.raises(BrowserLaunchError, match="lightpanda-py ist nicht installiert"):
            async with launch_robust_browser(engine="lightpanda"):
                pass


# ─────────────────────────────────────────────────────────────
# Readiness Helper Tests
# ─────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_wait_for_lightpanda_ready_success():
    """_wait_for_lightpanda_ready should return when /json/version responds with 200."""
    mock_response = MagicMock()
    mock_response.status_code = 200

    with patch("httpx.AsyncClient.get", AsyncMock(return_value=mock_response)):
        await _wait_for_lightpanda_ready("127.0.0.1", 9222, timeout=1.0)


@pytest.mark.asyncio
async def test_wait_for_lightpanda_ready_timeout():
    """Should raise BrowserLaunchError after timeout if server never responds."""
    with patch("httpx.AsyncClient.get", AsyncMock(side_effect=Exception("connection refused"))):
        with pytest.raises(BrowserLaunchError, match="nicht bereit nach"):
            await _wait_for_lightpanda_ready("127.0.0.1", 9222, timeout=0.3, poll_interval=0.1)
