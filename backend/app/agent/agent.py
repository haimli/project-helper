from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

from app.agent.prompts import PROJECT_AGENT_SYSTEM_PROMPT
from app.agent.tools import create_project_tools
from app.services.llm_service import LLMService


def create_project_agent(repo_path: str, chat_history: list[dict]):
    llm_service = LLMService()
    llm: ChatOpenAI = llm_service.get_streaming_llm()
    tools = create_project_tools(repo_path)

    llm_with_tools = llm.bind_tools(tools)

    prompt = ChatPromptTemplate.from_messages([
        ("system", PROJECT_AGENT_SYSTEM_PROMPT),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ])

    agent = (
        RunnablePassthrough.assign(
            agent_scratchpad=lambda x: x.get("intermediate_steps", []),
        )
        | prompt
        | llm_with_tools
    )

    return agent, tools
