import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.config.database import get_database, close_database
from dotenv import load_dotenv
from app.routes.notes import router as note_router
from app.routes.auth import router as auth_router
from app.routes.upload import router as upload_router
from contextlib import asynccontextmanager

load_dotenv()
host_url = os.getenv("host", "127.0.0.1")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code chạy khi ứng dụng BẮT ĐẦU
    get_database()
    print("Đã kết nối MongoDB.")
    
    yield
    
    # Code chạy khi ứng dụng DỪNG (Shutdown)
    close_database()

app = FastAPI(title="NoteApp API - Group 6", lifespan=lifespan)

# Mount thư mục static/uploads để phục vụ truy cập file ảnh qua HTTP URL
UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/static/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# Đăng ký các API Routers
app.include_router(note_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(auth_router)  # Đăng ký không prefix cho /auth/login, /auth/profile
app.include_router(upload_router, prefix="/api")
app.include_router(upload_router)  # Đăng ký không prefix cho /upload

@app.get("/")
def root():
    return {"message": "Server FastAPI hoạt động ổn định"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=host_url, port=8000, reload=True)