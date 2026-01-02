# 📡 Campaign Protocol MCP

**Automated Advertising Intelligence for Model Context Protocol Agents.**

> *Building the bridge between "Building in Public" and "Automated Marketing".*

![Status](https://img.shields.io/badge/Status-v2.0_Beta-green) ![Python](https://img.shields.io/badge/Built_With-FastMCP-blue)

## 🎯 Mission
**Campaign Protocol** is a specialized MCP Server designed to give AI Agents "Hunter" capabilities. It allows an LLM to actively search the open web (GitHub, StackExchange) for relevant technical discussions, analyze user problems, and draft high-value strategic replies that subtly promote your solution.

It is currently being built live as part of the **CyberSecLife Origin Hunter** project.

## ⚡ Capabilities (v2.0)

### 1. The Scout (`search_for_conversations`)
* **Function:** Connects to GitHub & StackExchange APIs.
* **Action:** Finds real-time issues and questions matching your niche keywords (e.g., "MCP server error", "python automation").
* **Bypass:** Uses direct API uplinks to avoid search engine anti-bot blocking.

### 2. The Deep Scan (`read_github_issue`)
* **Function:** Retrieving full issue context.
* **Action:** Reads the body of user complaints to understand the *exact* pain point, allowing for specific, non-spammy solutions.

### 3. The Ghost Writer (`generate_strategy_reply`)
* **Function:** Context-aware copywriting.
* **Action:** Takes a user's problem and your `persona.json` settings to auto-draft a helpful, technical response that links to your product.

---

## 🛠️ Installation

### Prerequisites
* Python 3.10+
* `uv` or `pip`

### Setup
```bash
# Clone the protocol
git clone [https://github.com/YOUR_USERNAME/campaign-protocol-mcp.git](https://github.com/YOUR_USERNAME/campaign-protocol-mcp.git)
cd campaign-protocol-mcp

# Create environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install "mcp[cli]" fastmcp requests
