import asyncio
import os
from dotenv import load_dotenv
from agent_framework.azure import AzureOpenAIResponsesClient
from azure.identity import AzureCliCredential

load_dotenv('.env03')
AZURE_OPENAI_ENDPOINT=os.getenv('AZURE_OPENAI_ENDPOINT')
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=os.getenv('AZURE_OPENAI_CHAT_DEPLOYMENT_NAME')
async def main():
    agent = AzureOpenAIResponsesClient(
        api_version="preview",
        credential=AzureCliCredential(),
        deployment_name=AZURE_OPENAI_CHAT_DEPLOYMENT_NAME,
        endpoint=AZURE_OPENAI_ENDPOINT).create_agent(
        instructions="You are good at telling jokes.",
        name="Joker"
    )

    result = await agent.run("Tell me a joke about a pirate.")
    print(result.text)

if __name__ == "__main__":
    asyncio.run(main())


