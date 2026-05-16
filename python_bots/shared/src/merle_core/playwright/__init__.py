"""
merle_core.playwright

Robust Playwright Wrapper für Merle RPA-Bots (Chromium + Lightpanda).

Unterstützte Engines:
- "chromium" (Default) – volle Playwright-Kompatibilität
- "lightpanda" – Zig-basierte, ressourcenschonende CDP-Alternative (via lightpanda-py)

Features:
- Engine-agnostischer Launcher (BROWSER_ENGINE=lightpanda|chromium)
- Stealth-Modus (Anti-Detection)
- Automatische Screenshots + HTML-Dumps bei Fehlern (Chromium-better)
- Proxy-Support
- Robuster CDP Readiness-Check für Lightpanda

Verwendung:
    from merle_core.playwright import launch_robust_browser

    async with launch_robust_browser(
        engine="lightpanda",          # oder "chromium"
        stealth=True,
        screenshot_on_failure=True,
    ) as browser:
        page = await browser.new_page()
        await page.goto("https://example.com")
"""

from .browser import BrowserEngine, RobustBrowser, launch_robust_browser
from .utils import robust_goto, safe_click, safe_fill

__all__ = [
    "BrowserEngine",
    "RobustBrowser",
    "launch_robust_browser",
    "robust_goto",
    "safe_click",
    "safe_fill",
]
