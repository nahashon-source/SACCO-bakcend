"""
Shared response schemas. Every endpoint returns ApiResponse[T] — this is
the contract the frontend's ApiResponse<T> type was built against.
"""

from typing import Generic, TypeVar

from pydantic import BaseModel

from app.schemas.base import CamelModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    success: bool
    message: str
    data: T | None = None
    errors: list[str] | None = None


class PaginatedData(CamelModel, Generic[T]):
    items: list[T]
    page: int
    page_size: int
    total_items: int
    total_pages: int
