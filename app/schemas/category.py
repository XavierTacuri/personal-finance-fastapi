from sqlmodel import SQLModel
from pydantic import field_validator

class Category(SQLModel):
    name: str
    @field_validator("name")
    def normalize_name(cls, v):
        return v.strip().lower()
