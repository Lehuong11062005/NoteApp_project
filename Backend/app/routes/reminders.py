from fastapi import APIRouter, HTTPException, status
from app.schemas.reminder_schema import ReminderCreateSchema, ReminderUpdateSchema
from app.services.reminder_service import ReminderService

router = APIRouter(prefix="/reminders", tags=["Reminders"])
reminder_service = ReminderService()


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_reminder(reminder: ReminderCreateSchema):
    try:
        return reminder_service.create_reminder(reminder)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", status_code=status.HTTP_200_OK)
def get_reminders(user_id: str):
    if not user_id:
        raise HTTPException(status_code=400, detail="user_id is required")
    try:
        return reminder_service.get_reminders_by_user(user_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{reminder_id}", status_code=status.HTTP_200_OK)
def update_reminder(reminder_id: str, reminder: ReminderUpdateSchema):
    try:
        return reminder_service.update_reminder(reminder_id, reminder)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{reminder_id}", status_code=status.HTTP_200_OK)
def delete_reminder(reminder_id: str):
    try:
        return reminder_service.delete_reminder(reminder_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
