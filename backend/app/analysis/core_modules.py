import json

from app.agent.prompts import CORE_MODULES_PROMPT
from app.services.llm_service import LLMService


class CoreModuleAnalyzer:
    def __init__(self, llm: LLMService) -> None:
        self.llm = llm

    async def analyze(self, repo_path: str, dir_tree: str, key_file_contents: dict[str, str]) -> list[dict]:
        files_summary = "\n\n".join(f"--- {name} ---\n{content[:3000]}" for name, content in key_file_contents.items())
        user_prompt = f"Directory structure:\n{dir_tree}\n\nKey files:\n{files_summary}"
        response = await self.llm.analyze(CORE_MODULES_PROMPT, user_prompt)
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return [{"name": "unknown", "responsibility": response}]
