# Taiwan Weather & Disaster MCP Server

A Model Context Protocol (MCP) server that provides real-time weather forecasts, observations, and earthquake reports for Taiwan using the **Central Weather Administration (CWA) Open Data API**.

## 🇹🇼 Features
- **Forecast 36h**: General weather outlook for any city/county.
- **Current Observation**: Real-time temperature, rain, and humidity from weather stations.
- **Earthquakes**: Latest significant earthquake reports.

## 🔑 Prerequisites
You need a **CWA API Key** (Authorization Token).
1. Register for free at [CWA Open Data Platform](https://opendata.cwa.gov.tw/user/authkey).
2. Login and retrieve your API Key.

## 🛠 Installation

1. **Clone and Install Dependencies**:
   ```bash
   git clone https://github.com/your-username/mcp-tw-weather.git
   cd mcp-tw-weather
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

## ⚙️ Configuration

### Claude Desktop
Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "tw-weather": {
      "command": "/absolute/path/to/mcp-tw-weather/.venv/bin/python",
      "args": ["/absolute/path/to/mcp-tw-weather/src/server.py"],
      "env": {
        "CWA_API_KEY": "YOUR_CWA_API_KEY_HERE"
      }
    }
  }
}
```

### Dive
1. Go to **Settings > Modules**.
2. Click **Add Module**.
3. **Type**: `stdio`
4. **Command**: `/path/to/.venv/bin/python` (or system python if deps installed)
5. **Args**: `/path/to/src/server.py`
6. **Environment Variables**:
   - Key: `CWA_API_KEY`
   - Value: `YOUR_KEY`

## 📊 Usage Examples
- "What's the weather in Taipei?"
- "Any rain in Kaohsi tomorrow?"
- "Was there an earthquake just now?"
- "Check current temperature in Banqiao."

## 📜 License
MIT
