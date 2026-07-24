from fastapi import APIRouter, UploadFile, File, Depends, Query
from app.services import upload_service
from app.middleware.jwt_auth import get_current_user
from app.config.database import get_database

router = APIRouter(prefix="/upload", tags=["Upload"])


# ─────────────────────────────────────────────────────────────────
#  1. Upload ảnh đại diện (Avatar) → lưu vào users collection
# ─────────────────────────────────────────────────────────────────

@router.post(
    "/avatar",
    summary="Upload ảnh đại diện",
    description=(
        "Upload ảnh đại diện lên ImgBB và **tự động lưu URL vào MongoDB** (collection `users`).\n\n"
        "- Yêu cầu JWT token trong header: `Authorization: Bearer <token>`\n"
        "- Hỗ trợ định dạng: `jpg`, `jpeg`, `png`, `gif`, `webp`\n"
        "- Giới hạn kích thước: **10 MB**"
    )
)
async def upload_avatar(
    file: UploadFile = File(..., description="File ảnh đại diện"),
    current_user: dict = Depends(get_current_user),
    db=Depends(get_database)
):
    """
    **Response mẫu:**
    ```json
    {
      "success": true,
      "message": "Cập nhật ảnh đại diện thành công!",
      "data": {
        "url": "https://i.ibb.co/...",
        "thumb_url": "https://i.ibb.co/...",
        "delete_url": "https://ibb.co/...",
        "width": 400,
        "height": 400,
        "size": 45678,
        "filename": "avatar.jpg"
      }
    }
    ```
    """
    image_info = await upload_service.upload_avatar(
        file=file,
        db=db,
        user_id=current_user["user_id"]
    )
    return {
        "success": True,
        "message": "Cập nhật ảnh đại diện thành công!",
        "data": image_info
    }


# ─────────────────────────────────────────────────────────────────
#  2. Upload ảnh ghi chú → gắn vào Note trong notes collection
# ─────────────────────────────────────────────────────────────────

@router.post(
    "/note-image",
    summary="Upload ảnh cho ghi chú",
    description=(
        "Upload ảnh lên ImgBB và **tự động gắn URL vào ghi chú** trong MongoDB (collection `notes`).\n\n"
        "- Yêu cầu JWT token\n"
        "- Truyền `note_id` qua query string: `/upload/note-image?note_id=<id>`\n"
        "- Hỗ trợ định dạng: `jpg`, `jpeg`, `png`, `gif`, `webp`\n"
        "- Giới hạn kích thước: **10 MB**"
    )
)
async def upload_note_image(
    file: UploadFile = File(..., description="File ảnh ghi chú"),
    note_id: str = Query(..., description="ID của ghi chú cần đính kèm ảnh"),
    current_user: dict = Depends(get_current_user),
    db=Depends(get_database)
):
    """
    **Response mẫu:**
    ```json
    {
      "success": true,
      "message": "Đính kèm ảnh vào ghi chú thành công!",
      "note_id": "6884f...",
      "data": {
        "url": "https://i.ibb.co/...",
        "thumb_url": "https://i.ibb.co/...",
        "delete_url": "https://ibb.co/...",
        "width": 800,
        "height": 600,
        "size": 123456,
        "filename": "note_img.png"
      }
    }
    ```
    """
    image_info = await upload_service.upload_note_image(
        file=file,
        db=db,
        note_id=note_id,
        user_id=current_user["user_id"]
    )
    return {
        "success": True,
        "message": "Đính kèm ảnh vào ghi chú thành công!",
        "note_id": note_id,
        "data": image_info
    }


# ─────────────────────────────────────────────────────────────────
#  3. Upload ảnh thuần → chỉ trả về URL, KHÔNG lưu DB
# ─────────────────────────────────────────────────────────────────

@router.post(
    "/image",
    summary="Upload ảnh (chỉ lấy URL)",
    description=(
        "Upload ảnh lên ImgBB và **chỉ trả về URL**, không lưu vào MongoDB.\n\n"
        "Dùng khi client cần URL trước khi tạo ghi chú (ví dụ: draft note chưa có ID).\n\n"
        "- Yêu cầu JWT token\n"
        "- Hỗ trợ định dạng: `jpg`, `jpeg`, `png`, `gif`, `webp`\n"
        "- Giới hạn kích thước: **10 MB**"
    )
)
async def upload_image(
    file: UploadFile = File(..., description="File ảnh cần upload"),
    current_user: dict = Depends(get_current_user)
):
    image_info = await upload_service.upload_image_only(file)
    return {
        "success": True,
        "message": "Upload ảnh thành công! URL chưa được lưu vào ghi chú nào.",
        "data": image_info
    }


# ─────────────────────────────────────────────────────────────────
#  4. Upload ảnh đại diện (không cần đăng nhập – dùng khi đăng ký)
# ─────────────────────────────────────────────────────────────────

@router.post(
    "/image/public",
    summary="Upload ảnh (không cần đăng nhập)",
    description=(
        "Upload ảnh lên ImgBB **không yêu cầu đăng nhập**.\n\n"
        "Dùng cho trường hợp chọn ảnh đại diện trước khi tạo tài khoản.\n"
        "URL trả về có thể truyền vào API đăng ký.\n\n"
        "- Hỗ trợ định dạng: `jpg`, `jpeg`, `png`, `gif`, `webp`\n"
        "- Giới hạn kích thước: **10 MB**"
    )
)
async def upload_image_public(
    file: UploadFile = File(..., description="File ảnh cần upload")
):
    image_info = await upload_service.upload_image_only(file)
    return {
        "success": True,
        "message": "Upload ảnh thành công!",
        "data": image_info
    }
