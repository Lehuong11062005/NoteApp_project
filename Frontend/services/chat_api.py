import os
import requests

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")


from Frontend.services.api_client import APIClient

class ChatAPI:
    @staticmethod
    def send_message(user_id: str, message: str):
        """Gửi câu hỏi lên Backend FastAPI đồng bộ với NoteAPI"""
        payload = {
            "user_id": user_id, 
            "message": message
        }
        
        # Sử dụng APIClient thay vì requests gốc
        res = APIClient.post("/api/chat", data=payload)

        if res.status_code == 200:
            data = res.json()
            return True, data.get("reply", "Không nhận được phản hồi.")
        else:
            # Tận dụng luôn hàm _parse_error nếu bạn muốn, 
            # hoặc báo lỗi thẳng như hiện tại
            return False, f"Lỗi Server ({res.status_code}): {res.text}"