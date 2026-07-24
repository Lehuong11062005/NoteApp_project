from fastapi import APIRouter, HTTPException, status
from app.schemas.note_schema import NoteCreateSchema
from app.services.note_service import NoteService

router =APIRouter(prefix="/notes", tags=["Notes"])
note_service= NoteService()

@router.post("/",status_code=status.HTTP_201_CREATED)
def create_new_note(note:NoteCreateSchema):
    try:
        result=note_service.create_note(note_data=note)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

    