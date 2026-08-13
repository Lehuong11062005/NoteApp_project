from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.reminder_schema import ReminderCreateSchema, ReminderUpdateSchema
from app.services.reminder_service import ReminderService
from app.middleware.jwt_auth import verify_token 

router = APIRouter(prefix="/reminders", tags=["Reminders"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_reminder(
    reminder: ReminderCreateSchema,
    reminder_service: ReminderService = Depends()
):
    try:
        return reminder_service.create_reminder(reminder)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", status_code=status.HTTP_200_OK)
def get_reminders(
    current_user: dict = Depends(verify_token),   
    reminder_service: ReminderService = Depends()
):
    try:
        # Lấy user_id chuẩn xác và bảo mật từ Token
        user_id = current_user.get("sub") 
        if not user_id:
            raise HTTPException(status_code=400, detail="Không tìm thấy định danh người dùng.")
            
        return reminder_service.get_reminders_by_user(user_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{reminder_id}", status_code=status.HTTP_200_OK)
def update_reminder(
    reminder_id: str, 
    reminder: ReminderUpdateSchema,
    reminder_service: ReminderService = Depends()
):
    try:
        return reminder_service.update_reminder(reminder_id, reminder)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{reminder_id}", status_code=status.HTTP_200_OK)
def delete_reminder(
    reminder_id: str,
    reminder_service: ReminderService = Depends()
):
    try:
        return reminder_service.delete_reminder(reminder_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))