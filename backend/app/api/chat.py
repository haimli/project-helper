import json
from typing import AsyncGenerator

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sse_starlette.sse import EventSourceResponse

from app.database import get_db
from app.models.chat_session import ChatSession
from app.models.project import Project
from app.schemas.chat import MessageCreate, MessageListResponse, MessageResponse, SessionCreate, SessionListResponse, SessionResponse
from app.services.chat_service import ChatService
from app.services.git_service import GitService

router = APIRouter()


@router.post("/sessions", response_model=SessionResponse)
async def create_session(request: SessionCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Project).where(Project.id == request.project_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Project not found")
    session = await ChatService.create_session(db, request.project_id)
    return session


@router.get("/sessions", response_model=SessionListResponse)
async def list_sessions(project_id: int, db: AsyncSession = Depends(get_db)):
    sessions = await ChatService.get_sessions(db, project_id)
    return SessionListResponse(items=sessions)


@router.get("/{session_id}/messages", response_model=MessageListResponse)
async def get_messages(session_id: int, db: AsyncSession = Depends(get_db)):
    session = await ChatService.get_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    messages = await ChatService.get_messages(db, session_id)
    return MessageListResponse(items=messages)


@router.post("/{session_id}/messages")
async def send_message(
    session_id: int,
    request: MessageCreate,
    db: AsyncSession = Depends(get_db),
):
    session = await ChatService.get_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    result = await db.execute(select(Project).where(Project.id == session.project_id))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    await ChatService.save_message(db, session_id, "user", request.content)

    if session.title == "New Chat":
        session.title = request.content[:50]
        await db.commit()

    chat_history = await ChatService.get_chat_history(db, session_id)
    git = GitService()
    repo_path = git.get_repo_local_path(project.repo_name)

    from app.agent.agent import create_project_agent
    agent_runnable, agent_tools = create_project_agent(repo_path, chat_history)

    async def event_generator() -> AsyncGenerator[dict, None]:
        full_response = ""
        try:
            async for event in agent_runnable.astream_events(
                {"input": request.content, "chat_history": chat_history},
                version="v2",
            ):
                kind = event.get("event")
                if kind == "on_chat_model_stream":
                    chunk = event["data"]["chunk"]
                    content = chunk.content if hasattr(chunk, "content") else str(chunk)
                    if content:
                        full_response += content
                        yield {"event": "token", "data": json.dumps({"content": content})}

                elif kind == "on_tool_start":
                    tool_name = event.get("name", "unknown")
                    tool_input = event.get("data", {}).get("input", {})
                    yield {"event": "tool_call", "data": json.dumps({"tool": tool_name, "input": tool_input})}

                elif kind == "on_tool_end":
                    tool_name = event.get("name", "unknown")
                    output = event.get("data", {}).get("output", "")
                    yield {"event": "tool_result", "data": json.dumps({"tool": tool_name, "output": str(output)})}

            yield {"event": "done", "data": json.dumps({})}

        except Exception as e:
            yield {"event": "error", "data": json.dumps({"detail": str(e)})}
            full_response = f"Error: {e}"

        finally:
            if full_response:
                await ChatService.save_message(db, session_id, "assistant", full_response)

    return EventSourceResponse(event_generator())
