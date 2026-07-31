"""
LLM Client

Wrapper around the LLM used by the demo application.
Initially this uses a fake implementation.
Later it can be replaced with SageMaker Runtime.
"""

from __future__ import annotations

import json
from typing import Any

from mcp_server.models import (
    ResolveQueryRequest,
    ResolveQueryResponse,
)

from demo.prompt import (
    SYSTEM_PROMPT,
    build_user_prompt,
)


class LLMClient:
    """
    Thin wrapper around an LLM.

    Currently this is a fake implementation.
    Replace _invoke() with SageMaker Runtime later.
    """

    async def to_semantic_request(
        self,
        question: str,
    ) -> ResolveQueryRequest:
        """
        Convert a natural language question into
        ResolveQueryRequest.
        """

        prompt = f"""
Convert the following question into JSON.

Return ONLY JSON.

Schema

{{
    "metrics": [],
    "dimensions": [],
    "filters": [],
    "analysis": [],
    "patterns": []
}}

Question

{question}
"""

        response = await self._invoke(prompt)

        return ResolveQueryRequest.model_validate_json(response)

    async def generate_sql(
        self,
        question: str,
        metadata: ResolveQueryResponse,
    ) -> str:
        """
        Generate Athena SQL using Semantic metadata.
        """

        prompt = build_user_prompt(
            question=question,
            semantic_context=metadata.model_dump(),
        )

        return await self._invoke(
            SYSTEM_PROMPT + "\n\n" + prompt
        )

    async def _invoke(
        self,
        prompt: str,
    ) -> str:
        """
        Fake LLM.

        Replace this with SageMaker Runtime later.
        """

        #
        # Semantic Request Demo
        #
        if "Convert the following question" in prompt:

            fake = {
                "metrics": [
                    "발송 성공 건수"
                ],
                "dimensions": [
                    "채널"
                ],
                "filters": [
                    "지난달"
                ],
                "analysis": [],
                "patterns": [],
            }

            return json.dumps(
                fake,
                ensure_ascii=False,
            )

        #
        # SQL Demo
        #
        return """
SELECT
    channel,
    SUM(success_count) AS send_success_count
FROM notification_status
WHERE request_date BETWEEN DATE '2026-06-01'
                      AND DATE '2026-06-30'
GROUP BY channel;
""".strip()