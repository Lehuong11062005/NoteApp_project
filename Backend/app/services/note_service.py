from datetime import datetime
from app.schemas.note_schema import NoteCreateSchema
from app.repositories.note_repository import NoteRepository

class NoteService:
    def __init__(self):
        self.note_repo=NoteRepository()

    def create_note(self, note_data: NoteCreateSchema, user_id:str):
        data =note_data.dict()

        data["create_at"]=datetime.now()
        data["update_at"]=datetime.now()
        data["user_id"]=user_id

        note_id=self.note_repo.create_note(data)

        return {"id":note_id,
                "message":"Tạo ghi chú thành công"
                }