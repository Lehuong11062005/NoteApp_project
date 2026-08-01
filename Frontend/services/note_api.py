from Frontend.services.api_client import APIClient
from typing import Optional


class NoteAPI:
    @staticmethod
    def get_all(user_id: Optional[str] = None):
        try:
            params = {"user_id": user_id} if user_id else {}
            res = APIClient.get("/api/notes/", params=params)
            if res.status_code == 200:
                return True, res.json()
            
            error_detail = res.json().get("detail", "Lỗi lấy danh sách ghi chú")
            return False, error_detail
        except Exception as e:
            return False, str(e)

    @staticmethod
    def create_note(
        title: str,
        content: str,
        category: str,
        priority: str,
        reminder_time: Optional[str] = None,
        image_url: Optional[str] = None,
        user_id: Optional[str] = None,
    ):
        payload = {
            "title": title,
            "content": content,
            "category": category,
            "priority": priority,
            "reminder_time": reminder_time,
            "image_url": image_url,
            "user_id": user_id,
        }

        try:
            response = APIClient.post("/api/notes/", data=payload)
            if response.status_code == 201:
                return True, "Thêm Ghi Chú Thành Công"
            
            error_detail = response.json().get("detail", "Lỗi tạo ghi chú")
            return False, error_detail
        except Exception as e:
            return False, f"Lỗi kết nối API: {str(e)}"

    @staticmethod
    def update_note(
        note_id: str,
        title: str,
        content: str,
        category: str,
        priority: str,
        reminder_time: Optional[str] = None,
        image_url: Optional[str] = None,
    ):
        payload = {
            "title": title,
            "content": content,
            "category": category,
            "priority": priority,
            "reminder_time": reminder_time,
            "image_url": image_url,
        }

        try:
            response = APIClient.put(f"/api/notes/{note_id}", data=payload)
            if response.status_code == 200:
                return True, "Cập nhật Ghi Chú Thành Công"

            error_detail = response.json().get("detail", "Lỗi cập nhật ghi chú")
            return False, error_detail
        except Exception as e:
            return False, f"Lỗi kết nối API: {str(e)}"