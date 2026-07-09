"""
Abstract repository interface. Both mock (in-memory) and future real
(SQLAlchemy) repositories implement this same interface, so services
never know or care which one they're talking to.
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    @abstractmethod
    async def get_by_id(self, entity_id: int) -> T | None: ...

    @abstractmethod
    async def list_all(self) -> list[T]: ...

    @abstractmethod
    async def create(self, entity: T) -> T: ...

    @abstractmethod
    async def update(self, entity_id: int, updates: dict) -> T | None: ...

    @abstractmethod
    async def delete(self, entity_id: int) -> bool: ...
