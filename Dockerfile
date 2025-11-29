FROM gcr.io/kaggle-images/python

# Kaggle環境に合わせる
WORKDIR /kaggle/working

# ライブラリの追加インストールが必要な場合はここで行う
# Kaggle公式イメージにはほとんど入っているが、自作パッケージの依存などはここで
COPY pyproject.toml ./
# 編集可能モードでパッケージをインストール
RUN pip install -e .

# 起動時のデフォルトコマンドをJupyter Labにする（docker-composeで上書き可能）
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=''"]
