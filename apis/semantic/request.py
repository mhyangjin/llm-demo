from pydantic import BaseModel


class SemanticQueryRequest(BaseModel):
    metrics: list[str] = []
    dimensions: list[str] = []
    filters: list[str] = []

    analysis: list[str] = []
    patterns: list[str] = []