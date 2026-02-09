from typing import Any
from weather_mcp.clients.openmeteo import make_json_get
from weather_mcp.settings import OPENMETEO_API_BASE


def _validate_lat_lon(latitude: float, longitude: float) -> str | None:
    if not (-90.0 <= latitude <= 90.0):
        return "latitude must be between -90 and 90"
    if not (-180.0 <= longitude <= 180.0):
        return "longitude must be between -180 and 180"
    return None

async def get_current_weather(latitude: float, longitude: float) -> dict[str, Any] | str:
    """Get current weather for a location (raw Open-Meteo JSON)."""
    err = _validate_lat_lon(latitude, longitude)
    if err:
        return err

    url = (
        f"{OPENMETEO_API_BASE}/forecast"
        f"?latitude={latitude}&longitude={longitude}"
        f"&current=temperature_2m,is_day,showers,cloud_cover,wind_speed_10m,wind_direction_10m,"
        f"pressure_msl,snowfall,precipitation,relative_humidity_2m,apparent_temperature,rain,"
        f"weather_code,surface_pressure,wind_gusts_10m"
    )

    data = await make_json_get(url)
    if data is None:
        return "Failed to fetch weather data from Open-Meteo"
    return data
