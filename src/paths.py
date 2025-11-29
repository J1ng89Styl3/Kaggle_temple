from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def project_root() -> Path:
    return ROOT


def config_dir() -> Path:
    return ROOT / "configs"


def artifacts_dir(config_artifacts: str) -> Path:
    return ROOT / config_artifacts


def input_dir(config_input: str) -> Path:
    path = Path(config_input)
    if path.is_absolute():
        return path

    # Docker/Kaggle環境: /kaggle/input が存在し、ルートが /kaggle/working の場合
    # configs/base.yaml で "input" と指定されていれば /kaggle/input を指すようにする
    if Path("/kaggle/input").exists() and ROOT == Path("/kaggle/working"):
        return Path("/kaggle") / config_input

    return ROOT / config_input


def notebooks_dir() -> Path:
    return ROOT / "notebooks"
