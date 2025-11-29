import argparse
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import KFold, StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline

from .config import Config, load_config
from .data_loader import ensure_artifacts_dir, load_train
from .features import prepare_xy
from .logging_utils import get_logger
from .model_factory import create_model

logger = get_logger(__name__)


def build_pipeline(config: Config) -> tuple[Pipeline, pd.DataFrame, pd.Series]:
    train_df = load_train(config)
    X, y, preprocessor = prepare_xy(train_df, config)

    model = create_model(config)
    pipeline = Pipeline(
        [
            ("preprocess", preprocessor),
            ("model", model),
        ]
    )
    return pipeline, X, y


def make_cv(config: Config):
    if config.project.task.lower() == "classification" and config.cv.stratified:
        return StratifiedKFold(
            n_splits=config.cv.folds,
            shuffle=config.cv.shuffle,
            random_state=config.project.random_state,
        )
    return KFold(
        n_splits=config.cv.folds,
        shuffle=config.cv.shuffle,
        random_state=config.project.random_state,
    )


def run_training(config: Config, config_path: Path) -> Path:
    pipeline, X, y = build_pipeline(config)
    cv = make_cv(config)

    logger.info("Running %d-fold CV with metric '%s'", config.cv.folds, config.cv.metric)
    scores = cross_val_score(
        pipeline,
        X,
        y,
        scoring=config.cv.metric,
        cv=cv,
        n_jobs=-1,
    )

    logger.info("CV scores: %s", np.round(scores, 4))
    logger.info("CV mean: %.4f +/- %.4f", scores.mean(), scores.std())

    pipeline.fit(X, y)
    artifacts = ensure_artifacts_dir(config)
    model_path = artifacts / "model.joblib"
    joblib.dump(
        {
            "pipeline": pipeline,
            "config_path": str(config_path.resolve()),
            "cv_scores": scores.tolist(),
        },
        model_path,
    )
    logger.info("Saved trained model to %s", model_path)
    return model_path


def main():
    parser = argparse.ArgumentParser(description="Train a model using the Kaggle template.")
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("configs/base.yaml"),
        help="Path to YAML config.",
    )
    args = parser.parse_args()

    config = load_config(args.config)
    run_training(config, args.config)


if __name__ == "__main__":
    main()
