# File: src/analyst.py

import json
import typing
from pathlib import Path
from llama_cpp import Llama
from pydantic import ValidationError, TypeAdapter

# Import our custom modules
from . import prompts
from . import schemas

class Analyst:
    """
    The core class that loads the LLM and performs analysis tasks.
    """    
    def __init__(self, model_path: str, verbose: bool = True):
        """
        Initializes the Analyst by loading the specified GGUF model.

        Args:
            model_path (str): The file path to the GGUF language model.
            verbose (bool): Whether to print status messages. Defaults to True.
        """
        self.verbose = verbose
        if self.verbose:
            print("🤖 Initializing Analyst...")
        if not Path(model_path).exists():
            raise FileNotFoundError(f"Model file not found at {model_path}")

        # Load the language model from the given path.
        # n_gpu_layers=-1 attempts to offload all layers to the GPU (Metal on macOS).
        # n_ctx sets the context window size, which is the maximum number of tokens
        # the model can consider at once. 4096 is a good default for modern models.
        # verbose=False keeps the console output clean from llama.cpp's own logs.
        self.llm = Llama(
            model_path=model_path,
            n_gpu_layers=-1,
            n_ctx=4096,
            verbose=False,
            chat_format="chatml", # Qwen2 models use the ChatML format
        )

        # Pre-generate the JSON schema for action items for efficiency.
        self.action_item_schema = schemas.ActionItem.model_json_schema()
        if self.verbose:
            print("✅ Analyst initialized successfully.")

    def _create_chat_completion(self, prompt: str, temperature: float = 0.2) -> str:
        """
        A helper method to run a chat completion with the loaded model.
        """
        response = self.llm.create_chat_completion(
            messages=[
                {"role": "system", "content": "You are a helpful meeting analysis assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
        )
        # Extract the content from the response.
        content = response['choices'][0]['message']['content']
        return content.strip() if content else ""

    def summarize(self, transcript: str) -> str:
        """
        Generates a summary for the given transcript.

        Args:
            transcript (str): The meeting transcript text.

        Returns:
            str: The generated summary.
        """
        if self.verbose:
            print("⏳ Generating summary...")
        prompt = prompts.PROMPT_SUMMARY.format(transcript=transcript)
        summary = self._create_chat_completion(prompt)
        if self.verbose:
            print("✅ Summary generated.")
        return summary

    def extract_decisions(self, transcript: str) -> list[str]:
        """
        Extracts key decisions from the given transcript.

        Args:
            transcript (str): The meeting transcript text.

        Returns:
            list[str]: A list of key decisions.
        """
        if self.verbose:
            print("⏳ Extracting decisions...")
        prompt = prompts.PROMPT_DECISIONS.format(transcript=transcript)
        response_text = self._create_chat_completion(prompt)

        # Parse the numbered list output into a Python list
        decisions = [
            line.strip() for line in response_text.split('\n')
            if line.strip() and line.strip()[0].isdigit()
        ]
        if self.verbose:
            print(f"✅ Found {len(decisions)} decisions.")
        return decisions

    def extract_action_items(self, transcript: str) -> list[schemas.ActionItem]:
        """
        Extracts action items from the transcript and validates them against the schema.

        Args:
            transcript (str): The meeting transcript text.

        Returns:
            list[schemas.ActionItem]: A list of validated ActionItem objects.
        """
        if self.verbose:
            print("⏳ Extracting action items...")
        prompt = prompts.PROMPT_ACTION_ITEMS.format(
            schema=self.action_item_schema,
            transcript=transcript
        )

        # We set a very low temperature to make the JSON output more reliable.
        json_output = self._create_chat_completion(prompt, temperature=0.0)

        try:
            # Pydantic's TypeAdapter is a powerful tool to parse and validate
            # JSON data directly into a list of our Pydantic models.
            # This is more robust than using json.loads() and a manual loop.
            adapter = TypeAdapter(typing.List[schemas.ActionItem])
            action_items = adapter.validate_json(json_output)
            if self.verbose:
                print(f"✅ Found and validated {len(action_items)} action items.")
            return action_items
        except (ValidationError, json.JSONDecodeError) as e:
            if self.verbose:
                print(f"❌ Error parsing or validating action items JSON: {e}")
                print(f"   LLM Output that failed parsing:\n---\n{json_output}\n---")
            return []