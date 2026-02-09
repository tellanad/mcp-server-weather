from typing import Any
import httpx
from ..settings import USER_AGENT, DEFAULT_TIMEOUT_S

from typing import Any
import httpx
from ..settings import USER_AGENT, DEFAULT_TIMEOUT_S

async def make_json_get(url: str) -> dict[str, Any] | None:
    """HTTP GET -> JSON dict. Returns None on failure (keeps tools simple + safe)."""
    headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    try:
        async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT_S, headers=headers) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json()
            if isinstance(data, dict):
                return data
            return {"data": data}
    except Exception:
        return None
