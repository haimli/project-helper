import asyncio
from typing import TypedDict


class ProgressEvent(TypedDict):
    stage: str
    progress: int
    detail: str


class ProgressManager:
    _instance: "ProgressManager | None" = None
    _subscribers: dict[int, list[asyncio.Queue[ProgressEvent]]]

    def __init__(self) -> None:
        self._subscribers = {}

    @classmethod
    def get_instance(cls) -> "ProgressManager":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    async def subscribe(self, project_id: int) -> asyncio.Queue[ProgressEvent]:
        queue: asyncio.Queue[ProgressEvent] = asyncio.Queue()
        if project_id not in self._subscribers:
            self._subscribers[project_id] = []
        self._subscribers[project_id].append(queue)
        return queue

    def unsubscribe(self, project_id: int, queue: asyncio.Queue[ProgressEvent]) -> None:
        if project_id in self._subscribers:
            self._subscribers[project_id].remove(queue)
            if not self._subscribers[project_id]:
                del self._subscribers[project_id]

    async def emit(self, project_id: int, event: ProgressEvent) -> None:
        if project_id in self._subscribers:
            for queue in self._subscribers[project_id]:
                await queue.put(event)

    async def complete(self, project_id: int) -> None:
        await self.emit(project_id, ProgressEvent(stage="complete", progress=100, detail="Analysis complete"))
        if project_id in self._subscribers:
            del self._subscribers[project_id]
