from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.note_schema import NoteCreateSchema
from app.services.note_service import NoteService
from app.middleware.jwt_auth import verify_token

router = APIRouter(prefix="/notes", tags=["Notes"])
note_service = NoteService()


@router.get("/", status_code=status.HTTP_200_OK)
def get_notes(user_id: str = None, current_user: dict = Depends(verify_token)):
    try:
        # Nếu có JWT, ưu tiên lấy user_id từ token (sub) để bảo mật hơn
        if current_user and current_user.get("sub"):
            target_user_id = current_user.get("sub")
        else:
            target_user_id = user_id

        if not target_user_id:
            raise HTTPException(status_code=400, detail="user_id is required")

        return note_service.get_notes_by_user(user_id=target_user_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_new_note(note: NoteCreateSchema, current_user: dict = Depends(verify_token)):
    try:
        username = current_user.get("sub") if current_user else None
        result = note_service.create_note(note_data=note, user_id=username)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/search", status_code=status.HTTP_200_OK)
def search_notes(keyword: str, user_id: str = None, current_user: dict = Depends(verify_token)):
    try:
        if current_user and current_user.get("sub"):
            target_user_id = current_user.get("sub")
        else:
            target_user_id = user_id

        if not target_user_id:
            raise HTTPException(status_code=400, detail="user_id is required")

        return note_service.search_notes_by_user(user_id=target_user_id, keyword=keyword)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{note_id}", status_code=status.HTTP_200_OK)
def update_note(note_id: str, note: NoteCreateSchema):
    try:
        return note_service.update_note(note_id=note_id, note_data=note)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{note_id}", status_code=status.HTTP_200_OK)
def delete_note(note_id: str):
    try:
        return note_service.delete_note(note_id=note_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))