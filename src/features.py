from typing import Tuple

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from .config import Config


def select_feature_frame(df: pd.DataFrame, config: Config) -> pd.DataFrame:
    drop_cols = set(config.features.drop_columns)
    for col in (config.project.target, config.project.id_column):
        if col:
            drop_cols.add(col)
    keep_df = df.drop(columns=[c for c in drop_cols if c in df.columns])
    return keep_df


def build_preprocessor(
    df: pd.DataFrame, config: Config
) -> Tuple[ColumnTransformer, pd.DataFrame]:
    feature_df = select_feature_frame(df, config)
    cat_cols = feature_df.select_dtypes(include=["object", "category"]).columns.tolist()
    num_cols = feature_df.select_dtypes(exclude=["object", "category"]).columns.tolist()

    transformers = []
    if num_cols:
        num_steps = []
        if config.features.numeric_imputer != "none":
            num_steps.append(
                ("imputer", SimpleImputer(strategy=config.features.numeric_imputer))
            )
        if config.features.scale_numeric:
            num_steps.append(("scaler", StandardScaler()))
        num_transformer = Pipeline(num_steps) if num_steps else "passthrough"
        transformers.append(("num", num_transformer, num_cols))

    if cat_cols:
        cat_steps = []
        if config.features.categorical_imputer != "none":
            cat_steps.append(
                (
                    "imputer",
                    SimpleImputer(strategy=config.features.categorical_imputer),
                )
            )
        cat_steps.append(("encoder", OneHotEncoder(handle_unknown="ignore")))
        cat_transformer = Pipeline(cat_steps) if cat_steps else "passthrough"
        transformers.append(("cat", cat_transformer, cat_cols))

    preprocessor = ColumnTransformer(
        transformers=transformers,
        remainder="drop",
    )
    return preprocessor, feature_df


def prepare_xy(
    train_df: pd.DataFrame, config: Config
) -> tuple[pd.DataFrame, pd.Series, ColumnTransformer]:
    if config.project.target not in train_df.columns:
        raise KeyError(f"Target column '{config.project.target}' not in training data")

    y = train_df[config.project.target]
    preprocessor, feature_df = build_preprocessor(train_df, config)
    return feature_df, y, preprocessor
