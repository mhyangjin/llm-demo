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
import os
from demo.llm.llm import LLM
from demo.runtime.fake_runtime import FakeRuntime
from demo.runtime.sagemaker_runtime import SageMakerRuntime
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
    USE_FAKE = os.getenv("USE_FAKE", "false").lower() == "true"

    if USE_FAKE :
        print("Using FakeRuntime")
        runtime = FakeRuntime()
    else :
        print("Using SageMakerRuntime")
        runtime = SageMakerRuntime(
                endpoint_name="semantic-agent",
                region_name="ap-northeast-2",
        )

    llm = LLM(runtime)



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

        print(
            json.dumps(
                semantic_response.model_dump(),
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