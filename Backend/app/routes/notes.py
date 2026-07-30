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

@router.get("/", status_code=status.HTTP_200_OK)
def get_all_notes():
    try:
        return note_service.get_all_notes()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{note_id}", status_code=status.HTTP_200_OK)
def update_existing_note(note_id: str, note: NoteCreateSchema):
    try:
        result = note_service.update_note(note_id=note_id, note_data=note)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

    