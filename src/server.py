"""
Taiwan Weather MCP Server using FastMCP.
Supports both STDIO and Streamable HTTP transport modes.
"""
import sys
import os
import argparse

# Add current directory to path so we can import 'logic' and 'config'
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastmcp import FastMCP
import logic

# Initialize FastMCP
mcp = FastMCP("mcp-tw-weather")

@mcp.tool()
async def get_weather_forecast_36h(location_name: str = "臺北市") -> str:
    """
    Get the 36-hour weather forecast for a specific city in Taiwan.
    Args:
        location_name: City or County name in Traditional Chinese (e.g., '臺北市', '高雄市').
    """
    return logic.get_forecast_36h(location_name)

@mcp.tool()
async def get_current_observation(location_name: str) -> str:
    """
    Get real-time weather data (Temp, Rain, Humidity) for a specific location or station.
    Args:
        location_name: Station name or City name (e.g., '臺北', '板橋').
    """
    return logic.get_current_observation(location_name)

@mcp.tool()
async def get_latest_earthquakes(limit: int = 3, include_small: bool = False) -> str:
    """
    Get the most recent significant earthquake reports in Taiwan.
    Args:
        limit: Number of reports to return (default 3).
        include_small: Include small regional earthquakes (default False).
    """
    return logic.get_latest_earthquakes(limit, include_small)

def main():
    parser = argparse.ArgumentParser(description="Taiwan Weather MCP Server")
    parser.add_argument("--mode", choices=["stdio", "http"], default="stdio", help="Transport mode")
    parser.add_argument("--port", type=int, default=8000, help="HTTP port (only for http mode)")
    args = parser.parse_args()

    if not os.environ.get("CWA_API_KEY"):
        print("WARNING: CWA_API_KEY is not set. API calls will fail.", file=sys.stderr)

    if args.mode == "stdio":
        mcp.run()
    else:
        print(f"Starting FastMCP in streamable-http mode on port {args.port}...", file=sys.stderr)
        mcp.run(
            transport="streamable-http",
            host="0.0.0.0",
            port=args.port,
            path="/mcp"
        )

if __name__ == "__main__":
    main()
