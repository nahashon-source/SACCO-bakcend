"""
Shared response schemas. Every endpoint returns ApiResponse[T] — this is
the contract the frontend's ApiResponse<T> type was built against. Never
return a raw Pydantic model or ORM object directly from a route.
"""

from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    success: bool
    message: str
    data: T | None = None
    errors: list[str] | None = None


class PaginatedData(BaseModel, Generic[T]):
    items: list[T]
    page: int
    page_size: int
    total_items: int
    total_pages: int
