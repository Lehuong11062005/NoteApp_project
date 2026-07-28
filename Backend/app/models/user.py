from pydantic import BaseModel, Field
from typing import Optional

class UserModel(BaseModel):
    id: Optional[str] = None
    username: str
    password: str