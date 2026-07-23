from fastapi import FastAPI
# from app.config.database import get_database, close_database
import os
from dotenv import load_dotenv

# 1. Import file auth.py từ thư mục routes
from app.routes import auth 

load_dotenv()
# Lấy biến môi trường HOST, nếu file .env chưa có thì mặc định dùng "127.0.0.1"
host_url = os.getenv("HOST", "127.0.0.1")

app = FastAPI(title="The Project of Group 6")

# 2. Đăng ký router auth vào app
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Server hoat dong on dinh"}

if __name__ == "__main__":
    import uvicorn
    # Cập nhật thành "app.main:app" để uvicorn hiểu đúng đường dẫn file
    uvicorn.run("app.main:app", host=host_url, port=8000, reload=True)