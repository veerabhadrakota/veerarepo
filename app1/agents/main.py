import asyncio, json
from adomcp.mcp_client import AdoMcpClient

async def main():
    adoProject = "your_projectname"

    client = AdoMcpClient("https://dev.azure.com/your_org", adoProject ,auth_mode="pat")
    tools = await client.list_tools()
    # print("Tools available:", tools)

    res = await client._raw_call_tool("list_projects", {})
    # print("Projects:", res)
    # print(json.dumps(client._extract_structured(res), indent=2, ensure_ascii=False))

    work_item = await client.get_work_item(adoProject, 1)
    print("Title:", work_item.fields.get("System.Title"))
    print("Description:", work_item.fields.get("System.Description"))

asyncio.run(main())
