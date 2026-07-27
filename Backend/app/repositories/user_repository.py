from bson import ObjectId
from datetime import datetime

def get_user_by_username(db, username: str):
    """Tìm user trong MongoDB theo username"""
    return db["users"].find_one({"username": username})

def get_user_by_id(db, user_id: str):
    """Tìm user trong MongoDB theo _id (ObjectId)"""
    try:
        return db["users"].find_one({"_id": ObjectId(user_id)})
    except Exception:
        return None

def create_user(db, user_document: dict) -> str:
    """Insert user mới vào collection 'users'."""
    result = db["users"].insert_one(user_document)
    return str(result.inserted_id)

def update_avatar(db, user_id: str, avatar_url: str) -> bool:
    """Cập nhật URL ảnh đại diện của user trong MongoDB."""
    try:
        result = db["users"].update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {
                "avatar_url": avatar_url,
                "updated_at": datetime.utcnow()
            }}
        )
        return result.matched_count > 0
    except Exception:
        return False
