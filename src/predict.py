import argparse
from pathlib import Path

import joblib
import pandas as pd

from .config import load_config
from .data_loader import load_test
from .logging_utils import get_logger
from .paths import artifacts_dir, input_dir

logger = get_logger(__name__)


def load_pipeline(model_path: Path):
    saved = joblib.load(model_path)
    if isinstance(saved, dict) and "pipeline" in saved:
        return saved["pipeline"]
    return saved


def build_submission(
    config_path: Path, model_path: Path, output_path: Path | None = None
) -> Path:
    config = load_config(config_path)
    test_df = load_test(config)
    pipeline = load_pipeline(model_path)

    task = config.project.task.lower()
    if task == "classification":
        preds = pipeline.predict_proba(test_df)[:, 1]
    else:
        preds = pipeline.predict(test_df)

    input_base = input_dir(config.data.input_dir)
    sample_path = input_base / config.data.sample_submission
    id_col = config.project.id_column or "id"
    target_col = config.project.target

    if sample_path.exists():
        sample = pd.read_csv(sample_path)
        submit_df = sample.copy()
        if id_col in test_df.columns and sample.columns[0] in submit_df.columns:
            submit_df[sample.columns[0]] = test_df[id_col]
        submit_df[sample.columns[-1]] = preds
    else:
        id_series = (
            test_df[id_col] if id_col in test_df.columns else range(len(test_df))
        )
        submit_df = pd.DataFrame({id_col: id_series, target_col: preds})

    artifacts = artifacts_dir(config.project.artifacts_dir)
    artifacts.mkdir(parents=True, exist_ok=True)
    output_path = output_path or artifacts / "submission.csv"
    submit_df.to_csv(output_path, index=False)
    logger.info("Wrote submission file to %s", output_path)
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Generate submission from trained model.")
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("configs/base.yaml"),
        help="Path to YAML config used for training.",
    )
    parser.add_argument(
        "--model",
        type=Path,
        default=Path("artifacts/model.joblib"),
        help="Path to trained model artifact.",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Optional output CSV path. Defaults to artifacts/submission.csv",
    )
    args = parser.parse_args()

    build_submission(args.config, args.model, args.out)


if __name__ == "__main__":
    main()
