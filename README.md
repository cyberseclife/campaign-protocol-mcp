## 🛠️ Installation & Setup

Follow this 3-step launch sequence to get your AI Hunter online.

### 1. Environment Setup
Clone the repo and install the core protocol handlers.

```bash
# Clone the protocol
git clone [https://github.com/cyberseclife/campaign-protocol-mcp.git](https://github.com/cyberseclife/campaign-protocol-mcp.git)
cd campaign-protocol-mcp

# Create and activate environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install "mcp[cli]" fastmcp requests
```

### 2. Configure your Persona
Open `persona.json` and define your brand. This is the **Identity** your AI agent will use when drafting replies and social posts.

### 3. Activate the Agent (The Most Important Step)
To let your AI Agent (Gemini, Claude, etc.) use these tools, you must link this server to your agent's configuration file.

#### **For Gemini CLI users:**
Edit `~/.gemini/settings.json` and add:

```json
"cyberseclife-dev": {
  "command": "python3",
  "args": ["/absolute/path/to/campaign-protocol-mcp/server.py"],
  "env": { "PYTHONPATH": "/absolute/path/to/campaign-protocol-mcp" }
}
```

#### **For Claude Desktop users:**
Edit `~/Library/Application Support/Claude/claude_desktop_config.json` and add:

```json
"mcpServers": {
  "cyberseclife-dev": {
    "command": "python3",
    "args": ["/absolute/path/to/campaign-protocol-mcp/server.py"]
  }
}
```
