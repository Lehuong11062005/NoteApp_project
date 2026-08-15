from typing import List, Tuple, Union
from Frontend.services.notification_api import NotificationAPI
from Frontend.models.notification import Notification


class NotificationController:
    def get_notifications(self, skip: int = 0, limit: int = 50) -> Tuple[bool, Union[List[Notification], str]]:
        success, data = NotificationAPI.get_notifications(skip=skip, limit=limit)
        if success and isinstance(data, list):
            notifications = [Notification.from_dict(item) for item in data]
            return True, notifications
        return False, data if isinstance(data, str) else "Không thể tải danh sách thông báo"

    def get_unread_count(self) -> int:
        success, count = NotificationAPI.get_unread_count()
        return count if success else 0

    def mark_as_read(self, notif_id: str) -> Tuple[bool, str]:
        success, data = NotificationAPI.mark_as_read(notif_id)
        if success:
            return True, data.get("message", "Đã đánh dấu đã đọc") if isinstance(data, dict) else "Thành công"
        return False, data if isinstance(data, str) else "Thao tác thất bại"

    def mark_all_as_read(self) -> Tuple[bool, str]:
        success, data = NotificationAPI.mark_all_as_read()
        if success:
            return True, data.get("message", "Đã đánh dấu tất cả đã đọc") if isinstance(data, dict) else "Thành công"
        return False, data if isinstance(data, str) else "Thao tác thất bại"

    def delete_notification(self, notif_id: str) -> Tuple[bool, str]:
        success, data = NotificationAPI.delete_notification(notif_id)
        if success:
            return True, data.get("message", "Đã xóa thông báo") if isinstance(data, dict) else "Thành công"
        return False, data if isinstance(data, str) else "Thao tác thất bại"

    def delete_all_notifications(self) -> Tuple[bool, str]:
        success, data = NotificationAPI.delete_all_notifications()
        if success:
            return True, data.get("message", "Đã xóa tất cả thông báo") if isinstance(data, dict) else "Thành công"
        return False, data if isinstance(data, str) else "Thao tác thất bại"
