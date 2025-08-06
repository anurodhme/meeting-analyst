# File: src/prompts.py

# This file contains the prompt templates for interacting with the LLM.
# A good prompt is specific, gives clear instructions, and provides examples.

# --- Prompt Templates ---

# Note: We use {transcript} as a placeholder.
# We will insert the actual transcript text into it later using .format().
PROMPT_SUMMARY = """
You are an expert meeting analyst. Your task is to provide a concise summary of the following meeting transcript.
Focus on the key outcomes, talking points, and overall sentiment of the meeting.
Format the summary as 3-5 key bullet points.

Here is the transcript:
---
{transcript}
---

Summary in bullet points:
"""

# Note: We use {transcript} as a placeholder.
PROMPT_DECISIONS = """
You are an expert meeting analyst. Your task is to extract all key decisions made during the meeting from the following transcript.
A decision is a firm conclusion or resolution that has been agreed upon.
List each decision clearly and concisely as a numbered list. If no decisions were made, state "No key decisions were made."

Here is the transcript:
---
{transcript}
---

Key Decisions:
"""

# NOTE: This is a standard template string, not an f-string.
# We will insert the JSON schema and the transcript into the {schema} and {transcript}
# placeholders later in our main application logic. This is a more robust method.
PROMPT_ACTION_ITEMS = """
You are an expert meeting analyst. Your task is to identify and extract all action items from the following meeting transcript.
An action item is a discrete task to be completed by one or more individuals by a specific deadline.

Analyze the transcript and for each action item, extract the following information:
1.  **task**: The specific action to be taken.
2.  **owner**: The person or group responsible for the task.
3.  **deadline**: The deadline for the task.

Respond ONLY with a valid JSON array of objects that conforms to the following JSON Schema. Do NOT include any other text, explanations, or apologies in your response.

### JSON Schema:
```json
{schema}
Transcript:
{transcript}
JSON Output:
"""