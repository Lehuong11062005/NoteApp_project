from contextlib import asynccontextmanager
from fastapi import FastAPI
import os
from dotenv import load_dotenv

# --- CÁC IMPORT CỦA DỰ ÁN ---
# Giả sử bạn đã có file config database do Hưởng viết
from app.config.database import get_database, close_database 

# Router của các module khác (có sẵn trong ảnh của bạn)
# from app.routes.notes import note_router
# Thêm import Router Auth của Đức
from app.routes import auth  

load_dotenv()
host_url = os.getenv("host", "127.0.0.1") # Nên set default để tránh lỗi nếu .env thiếu

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code chạy khi ứng dụng BẮT ĐẦU
    get_database()
    print("Đã kết nối MongoDB.")
    
    yield # Trạng thái server đang chạy
    
    # Code chạy khi ứng dụng DỪNG (Shutdown)
    close_database()

app = FastAPI(title="The Project of Group 6", lifespan=lifespan)

# --- ĐĂNG KÝ CÁC ROUTER TẠI ĐÂY ---

# Router có sẵn của team bạn
# app.include_router(note_router, prefix="/api")
# Nhúng Router Auth của Đức vào hệ thống
app.include_router(auth.router) 


@app.get("/")
def root():
    return {"message": "Server hoat dong on dinh"}

if __name__ == "__main__":
    import uvicorn
    # Lưu ý: Nếu chạy từ thư mục gốc (Backend), có thể cần đổi thành "app.main:app"
    uvicorn.run("main:app", host=host_url, port=8000, reload=True)