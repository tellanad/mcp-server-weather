# Weather MCP Server 🌦️

A production-ready **Model Context Protocol (MCP)** server that exposes real-time weather and forecast data using **Open-Meteo APIs**, designed for LLM agents and tool-based workflows.

This server can run:
- Locally using `mcp dev` (MCP Inspector)
- Inside Docker using **HTTP transport** (cloud / agent-platform ready)

---

## Features

- MCP tools for real-world IO (weather + geocoding)
- Prevents LLM hallucinations by delegating data access to tools
- Supports HTTP transport for Docker & cloud
- Clean `src/` layout with absolute imports
- Built with `uv` for fast, reproducible environments

---

## Available MCP Tools

| Tool | Description |
|-----|------------|
| `location(query, count)` | Resolve place names to latitude/longitude |
| `current_weather(lat, lon)` | Fetch current weather conditions |
| `forecast(lat, lon, hours)` | Fetch hourly weather forecast |

---

## Project Structure
mcp-server-weather/
├─ Dockerfile
├─ docker-compose.yml
├─ pyproject.toml
├─ uv.lock
├─ README.md
└─ src/
└─ weather_mcp/
├─ server.py
├─ settings.py
├─ clients/
│ └─ openmeteo.py
└─ tools/
├─ current_weather.py
├─ forecast.py
└─ location.py



---

## Prerequisites

- Python **3.11+**
- Docker (optional)
- `uv` package manager

Install `uv`:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh

Local Development (MCP Inspector)
uv venv
source .venv/bin/activate
uv sync
PYTHONPATH=src uv run mcp dev src/weather_mcp/server.py


Open MCP Inspector

Open http://localhost:5173

Click Connect

Go to Tools → List Tools

Test:

location("San Francisco")

current_weather(lat, lon)

forecast(lat, lon, hours=24)
Docker Deployment (HTTP Transport)
Build the image
docker build -t weather-mcp .

Run the container
docker run --rm -p 8000:8000 weather-mcp


MCP endpoint:

http://localhost:8000/mcp

Configuration

Environment variables:

Variable	Default	Description
MCP_TRANSPORT	http	http (Docker) or stdio (local tools)
MCP_HOST	0.0.0.0	Bind address
MCP_PORT	8000	Server port

Example:

MCP_TRANSPORT=http MCP_PORT=8000 python -m weather_mcp.server

Design Rationale

LLMs should not fetch external data directly

MCP tools:

isolate side effects

reduce hallucinations

improve observability

lower token and latency costs

This server integrates cleanly with:

LangGraph

Claude Desktop

OpenAI Agents SDK

Enterprise agent platforms

Future Improvements

Shared httpx.AsyncClient with connection pooling

In-memory caching (lat/lon + TTL)

Payload trimming for lower token usage

Authentication & rate limiting

Kubernetes health checks