from app.agent.prompts import DATA_FLOW_PROMPT
from app.services.llm_service import LLMService


class DataFlowAnalyzer:
    def __init__(self, llm: LLMService) -> None:
        self.llm = llm

    async def analyze(self, repo_path: str, dir_tree: str, core_modules: list[dict], key_file_contents: dict[str, str]) -> str:
        import json

        modules_desc = json.dumps(core_modules, ensure_ascii=False, indent=2)
        files_summary = "\n\n".join(f"--- {name} ---\n{content[:2000]}" for name, content in list(key_file_contents.items())[:5])
        user_prompt = f"Directory structure:\n{dir_tree}\n\nCore modules:\n{modules_desc}\n\nKey files:\n{files_summary}"
        return await self.llm.analyze(DATA_FLOW_PROMPT, user_prompt)
