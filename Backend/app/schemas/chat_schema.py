from pydantic import BaseModel

class ChatRequestSchema(BaseModel):
    user_id: str
    message: str