"""
Semantic Layer Demo

Question
    ↓
LLM
    ↓
ResolveQueryRequest
    ↓
Semantic Layer MCP
    ↓
ResolveQueryResponse
    ↓
LLM
    ↓
Athena SQL
"""

from __future__ import annotations

import asyncio
import json

from demo.fake_llm import FakeLLM
from demo.semantic_client import SemanticClient


LINE = "=" * 80


def print_title(title: str) -> None:
    print()
    print(LINE)
    print(title)
    print(LINE)


async def run(question: str) -> None:
    """
    Execute the complete Text-to-SQL flow.
    """

    llm = FakeLLM()

    async with SemanticClient() as semantic:

        #
        # Question
        #

        print_title("Question")
        print(question)

        #
        # Step 1
        #

        print_title("Step 1. Natural Language -> ResolveQueryRequest")

        semantic_request = await llm.to_semantic_request(question)

        print(
            json.dumps(
                semantic_request.model_dump(),
                indent=2,
                ensure_ascii=False,
            )
        )

        #
        # Step 2
        #

        print_title("Step 2. Semantic Layer")

        semantic_response = await semantic.resolve_semantics(
            semantic_request
        )

        #
        # SemanticClient currently returns dict
        #

        if hasattr(semantic_response, "model_dump"):
            body = semantic_response.model_dump()
        else:
            body = semantic_response

        print(
            json.dumps(
                body,
                indent=2,
                ensure_ascii=False,
            )
        )

        #
        # Step 3
        #

        print_title("Step 3. Metadata -> Athena SQL")

        sql = await llm.generate_sql(
            question,
            semantic_response,
        )

        print(sql)


async def main() -> None:
    """
    Demo entry point.
    """

    print()
    print(LINE)
    print("Semantic Layer Text-to-SQL Demo")
    print(LINE)

    while True:

        question = input(
            "\nQuestion ('exit' to quit)\n> "
        ).strip()

        if not question:
            continue

        if question.lower() in {
            "exit",
            "quit",
            "q",
        }:
            break

        try:
            await run(question)

        except KeyboardInterrupt:
            raise

        except Exception as e:
            print()
            print("ERROR")
            print(e)


if __name__ == "__main__":
    asyncio.run(main())