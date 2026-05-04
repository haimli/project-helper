import json

from app.agent.prompts import READING_GUIDE_PROMPT
from app.services.llm_service import LLMService


class ReadingGuideGenerator:
    def __init__(self, llm: LLMService) -> None:
        self.llm = llm

    async def generate(self, repo_path: str, dir_tree: str, core_modules: list[dict]) -> list[dict]:
        modules_desc = json.dumps(core_modules, ensure_ascii=False, indent=2)
        user_prompt = f"Directory structure:\n{dir_tree}\n\nCore modules:\n{modules_desc}"
        response = await self.llm.analyze(READING_GUIDE_PROMPT, user_prompt)
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return [{"order": 1, "title": "Start Here", "reason": response}]
