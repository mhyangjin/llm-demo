from abc import ABC
from demo.runtime.base_runtime import BaseRuntime
from demo.models import ResolveQueryRequest

class LLM(ABC):

    def __init__(

            self,

            runtime: BaseRuntime,

    ) :

        self.runtime = runtime

    async def to_semantic_request(
        self,
        question: str,
    ) -> ResolveQueryRequest:
        """
        Convert a natural language question into a
        ResolveQueryRequest.

        This is a deterministic mock implementation.
        """

        response = await self.runtime.invoke(

                system_prompt="",

                user_prompt=question,

        )

        return ResolveQueryRequest.model_validate_json(response)



    async def health(self) -> bool:
        """
        Fake health check.
        """

        return True