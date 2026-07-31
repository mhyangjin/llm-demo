from pydantic import BaseModel


class SemanticQueryResponse(BaseModel):
    metrics: list[str]
    dimensions: list[str]
    tables: list[str]
    filters: list[dict]