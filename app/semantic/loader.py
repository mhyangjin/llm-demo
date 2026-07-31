from pathlib import Path
from typing import Type, TypeVar
import yaml

from .models import (
    BaseMetricModel,
    DerivedMetricModel,
    TableModel,
    DimensionModel,
    MetricGlossaryFile,
    DimensionGlossaryFile,
    FilterGlossaryFile,
    AnalysisGlossaryFile,
    AnalysisPatternModel,
)

T = TypeVar("T")


def load_yaml(path: str | Path) -> dict:
    with Path(path).open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data or {}


class MetadataLoader:

    @staticmethod
    def _load_yaml(path: str | Path) -> dict:
        return load_yaml(path)

    @classmethod
    def load(cls, path: str | Path, model: Type[T]) -> T:
        data = cls._load_yaml(path)
        return model.model_validate(data)

    @classmethod
    def load_metric(cls, path: str | Path):
        data = cls._load_yaml(path)

        metric_type = data.get("type", "base")

        if metric_type == "derived":
            return DerivedMetricModel.model_validate(data)

        return BaseMetricModel.model_validate(data)

    @classmethod
    def load_directory(cls, directory: str | Path, loader):
        directory = Path(directory)

        result = {}

        files = sorted({*directory.glob("*.yaml"), *directory.glob("*.yml")})
        for file in files:
            obj = loader(file)
            result[file.stem] = obj

        return result

    #
    # Tables
    #
    @classmethod
    def load_tables(cls, directory):
        return cls.load_directory(
            directory,
            lambda p: cls.load(p, TableModel),
        )

    #
    # Dimensions
    #
    @classmethod
    def load_dimensions(cls, directory):
        return cls.load_directory(
            directory,
            lambda p: cls.load(p, DimensionModel),
        )

    #
    # Metrics
    #
    @classmethod
    def load_metrics(cls, directory):
        directory = Path(directory)
        result = cls.load_directory(directory, cls.load_metric)

        if directory.exists() and directory.is_dir():
            for subdirectory in sorted(directory.iterdir()):
                if not subdirectory.is_dir():
                    continue
                result.update(cls.load_directory(subdirectory, cls.load_metric))

        return result

    #
    # Patterns
    #
    @classmethod
    def load_patterns(cls, directory):
        return cls.load_directory(
            directory,
            lambda p: cls.load(p, AnalysisPatternModel),
        )

    #
    # Glossary
    #
    @classmethod
    def load_metric_glossary(cls, path):
        return cls.load(path, MetricGlossaryFile)

    @classmethod
    def load_dimension_glossary(cls, path):
        return cls.load(path, DimensionGlossaryFile)

    @classmethod
    def load_filter_glossary(cls, path):
        return cls.load(path, FilterGlossaryFile)

    @classmethod
    def load_analysis_glossary(cls, path):
        return cls.load(path, AnalysisGlossaryFile)