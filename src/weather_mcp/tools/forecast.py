from typing import Any
from ..clients.openmeteo import make_json_get
from ..settings import OPENMETEO_API_BASE
from .current_weather import _validate_lat_lon

async def get_forecast(latitude: float, longitude: float, hours: int = 24) -> dict[str, Any] | str:
    """Get hourly forecast for a location. hours is a hint; Open-Meteo returns series—LLM can slice."""
    err = _validate_lat_lon(latitude, longitude)
    if err:
        return err

    # Open-Meteo supports hourly params; we’ll fetch a useful set.
    # We include forecast_days to cap payload size (cost/latency friendly).
    forecast_days = 1
    if hours > 24:
        forecast_days = 2
    if hours > 48:
        forecast_days = 3
    if hours > 72:
        forecast_days = 7

    url = (
        f"{OPENMETEO_API_BASE}/forecast"
        f"?latitude={latitude}&longitude={longitude}"
        f"&hourly=temperature_2m,relative_humidity_2m,precipitation_probability,precipitation,"
        f"rain,showers,snowfall,cloud_cover,wind_speed_10m,wind_gusts_10m,wind_direction_10m,weather_code"
        f"&forecast_days={forecast_days}"
        f"&timezone=auto"
    )

    data = await make_json_get(url)
    return data if data else "Unable to fetch forecast data for this location."
