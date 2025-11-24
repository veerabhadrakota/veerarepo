import os
import json
from typing import Any, Dict, List, Optional

from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters


class AdoMcpClient:
    """
    Helper to talk to the Azure DevOps MCP server over STDIO.
    Handles:
      - starting the MCP server via npx
      - calling tools like wit_get_work_item, wit_add_work_item_comment
    """

    def __init__(self, org_url: str, pat_env_var: str = "AZURE_DEVOPS_EXT_PAT"):
        pat = os.getenv(pat_env_var)
        if not pat:
            raise RuntimeError(
                f"Environment variable {pat_env_var} is not set. "
                f"Please set your Azure DevOps PAT in {pat_env_var}."
            )

        self.server_params = StdioServerParameters(
            command="npx",
            args=[
                "-y",
                "@azure-devops/mcp@next",
                "server",
                org_url,
                "--authentication",
                "azcli",
                "--domains",
                "core",
                "work-items",
                "test-plans",
            ]
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
    ) -> Dict[str, Any]:
        """
        Get a single work item. Returns a dict with fields like 'fields', 'id', etc.
        """
        params: Dict[str, Any] = {
            "project": project,
            "id": work_item_id,
        }
        if fields:
            params["fields"] = fields

        result = await self._raw_call_tool("wit_get_work_item", params)
        structured = self._extract_structured(result)

        # We expect something like:
        # {
        #   "id": 123,
        #   "fields": {
        #       "System.Title": "...",
        #       "System.Description": "..."
        #   }
        # }
        if isinstance(structured, dict):
            return structured
        else:
            # If it's not dict, wrap so caller can still use it
            return {"raw": structured}

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
