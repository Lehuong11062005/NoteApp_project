from fastapi import APIRouter, HTTPException, status
from app.schemas.note_schema import NoteCreateSchema
from app.services.note_service import NoteService

router = APIRouter(prefix="/notes", tags=["Notes"])
note_service = NoteService()

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_new_note(note: NoteCreateSchema):
    try:
        result = note_service.create_note(note_data=note)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", status_code=status.HTTP_200_OK)
def get_notes(user_id: str):
    if not user_id:
        raise HTTPException(status_code=400, detail="user_id is required")
    try:
        return note_service.get_notes_by_user(user_id=user_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    