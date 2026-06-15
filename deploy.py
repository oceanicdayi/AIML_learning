"""Deploy this repository to the matching Hugging Face Space.

Required environment variables:
- HF_TOKEN: a Hugging Face token with write access to the Space

Optional environment variables:
- HF_SPACE_ID: target Space repo id, defaults to oceanicdayi/AIML_learning
"""

import os
from pathlib import Path

from huggingface_hub import HfApi

ROOT = Path(__file__).resolve().parent
SPACE_ID = os.environ.get("HF_SPACE_ID", "oceanicdayi/AIML_learning")
IGNORE_PATTERNS = [
    ".git/*",
    ".github/*",
    "__pycache__/*",
    "*.pyc",
    ".venv/*",
    "venv/*",
    "env/*",
    ".DS_Store",
]


def main() -> None:
    token = os.environ.get("HF_TOKEN")
    if not token:
        raise SystemExit("Missing HF_TOKEN. Add it as a GitHub Actions repository secret.")

    api = HfApi(token=token)
    api.upload_folder(
        folder_path=str(ROOT),
        repo_id=SPACE_ID,
        repo_type="space",
        ignore_patterns=IGNORE_PATTERNS,
        commit_message="Deploy AIML learning app from GitHub Actions",
    )
    print(f"Deployment requested for https://huggingface.co/spaces/{SPACE_ID}")


if __name__ == "__main__":
    main()
