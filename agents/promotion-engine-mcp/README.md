# 📘 Promotion Engine MCP Server

A lightweight **Model Context Protocol (MCP)** server that exposes the Promotion Engine Azure Function App as a tool for Azure AI Foundry agents.

This component allows the agent to call your backend even when REST tools, OpenAPI tools, and A2A tools are disabled in your Foundry environment.

---

## 🧩 Why This MCP Server Exists

Your Azure AI Foundry environment only enables **MCP tools**, which means:

- Agents cannot call external REST APIs directly  
- Code Interpreter cannot access the internet  
- OpenAPI and A2A tools are disabled

Because of these restrictions, your Promotion Engine Agent cannot reach your Azure Function App on its own.

The MCP server solves this by acting as a **bridge**:

1. The agent calls the MCP tool (`getPromotions`)
2. The MCP server receives the request
3. The MCP server calls your Azure Function App
4. The promotion result is returned to the agent

This keeps your architecture clean, modular, and fully compatible with Foundry.

---

## 📂 Folder Location in the Project

Your updated project structure:

```
promotion-engine/
│
├── README.md
├── AGENTS.md
├── spec.md
├── plan.md
├── architecture/
│   ├── boundaries.md
│   ├── tradeoffs.md
│   └── data-flow.md
│
├── src/
│   ├── azure-functions/
│   │   └── get_promotions/
│   │       ├── function.json
│   │       ├── index.py
│   │       └── requirements.txt
│       └── data/
│           └── promotions.json
│
├── agents/
│   └── promotion-engine-mcp/
│       ├── mcp_server.py
│       ├── requirements.txt
│       └── README.md   ← this file
│
└── tests/
    └── test_promotions.py
```

Placing the MCP server inside `agents/` keeps your backend, agent tools, and documentation neatly organized.

---

## 🛠️ MCP Tool: `getPromotions`

### **Purpose**

Fetch the best promotion for a customer scenario using your Azure Function App.

### **Input Fields**

- `category` — string  
- `customer_segment` — string  
- `cart_value` — number  
- `season` — string  
- `language` — string

### **Output**

A JSON promotion object returned by your Function App.

---

## 🚀 Running the MCP Server Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the server:

```bash
python mcp_server.py
```

The server will expose an MCP endpoint that Azure AI Foundry can connect to.

---

## 🔗 Connecting MCP Server to Azure AI Foundry

Inside **Build an agent → Tools → Custom → Model Context Protocol (MCP)**:

1. Click **Add MCP tool**
2. Enter your MCP server endpoint URL
  Example:  
   `http://localhost:3000`
3. Select the tool: **getPromotions**
4. Save

Your agent can now call your Promotion Engine backend through MCP.

---

## 🧠 Architecture Overview

```
Azure AI Foundry Agent
        |
        |  (MCP protocol)
        v
promotion-engine-mcp server
        |
        |  (HTTP POST)
        v
Azure Function App (Promotion Engine)
```

This design is:

- modular  
- compliant  
- production‑ready  
- future‑proof for multi-agent systems

---

## 📌 Notes

- The MCP server is intentionally lightweight and easy to deploy.  
- You can run it locally or host it in Azure Container Apps.  
- It is designed to be extended with additional tools as your agent system grows.  
- Keeping it inside the main Promotion Engine repo ensures clean architecture and version control.

---

