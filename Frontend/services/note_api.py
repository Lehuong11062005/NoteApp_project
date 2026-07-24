import requests
import os
from dotenv import  load_dotenv
from typing import Optional

load_dotenv()

Base_URL=os.getenv("BASE_URL")
TIMEOUT_SECONDS=5

class NoteAPI:
    @staticmethod
    def create_note(title:str, content:str,category:str,priority:str, reminder_time:[str]=None, image_url:Optional[str]=None):
        url=f"{Base_URL}/api/notes"

        payload={
            "title": title,
            "content":content,
            "category":category,
            "priority":priority,
            "reminder_time": reminder_time,
            "image_url": image_url
        }
    
        try:
            respon= requests.post(url, json=payload,timeout=TIMEOUT_SECONDS)
            if respon.status_code== 201:
                return True,"Thêm Ghi Chú Thành Công"
            error_detail=respon.json().get("detail","Lỗi tạo ghi chú")
            return False,error_detail
        except requests.exceptions.RequestException as e:
            return False,f"Lỗi kết nối API: {str(e)}"
        except requests.exceptions.Timeout:
            return False,"Lỗi: Yêu cầu API đã hết thời gian chờ"
        except Exception as e:
            return False,f"Lỗi không xác định: {str(e)}"
    
