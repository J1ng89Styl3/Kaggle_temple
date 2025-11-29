#!/usr/bin/env bash
set -euo pipefail

# Load Kaggle credentials from .env and pass through to kaggle CLI.
if [ ! -f ".env" ]; then
  echo ".env not found. Copy .env.example and set KAGGLE_USERNAME/KAGGLE_KEY/KAGGLE_COMPETITION." >&2
  exit 1
fi

set -a
source .env
set +a

exec kaggle "$@"
