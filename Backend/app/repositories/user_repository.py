from bson import ObjectId
from pymongo.database import Database

def get_user_by_username(db: Database, username: str):
    """Tìm user trong MongoDB theo username (Dùng cho Đăng nhập)"""
    return db["users"].find_one({"username": username})

def get_user_by_id(db: Database, user_id: str):
    """Tìm user trong MongoDB theo _id ObjectId (Dùng cho lấy Profile)"""
    try:
        return db["users"].find_one({"_id": ObjectId(user_id)})
    except Exception:
        return None

def create_user(db: Database, user_document: dict) -> str:
    """Insert user mới vào collection 'users'.
    Trả về inserted_id dưới dạng chuỗi (Dùng cho Đăng ký)."""
    result = db["users"].insert_one(user_document)
    return str(result.inserted_id)