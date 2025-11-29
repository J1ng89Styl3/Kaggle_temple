from pathlib import Path

import pandas as pd

from .config import Config
from .logging_utils import get_logger
from .paths import artifacts_dir, input_dir

logger = get_logger(__name__)


def load_train_test(config: Config) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load train and test CSVs from the configured input directory."""
    base = input_dir(config.data.input_dir)
    train_path = base / config.data.train_file
    test_path = base / config.data.test_file

    if not train_path.exists():
        logger.warning("Train file missing at %s", train_path)
    if not test_path.exists():
        logger.warning("Test file missing at %s", test_path)

    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)
    return train_df, test_df


def load_train(config: Config) -> pd.DataFrame:
    base = input_dir(config.data.input_dir)
    train_path = base / config.data.train_file
    if not train_path.exists():
        logger.warning("Train file missing at %s", train_path)
    return pd.read_csv(train_path)


def load_test(config: Config) -> pd.DataFrame:
    base = input_dir(config.data.input_dir)
    test_path = base / config.data.test_file
    if not test_path.exists():
        logger.warning("Test file missing at %s", test_path)
    return pd.read_csv(test_path)


def ensure_artifacts_dir(config: Config) -> Path:
    artifacts = artifacts_dir(config.project.artifacts_dir)
    artifacts.mkdir(parents=True, exist_ok=True)
    return artifacts
