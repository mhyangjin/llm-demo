"""
Simple MCP client test.
"""

from __future__ import annotations

import asyncio
import json

from fastmcp import Client


SERVER_URL = "http://127.0.0.1:8092/mcp"


async def main() -> None:
    print("=" * 80)
    print("Semantic Layer MCP Test")
    print("=" * 80)

    request = {
        "metrics": [
            "발송 성공 건수",
        ],
        "dimensions": [
            "채널",
        ],
        "filters": [
            "지난달",
        ],
        "analysis": [],
        "patterns": [],
    }

    print("Calling resolve_semantics()...\n")

    print("Request")
    print(
        json.dumps(
            request,
            indent=2,
            ensure_ascii=False,
        )
    )

    async with Client(SERVER_URL) as client:
        result = await client.call_tool(
            "resolve_semantics",
            {
                "request": request,
            },
        )

    print("\n" + "=" * 80)
    print("Response")
    print("=" * 80)

    response = result.structured_content

    print(
        json.dumps(
            response,
            indent=2,
            ensure_ascii=False,
            default=str,
        )
    )


if __name__ == "__main__":
    asyncio.run(main())