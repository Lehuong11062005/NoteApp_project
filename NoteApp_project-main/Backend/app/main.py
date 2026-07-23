from fastapi import FastAPI

# 1. Thêm dòng này để import router từ file route của bạn sang (sửa lại đường dẫn file cho đúng thực tế nếu cần)
from app.routes.auth import router as auth_router
app = FastAPI(title="Note App API")

# Ở đây có thể có các cấu hình Middleware hoặc các route khác của Leader...

# 2. Thêm dòng này vào để FastAPI chính thức nhận diện API `/register` của bạn
app.include_router(auth_router) 

@app.get("/")
def read_root():
    return {"message": "Server đang chạy ổn định!"}