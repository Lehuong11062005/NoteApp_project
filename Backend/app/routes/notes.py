from fastapi import APIRouter, Depends, HTTPException, status
from app.middleware.jwt_auth import verify_token
from app.schemas.note_schema import NoteCreateSchema
from app.services.note_service import NoteService

router = APIRouter(prefix="/notes", tags=["Notes"])


@router.get("/", status_code=status.HTTP_200_OK)
def get_notes(
    skip: int = 0, 
    limit: int = 50,
    current_user: dict = Depends(verify_token),
    note_service: NoteService = Depends()
):
    """Lấy danh sách ghi chú của người dùng (có phân trang)."""
    user_id = current_user["sub"]
    return note_service.get_notes_by_user(user_id=user_id, skip=skip, limit=limit)


@router.get("/search", status_code=status.HTTP_200_OK)
def search_notes(
    keyword: str = "",
    skip: int = 0, 
    limit: int = 50,
    current_user: dict = Depends(verify_token),
    note_service: NoteService = Depends()
):
    """Tìm kiếm ghi chú theo từ khóa."""
    user_id = current_user["sub"]
    return note_service.search_notes_by_user(user_id=user_id, keyword=keyword, skip=skip, limit=limit)


@router.get("/statistics", status_code=status.HTTP_200_OK)
def get_note_statistics(
    period: str = "day",
    current_user: dict = Depends(verify_token),
    note_service: NoteService = Depends()
):
    """Lấy thống kê ghi chú theo ngày hoặc tháng."""
    if period not in {"day", "month"}:
        raise HTTPException(status_code=400, detail="period must be day or month")
    user_id = current_user["sub"]
    return note_service.get_note_counts_by_date(user_id=user_id, period=period)


@router.get("/statistics/category", status_code=status.HTTP_200_OK)
def get_note_statistics_by_category(
    current_user: dict = Depends(verify_token),
    note_service: NoteService = Depends()
):
    """Lấy thống kê ghi chú theo danh mục."""
    user_id = current_user["sub"]
    return note_service.get_note_counts_by_category(user_id=user_id)


@router.get("/{note_id}", status_code=status.HTTP_200_OK)
def get_note_by_id(
    note_id: str, 
    current_user: dict = Depends(verify_token),
    note_service: NoteService = Depends()
):
    """Lấy thông tin chi tiết một ghi chú."""
    user_id = current_user["sub"]
    note = note_service.get_note_by_id(note_id=note_id, user_id=user_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ghi chú không tồn tại hoặc bạn không có quyền truy cập")
    return note


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_new_note(
    note: NoteCreateSchema, 
    current_user: dict = Depends(verify_token),
    note_service: NoteService = Depends()
):
    """Tạo mới một ghi chú."""
    user_id = current_user["sub"]
    return note_service.create_note(note_data=note, user_id=user_id)


@router.put("/{note_id}", status_code=status.HTTP_200_OK)
def update_note(
    note_id: str,
    note: NoteCreateSchema,
    current_user: dict = Depends(verify_token),
    note_service: NoteService = Depends()
):
    """Cập nhật ghi chú."""
    user_id = current_user["sub"]
    try:
        return note_service.update_note(note_id=note_id, note_data=note, user_id=user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{note_id}", status_code=status.HTTP_200_OK)
def delete_note(
    note_id: str, 
    current_user: dict = Depends(verify_token),
    note_service: NoteService = Depends()
):
    """Xóa ghi chú."""
    user_id = current_user["sub"]
    try:
        return note_service.delete_note(note_id=note_id, user_id=user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))