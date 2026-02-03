# ☀️ 台灣天氣助手 (mcp-tw-weather)

這是一個基於 **FastMCP** 框架開發的 Model Context Protocol (MCP) 伺服器，支援查詢台灣即時天氣、預報以及地震資訊。

## ✨ 特點
- **雙傳輸模式**：同時支援 `stdio` (本機) 與 `streamable-http` (遠端/Docker) 模式。
- **即時預報**：提供 36 小時天氣預報與降雨機率。
- **地震警報**：同步 CWA 獲取最新顯著有感地震報告。

---

## 🚀 傳輸模式 (Transport Modes)

### 1. 本機模式 (STDIO) - 預設
適合與 Claude Desktop 搭配使用。
```bash
python src/server.py --mode stdio
```

### 2. 遠端模式 (HTTP)
適合 Docker 部署與遠端存取。
```bash
python src/server.py --mode http --port 8000
```
- **服務 URL**: `http://localhost:8000/mcp`

---

## 🛠️ 配置

需要中央氣象署 (CWA) API Key。
```env
CWA_API_KEY=your_api_key_here
```

---

## 🔌 客戶端配置範例

### Claude Desktop (STDIO)
```json
{
  "mcpServers": {
    "tw-weather": {
      "command": "python",
      "args": ["/絕對路徑/src/server.py", "--mode", "stdio"],
      "env": {
        "CWA_API_KEY": "YOUR_KEY"
      }
    }
  }
}
```

### Dive / HTTP 客戶端
- **Type**: `streamable`
- **URL**: `http://localhost:8000/mcp`
