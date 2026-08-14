import os
from fastapi import Depends, HTTPException, status
from google import genai
from google.genai import types

from app.repositories.note_repository import NoteRepository
from app.schemas.chat_schema import ChatRequestSchema


class ChatService:
    def __init__(
        self,
        note_repo: NoteRepository = Depends()
    ):
        self.note_repo = note_repo

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise RuntimeError("GEMINI_API_KEY chưa được cấu hình.")

        # Khởi tạo client
        self.client = genai.Client(api_key=api_key)

        # Sử dụng model gemini-3.5-flash (đã được xác nhận khả dụng trong tài khoản của bạn)
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

    def answer_chat_query(
        self,
        chat_data: ChatRequestSchema
    ) -> dict:

        # ==========================================
        # 1. Lấy tất cả ghi chú của user
        # ==========================================

        # 1. Lấy tất cả ghi chú của user
        user_notes = self.note_repo.get_notes_by_user(chat_data.user_id)

        if user_notes:
            notes_context = []
            for index, note in enumerate(user_notes, start=1):
                title = note.get("title", "Không có tiêu đề")
                content = note.get("content", "")
                notes_context.append(f"Ghi chú {index}:\nTiêu đề: {title}\nNội dung:\n{content}".strip())
            
            context = "\n\n".join(notes_context)
        else:
            context = "Người dùng hiện tại chưa có ghi chú nào trong hệ thống."

        # ==========================================
        # 2. Xây dựng cấu hình và Prompt
        # ==========================================
        instructions = """
Bạn là trợ lý AI cho ứng dụng quản lý ghi chú Smart Note.
Nhiệm vụ của bạn là trả lời câu hỏi của người dùng dựa trên các ghi chú được cung cấp.

QUY TẮC:
1. Trả lời bằng tiếng Việt.
2. Trả lời ngắn gọn, rõ ràng và tự nhiên.
3. Chỉ sử dụng thông tin có trong các ghi chú. Không tự bịa.
4. Ưu tiên thông tin của ghi chú được hỏi cụ thể.
"""
        
        user_input = f"DANH SÁCH GHI CHÚ:\n{context}\n\nCÂU HỎI: {chat_data.message}"

        # ==========================================
        # 3. Gọi API (Sử dụng luồng Chat chuẩn)
        # ==========================================
        try:
            # Dùng GenerateContentConfig chuẩn xác của SDK
            chat_session = self.client.chats.create(
                model=self.model_name,
                config=types.GenerateContentConfig(
                    system_instruction=instructions,
                    temperature=0.3
                )
            )

            response = chat_session.send_message(user_input)

            reply = response.text.strip() if response.text else "Xin lỗi, tôi chưa tạo được câu trả lời."

            return {"reply": reply}

        except Exception as e:
            print(f"[Gemini ERROR] {type(e).__name__}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Lỗi AI: {str(e)}"
            )