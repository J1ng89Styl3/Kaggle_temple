Use this folder for exploratory notebooks.

Recommended first notebook steps:
1. Load `input/train.csv` and inspect column types.
2. Update `configs/base.yaml` with `target`, `id_column`, and any columns to drop.
3. Run `python -m src.train` to train a baseline model.
4. Use `python -m src.predict` to produce `artifacts/submission.csv`.
