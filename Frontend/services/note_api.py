from typing import Any, Optional, Tuple, Dict
from Frontend.services.api_client import APIClient

class NoteAPI:
    @staticmethod
    def _parse_error(response) -> str:
        """Hàm phụ trợ để bắt lỗi JSON an toàn, chống crash app."""
        try:
            return response.json().get("detail", "Lỗi không xác định từ máy chủ")
        except ValueError:
            return f"Lỗi hệ thống hoặc mất kết nối (Mã lỗi: {response.status_code})"

    @staticmethod
    def _build_payload(
        title: str, content: str, category: str, priority: str, 
        reminder_time: Optional[str], image_url: Optional[str],
        status: Optional[str] = None  # ✅ THÊM status VÀO ĐÂY
    ) -> Dict[str, Any]:
        """Gom chung logic tạo dữ liệu gửi lên để không bị lặp code."""
        payload = {
            "title": title,
            "content": content,
            "category": category,
            "priority": priority,
            "reminder_time": reminder_time,
            "image_url": image_url,
        }
        # Chỉ đẩy status vào payload nếu có giá trị (tránh lỗi khi tạo mới)
        if status:
            payload["status"] = status
            
        return payload

    @staticmethod
    def get_all() -> Tuple[bool, Any]:
        """Lấy danh sách các ghi chú của user đang đăng nhập."""
        res = APIClient.get("/api/notes/")
        if res.status_code == 200:
            return True, res.json()
        return False, NoteAPI._parse_error(res)

    @staticmethod
    def search(keyword: str = "") -> Tuple[bool, Any]:
        """Tìm kiếm ghi chú."""
        params = {"keyword": keyword} if keyword else {}
        res = APIClient.get("/api/notes/search", params=params)
        if res.status_code == 200:
            return True, res.json()
        return False, NoteAPI._parse_error(res)

    @staticmethod
    def get_statistics(period: str = "day") -> Tuple[bool, Any]:
        """Lấy thống kê ghi chú."""
        res = APIClient.get("/api/notes/statistics", params={"period": period})
        if res.status_code == 200:
            return True, res.json()
        return False, NoteAPI._parse_error(res)

    @staticmethod
    def create_note(
        title: str, content: str, category: str, priority: str,
        reminder_time: Optional[str] = None, image_url: Optional[str] = None
    ) -> Tuple[bool, str]:
        """Tạo ghi chú mới."""
        payload = NoteAPI._build_payload(title, content, category, priority, reminder_time, image_url)
        res = APIClient.post("/api/notes/", data=payload)
        
        if res.status_code == 201:
            return True, "Thêm Ghi Chú Thành Công"
        return False, NoteAPI._parse_error(res)

    @staticmethod
    def update_note(
        note_id: str, title: str, content: str, category: str, priority: str,
        reminder_time: Optional[str] = None, image_url: Optional[str] = None,
        status: Optional[str] = None  # ✅ THÊM status VÀO ĐÂY
    ) -> Tuple[bool, str]:
        """Cập nhật ghi chú đã có."""
        # Truyền status xuống _build_payload
        payload = NoteAPI._build_payload(title, content, category, priority, reminder_time, image_url, status)
        res = APIClient.put(f"/api/notes/{note_id}", data=payload)
        
        if res.status_code == 200:
            return True, "Cập Nhật Ghi Chú Thành Công"
        return False, NoteAPI._parse_error(res)

    @staticmethod
    def delete_note(note_id: str) -> Tuple[bool, str]:
        """Xóa ghi chú theo ID."""
        res = APIClient.delete(f"/api/notes/{note_id}")
        if res.status_code == 200:
            return True, "Xóa Ghi Chú Thành Công"
        return False, NoteAPI._parse_error(res)