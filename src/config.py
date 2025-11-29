from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

import yaml


@dataclass
class ProjectConfig:
    target: str
    id_column: str
    task: str
    random_state: int
    artifacts_dir: str


@dataclass
class DataConfig:
    input_dir: str
    train_file: str
    test_file: str
    sample_submission: str
    test_size: float
    stratify: bool


@dataclass
class FeatureConfig:
    drop_columns: List[str]
    numeric_imputer: str
    categorical_imputer: str
    scale_numeric: bool


@dataclass
class ModelConfig:
    type: str
    params: Dict[str, Any]


@dataclass
class CVConfig:
    folds: int
    shuffle: bool
    stratified: bool
    metric: str


@dataclass
class Config:
    project: ProjectConfig
    data: DataConfig
    features: FeatureConfig
    model: ModelConfig
    cv: CVConfig


def load_yaml(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_config(path: str | Path) -> Config:
    cfg_path = Path(path)
    raw = load_yaml(cfg_path)

    project = ProjectConfig(**raw["project"])
    data = DataConfig(**raw["data"])
    features = FeatureConfig(**raw["features"])
    model = ModelConfig(**raw["model"])
    cv = CVConfig(**raw["cv"])

    return Config(
        project=project,
        data=data,
        features=features,
        model=model,
        cv=cv,
    )
