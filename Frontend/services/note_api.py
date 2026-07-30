import requests
from Frontend.services.api_client import APIClient
from typing import Optional

class NoteAPI:
    @staticmethod
    def get_all(user_id: Optional[str] = None):
        url = f"{APIClient.BASE_URL}/api/notes"
        params = {"user_id": user_id} if user_id else {}
        try:
            res = requests.get(url, params=params, timeout=APIClient.TIMEOUT)
            if res.status_code == 200:
                return True, res.json()
            return False, "Lỗi lấy danh sách ghi chú"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def create_note(title: str, content: str, category: str, priority: str, reminder_time: Optional[str] = None, image_url: Optional[str] = None, user_id: Optional[str] = None):
        url = f"{APIClient.BASE_URL}/api/notes"

        payload = {
            "title": title,
            "content": content,
            "category": category,
            "priority": priority,
            "reminder_time": reminder_time,
            "image_url": image_url,
            "user_id": user_id
        }
    
        try:
            respon = requests.post(url, json=payload, timeout=APIClient.TIMEOUT)
            if respon.status_code == 201:
                return True, "Thêm Ghi Chú Thành Công"
            error_detail = respon.json().get("detail", "Lỗi tạo ghi chú")
            return False, error_detail
        except requests.exceptions.RequestException as e:
            return False, f"Lỗi kết nối API: {str(e)}"
        except requests.exceptions.Timeout:
            return False, "Lỗi: Yêu cầu API đã hết thời gian chờ"
        except Exception as e:
            return False, f"Lỗi không xác định: {str(e)}"
