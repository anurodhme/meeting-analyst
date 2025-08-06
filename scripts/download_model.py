# File: meeting-analyst/scripts/download_model.py

import os
from pathlib import Path
from huggingface_hub import hf_hub_download  # <-- single-file downloader

# --- Configuration ---
MODEL_REPO = "Qwen/Qwen3-0.6B-GGUF"
MODEL_FILE = "Qwen3-0.6B-Q8_0.gguf"
MODEL_DIR  = "models"

def download_model():
    """
    Downloads the specified Qwen3-0.6B GGUF file into models/
    """
    project_root = Path(__file__).parent.parent
    model_path   = project_root / MODEL_DIR
    target_file  = model_path / MODEL_FILE

    print(f"Ensuring model directory exists at: {model_path}")
    model_path.mkdir(parents=True, exist_ok=True)

    if target_file.exists():
        print(f"✅ Model already exists at {target_file}. Skipping download.")
        return

    print(f"Downloading {MODEL_FILE} from {MODEL_REPO}...")
    try:
        hf_hub_download(
            repo_id=MODEL_REPO,
            filename=MODEL_FILE,
            local_dir=str(model_path),
            local_dir_use_symlinks=False,
            resume_download=True,
        )
        print("\n✅ Download complete!")
        print(f"Model saved to: {target_file}")

    except Exception as e:
        print(f"\n❌ An error occurred during download: {e}")
        print("Please check your internet connection and that the repository and filename are correct.")

if __name__ == "__main__":
    download_model()