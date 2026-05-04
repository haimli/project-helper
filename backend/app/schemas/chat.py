from datetime import datetime

from pydantic import BaseModel


class SessionCreate(BaseModel):
    project_id: int


class SessionResponse(BaseModel):
    id: int
    project_id: int
    title: str
    created_at: datetime

    model_config = {"from_attributes": True}


class MessageCreate(BaseModel):
    content: str


class MessageResponse(BaseModel):
    id: int
    session_id: int
    role: str
    content: str
    tool_name: str | None = None
    tool_input: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class SessionListResponse(BaseModel):
    items: list[SessionResponse]


class MessageListResponse(BaseModel):
    items: list[MessageResponse]
