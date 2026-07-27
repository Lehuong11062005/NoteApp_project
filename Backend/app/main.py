from fastapi import FastAPI
from app.config.database import get_database, close_database
import os
from dotenv import load_dotenv
from app.routes.notes import router as note_router
# 1. Import router chứa các API Đăng ký / Đăng nhập
from app.routes.auth import router as auth_router 
from contextlib import asynccontextmanager

load_dotenv()
host_url = os.getenv("host")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code chạy khi ứng dụng BẮT ĐẦU
    get_database()
    print("Đã kết nối MongoDB.")
    yield
    # Code chạy khi ứng dụng DỪNG (Shutdown)
    close_database()

app = FastAPI(title="The Project of Group 6", lifespan=lifespan)

# 2. Nhúng cả 2 router vào FastAPI app
app.include_router(note_router, prefix="/api")
app.include_router(auth_router, prefix="/auth")  # Prefix /auth sẽ tạo ra URL: http://127.0.0.1:8000/auth/register

@app.get("/")
def root():
    return {"messsage": "Server hoat dong on dinh"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=host_url, port=8000, reload=True)