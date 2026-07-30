from fastapi import APIRouter, UploadFile, File, Depends, Query
from app.services import upload_service
from app.middleware.jwt_auth import get_current_user
from app.config.database import get_database

router = APIRouter(prefix="/upload", tags=["Upload"])

@router.post("", summary="Upload ảnh và trả về URL")
@router.post("/", summary="Upload ảnh và trả về URL")
async def upload_image_general(
    file: UploadFile = File(..., description="File ảnh cần upload")
):
    """
    **API POST /upload (hoặc /api/upload)**
    Lưu file ảnh vào server, trả về thông tin URL ảnh.
    """
    image_info = await upload_service.upload_image_only(file)
    return {
        "success": True,
        "message": "Upload ảnh thành công!",
        "url": image_info["url"],
        "data": image_info
    }

@router.post("/avatar", summary="Upload ảnh đại diện")
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
    db=Depends(get_database)
):
    image_info = await upload_service.upload_avatar(file, db, current_user["user_id"])
    return {
        "success": True,
        "message": "Cập nhật ảnh đại diện thành công!",
        "url": image_info["url"],
        "data": image_info
    }

@router.post("/note-image", summary="Upload ảnh cho ghi chú")
async def upload_note_image(
    file: UploadFile = File(...),
    note_id: str = Query(...),
    current_user: dict = Depends(get_current_user),
    db=Depends(get_database)
):
    image_info = await upload_service.upload_note_image(file, db, note_id, current_user["user_id"])
    return {
        "success": True,
        "message": "Đính kèm ảnh vào ghi chú thành công!",
        "url": image_info["url"],
        "data": image_info
    }

@router.post("/image", summary="Upload ảnh lên ImgBB và trả về URL công khai")
async def upload_image_local_endpoint(
    file: UploadFile = File(..., description="File ảnh cần upload"),
    current_user: dict = Depends(get_current_user)
):
    """
    **API POST /api/upload/image**
    Upload ảnh lên ImgBB (hoặc lưu local nếu không có API key) và trả về URL công khai.
    Yêu cầu JWT xác thực.
    """
    image_info = await upload_service.upload_image_only(file)
    return {"url": image_info["url"]}
