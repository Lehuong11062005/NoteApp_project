from datetime import datetime
from app.repositories.reminder_repository import ReminderRepository
from app.schemas.reminder_schema import ReminderCreateSchema, ReminderUpdateSchema


class ReminderService:
    def __init__(self):
        self.reminder_repo = ReminderRepository()

    def create_reminder(self, reminder_data: ReminderCreateSchema):
        data = reminder_data.dict()
        data["created_at"] = datetime.now()
        data["updated_at"] = datetime.now()
        reminder_id = self.reminder_repo.create_reminder(data)
        return {
            "id": reminder_id,
            "message": "Tạo nhắc nhở thành công"
        }

    def get_reminders_by_user(self, user_id: str):
        return self.reminder_repo.get_reminders_by_user(user_id)

    def update_reminder(self, reminder_id: str, reminder_data: ReminderUpdateSchema):
        update_data = reminder_data.dict(exclude_unset=True)
        if not update_data:
            return {"message": "Không có dữ liệu để cập nhật"}
        self.reminder_repo.update_reminder(reminder_id, update_data)
        return {"message": "Cập nhật nhắc nhở thành công"}

    def delete_reminder(self, reminder_id: str):
        deleted_count = self.reminder_repo.delete_reminder(reminder_id)
        return {
            "deleted_count": deleted_count,
            "message": "Xóa nhắc nhở thành công" if deleted_count else "Không tìm thấy nhắc nhở"
        }
