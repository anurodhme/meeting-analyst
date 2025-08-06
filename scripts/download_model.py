# File: meeting-analyst/scripts/download_model.py

import os
from pathlib import Path
from huggingface_hub import snapshot_download

# --- Configuration ---
MODEL_REPO = "Qwen/Qwen3-0.6B"        # New repository
MODEL_DIR  = "models"                  # Local root for all downloaded models

def download_model():
    """
    Downloads the full Qwen3-0.6B model (safetensors) into:
        <project-root>/models/Qwen3-0.6B/
    """
    project_root = Path(__file__).parent.parent
    target_dir = project_root / MODEL_DIR / MODEL_REPO.split("/")[-1]  # -> models/Qwen3-0.6B

    print(f"Ensuring model directory exists at: {target_dir}")
    target_dir.mkdir(parents=True, exist_ok=True)

    # snapshot_download pulls the *entire* repo (weights, tokenizer, configs)
    print(f"Downloading '{MODEL_REPO}' into {target_dir} …")
    try:
        snapshot_download(
            repo_id=MODEL_REPO,
            local_dir=str(target_dir),
            local_dir_use_symlinks=False,
            resume_download=True,
        )
        print("\n✅ Download complete!")
        print(f"Model saved to: {target_dir}")

    except Exception as e:
        print(f"\n❌ An error occurred during download: {e}")
        print("Please check your internet connection and that the repository is correct.")

if __name__ == "__main__":
    download_model()