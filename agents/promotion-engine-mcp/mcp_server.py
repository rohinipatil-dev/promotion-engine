import os
import requests
from mcp.server.fastmcp import FastMCP

FUNCTION_KEY = os.getenv("PROMOTION_ENGINE_FUNC_APP_KEY")
PROMOTION_ENGINE_URL = (
    "https://promotion-engine-tool-func-ftc2d8buckf4dud8.uaenorth-01.azurewebsites.net/api/get-promotions"
    f"?code={FUNCTION_KEY}"
)


mcp = FastMCP(
    "promotion-engine-mcp",
    host="0.0.0.0",
    port=int(os.getenv("MCP_PORT", "3000")),
)


@mcp.tool(
    name="getPromotions",
    description="Fetch the best promotion for a customer scenario.",
)
def get_promotions(
    category: str,
    customer_segment: str,
    cart_value: float,
    season: str,
    language: str,
) -> str:
    """Call the Azure Function App with the provided parameters."""
    params = {
        "category": category,
        "customer_segment": customer_segment,
        "cart_value": cart_value,
        "season": season,
        "language": language,
    }

    try:
        response = requests.post(PROMOTION_ENGINE_URL, json=params, timeout=10)
        response.raise_for_status()
        return str(response.json())
    except Exception as e:
        return f"Error calling Promotion Engine: {e}"


if __name__ == "__main__":
    transport = os.getenv("MCP_TRANSPORT", "streamable-http")
    host = mcp.settings.host
    port = mcp.settings.port

    if transport == "stdio":
        print(
            "Starting MCP server on stdio.\n"
            "This mode is for MCP clients (Cursor, Claude Desktop, etc.) that launch the process.\n"
            "Do not run it interactively in a terminal — pressing Enter will cause JSON errors.\n"
            "For local HTTP testing or Azure AI Foundry, use: MCP_TRANSPORT=streamable-http python mcp_server.py"
        )
    elif transport == "streamable-http":
        print(f"Starting MCP server at http://{host}:{port}/mcp")
    elif transport == "sse":
        print(f"Starting MCP server at http://{host}:{port}/sse")

    try:
        mcp.run(transport=transport)
    except OSError as exc:
        if getattr(exc, "winerror", None) == 10048 or exc.errno in {48, 98, 10048}:
            print(
                f"\nPort {port} is already in use on {host}.\n"
                "Stop the other MCP server instance, or start on a different port:\n"
                f"  $env:MCP_PORT=\"3001\"; python .\\mcp_server.py"
            )
        raise
