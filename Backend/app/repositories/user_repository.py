from bson import ObjectId

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
    """Insert user mới vào collection 'users'.
    Trả về inserted_id dưới dạng chuỗi."""
    result = db["users"].insert_one(user_document)
    return str(result.inserted_id)