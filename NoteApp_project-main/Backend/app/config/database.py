# app/config/database.py
import motor.motor_asyncio
from app.config.settings import settings

# 1. Tạo client kết nối tới MongoDB từ đường dẫn URL trong file .env
client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_URI)

# 2. Kết nối trực tiếp vào Database cụ thể (Note_app)
db = client[settings.MONGO_DB_NAME]