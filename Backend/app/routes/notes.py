from fastapi import APIRouter, HTTPException, status, Depends
from app.middleware.jwt_auth import verify_token
from app.schemas.note_schema import NoteCreateSchema
from app.services.note_service import NoteService

router =APIRouter(prefix="/notes", tags=["Notes"])
note_service= NoteService()

@router.post("/",status_code=status.HTTP_201_CREATED)
def create_new_note(note:NoteCreateSchema, user_info = Depends(verify_token)):
    try:
        result=note_service.create_note(note_data=note)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

    