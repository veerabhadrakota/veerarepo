from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.azure import AzureProvider
import config

model = OpenAIChatModel(
   config.AZURE_DEPLOYMENT_NAME,
    provider=AzureProvider(
        azure_endpoint=config.AZURE_OPENAI_ENDPOINT,
        api_version=config.AZURE_OPENAI_API_VERSION,
        api_key=config.AZURE_OPENAI_API_KEY,
    ),
)
agent = Agent(model)
result_sync = agent.run_sync('What is the capital of India?')
print(result_sync.output)

