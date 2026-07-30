from datetime import datetime
from bson import ObjectId
from app.schemas.note_schema import NoteCreateSchema
from app.repositories.note_repository import NoteRepository

class NoteService:
    def __init__(self):
        self.note_repo=NoteRepository()

    def create_note(self, note_data: NoteCreateSchema, user_id:str = "gress"):
        data =note_data.dict()

        data["create_at"]=datetime.now()
        data["update_at"]=datetime.now()
        data["user_id"]=user_id

        note_id=self.note_repo.create_note(data)

        return {"id":note_id,
                "message":"Tạo ghi chú thành công"
                }

    def update_note(self, note_id: str, note_data: NoteCreateSchema, user_id:str = "gress"):
        if not ObjectId.is_valid(note_id):
            raise ValueError("ID ghi chú không hợp lệ")

        data = note_data.dict()
        data["update_at"] = datetime.now()
        data["user_id"] = user_id

        updated = self.note_repo.update_note(note_id, data)
        if not updated:
            raise ValueError("Không tìm thấy ghi chú để cập nhật")

        return {"id": note_id,
                "message": "Cập nhật ghi chú thành công"}

    def get_all_notes(self):
        notes = self.note_repo.get_all_notes()
        return notes
