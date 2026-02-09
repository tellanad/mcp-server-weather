from mcp.server.fastmcp import FastMCP

mcp = FastMCP("weather")

from weather_mcp.tools.current_weather import get_current_weather
from weather_mcp.tools.forecast import get_forecast
from weather_mcp.tools.location import get_location

@mcp.tool()
async def current_weather(latitude: float, longitude: float):
    """Get current weather by latitude/longitude (returns raw JSON)."""
    return await get_current_weather(latitude, longitude)

@mcp.tool()
async def forecast(latitude: float, longitude: float, hours: int = 24):
    """Get hourly forecast by latitude/longitude (returns raw JSON)."""
    return await get_forecast(latitude, longitude, hours)

@mcp.tool()
async def location(query: str, count: int = 5):
    """Get candidate locations + lat/lon from a human query (city, address, etc)."""
    return await get_location(query, count)

if __name__ == "__main__":
    transport = os.getenv("MCP_TRANSPORT", "http")   # "http" for Docker, "stdio" for Claude Desktop
    host = os.getenv("MCP_HOST", "0.0.0.0")
    port = int(os.getenv("MCP_PORT", "8000"))
    mcp.run(transport=transport, host=host, port=port)
