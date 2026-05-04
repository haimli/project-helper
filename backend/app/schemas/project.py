from datetime import datetime

from pydantic import BaseModel, HttpUrl


class ProjectCreate(BaseModel):
    repo_url: str


class ProjectResponse(BaseModel):
    id: int
    repo_url: str
    repo_name: str
    status: str
    error_message: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ProjectListResponse(BaseModel):
    items: list[ProjectResponse]
    total: int
