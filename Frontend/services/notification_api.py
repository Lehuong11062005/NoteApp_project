from Frontend.services.api_client import APIClient


class NotificationAPI:
    @staticmethod
    def get_notifications(skip: int = 0, limit: int = 50):
        res = APIClient.get(f"/api/notifications/?skip={skip}&limit={limit}")
        if res.status_code == 200:
            return True, res.json()
        try:
            err = res.json().get("detail", "Không thể lấy danh sách thông báo")
        except Exception:
            err = "Lỗi kết nối máy chủ"
        return False, err

    @staticmethod
    def get_unread_count():
        res = APIClient.get("/api/notifications/unread-count")
        if res.status_code == 200:
            return True, res.json().get("unread_count", 0)
        return False, 0

    @staticmethod
    def mark_as_read(notif_id: str):
        res = APIClient.put(f"/api/notifications/{notif_id}/read")
        if res.status_code == 200:
            return True, res.json()
        try:
            err = res.json().get("detail", "Không thể đánh dấu đã đọc")
        except Exception:
            err = "Lỗi kết nối máy chủ"
        return False, err

    @staticmethod
    def mark_all_as_read():
        res = APIClient.put("/api/notifications/read-all")
        if res.status_code == 200:
            return True, res.json()
        try:
            err = res.json().get("detail", "Không thể đánh dấu tất cả đã đọc")
        except Exception:
            err = "Lỗi kết nối máy chủ"
        return False, err

    @staticmethod
    def delete_notification(notif_id: str):
        res = APIClient.delete(f"/api/notifications/{notif_id}")
        if res.status_code == 200:
            return True, res.json()
        try:
            err = res.json().get("detail", "Không thể xóa thông báo")
        except Exception:
            err = "Lỗi kết nối máy chủ"
        return False, err

    @staticmethod
    def delete_all_notifications():
        res = APIClient.delete("/api/notifications/clear-all")
        if res.status_code == 200:
            return True, res.json()
        try:
            err = res.json().get("detail", "Không thể xóa tất cả thông báo")
        except Exception:
            err = "Lỗi kết nối máy chủ"
        return False, err
