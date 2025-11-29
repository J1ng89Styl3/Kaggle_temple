#!/usr/bin/env bash
set -euo pipefail

# Check arguments
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <notebook_path> <title_slug>"
    echo "Example: $0 notebooks/santa2025-ver2.ipynb santa-2025-solution"
    exit 1
fi

NB_PATH=$1
TITLE_SLUG=$2
KERNEL_TITLE=$(echo "$TITLE_SLUG" | tr '-' ' ' | awk '{for(i=1;i<=NF;i++)sub(/./,toupper(substr($0,i,1)),$i)}1')
SUBMISSION_DIR="notebooks/submission/$TITLE_SLUG"
NB_FILENAME=$(basename "$NB_PATH")

# Load environment variables
if [ -f ".env" ]; then
    set -a
    source .env
    set +a
else
    echo "Error: .env file not found." >&2
    exit 1
fi

if [ -z "${KAGGLE_USERNAME:-}" ]; then
    echo "Error: KAGGLE_USERNAME is not set in .env" >&2
    exit 1
fi

if [ -z "${KAGGLE_COMPETITION:-}" ]; then
    echo "Error: KAGGLE_COMPETITION is not set in .env" >&2
    exit 1
fi

# Prepare submission directory
mkdir -p "$SUBMISSION_DIR"
cp "$NB_PATH" "$SUBMISSION_DIR/$NB_FILENAME"

# Generate kernel-metadata.json
cat <<EOF > "$SUBMISSION_DIR/kernel-metadata.json"
{
  "id": "${KAGGLE_USERNAME}/${TITLE_SLUG}",
  "title": "${KERNEL_TITLE}",
  "code_file": "${NB_FILENAME}",
  "language": "python",
  "kernel_type": "notebook",
  "is_private": true,
  "enable_gpu": false,
  "enable_internet": false,
  "dataset_sources": [],
  "competition_sources": ["${KAGGLE_COMPETITION}"],
  "kernel_sources": []
}
EOF

echo "Generated metadata for ${KAGGLE_USERNAME}/${TITLE_SLUG}"
echo "Pushing kernel to Kaggle..."

# Push using kaggle CLI (via container if available, or local)
if command -v kaggle &> /dev/null; then
    kaggle kernels push -p "$SUBMISSION_DIR"
else
    # If kaggle command is not local, try running via docker-compose
    if command -v docker-compose &> /dev/null; then
         # Check if the path is inside the project root and map it to container path
         # Here we assume the script is run from project root and maps nicely
         docker-compose exec -T kaggle-lab kaggle kernels push -p "$SUBMISSION_DIR"
    else
         echo "Error: 'kaggle' command not found and cannot find docker-compose."
         exit 1
    fi
fi

echo "Done! Check status at: https://www.kaggle.com/${KAGGLE_USERNAME}/${TITLE_SLUG}"

