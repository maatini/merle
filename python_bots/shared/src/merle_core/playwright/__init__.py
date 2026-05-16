"""
merle_core.playwright

Robust Playwright Wrapper für Merle RPA-Bots.

Features:
- Stealth-Modus (Anti-Detection)
- Automatische Screenshots + HTML-Dumps bei Fehlern
- Proxy-Support
- Integrierte Retry-Policy (browser_retry)
- Bessere Fehlermeldungen (ElementNotFoundError etc.)

Verwendung:
    from merle_core.playwright import launch_robust_browser

    async with launch_robust_browser(
        headless=True,
        stealth=True,
        proxy="http://user:pass@proxy:8080",
        screenshot_on_failure=True,
    ) as browser:
        page = await browser.new_page()
        await page.goto("https://example.com")
"""

from .browser import RobustBrowser, launch_robust_browser
from .utils import robust_goto, safe_click, safe_fill

__all__ = [
    "RobustBrowser",
    "launch_robust_browser",
    "robust_goto",
    "safe_click",
    "safe_fill",
]
