from langchain_openai import ChatOpenAI

from app.config import settings


class LLMService:
    def __init__(self) -> None:
        self._llm = ChatOpenAI(
            model=settings.DEEPSEEK_MODEL,
            openai_api_key=settings.DEEPSEEK_API_KEY,
            openai_api_base=settings.DEEPSEEK_API_BASE,
            temperature=0.3,
        )
        self._streaming_llm = ChatOpenAI(
            model=settings.DEEPSEEK_MODEL,
            openai_api_key=settings.DEEPSEEK_API_KEY,
            openai_api_base=settings.DEEPSEEK_API_BASE,
            temperature=0.3,
            streaming=True,
        )

    async def analyze(self, system_prompt: str, user_prompt: str) -> str:
        from langchain_core.messages import SystemMessage, HumanMessage

        messages = [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]
        response = await self._llm.ainvoke(messages)
        return response.content

    def get_streaming_llm(self) -> ChatOpenAI:
        return self._streaming_llm
