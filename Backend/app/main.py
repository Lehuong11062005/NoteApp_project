from fastapi import FastAPI
from app.config.database import get_database, close_database
import os
from dotenv import load_dotenv

from app.routes.notes import router as note_router
from app.routes.auth import router as auth_router
from app.routes.reminders import router as reminder_router
from app.routes.categories import router as category_router
from app.routes.user import router as user_router

from contextlib import asynccontextmanager

load_dotenv()
host_url = os.getenv("host")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code chạy khi ứng dụng BẮT ĐẦU
    get_database()
    print("Đã kết nối MongoDB.")
    yield
    # Code chạy khi ứng dụng DỪNG
    close_database()

app = FastAPI(title="The Project of Group 6", lifespan=lifespan)

# Nhúng các router vào FastAPI app
app.include_router(note_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(reminder_router, prefix="/api")
app.include_router(category_router, prefix="/api")
app.include_router(user_router, prefix="/api")

@app.get("/")
def root():
    return {"messsage": "Server hoat dong on dinh"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=host_url, port=8000, reload=True)