FROM python:3.11-slim

# System deps (curl for installing uv)
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install uv (fast + uses uv.lock)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app

# Copy dependency manifests first (better build cache)
COPY pyproject.toml uv.lock* /app/

# Install deps into system site-packages in the container
RUN uv sync --no-dev

# Copy your source
COPY src /app/src

# Ensure 'src' layout imports work
ENV PYTHONPATH=/app/src

EXPOSE 8000

# Run the server over HTTP
ENV MCP_TRANSPORT=http
ENV MCP_HOST=0.0.0.0
ENV MCP_PORT=8000

CMD ["python", "-m", "weather_mcp.server"]
