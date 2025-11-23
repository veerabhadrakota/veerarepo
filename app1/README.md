### Prerequisites

* Python 3.13+
* `pip` (Python package installer)
* `virtualenv` (or `conda` for environment management)

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/veerabhadrakota/veerarepo
   cd veerarepo
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Environment Variables

Create a `.env` file in the project root and configure the following environment variables. These variables control the
behavior of the orchestrator and agents.

```
# Logging
LOG_LEVEL=INFO # Default: INFO. Controls the verbosity of logging.

# Azure Open AI
AZURE_OPENAI_ENDPOINT=YOUR_AZURE_OPENAI_ENDPOINT
AZURE_OPENAI_API_KEY=YOUR_AZURE_OPENAI_API_KEY
AZURE_OPENAI_API_VERSION=YOUR_AZURE_OPENAI_API_VERSION
AZURE_DEPLOYMENT_NAME=YOUR_AZURE_DEPLOYMENT_NAME

# Azure DevOps
AZURE_DEVOPS_ORG=YOUR_AZURE_DEVOPS_ORG_NAME
AZURE_DEVOPS_PAT=YOUR_AZURE_DEVOPS_PAT_TOKEN

# Orchestrator
ORCHESTRATOR_HOST=localhost # Default: localhost. The host where the orchestrator runs.
ORCHESTRATOR_PORT=8000 # Default: 8000. The port the orchestrator listens on.
ORCHESTRATOR_URL=http://localhost:8000 # Default: http://localhost:8000. The full URL of the orchestrator.
ORCHESTRATOR_API_KEY=YOUR_ORCHESTRATOR_API_KEY # Optional. Set this to activate API key authentication for the orchestrator.

# Agent Configuration
AGENT_BASE_URL=http://localhost # Default: http://localhost. Base URL for agents.
PORT=8001 # Default: 8001. The internal port an agent listens on.
EXTERNAL_PORT=8001 # Default: 8001. The externally accessible port for the agent.

TESTCASE_GENERATION_PORT=8002
TESTCASE_GENERATION_EXTERNAL_PORT=8002

TESTCASE_CLASSIFICATION_PORT=8003
TESTCASE_CLASSIFICATION_EXTERNAL_PORT=8003

TESTCASE_REVIEW_PORT=8004
TESTCASE_REVIEW_EXTERNAL_PORT=8004

# Agent Discovery (for remote agents)
REMOTE_EXECUTION_AGENT_HOSTS=http://localhost # Default: http://localhost. Comma-separated URLs of remote agent hosts.
AGENT_DISCOVERY_PORTS=8001-8006 # Default: 8001-8006. Port range for agent discovery.
```

### ADO-MCP Server

1. Check Node.js & npm are installed
```
node -v
```

2. Install MCP globally
```
npm install -g @azure-devops/mcp
```

3. Verify the global install
```
mcp-server-azuredevops --help
```

If installation is OK, you should see help text with options like:

--organization
--authentication
--domains

4. Create an Azure DevOps PAT (Personal Access Token)

5. Set the PAT as environment variable (Windows)
The MCP server expects a PAT in AZURE_DEVOPS_EXT_PAT when using --authentication env.
Quick way (for current PowerShell session only)

In PowerShell:
```
$env:AZURE_DEVOPS_EXT_PAT = "YOUR_PAT_VALUE_HERE"
echo $env:AZURE_DEVOPS_EXT_PAT
```

5.1 Test ADO Access
```
$pat = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(":$env:AZURE_DEVOPS_EXT_PAT"))
Invoke-WebRequest -Uri "https://dev.azure.com/YOUR_ORGANIZATION_NAME/_apis/projects?api-version=7.0" -Headers @{ Authorization = "Basic $pat" }
```

5.2 
```
setx PATH "$Env:PATH;C:\Users\$Env:USERNAME\AppData\Roaming\npm"
```

6. Hook it into VS Code MCP (optional but likely your next step)
If you’re using the Model Context Protocol extension in VS Code:

```
Your mcp.json might look like:
{
  "servers": {
    "ado": {
      "command": "mcp-server-azuredevops",
      "args": [
        "YOUR_ORGANIZATION_NAME",
        "--authentication", "env",
        "--domains", "all"
      ],
      "env": {
        "AZURE_DEVOPS_EXT_PAT": "${env:AZURE_DEVOPS_EXT_PAT}"
      }
    }
  }
}
```

8. Where is the mcp-server-azuredevops EXE located?
```
where mcp-server-azuredevops
```



