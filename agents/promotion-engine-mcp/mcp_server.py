import asyncio
import requests
from mcp.server import Server
from mcp.types import (
    Tool,
    ToolInputSchema,
    ToolOutput,
    TextContent
)

# Azure Function App endpoint
PROMOTION_ENGINE_URL = "https://promotion-engine-tool-func.uaenorth.azurewebsites.net/api/get-promotions"

# Create MCP server
server = Server("promotion-engine-mcp")

# Define MCP tool schema
get_promotions_tool = Tool(
    name="getPromotions",
    description="Fetch the best promotion for a customer scenario.",
    input_schema=ToolInputSchema(
        type="object",
        properties={
            "category": {"type": "string"},
            "customer_segment": {"type": "string"},
            "cart_value": {"type": "number"},
            "season": {"type": "string"},
            "language": {"type": "string"}
        },
        required=["category", "customer_segment", "cart_value", "season", "language"]
    )
)

@server.tool(get_promotions_tool)
async def get_promotions_handler(params):
    """Call the Azure Function App with the provided parameters."""
    try:
        response = requests.post(PROMOTION_ENGINE_URL, json=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        return ToolOutput(
            content=[TextContent(type="text", text=str(data))]
        )

    except Exception as e:
        return ToolOutput(
            content=[TextContent(type="text", text=f"Error calling Promotion Engine: {e}")]
        )

async def main():
    await server.run()

if __name__ == "__main__":
    asyncio.run(main())
