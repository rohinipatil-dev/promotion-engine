FROM python:3.13-slim

WORKDIR /app

# Install system deps if needed (optional)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy code
COPY . /app

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

# Environment for MCP
ENV MCP_TRANSPORT=streamable-http
ENV MCP_PORT=3000

# Expose MCP HTTP port
EXPOSE 3000

# Run MCP server
CMD ["python", "mcp_server.py"]
