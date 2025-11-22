from pydantic_ai import Agent, Tool
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.azure import AzureProvider

import config
MAX_RETRIES = 3
REGISTRATION_PATH = f"{config.ORCHESTRATOR_URL}/register"
