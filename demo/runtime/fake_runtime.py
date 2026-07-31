from __future__ import annotations

import json

from .base_runtime import BaseRuntime


class FakeRuntime(BaseRuntime):

    async def invoke(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
    ) -> str:

        q = user_prompt.lower()

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

        return json.dumps(
            {
                "metrics": metrics,
                "dimensions": dimensions,
                "filters": filters,
                "analysis": analysis,
                "patterns": patterns,
            },
            ensure_ascii=False,
        )