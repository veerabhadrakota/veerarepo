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
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Environment Variables

Create a `.env` file in the project root and configure the following environment variables. These variables control the
behavior of the orchestrator and agents.

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

