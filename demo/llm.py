from abc import ABC, abstractmethod

class BaseLLM(ABC):

    @abstractmethod
    async def to_semantic_request(self, question: str) -> ResolveQueryRequest:
        ...

    @abstractmethod
    async def generate_sql(
        self,
        question: str,
        metadata: ResolveQueryResponse,
    ) -> str:
        ...