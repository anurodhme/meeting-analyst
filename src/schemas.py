# File: src/schemas.py

from pydantic import BaseModel, Field

# Pydantic models define the structure of our desired output.
# By using them, we can ensure the LLM's output is structured and validated.

class ActionItem(BaseModel):
    """
    Represents a single action item extracted from a meeting transcript.
    """
    task: str = Field(description="The specific, concise action to be taken. Must be a complete sentence.")
    owner: str = Field(description="The person or group responsible for the task. If not mentioned, assign to 'Team'.")
    deadline: str = Field(description="The deadline for completing the task. Be specific, e.g., 'EOD Friday, Aug 8, 2025'. If not mentioned, state 'Not specified'.")

    class Config:
        # This allows us to generate a JSON schema example for the model.
        schema_extra = {
            "example": {
                "task": "Finalize the quarterly report and send it to management.",
                "owner": "Alice",
                "deadline": "End of Day, August 8, 2025"
            }
        }