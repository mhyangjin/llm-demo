from fastapi import APIRouter

from app.semantic import create_service
from apis.semantic.request import SemanticQueryRequest
from apis.semantic.response import SemanticQueryResponse

semantic_router = APIRouter()

service = create_service("./metadata")


@semantic_router.post(
    "/query",
    response_model=SemanticQueryResponse,
)
def query(request: SemanticQueryRequest):

    resolved = service.resolve_terms(
        metrics=request.metrics,
        dimensions=request.dimensions,
        filters=request.filters,
        analysis=request.analysis,
        patterns=request.patterns,
    )

    return SemanticQueryResponse(
        metrics=[
            metric.metric_name
            for metric in resolved.metrics
        ],
        dimensions=[
            dimension.dimension_id
            for dimension in resolved.dimensions
        ],
        tables=[
            table.table_name
            for table in resolved.tables
        ],
        filters=[
            filter.model_dump()
            for filter in resolved.filters
        ],
    )