import httpx
import base64
import os
from fastapi import HTTPException, UploadFile, status
from dotenv import load_dotenv

load_dotenv()

IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")
IMGBB_UPLOAD_URL = "https://api.imgbb.com/1/upload"

# Các loại MIME được phép upload
ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}

# Map phần mở rộng → MIME type (dùng khi client gửi application/octet-stream)
EXTENSION_TO_MIME = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".gif": "image/gif",
    ".webp": "image/webp",
}

# Giới hạn kích thước file: 10 MB
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024


# ─────────────────────────────────────────
#  PRIVATE: Hàm gốc gọi ImgBB API
# ─────────────────────────────────────────

async def _upload_to_imgbb(file: UploadFile) -> dict:
    """Hàm nội bộ: validate file, encode base64 và upload lên ImgBB.

    Returns:
        dict thông tin ảnh từ ImgBB:
        { url, display_url, thumb_url, delete_url, width, height, size, filename }
    """

    # 1. Kiểm tra API key đã cấu hình chưa
    if not IMGBB_API_KEY or IMGBB_API_KEY == "YOUR_IMGBB_API_KEY":
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="ImgBB API key chưa được cấu hình. Vui lòng thêm IMGBB_API_KEY vào file .env"
        )

    # 2. Xác định MIME type thực tế
    # Postman và một số client gửi 'application/octet-stream' thay vì MIME type đúng
    # → fallback: tự detect từ phần mở rộng của tên file
    content_type = file.content_type or ""
    if content_type not in ALLOWED_CONTENT_TYPES:
        ext = os.path.splitext(file.filename or "")[1].lower()
        content_type = EXTENSION_TO_MIME.get(ext, content_type)

    if content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Định dạng file không được hỗ trợ: '{file.content_type}'. "
                   f"Chỉ chấp nhận: {', '.join(sorted(ALLOWED_CONTENT_TYPES))}. "
                   f"Tên file: '{file.filename}'"
        )

    # 3. Đọc nội dung file
    file_bytes = await file.read()

    # 4. Kiểm tra kích thước file
    if len(file_bytes) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File quá lớn. Tối đa {MAX_FILE_SIZE_BYTES // (1024 * 1024)} MB."
        )

    # 5. Encode file sang base64
    image_base64 = base64.b64encode(file_bytes).decode("utf-8")

    # 6. Gọi ImgBB API để upload
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                IMGBB_UPLOAD_URL,
                data={
                    "key": IMGBB_API_KEY,
                    "image": image_base64,
                    "name": file.filename or "uploaded_image",
                }
            )
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Kết nối tới ImgBB bị timeout. Vui lòng thử lại."
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Lỗi kết nối tới ImgBB: {str(e)}"
        )

    # 7. Xử lý phản hồi từ ImgBB
    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"ImgBB trả về lỗi (HTTP {response.status_code}): {response.text}"
        )

    result = response.json()
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"ImgBB upload thất bại: {result.get('error', {}).get('message', 'Unknown error')}"
        )

    # 8. Trích xuất thông tin ảnh từ response
    data = result.get("data", {})
    return {
        "url": data.get("url"),
        "display_url": data.get("display_url"),
        "thumb_url": data.get("thumb", {}).get("url"),
        "delete_url": data.get("delete_url"),
        "width": data.get("width"),
        "height": data.get("height"),
        "size": data.get("size"),
        "filename": data.get("image", {}).get("filename"),
    }


# ─────────────────────────────────────────
#  PUBLIC: Ảnh đại diện (Avatar)
# ─────────────────────────────────────────

async def upload_avatar(file: UploadFile, db, user_id: str) -> dict:
    """Upload ảnh đại diện lên ImgBB và lưu URL vào MongoDB (collection users).

    Args:
        file:    File ảnh từ request
        db:      MongoDB database instance
        user_id: ID của user đang đăng nhập

    Returns:
        dict thông tin ảnh đã upload
    """
    from app.repositories import user_repository

    # Upload lên ImgBB
    image_info = await _upload_to_imgbb(file)

    # Lưu avatar_url vào MongoDB
    updated = user_repository.update_avatar(db, user_id, image_info["url"])
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy thông tin user để cập nhật avatar."
        )

    return image_info


# ─────────────────────────────────────────
#  PUBLIC: Ảnh ghi chú (Note Image)
# ─────────────────────────────────────────

async def upload_note_image(file: UploadFile, db, note_id: str, user_id: str) -> dict:
    """Upload ảnh lên ImgBB và gắn URL vào Note trong MongoDB.

    Args:
        file:    File ảnh từ request
        db:      MongoDB database instance
        note_id: ID của ghi chú cần đính kèm ảnh
        user_id: ID của user đang đăng nhập (kiểm tra quyền sở hữu)

    Returns:
        dict thông tin ảnh đã upload
    """
    from app.repositories import note_repository
    from app.models.note import create_image_entry

    # Upload lên ImgBB
    image_info = await _upload_to_imgbb(file)

    # Tạo image entry chuẩn
    image_entry = create_image_entry(
        url=image_info["url"],
        thumb_url=image_info.get("thumb_url"),
        delete_url=image_info.get("delete_url"),
        filename=image_info.get("filename"),
        width=image_info.get("width"),
        height=image_info.get("height"),
        size=image_info.get("size"),
    )

    # Gắn ảnh vào Note trong MongoDB
    updated = note_repository.add_image_to_note(db, note_id, user_id, image_entry)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy ghi chú ID '{note_id}' hoặc bạn không có quyền chỉnh sửa."
        )

    return image_info


# ─────────────────────────────────────────
#  PUBLIC: Upload thuần (không lưu DB)
# ─────────────────────────────────────────

async def upload_image_only(file: UploadFile) -> dict:
    """Upload ảnh lên ImgBB và trả về URL mà KHÔNG lưu vào DB.
    Dùng khi client tự quản lý URL (ví dụ: khi tạo Note mới chưa có ID).

    Returns:
        dict thông tin ảnh đã upload
    """
    return await _upload_to_imgbb(file)
