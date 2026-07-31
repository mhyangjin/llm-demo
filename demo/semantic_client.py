"""
Semantic Layer MCP Client

Thin wrapper around the Semantic Layer MCP Server.
"""

from __future__ import annotations

from typing import Any

from fastmcp import Client
from demo.models import ResolveQueryRequest, ResolveQueryResponse

class SemanticClient:
    """
    Thin wrapper for the Semantic Layer MCP Server.
    """

    def __init__(
        self,
        server_url: str = "http://127.0.0.1:8000/mcp",
    ) -> None:
        self.server_url = server_url
        self.client = Client(server_url)

    async def __aenter__(self) -> "SemanticClient":
        await self.client.__aenter__()
        return self

    async def __aexit__(
            self,
            exc_type,
            exc_val,
            exc_tb,
    ) -> None :
        await self.client.__aexit__(exc_type, exc_val, exc_tb)

    async def call_tool(self, tool: str, **kwargs) -> Any :
        try :
            result = await self.client.call_tool(tool, kwargs)
            return result.structured_content
        except Exception as e :
            raise RuntimeError(f"MCP tool '{tool}' failed: {e}") from e

    async def resolve_semantics(
            self,
            request: ResolveQueryRequest,
    ) -> ResolveQueryResponse :
        result = await self.call_tool(
                "resolve_semantics",
                request=request,
        )
        return ResolveQueryResponse.model_validate(result)

    async def get_metric(self, name: str) -> Any:
        """
        Get metric metadata.
        """
        return await self.call_tool(
            "get_metric",
                name=name
        )

    async def get_dimension(self, name: str) -> Any:
        """
        Get dimension metadata.
        """
        return await self.call_tool(
            "get_dimension",
                name=name
        )

    async def get_table(self, name: str) -> Any:
        """
        Get table metadata.
        """
        return await self.call_tool(
            "get_table",
                name=name
        )

    async def get_pattern(self, name: str) -> Any:
        """
        Get pattern metadata.
        """
        return await self.call_tool(
            "get_pattern",
                name=name
        )