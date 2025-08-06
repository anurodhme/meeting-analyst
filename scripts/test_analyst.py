# File: scripts/test_analyst.py

from pathlib import Path
from src.analyst import Analyst

# --- Configuration ---
# Define the paths relative to the project root.
MODEL_PATH = "/Users/anurodhbudhathoki/meeting-analyst/models/Qwen3-0.6B"
TRANSCRIPT_PATH = "/Users/anurodhbudhathoki/meeting-analyst/data/sample_transcripts/demo.txt"

def run_test():
    """
    Runs a full analysis on the demo transcript and prints the results.
    """
    print("--- 🚀 Starting Analyst Smoke Test ---")

    # Ensure the necessary files exist before starting.
    if not Path(MODEL_PATH).exists():
        print(f"❌ ERROR: Model file not found at {MODEL_PATH}")
        print("Please run the download script first: python scripts/download_model.py")
        return
    
    if not Path(TRANSCRIPT_PATH).exists():
        print(f"❌ ERROR: Demo transcript not found at {TRANSCRIPT_PATH}")
        return

    # 1. Read the transcript data from the file.
    print(f"\n📖 Reading transcript from: {TRANSCRIPT_PATH}")
    with open(TRANSCRIPT_PATH, 'r') as f:
        transcript_text = f.read()

    # 2. Initialize our Analyst class with the model.
    #    (This will take a moment as it loads the model into memory)
    analyst = Analyst(model_path=MODEL_PATH)

    # 3. Run the analysis methods.
    summary = analyst.summarize(transcript_text)
    decisions = analyst.extract_decisions(transcript_text)
    action_items = analyst.extract_action_items(transcript_text)

    # 4. Print the results in a clean format.
    print("\n\n--- 📊 ANALYSIS RESULTS ---")
    
    print("\n📌 SUMMARY:")
    print(summary)

    print("\n⚖️ KEY DECISIONS:")
    if decisions:
        for i, decision in enumerate(decisions, 1):
            print(f"  {i}. {decision}")
    else:
        print("  No decisions found.")

    print("\n✅ ACTION ITEMS:")
    if action_items:
        for item in action_items:
            print(f"  - Task:       {item.task}")
            print(f"    Owner:      {item.owner}")
            print(f"    Deadline:   {item.deadline}")
            print("-" * 20)
    else:
        print("  No action items found.")
    
    print("\n--- ✅ Test Complete ---")


if __name__ == "__main__":
    run_test()