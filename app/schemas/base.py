"""
Base schema with camelCase JSON serialization. The frontend's TypeScript
types (ApiResponse<T>, PaginatedData<T>, and every domain type) use
camelCase — this base class converts our snake_case Python field names
to camelCase automatically on output, so the two codebases don't drift
apart field-name-by-field-name.

Inherit CamelModel instead of BaseModel for any schema returned to the
frontend. Internal-only models (app/models/*) stay snake_case as normal
Python convention — this conversion is strictly an API-boundary concern.
"""

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class CamelModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )
