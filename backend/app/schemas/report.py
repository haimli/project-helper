from datetime import datetime

from pydantic import BaseModel


class TechStackItem(BaseModel):
    languages: list[dict]
    frameworks: list[dict]
    build_tools: list[str]
    runtime: list[str]


class CoreModuleItem(BaseModel):
    name: str
    path: str
    responsibility: str
    key_files: list[str]
    depends_on: list[str]


class DesignPatternItem(BaseModel):
    name: str
    description: str
    examples: list[str]


class ReadingSuggestionItem(BaseModel):
    order: int
    title: str
    reason: str
    path: str


class ReportResponse(BaseModel):
    id: int
    project_id: int
    overview: str
    tech_stack: str
    directory_structure: str
    core_modules: str
    data_flow: str
    design_patterns: str
    reading_suggestions: str
    created_at: datetime

    model_config = {"from_attributes": True}
