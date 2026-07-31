from .repository import (
    MetadataRegistry,
    MetadataRepository,
)

from .service import SemanticService


def create_service(metadata_root: str) -> SemanticService:
    registry = MetadataRegistry.load(metadata_root)

    repository = MetadataRepository(registry)

    return SemanticService(repository)