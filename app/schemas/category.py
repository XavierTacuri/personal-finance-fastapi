from sqlmodel import SQLModel
from pydantic import field_validator
from datetime import datetime
class Category(SQLModel):
    name: str
    @field_validator("name")
    def normalize_name(cls, v):
        return v.strip().lower()

class CategoryOut(Category):
    id: int
    user_id: int
    is_active: bool
    created_at: datetime