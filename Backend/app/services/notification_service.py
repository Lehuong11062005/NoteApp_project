from typing import Any, Dict, List, Optional
from fastapi import Depends, HTTPException, status
from app.repositories.notification_repository import NotificationRepository


class NotificationService:
    def __init__(self, notif_repo: NotificationRepository = Depends()):
        self.notif_repo = notif_repo

    def get_notifications_by_user(self, user_id: str, skip: int = 0, limit: int = 50) -> List[Dict[str, Any]]:
        return self.notif_repo.get_by_user(user_id=user_id, skip=skip, limit=limit)

    def get_unread_count(self, user_id: str) -> Dict[str, int]:
        count = self.notif_repo.count_unread(user_id=user_id)
        return {"unread_count": count}

    def mark_as_read(self, notif_id: str, user_id: str) -> Dict[str, Any]:
        success = self.notif_repo.mark_as_read(notif_id=notif_id, user_id=user_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Không tìm thấy thông báo hoặc bạn không có quyền"
            )
        return {"message": "Đã đánh dấu thông báo là đã đọc"}

    def mark_all_as_read(self, user_id: str) -> Dict[str, Any]:
        modified_count = self.notif_repo.mark_all_as_read(user_id=user_id)
        return {
            "message": f"Đã đánh dấu {modified_count} thông báo là đã đọc",
            "modified_count": modified_count
        }

    def delete_notification(self, notif_id: str, user_id: str) -> Dict[str, Any]:
        success = self.notif_repo.delete(notif_id=notif_id, user_id=user_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Không tìm thấy thông báo hoặc bạn không có quyền xóa"
            )
        return {"message": "Đã xóa thông báo thành công"}

    def delete_all_notifications(self, user_id: str) -> Dict[str, Any]:
        deleted_count = self.notif_repo.delete_all(user_id=user_id)
        return {
            "message": f"Đã xóa toàn bộ {deleted_count} thông báo",
            "deleted_count": deleted_count
        }
