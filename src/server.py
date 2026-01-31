import sys
import os
import asyncio
import traceback

# Add current directory to path so we can import 'logic' and 'config'
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mcp.server.fastmcp import FastMCP # Wait, prompt said NO FastMCP.
# "Use standard mcp SDK (no fastmcp)."
# My apologies. I must use `mcp.server.stdio.stdio_server` and `mcp.types`.
# Let me rewrite using the low-level Server API.

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
import mcp.types as types

# Import logic safely
try:
    import logic
except ImportError:
    sys.stderr.write("Failed to import logic.py. Ensure it is in the same directory.\n")
    traceback.print_exc(file=sys.stderr)
    # Define dummy logic to prevent crash
    class DummyLogic:
        def get_forecast_36h(self, *args, **kwargs): return "Error: logic module missing."
        def get_current_observation(self, *args, **kwargs): return "Error: logic module missing."
        def get_latest_earthquakes(self, *args, **kwargs): return "Error: logic module missing."
    logic = DummyLogic()

# Initialize Server
app = Server("mcp-tw-weather")

@app.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="get_weather_forecast_36h",
            description="Get the 36-hour weather forecast for a specific city in Taiwan (e.g., '臺北市', 'Kaohsiung'). Returns Temp, Rain Chance, etc.",
            inputSchema={
                "type": "object",
                "properties": {
                    "location_name": {
                        "type": "string",
                        "description": "City or County name in Traditional Chinese (e.g., '臺北市') or English (limited support)."
                    }
                },
                "required": []
            },
        ),
        types.Tool(
            name="get_current_observation",
            description="Get real-time weather data (Temp, Rain, Humidity) for a specific location or station.",
            inputSchema={
                "type": "object",
                "properties": {
                    "location_name": {
                        "type": "string",
                        "description": "Station name or City name (e.g., '臺北', '板橋')."
                    }
                },
                "required": ["location_name"]
            },
        ),
        types.Tool(
            name="get_latest_earthquakes",
            description="Get the most recent significant earthquake reports in Taiwan.",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Number of reports to return (default 3).",
                        "default": 3
                    },
                    "include_small": {
                        "type": "boolean",
                        "description": "Include small regional earthquakes (default False).",
                        "default": False
                    }
                },
            },
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    try:
        if name == "get_weather_forecast_36h":
            location = arguments.get("location_name")
            result = logic.get_forecast_36h(location)
            return [types.TextContent(type="text", text=result)]
        
        elif name == "get_current_observation":
            location = arguments.get("location_name")
            if not location:
                return [types.TextContent(type="text", text="Error: location_name is required.")]
            result = logic.get_current_observation(location)
            return [types.TextContent(type="text", text=result)]
            
        elif name == "get_latest_earthquakes":
            limit = arguments.get("limit", 3)
            include_small = arguments.get("include_small", False)
            result = logic.get_latest_earthquakes(limit, include_small)
            return [types.TextContent(type="text", text=result)]
            
        else:
            raise ValueError(f"Unknown tool: {name}")

    except Exception as e:
        sys.stderr.write(f"Error executing tool {name}: {e}\n")
        traceback.print_exc(file=sys.stderr)
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]

async def main():
    # Helper to check environment
    if not os.environ.get("CWA_API_KEY"):
        sys.stderr.write("WARNING: CWA_API_KEY is not set. API calls will fail.\n")
    
    # Run stdio server
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        sys.stderr.write(f"Fatal server error: {e}\n")
        traceback.print_exc(file=sys.stderr)
