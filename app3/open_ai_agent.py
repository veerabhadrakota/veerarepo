import asyncio
import os
from dotenv import load_dotenv

from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential
load_dotenv(".env02")

async def main():
    # Set up Azure OpenAI client with Azure CLI credentials
    azure_openai_agent = AzureOpenAIChatClient(
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    ).create_agent(
        instructions="You are a helpful assistant that provides concise and accurate information.",
        name="HelpfulAssistant"
    )

    print("Agent created:", azure_openai_agent)
    while True:
        user_input = input("Enter your message (or 'q','bye','exit' to quit): ")
        if user_input.lower() in['exit','quit','q','bye']:
            print("Exiting the chat. Goodbye!")
            break

        print(await azure_openai_agent.run(user_input))

if __name__ == "__main__":
    asyncio.run(main())