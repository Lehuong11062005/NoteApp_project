from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.config.database import get_database, close_database
import os
from dotenv import load_dotenv

from app.routes.notes import router as note_router
from app.routes.auth import router as auth_router
from app.routes.reminders import router as reminder_router
from app.routes.categories import router as category_router
from app.routes.user import router as user_router
from app.routes.upload import router as upload_router
from app.routes.chat import router as chat_router
from app.routes.notifications import router as notification_router
from app.services.upload_service import UPLOAD_DIR
from app.services.scheduler_service import check_and_trigger_reminders
from apscheduler.schedulers.background import BackgroundScheduler

from contextlib import asynccontextmanager

load_dotenv()
host_url = os.getenv("host")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code chạy khi ứng dụng BẮT ĐẦU
    get_database()
    print("Đã kết nối MongoDB.")
    
    # Khởi động Scheduler kiểm tra nhắc nhở định kỳ mỗi 10 giây (realtime)
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_and_trigger_reminders, 'interval', seconds=10, id="reminder_job")
    scheduler.start()
    print("Đã khởi động APScheduler kiểm tra nhắc nhở.")
    
    yield
    # Code chạy khi ứng dụng DỪNG
    scheduler.shutdown(wait=False)
    print("Đã dừng APScheduler.")
    close_database()

app = FastAPI(title="The Project of Group 6", lifespan=lifespan)

# Mount thư mục lưu file upload static
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/static/uploads", StaticFiles(directory=UPLOAD_DIR), name="static_uploads")

# Nhúng các router vào FastAPI app
app.include_router(note_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(reminder_router, prefix="/api")
app.include_router(category_router, prefix="/api")
app.include_router(user_router, prefix="/api")
app.include_router(upload_router, prefix="/api")
app.include_router(chat_router, prefix="/api")
app.include_router(notification_router, prefix="/api")

@app.get("/")
def root():
    return {"messsage": "Server hoat dong on dinh"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=host_url, port=8000, reload=True)
