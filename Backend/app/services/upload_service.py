import os
import uuid
import base64
import httpx
from fastapi import HTTPException, UploadFile, status
from dotenv import load_dotenv

load_dotenv()

IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")
IMGBB_UPLOAD_URL = "https://api.imgbb.com/1/upload"

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}
EXTENSION_TO_MIME = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".gif": "image/gif",
    ".webp": "image/webp",
}

MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB

# Thư mục lưu file local trên server
UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def upload_file_local(file: UploadFile) -> dict:
    """Lưu file trực tiếp vào thư mục server local và trả về URL static."""
    content_type = file.content_type or ""
    ext = os.path.splitext(file.filename or "")[1].lower()
    if not ext:
        ext = ".png"

    if content_type not in ALLOWED_CONTENT_TYPES:
        content_type = EXTENSION_TO_MIME.get(ext, content_type)

    if content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Định dạng file '{file.filename}' không được hỗ trợ. Chỉ hỗ trợ: jpg, png, gif, webp"
        )

    file_bytes = await file.read()
    if len(file_bytes) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File quá lớn. Tối đa 10 MB."
        )

    filename = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as f:
        f.write(file_bytes)

    # URL nội bộ server static
    host_base = os.getenv("BASE_URL", "http://localhost:8000")
    file_url = f"{host_base}/static/uploads/{filename}"

    return {
        "url": file_url,
        "thumb_url": file_url,
        "filename": file.filename or filename,
        "size": len(file_bytes),
    }

async def _upload_to_imgbb(file: UploadFile) -> dict:
    """Upload ảnh lên ImgBB (nếu có API Key)."""
    if not IMGBB_API_KEY or IMGBB_API_KEY == "YOUR_IMGBB_API_KEY":
        return await upload_file_local(file)

    content_type = file.content_type or ""
    if content_type not in ALLOWED_CONTENT_TYPES:
        ext = os.path.splitext(file.filename or "")[1].lower()
        content_type = EXTENSION_TO_MIME.get(ext, content_type)

    if content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Định dạng file không được hỗ trợ: '{file.content_type}'"
        )

    file_bytes = await file.read()
    if len(file_bytes) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File quá lớn. Tối đa 10 MB."
        )

    image_base64 = base64.b64encode(file_bytes).decode("utf-8")

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
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                data = result.get("data", {})
                return {
                    "url": data.get("url"),
                    "display_url": data.get("display_url"),
                    "thumb_url": data.get("thumb", {}).get("url") or data.get("url"),
                    "delete_url": data.get("delete_url"),
                    "width": data.get("width"),
                    "height": data.get("height"),
                    "size": data.get("size"),
                    "filename": data.get("image", {}).get("filename"),
                }
    except Exception:
        pass

    # Fallback to local storage if ImgBB fails
    return await upload_file_local(file)

async def upload_image_only(file: UploadFile) -> dict:
    """Upload ảnh và trả về thông tin URL ảnh."""
    if IMGBB_API_KEY and IMGBB_API_KEY != "YOUR_IMGBB_API_KEY":
        return await _upload_to_imgbb(file)
    return await upload_file_local(file)

async def upload_avatar(file: UploadFile, db, user_id: str) -> dict:
    from app.repositories import user_repository
    image_info = await upload_image_only(file)
    user_repository.update_avatar(db, user_id, image_info["url"])
    return image_info

async def upload_note_image(file: UploadFile, db, note_id: str, user_id: str) -> dict:
    from app.repositories import note_repository
    from app.models.note import create_image_entry
    image_info = await upload_image_only(file)
    image_entry = create_image_entry(
        url=image_info["url"],
        thumb_url=image_info.get("thumb_url"),
        filename=image_info.get("filename"),
        size=image_info.get("size"),
    )
    note_repository.add_image_to_note(db, note_id, user_id, image_entry)
    return image_info

IMAGES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads", "images")

async def save_image(file: UploadFile) -> str:
    """Lưu file ảnh trực tiếp vào thư mục app/uploads/images/ và trả về URL static dạng http://127.0.0.1:8000/uploads/images/<filename>"""
    os.makedirs(IMAGES_DIR, exist_ok=True)
    
    content_type = file.content_type or ""
    ext = os.path.splitext(file.filename or "")[1].lower()
    if not ext:
        ext = ".png"

    if content_type not in ALLOWED_CONTENT_TYPES:
        content_type = EXTENSION_TO_MIME.get(ext, content_type)

    if content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Định dạng file '{file.filename}' không được hỗ trợ. Chỉ hỗ trợ: jpg, png, gif, webp"
        )

    file_bytes = await file.read()
    if len(file_bytes) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File quá lớn. Tối đa 10 MB."
        )

    filename = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(IMAGES_DIR, filename)

    with open(file_path, "wb") as f:
        f.write(file_bytes)

    # Lấy BASE_URL từ environment hoặc default http://127.0.0.1:8000
    host_base = os.getenv("BASE_URL", "http://127.0.0.1:8000")
    if "localhost" in host_base:
        host_base = host_base.replace("localhost", "127.0.0.1")
        
    return f"{host_base}/uploads/images/{filename}"
