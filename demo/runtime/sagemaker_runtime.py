from __future__ import annotations

import json
import boto3
import asyncio
from .base_runtime import BaseRuntime


class SageMakerRuntime(BaseRuntime):

    def __init__(
        self,
        endpoint_name: str,
        region_name: str,
    ):
        self.endpoint_name = endpoint_name

        self.client = boto3.client(
            "sagemaker-runtime",
            region_name=region_name,
        )

    async def invoke(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
    ) -> str:

        payload = {
            "system": system_prompt,
            "prompt": user_prompt,
        }

        response = await asyncio.to_thread(
                self.client.invoke_endpoint,
                EndpointName=self.endpoint_name,
                ContentType="application/json",
                Accept="application/json",
                Body=json.dumps(payload).encode("utf-8"),
        )

        body = response["Body"].read().decode("utf-8")

        return body