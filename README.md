# QLUX OMNI - Autonomous AI Agent Settlement Mesh & MCP Hub

> World's first high-yield, HTTP 402 micro-settlement and autonomous multi-service mesh for AI agents, powered by HandCash and BSV.

## 🚀 Overview
QLUX OMNI is a decentralized micro-payment and service mesh designed exclusively for AI agents, LLMs (such as Claude and GPT-based bots), and automated programs. It integrates instant **HTTP 402 Payment Required** protocols with real-time HandCash BSV settlements.

* **Live Endpoint**: Hosted on Render (Dynamic Mesh Hub)
* **Settlement Currency**: BSV (Bitcoin Satoshi Vision) via HandCash API
* **Supported Protocols**: OpenAPI 3.0, Model Context Protocol (MCP), HTTP 402

---

## 🛠️ Available Services & Pricing (High-Yield Tier)

| Service Type | Endpoint / Method | Description | Micro-Fee (USD) |
| :--- | :--- | :--- | :--- |
| **Data Query** | `POST /api/v1/omni/execute` | Real-time global matrix index & verified data feed | `$0.020 - $0.060` |
| **AI Prompt Processing** | `POST /api/v1/omni/execute` | Autonomous mesh inference & optimization | `$0.050 - $0.150` |
| **High-Speed Storage** | `POST /api/v1/omni/execute` | Decentralized high-speed vault record commit | `$0.015 - $0.045` |
| **Auction Settlement** | `POST /api/v1/omni/execute` | Cross-node resource bidding & settlement | `$0.040 - $0.120` |

---

## 🔌 Integration for AI Agents & Developers

### 1. OpenAPI Specification
AI agents can automatically parse the API schema at:
`https://<your-render-url>/openapi.json`

### 2. Model Context Protocol (MCP) Manifest
Claude and compatible MCP clients can connect using the manifest at:
`https://<your-render-url>/mcp/tools`

### 3. Execution Example (Python / Curl)
```bash
curl -X POST "https://<your-render-url>/api/v1/omni/execute" \
  -H "Content-Type: application/json" \
  -H "X-Payment-Token: ai_agent_alpha_premium" \
  -d '{
    "service_type": "ai_prompt",
    "payload": {
      "prompt": "Optimize cross-border AI routing and liquidity"
    }
  }'

