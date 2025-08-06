# src/analyst.py
from __future__ import annotations
from dataclasses import dataclass
from typing import List
from llama_cpp import Llama

@dataclass
class ActionItem:
    task: str
    owner: str
    deadline: str


class Analyst:
    """
    Meeting-analysis helper powered by a Qwen3-0.6B GGUF file via llama-cpp-python.
    """

    def __init__(self, model_path: str):
        self.llm = Llama(
            model_path=model_path,
            n_ctx=4096,          # adjust if your meetings are longer
            verbose=False,
            chat_format="chatml"  # Qwen models use ChatML
        )

    # --------------- internal helper ---------------
    def _chat(self, system: str, user: str, max_tokens: int = 512) -> str:
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ]
        out = self.llm.create_chat_completion(
            messages=messages,
            max_tokens=max_tokens,
            temperature=0.7
        )
        return out["choices"][0]["message"]["content"].strip()

    # --------------- public API ---------------
    def summarize(self, transcript: str) -> str:
        system = "You are a concise meeting assistant. Provide 3–6 bullet-point summary."
        return self._chat(system, transcript, max_tokens=400)

    def extract_decisions(self, transcript: str) -> List[str]:
        system = (
            "Return ONLY a numbered list of concrete decisions made in the meeting. "
            "Each decision on its own line."
        )
        raw = self._chat(system, transcript, max_tokens=300)
        return [line.lstrip("1234567890.- ") for line in raw.splitlines() if line.strip()]

    def extract_action_items(self, transcript: str) -> List[ActionItem]:
        system = (
            "Extract action items in CSV format exactly: Task,Owner,Deadline\n"
            "No headers, no extra lines."
        )
        raw = self._chat(system, transcript, max_tokens=500)
        items = []
        for line in raw.splitlines():
            if "," not in line:
                continue
            parts = [p.strip() for p in line.split(",", 2)]
            if len(parts) == 3:
                items.append(ActionItem(*parts))
        return items

if __name__ == "__main__":
    agent = Analyst(model_path="/Users/anurodhbudhathoki/meeting-analyst/models/Qwen3-0.6B-Q8_0.gguf")
    transcript = open("data/sample_transcripts/demo.txt").read()
    print(agent.summarize(transcript))