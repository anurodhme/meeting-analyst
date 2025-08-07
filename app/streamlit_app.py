# File: app/streamlit_app.py (Final, Cleaned Version)

import streamlit as st
import pandas as pd
from pathlib import Path
from dataclasses import asdict

# NOTE: The 'sys.path' hack has been removed.
# We will now run streamlit in a way that makes this import work correctly.
from src.analyst import Analyst
from src.schemas import ActionItem

# --- Configuration ---
MODEL_FILENAME = "Qwen3-0.6B-Q8_0.gguf" 
MODEL_PATH = Path("models") / MODEL_FILENAME

# --- Model Loading ---
@st.cache_resource
def load_analyst(model_path: Path) -> Analyst:
    """Loads the Analyst model and caches it."""
    if not model_path.exists():
        st.error(f"Model file not found at {model_path}")
        st.stop()
    return Analyst(model_path=str(model_path), verbose=False)

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Meeting Analyst",
    page_icon="🤖",
    layout="wide"
)

# --- Page Title ---
st.title("🤖 AI Meeting Analyst")
st.markdown("Get a concise summary, key decisions, and action items from your meeting transcript.")

# --- Load the Analyst model ---
with st.spinner(f"Loading AI model ({MODEL_FILENAME})... This may take a moment."):
    analyst = load_analyst(MODEL_PATH)

# --- UI Layout ---
st.header("1. Provide Your Transcript")
input_col, upload_col = st.columns(2)

with input_col:
    transcript_text = st.text_area(
        "Paste the full meeting transcript text here.",
        height=300,
        placeholder="Alice: Hi everyone, let's start the meeting..."
    )

with upload_col:
    uploaded_file = st.file_uploader(
        "Or upload a transcript file (.txt).",
        type=["txt"]
    )

analyze_button = st.button("Analyze Transcript", type="primary", use_container_width=True)

# --- Analysis Logic ---
if analyze_button:
    input_transcript = ""
    if uploaded_file is not None:
        try:
            input_transcript = uploaded_file.getvalue().decode("utf-8")
            st.info("Processing the uploaded file...")
        except Exception as e:
            st.error(f"Error reading file: {e}")
    elif transcript_text.strip():
        input_transcript = transcript_text
        st.info("Processing the text from the text area...")
    else:
        st.warning("Please paste a transcript or upload a file before analyzing.")

    if input_transcript:
        with st.spinner("The AI is analyzing the transcript... Please wait."):
            summary = analyst.summarize(input_transcript)
            decisions = analyst.extract_decisions(input_transcript)
            action_items = analyst.extract_action_items(input_transcript)

        st.success("Analysis complete!")
        
        st.header("2. Analysis Results")
        
        st.subheader("📌 Summary")
        st.markdown(summary)
        
        st.subheader("⚖️ Key Decisions")
        if decisions:
            decision_text = "\n".join(f"{i}. {decision}" for i, decision in enumerate(decisions, 1))
            st.markdown(decision_text)
        else:
            st.markdown("No key decisions were identified.")
        
        st.subheader("✅ Action Items")
        if action_items:
            action_items_df = pd.DataFrame([asdict(item) for item in action_items])
            st.dataframe(action_items_df, use_container_width=True)
        else:
            st.markdown("No action items were identified.")