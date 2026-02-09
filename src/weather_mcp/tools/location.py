from typing import Any
from ..clients.openmeteo import make_json_get
from ..settings import OPENMETEO_GEOCODE_BASE

async def get_location(query: str, count: int = 5) -> dict[str, Any] | str:
    """Geocode a location name -> candidate lat/lon results (raw Open-Meteo JSON)."""
    q = (query or "").strip()
    if not q:
        return "query must be a non-empty string"
    if count < 1 or count > 20:
        return "count must be between 1 and 20"

    url = f"{OPENMETEO_GEOCODE_BASE}/search?name={httpx_quote(q)}&count={count}&language=en&format=json"
    data = await make_json_get(url)
    return data if data else "Unable to fetch geocoding results for this query."

def httpx_quote(s: str) -> str:
    # minimal URL encoding without importing urllib (keeps dependencies minimal)
    return (
        s.replace("%", "%25")
         .replace(" ", "%20")
         .replace("#", "%23")
         .replace("&", "%26")
         .replace("?", "%3F")
         .replace("/", "%2F")
    )
