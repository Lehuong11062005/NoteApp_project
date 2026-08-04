from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from app.middleware.jwt_auth import verify_token
from app.schemas.note_schema import NoteCreateSchema
from app.services.note_service import NoteService

router = APIRouter(prefix="/notes", tags=["Notes"])
note_service = NoteService()


@router.get("/", status_code=status.HTTP_200_OK)
def get_notes(
    user_id: Optional[str] = None, current_user: dict = Depends(verify_token)
):
    """Lấy danh sách ghi chú của người dùng (ưu tiên lấy user_id từ JWT token)."""
    try:
        target_user_id = (
            current_user.get("sub")
            if current_user and current_user.get("sub")
            else user_id
        )

        if not target_user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="user_id is required",
            )

        return note_service.get_notes_by_user(user_id=target_user_id)
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@router.get("/all", status_code=status.HTTP_200_OK)
def get_all_notes(current_user: dict = Depends(verify_token)):
    """Lấy tất cả ghi chú trong hệ thống (đổi route thành /all để tránh trùng với /)."""
    try:
        return note_service.get_all_notes()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@router.get("/{note_id}", status_code=status.HTTP_200_OK)
def get_note_by_id(note_id: str, current_user: dict = Depends(verify_token)):
    """Lấy thông tin chi tiết một ghi chú theo note_id."""
    try:
        note = note_service.get_note_by_id(note_id=note_id)
        if not note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
            )
        return note
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_new_note(
    note: NoteCreateSchema, current_user: dict = Depends(verify_token)
):
    """Tạo mới một ghi chú cho người dùng hiện tại."""
    try:
        username = current_user.get("sub") if current_user else None
        return note_service.create_note(note_data=note, user_id=username)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@router.put("/{note_id}", status_code=status.HTTP_200_OK)
def update_note(
    note_id: str,
    note: NoteCreateSchema,
    current_user: dict = Depends(verify_token),
):
    """Cập nhật ghi chú theo note_id."""
    try:
        result = note_service.update_note(note_id=note_id, note_data=note)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Note not found or update failed"
            )
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@router.delete("/{note_id}", status_code=status.HTTP_200_OK)
def delete_note(note_id: str, current_user: dict = Depends(verify_token)):
    """Xóa ghi chú theo note_id."""
    try:
        result = note_service.delete_note(note_id=note_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Note not found or delete failed"
            )
        return result
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )