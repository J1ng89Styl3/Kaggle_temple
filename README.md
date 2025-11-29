# Kaggle Template

Kaggle コンペティション用テンプレート（Docker / Kaggle 公式イメージ対応）

## 特徴
- **Kaggle Notebook 環境の完全再現**: 公式 Docker イメージを使用。
- **簡単な環境構築**: `docker-compose up -d` だけで Jupyter Lab が起動。
- **認証の簡略化**: `.env` ファイルのみで Kaggle API 認証を管理（`kaggle.json` ファイル管理不要）。
- **Code Competition 対応**: ローカルの Notebook をコマンド一発で Kaggle にアップロード・実行・提出可能。

## セットアップ

### 1. 前提条件
- Docker / Docker Compose がインストールされていること。
- Kaggle アカウントと API トークンを持っていること。

### 2. プロジェクトの準備
```bash
# .envファイルの作成
cp .env.example .env
```

`.env` を編集し、Kaggle の認証情報とコンペ名を入力します。
**注意**: `KAGGLE_KEY` は `kaggle.json` の中身の文字列をそのまま使用してください（`KGAT_` などの接頭辞は不要な場合があります）。

```bash
KAGGLE_USERNAME=your_username
KAGGLE_KEY=xxxxxxxxxxxxxx
KAGGLE_COMPETITION=santa-2025
```

### 3. 起動
```bash
docker-compose up -d
```
※ 初回は Kaggle 公式イメージ（約18GB）をプルするため時間がかかります。

### 4. Jupyter Lab へのアクセス
ブラウザで `http://localhost:8888` を開きます。

## 使い方

### コンテナ内での操作（推奨）
シェルに入る必要はなく、`docker-compose exec` 経由でコマンドを実行できます。

#### データのダウンロード
```bash
# input/ フォルダにデータセットをダウンロード
docker-compose exec kaggle-lab ./scripts/kaggle.sh competitions download -c $KAGGLE_COMPETITION -p input --unzip
```

#### Notebook のアップロード & 実行 (Code Competition 提出)
ローカルの Notebook を Kaggle 上で実行（Push）し、提出可能な状態にします。
```bash
# Usage: ./scripts/push_kernel.sh [Notebookパス] [URLスラッグ]
./scripts/push_kernel.sh notebooks/santa2025-ver2.ipynb santa-2025-ver2
```
実行後、表示される URL にアクセスし、完了後に "Submit" ボタンを押してください。

#### 直接コマンドで提出（CSV提出の場合）
```bash
docker-compose exec kaggle-lab ./scripts/kaggle.sh competitions submit -c $KAGGLE_COMPETITION -f submission.csv -m "message"
```

## ディレクトリ構成
- `configs/` : 設定ファイル
- `src/` : ソースコード
- `input/` : データセット（`/kaggle/input` にマウント）
- `notebooks/` : Notebook
- `scripts/` : ユーティリティスクリプト
- `artifacts/` : 生成物（モデル、提出ファイル等）

## トラブルシューティング
- **401 Unauthorized**: `.env` の `KAGGLE_USERNAME` / `KAGGLE_KEY` が間違っています。修正後、`docker-compose up -d` で反映させてください。
- **Mac (Apple Silicon) での警告**: `linux/amd64` イメージを使用しているため、エミュレーション実行となり警告が出ますが、動作に問題はありません（速度はネイティブより遅くなります）。
