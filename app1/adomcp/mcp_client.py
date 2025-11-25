import os
import json
from typing import Any, Dict, List, Optional

from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters

from models.work_item_request import GetWorkItemRequest
from models.work_item_response import WorkItemResponse

class AdoMcpClient:
    """
    Helper to talk to the Azure DevOps MCP server over STDIO.
    Handles:
      - starting the MCP server via npx
      - calling tools like wit_get_work_item, wit_add_work_item_comment
    """
    def __init__(self, org_url, project, auth_mode: str = "azure-cli"):
        allowed_modes = {"azure-cli", "pat", "azure-identity"}
        if auth_mode not in allowed_modes:
            raise ValueError(f"Invalid auth_mode: {auth_mode}. Must be one of {allowed_modes}")

        # Base environment configuration
        environ = {
            "AZURE_DEVOPS_ORG_URL": org_url,
            "AZURE_DEVOPS_AUTH_METHOD": auth_mode,
            "AZURE_DEVOPS_DEFAULT_PROJECT": project
        }

        # Additional rule for PAT mode
        if auth_mode == "pat":
            pat = os.getenv("AZURE_DEVOPS_PAT")
            if not pat:
                raise ValueError("auth_mode is 'pat' but no PAT provided")
            environ["AZURE_DEVOPS_PAT"] = pat

        self.server_params = StdioServerParameters(
            command="npx",
            args=[
                "-y",
                "@tiberriver256/mcp-server-azure-devops"
            ],
            env=environ
        )

    async def list_tools(self) -> List[str]:
        """Return a simple list of available tool names."""
        async with stdio_client(self.server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.list_tools()
                return [t.name for t in result.tools]

    async def _raw_call_tool(self, tool_name: str, params: Dict[str, Any]) -> Any:
        """Low-level call to an MCP tool, returns the raw ToolResponse."""
        async with stdio_client(self.server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()

                tools_result = await session.list_tools()
                tool_names = [t.name for t in tools_result.tools]
                if tool_name not in tool_names:
                    raise ValueError(
                        f"Tool '{tool_name}' not found. Available: {tool_names}"
                    )

                return await session.call_tool(tool_name, params)

    @staticmethod
    def _extract_structured(result: Any) -> Any:
        """
        Try to extract structured JSON-like data from MCP ToolResponse.
        Falls back to parsing text content as JSON or raw string.
        """
        # ToolResponse usually has: isError, structuredContent, content
        if getattr(result, "isError", False):
            # Grab text error message if present
            texts = []
            for c in getattr(result, "content", []):
                text = getattr(c, "text", None)
                if text:
                    texts.append(text)
            message = "\n".join(texts) or "Unknown MCP error"
            raise RuntimeError(f"MCP tool error: {message}")

        # First, prefer structuredContent if present
        structured = getattr(result, "structuredContent", None)
        if structured is not None:
            return structured

        # Otherwise, try to parse text contents as JSON
        texts = []
        for c in getattr(result, "content", []):
            text = getattr(c, "text", None)
            if text:
                texts.append(text)
        joined = "\n".join(texts)

        if not joined:
            return None

        try:
            return json.loads(joined)
        except Exception:
            # Couldn’t parse as JSON, return raw text
            return joined

    async def get_work_item(
        self,
        project: str,
        work_item_id: int,
        fields: Optional[List[str]] = None,
    ) -> WorkItemResponse:
        """
        Get a single work item. Returns a dict with fields like 'fields', 'id', etc.
        """
        if not project:
            raise ValueError("project cannot be empty")

        if work_item_id <= 0:
            raise ValueError("work_item_id must be a positive integer")

        request = GetWorkItemRequest(
            project=project,
            workItemId=work_item_id,
            fields=fields,
        )

        print("Requesting work item:", request)

        result = await self._raw_call_tool("get_work_item", request.model_dump(exclude_none=True))
        structured = self._extract_structured(result)

        return WorkItemResponse(**structured)
        # We expect something like:
        # {
        #   "id": 123,
        #   "fields": {
        #       "System.Title": "...",
        #       "System.Description": "..."
        #   }
        # }

    async def add_work_item_comment(
        self,
        project: str,
        work_item_id: int,
        comment: str,
        fmt: str = "markdown",
    ) -> Any:
        """
        Add a comment to a work item using wit_add_work_item_comment.
        """
        params = {
            "project": project,
            "workItemId": work_item_id,
            "comment": comment,
            "format": fmt,
        }

        result = await self._raw_call_tool("wit_add_work_item_comment", params)
        # If there's an error, _extract_structured will raise
        return self._extract_structured(result)
