from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.note_schema import NoteCreateSchema
from app.services.note_service import NoteService

from app.middleware.jwt_auth import verify_token

router =APIRouter(prefix="/notes", tags=["Notes"])
note_service= NoteService()
@router.get("/",status_code=status.HTTP_200_OK)
def get_all_notes(current_user: dict = Depends(verify_token)):
    # try:
    #     username = current_user.get("sub")
    #     notes=note_service.get_all_notes(user_id=username)
    #     return notes
    # except Exception as e:
    #     raise HTTPException(status_code=400, detail=str(e))
    pass

@router.post("/",status_code=status.HTTP_201_CREATED)
def create_new_note(note:NoteCreateSchema, current_user: dict = Depends(verify_token)):
    try:
        username = current_user.get("sub")
        result=note_service.create_note(note_data=note, user_id=username)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

    