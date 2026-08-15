from fastapi import APIRouter, Depends, HTTPException, status
from app.middleware.jwt_auth import verify_token
from app.services.notification_service import NotificationService

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("/", status_code=status.HTTP_200_OK)
def get_notifications(
    skip: int = 0,
    limit: int = 50,
    current_user: dict = Depends(verify_token),
    notification_service: NotificationService = Depends()
):
    """Lấy danh sách thông báo của người dùng hiện tại."""
    user_id = current_user.get("sub")
    if not user_id:
        raise HTTPException(status_code=400, detail="Không tìm thấy định danh người dùng")
    return notification_service.get_notifications_by_user(user_id=user_id, skip=skip, limit=limit)


@router.get("/unread-count", status_code=status.HTTP_200_OK)
def get_unread_count(
    current_user: dict = Depends(verify_token),
    notification_service: NotificationService = Depends()
):
    """Lấy số lượng thông báo chưa đọc."""
    user_id = current_user.get("sub")
    if not user_id:
        raise HTTPException(status_code=400, detail="Không tìm thấy định danh người dùng")
    return notification_service.get_unread_count(user_id=user_id)


@router.put("/read-all", status_code=status.HTTP_200_OK)
def mark_all_as_read(
    current_user: dict = Depends(verify_token),
    notification_service: NotificationService = Depends()
):
    """Đánh dấu tất cả thông báo là đã đọc."""
    user_id = current_user.get("sub")
    if not user_id:
        raise HTTPException(status_code=400, detail="Không tìm thấy định danh người dùng")
    return notification_service.mark_all_as_read(user_id=user_id)


@router.put("/{notification_id}/read", status_code=status.HTTP_200_OK)
def mark_as_read(
    notification_id: str,
    current_user: dict = Depends(verify_token),
    notification_service: NotificationService = Depends()
):
    """Đánh dấu 1 thông báo cụ thể là đã đọc."""
    user_id = current_user.get("sub")
    if not user_id:
        raise HTTPException(status_code=400, detail="Không tìm thấy định danh người dùng")
    return notification_service.mark_as_read(notif_id=notification_id, user_id=user_id)


@router.delete("/clear-all", status_code=status.HTTP_200_OK)
def delete_all_notifications(
    current_user: dict = Depends(verify_token),
    notification_service: NotificationService = Depends()
):
    """Xóa tất cả thông báo của người dùng."""
    user_id = current_user.get("sub")
    if not user_id:
        raise HTTPException(status_code=400, detail="Không tìm thấy định danh người dùng")
    return notification_service.delete_all_notifications(user_id=user_id)


@router.delete("/{notification_id}", status_code=status.HTTP_200_OK)
def delete_notification(
    notification_id: str,
    current_user: dict = Depends(verify_token),
    notification_service: NotificationService = Depends()
):
    """Xóa một thông báo theo ID."""
    user_id = current_user.get("sub")
    if not user_id:
        raise HTTPException(status_code=400, detail="Không tìm thấy định danh người dùng")
    return notification_service.delete_notification(notif_id=notification_id, user_id=user_id)
