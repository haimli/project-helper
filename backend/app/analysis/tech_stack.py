import json

from app.agent.prompts import TECH_STACK_PROMPT
from app.services.llm_service import LLMService


class TechStackAnalyzer:
    def __init__(self, llm: LLMService) -> None:
        self.llm = llm

    async def analyze(self, repo_path: str, key_file_contents: dict[str, str]) -> dict:
        files_summary = "\n\n".join(f"--- {name} ---\n{content[:3000]}" for name, content in key_file_contents.items())
        user_prompt = f"Here are the key configuration/dependency files from the project:\n\n{files_summary}"
        response = await self.llm.analyze(TECH_STACK_PROMPT, user_prompt)
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"raw": response}
