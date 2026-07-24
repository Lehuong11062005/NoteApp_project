from pymongo.database import Database

def get_user_by_username(db: Database, username: str):
    """Tìm user trong MongoDB theo username"""
    return db["users"].find_one({"username": username})

def create_user(db: Database, user_document: dict) -> str:
    """Lưu user mới vào MongoDB"""
    result = db["users"].insert_one(user_document)
    return str(result.inserted_id)