from pydantic import BaseModel, Field
from typing import Optional


class CategoryCreateSchema(BaseModel):
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    user_id: Optional[str] = None


class CategoryUpdateSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
