"""
Semantic Layer MCP Server
"""

from __future__ import annotations

from .tools import mcp


def create_server():
    """
    MCP Server 생성
    """
    return mcp


server = create_server()


if __name__ == "__main__":
    server.run()