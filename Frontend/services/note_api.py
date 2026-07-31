from services.api_client import APIClient
from typing import Optional

class NoteAPI:
    @staticmethod
    def get_all():
        try:
            # Dùng luôn APIClient.get để tự động gắn Token và Header
            res = APIClient.get("/api/notes/")
            if res.status_code == 200:
                return True, res.json()
            
            error_detail = res.json().get("detail", "Lỗi lấy danh sách ghi chú")
            return False, error_detail
        except Exception as e:
            return False, str(e)

    @staticmethod
    def create_note(title: str, content: str, category: str, priority: str, reminder_time: Optional[str] = None, image_url: Optional[str] = None):
        payload = {
            "title": title,
            "content": content,
            "category": category,
            "priority": priority,
            "reminder_time": reminder_time,
            "image_url": image_url
        }
    
        try:
            # Dùng luôn APIClient.post để tự động gắn Token và Header
            respon = APIClient.post("/api/notes/", data=payload)
            if respon.status_code == 201:
                return True, "Thêm Ghi Chú Thành Công"
                
            error_detail = respon.json().get("detail", "Lỗi tạo ghi chú")
            return False, error_detail
            
        except Exception as e:
            return False, f"Lỗi kết nối API: {str(e)}"