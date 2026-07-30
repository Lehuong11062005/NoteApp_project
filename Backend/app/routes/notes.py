from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.note_schema import NoteCreateSchema
from app.services.note_service import NoteService
from app.config.database import get_database

router = APIRouter(prefix="/notes", tags=["Notes"])

def get_note_service():
    return NoteService()

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_new_note(note: NoteCreateSchema, note_service: NoteService = Depends(get_note_service)):
    try:
        result = note_service.create_note(note_data=note)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))