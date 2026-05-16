"""
Mocked tests for the Playwright Robust Wrapper.

Real browser tests are expensive and environment-dependent.
These tests verify the wrapper logic using mocks.
"""

from unittest.mock import AsyncMock, patch

import pytest

from merle_core.playwright import launch_robust_browser, RobustBrowser


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
    """When an exception occurs inside the context, failure artifacts should be created."""

    with patch("merle_core.playwright.browser.async_playwright") as mock_pw:
        mock_pw.return_value.__aenter__.return_value.chromium.launch = AsyncMock(return_value=mock_browser)
        mock_browser.new_context = AsyncMock(return_value=mock_browser_context)
        mock_browser_context.new_page = AsyncMock(return_value=mock_page)

        failure_dir = tmp_path / "failures"

        with pytest.raises(ValueError):
            async with launch_robust_browser(
                headless=True,
                stealth=False,
                screenshot_on_failure=True,
                failure_dir=str(failure_dir),
            ) as browser:
                _page = await browser.new_page()
                # Simulate a real failure inside user code
                raise ValueError("Simulated bot failure")

        # Check that a failure directory was created
        assert any(failure_dir.iterdir()), "No failure artifacts were created"
