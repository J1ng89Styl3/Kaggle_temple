from typing import Any

from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LinearRegression, LogisticRegression

from .config import Config


def _inject_seed(params: dict[str, Any], seed: int) -> dict[str, Any]:
    if "random_state" not in params:
        params = {**params, "random_state": seed}
    return params


def create_model(config: Config):
    params = dict(config.model.params)
    params = _inject_seed(params, config.project.random_state)

    task = config.project.task.lower()
    model_type = config.model.type.lower()

    if model_type == "random_forest":
        if task == "regression":
            return RandomForestRegressor(**params)
        return RandomForestClassifier(**params)

    if model_type in {"log_reg", "logistic_regression"}:
        if task == "regression":
            return LinearRegression(**params)
        if "max_iter" not in params:
            params["max_iter"] = 1000
        return LogisticRegression(**params)

    raise ValueError(f"Unsupported model type '{config.model.type}' for task '{task}'")
