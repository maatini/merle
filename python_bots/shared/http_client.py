"""
Vorkonfigurierter HTTP-Client für RPA-Bots.

Nutzt httpx mit:
- Timeout-Konfiguration
- Retry-Mechanismen (tenacity)
- Standard-Headers
- Authentifizierung
"""

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type


class RpaHttpClient:
    """HTTP-Client mit RPA-spezifischen Defaults."""

    def __init__(self, base_url: str, api_key: str = "", timeout: float = 30.0):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout

    def _headers(self) -> dict[str, str]:
        headers = {
            "User-Agent": "RPA-Hybrid-Bot/1.0",
            "Accept": "application/json",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((httpx.HTTPStatusError, httpx.RequestError)),
    )
    async def get(self, path: str) -> dict:
        """GET-Request mit Retry."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                f"{self.base_url}{path}",
                headers=self._headers(),
            )
            response.raise_for_status()
            return response.json()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((httpx.HTTPStatusError, httpx.RequestError)),
    )
    async def post(self, path: str, data: dict) -> dict:
        """POST-Request mit Retry."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}{path}",
                headers=self._headers(),
                json=data,
            )
            response.raise_for_status()
            return response.json()
