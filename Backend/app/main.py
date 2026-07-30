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
host_url = os.getenv("host")

@asynccontextmanager
async def lifespan(app: FastAPI):
    get_database()
    print("Đã kết nối MongoDB.")
    yield
    # Code chạy khi ứng dụng DỪNG
    close_database()

app = FastAPI(title="The Project of Group 6", lifespan=lifespan)

# Nhúng router vào FastAPI app
app.include_router(note_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(upload_router, prefix="/api")

# Mount static files cho upload ảnh local (fallback khi không có ImgBB)
uploads_dir = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(uploads_dir, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")

@app.get("/")
def root():
    return {"messsage": "Server hoat dong on dinh"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=host_url, port=8000, reload=True)