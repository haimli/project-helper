from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.chat_session import ChatSession
from app.models.chat_message import ChatMessage


class ChatService:
    @staticmethod
    async def create_session(db: AsyncSession, project_id: int) -> ChatSession:
        session = ChatSession(project_id=project_id)
        db.add(session)
        await db.commit()
        await db.refresh(session)
        return session

    @staticmethod
    async def get_sessions(db: AsyncSession, project_id: int) -> list[ChatSession]:
        result = await db.execute(
            select(ChatSession).where(ChatSession.project_id == project_id).order_by(ChatSession.created_at.desc())
        )
        return list(result.scalars().all())

    @staticmethod
    async def get_session(db: AsyncSession, session_id: int) -> ChatSession | None:
        result = await db.execute(select(ChatSession).where(ChatSession.id == session_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def save_message(
        db: AsyncSession,
        session_id: int,
        role: str,
        content: str,
        tool_name: str | None = None,
        tool_input: str | None = None,
    ) -> ChatMessage:
        msg = ChatMessage(session_id=session_id, role=role, content=content, tool_name=tool_name, tool_input=tool_input)
        db.add(msg)
        await db.commit()
        await db.refresh(msg)
        return msg

    @staticmethod
    async def get_messages(db: AsyncSession, session_id: int) -> list[ChatMessage]:
        result = await db.execute(
            select(ChatMessage).where(ChatMessage.session_id == session_id).order_by(ChatMessage.created_at.asc())
        )
        return list(result.scalars().all())

    @staticmethod
    async def get_chat_history(db: AsyncSession, session_id: int) -> list[dict]:
        messages = await ChatService.get_messages(db, session_id)
        history = []
        for msg in messages:
            if msg.role == "user":
                history.append({"role": "user", "content": msg.content})
            elif msg.role == "assistant":
                history.append({"role": "assistant", "content": msg.content})
        return history
