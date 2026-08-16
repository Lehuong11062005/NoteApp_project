from fastapi import APIRouter, Depends
from app.middleware.jwt_auth import verify_token
from app.services.chat_service import ChatService
from app.schemas.chat_schema import ChatRequestSchema

router = APIRouter()

@router.post("/chat")
def chat_with_ai(
    chat_data: ChatRequestSchema,
    # 1. Ép xác thực Token, nếu có token thì lấy ra cục payload (chứa sub)
    token_payload: dict = Depends(verify_token), 
    chat_service: ChatService = Depends()
):
    # 2. Lấy ID thật từ chữ 'sub' trong Access Token
    real_user_id = token_payload.get("sub")
    
    # 3. Gán đè cái ID thật này vào dữ liệu trước khi ném cho Service xử lý
    chat_data.user_id = real_user_id

    # 4. Gọi hàm AI
    return chat_service.answer_chat_query(chat_data)