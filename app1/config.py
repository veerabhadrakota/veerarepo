"""
Centralized configuration for the application.
"""

from dotenv import load_dotenv
import os

load_dotenv()

# Logging
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()

# Azure Open  AI
AZURE_OPENAI_ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.environ.get("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_API_VERSION = os.environ.get("AZURE_OPENAI_API_VERSION")
AZURE_DEPLOYMENT_NAME = os.environ.get("AZURE_DEPLOYMENT_NAME")

# URLs
ORCHESTRATOR_HOST = os.environ.get("ORCHESTRATOR_HOST", "localhost")
ORCHESTRATOR_PORT = int(os.environ.get("ORCHESTRATOR_PORT", "8000"))
ORCHESTRATOR_URL = os.environ.get("ORCHESTRATOR_URL", f"http://{ORCHESTRATOR_HOST}:{ORCHESTRATOR_PORT}")

# Webhook URLs
NEW_REQUIREMENTS_WEBHOOK_URL = f"{ORCHESTRATOR_URL}/new-requirements-available"
STORY_READY_FOR_TEST_CASE_GENERATION_WEBHOOK_URL = f"{ORCHESTRATOR_URL}/story-ready-for-test-case-generation"
EXECUTE_TESTS_WEBHOOK_URL = f"{ORCHESTRATOR_URL}/execute-tests"

# Agent
AGENT_BASE_URL = os.environ.get("AGENT_BASE_URL", "http://localhost")
MCP_SERVER_ATTACHMENTS_FOLDER_PATH = "/tmp"
ATTACHMENTS_DESTINATION_FOLDER_PATH = "D://temp"
REMOTE_EXECUTION_AGENT_HOSTS = os.environ.get("REMOTE_EXECUTION_AGENT_HOSTS", AGENT_BASE_URL)
AGENT_DISCOVERY_PORTS = os.environ.get("AGENT_DISCOVERY_PORTS", "8001-8006")
MCP_SERVER_TIMEOUT_SECONDS = 30

# Orchestrator
class OrchestratorConfig:
    AUTOMATED_TC_LABEL = "automated"
    AGENTS_DISCOVERY_INTERVAL_SECONDS = 300
    TASK_EXECUTION_TIMEOUT = 500.0
    AGENT_DISCOVERY_TIMEOUT_SECONDS = 120
    INCOMING_REQUEST_WAIT_TIMEOUT = AGENT_DISCOVERY_TIMEOUT_SECONDS + 5
    MODEL_NAME = "google-gla:gemini-2.5-flash"
    API_KEY = os.environ.get("ORCHESTRATOR_API_KEY")

# Requirements Review Agent
class RequirementsReviewAgentConfig:
    THINKING_BUDGET = 10000
    OWN_NAME = "Requirements Reviewer Agent"
    PORT = int(os.environ.get("PORT", "8001"))
    EXTERNAL_PORT = int(os.environ.get("EXTERNAL_PORT", PORT))
    PROTOCOL = "http"
    MODEL_NAME = "google-gla:gemini-2.5-pro"
    MAX_REQUESTS_PER_TASK = 10

# Test Case Generation Agent
class TestCaseGenerationAgentConfig:
    THINKING_BUDGET = 0
    OWN_NAME = "Test Case Generation Agent"
    PORT = int(os.environ.get("TESTCASE_GENERATION_PORT", "8002"))
    EXTERNAL_PORT = int(os.environ.get("TESTCASE_GENERATION_EXTERNAL_PORT", PORT))
    PROTOCOL = "http"
    MODEL_NAME = "google-gla:gemini-2.5-flash"
    MAX_REQUESTS_PER_TASK = 10

# Test Case Classification Agent
class TestCaseClassificationAgentConfig:
    THINKING_BUDGET = 2000
    OWN_NAME = "Test Case Classification Agent"
    PORT = int(os.environ.get("TESTCASE_CLASSIFICATION_PORT", "8003"))
    EXTERNAL_PORT = int(os.environ.get("TESTCASE_CLASSIFICATION_EXTERNAL_PORT", PORT))
    PROTOCOL = "http"
    MODEL_NAME = "google-gla:gemini-2.5-flash"
    MAX_REQUESTS_PER_TASK = 5

# Test Case Review Agent
class TestCaseReviewAgentConfig:
    THINKING_BUDGET = 10000
    REVIEW_COMPLETE_STATUS_NAME = "Review Complete"
    OWN_NAME = "Test Case Review Agent"
    PORT = int(os.environ.get("TESTCASE_REVIEW_PORT", "8004"))
    EXTERNAL_PORT = int(os.environ.get("TESTCASE_REVIEW_EXTERNAL_PORT", PORT))
    PROTOCOL = "http"
    MODEL_NAME = "google-gla:gemini-2.5-pro"
    MAX_REQUESTS_PER_TASK = 5
