import asyncio
from ado_mcp_client import AdoMcpClient

async def main():
    client = AdoMcpClient("https://dev.azure.com/microsoftit")
    tools = await client.list_tools()
    print("Tools available:", tools)
    result = await client.get_work_item("veeratestproject",1)
    print("WorkItem:", result)

asyncio.run(main())
