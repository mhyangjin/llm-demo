"""
Fake LLM

Mock implementation of the LLM interface.

This class is used for local development before
connecting to SageMaker.

It implements the same interface as LLMClient.
"""

from __future__ import annotations

from mcp_server.models import (
    ResolveQueryRequest,
    ResolveQueryResponse,
)


class FakeLLM(BaseLLM):
    """
    Mock LLM used for local development.

    Responsibilities

    - Natural Language -> ResolveQueryRequest
    - ResolveQueryResponse -> Athena SQL
    """

    async def to_semantic_request(
        self,
        question: str,
    ) -> ResolveQueryRequest:
        """
        Convert a natural language question into a
        ResolveQueryRequest.

        This is a deterministic mock implementation.
        """

        q = question.lower()

        metrics: list[str] = []
        dimensions: list[str] = []
        filters: list[str] = []
        analysis: list[str] = []
        patterns: list[str] = []

        #
        # Metrics
        #

        if "성공" in q:
            metrics.append("발송 성공 건수")

        if "실패" in q:
            metrics.append("발송 실패 건수")

        if "발송" in q and not metrics:
            metrics.append("발송 건수")

        #
        # Dimensions
        #

        if "채널" in q:
            dimensions.append("채널")

        if "이벤트" in q:
            dimensions.append("이벤트")

        if "캠페인" in q:
            dimensions.append("캠페인")

        #
        # Filters
        #

        if "오늘" in q:
            filters.append("오늘")

        if "어제" in q:
            filters.append("어제")

        if "지난달" in q:
            filters.append("지난달")

        #
        # Pattern
        #

        if "피로도" in q:
            patterns.append("customer_fatigue")

        return ResolveQueryRequest(
            metrics=metrics,
            dimensions=dimensions,
            filters=filters,
            analysis=analysis,
            patterns=patterns,
        )

    async def generate_sql(
        self,
        question: str,
        metadata: ResolveQueryResponse,
    ) -> str:
        """
        Generate fake Athena SQL.

        This method only demonstrates the overall flow.
        """

        tables = metadata.tables or ["notification_status"]

        select_columns = []

        if metadata.dimensions:
            select_columns.extend(metadata.dimensions)

        if metadata.metrics:
            select_columns.extend(metadata.metrics)

        sql = []

        sql.append("SELECT")

        sql.append(
            "    " + ",\n    ".join(select_columns)
            if select_columns
            else "    *"
        )

        sql.append(f"FROM {tables[0]}")

        if metadata.filters:
            sql.append("WHERE ...")

        if metadata.dimensions:
            sql.append(
                "GROUP BY " + ", ".join(metadata.dimensions)
            )

        return "\n".join(sql)

    async def health(self) -> bool:
        """
        Fake health check.
        """

        return True