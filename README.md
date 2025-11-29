# Kaggle Template

Kaggle のタブular コンペをすぐ始められる軽量テンプレートです。

## セットアップ
- Python 3.9+ を想定しています。
- 依存を入れる: `pip install -e .[notebook,viz]`
- `input/` に `train.csv`, `test.csv`, `sample_submission.csv` を配置。
- `configs/base.yaml` で `target`, `id_column`, モデル種別などを調整。

### Kaggle API を使う場合（.env 利用）
- `.env` のみで認証を管理（`~/.kaggle/kaggle.json` 不要）。`cp .env.example .env` して `KAGGLE_USERNAME`, `KAGGLE_KEY`, `KAGGLE_COMPETITION` を記入（`.env` は `.gitignore` 済み）。
- `scripts/kaggle.sh` が `.env` を読み込んで `kaggle` CLI を実行:
  - データ取得: `./scripts/kaggle.sh competitions download -c $KAGGLE_COMPETITION -p input` → zip 展開後、CSV を `input/` に置く。
  - 提出: `./scripts/kaggle.sh competitions submit -c $KAGGLE_COMPETITION -f artifacts/submission.csv -m "first try"`

## 主要コマンド
- 学習 + クロスバリデーション: `python -m src.train --config configs/base.yaml`
- 推論 + 提出ファイル生成: `python -m src.predict --config configs/base.yaml --model artifacts/model.joblib`

## Docker で動かす場合
Kaggle Notebook とほぼ同等の環境（公式イメージ利用）を再現します。

1. ビルド & 起動:
   ```bash
   docker-compose up -d
   ```
   ※ 初回は Kaggle 公式イメージ（約18GB〜）をプルするため、時間がかかります。

2. Jupyter Lab にアクセス:
   ブラウザで `http://localhost:8888` を開きます。パスワード/トークンは不要に設定されています。

3. コンテナ内での操作:
   ```bash
   # シェルに入る
   docker-compose exec kaggle-lab bash
   ```
   
   コンテナ内のパス構成:
   - `/kaggle/working`: プロジェクトルート（ローカルのファイルをマウント）
   - `/kaggle/input`: データディレクトリ（ローカルの `input/` をマウント）

   コマンド例:
   ```bash
   # 学習
   python -m src.train --config configs/base.yaml
   
   # 提出 (kaggleコマンドはプリインストール済み、.envの認証情報を利用)
   ./scripts/kaggle.sh competitions submit -c $KAGGLE_COMPETITION -f artifacts/submission.csv -m "message"
   ```

## ディレクトリ構成
- `configs/` : 設定ファイル（`base.yaml`）
- `src/` : 学習・推論用モジュール（`train.py`, `predict.py` など）
- `input/` : Kaggle のデータを置く場所
- `notebooks/` : EDA や実験用ノートブック
- `artifacts/` : 学習済みモデル・提出 CSV（`.gitignore` 済み）

## フローの例
1. `input/train.csv` を開き、カラム名・ターゲット名を確認
2. `configs/base.yaml` を更新し、実行: `python -m src.train`
3. `artifacts/model.joblib` を使って提出ファイル作成: `python -m src.predict`
4. `artifacts/submission.csv` を Kaggle にアップロード
