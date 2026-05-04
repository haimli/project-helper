import json

from app.agent.prompts import DESIGN_PATTERNS_PROMPT
from app.services.llm_service import LLMService


class DesignPatternAnalyzer:
    def __init__(self, llm: LLMService) -> None:
        self.llm = llm

    async def analyze(self, repo_path: str, dir_tree: str, key_file_contents: dict[str, str]) -> list[dict]:
        files_summary = "\n\n".join(f"--- {name} ---\n{content[:2000]}" for name, content in list(key_file_contents.items())[:5])
        user_prompt = f"Directory structure:\n{dir_tree}\n\nKey files:\n{files_summary}"
        response = await self.llm.analyze(DESIGN_PATTERNS_PROMPT, user_prompt)
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return [{"name": "unknown", "description": response}]
