def get_user_by_username(db, username: str):
    """Tìm user trong MongoDB (Giả sử collection tên là 'users')"""
    return db["users"].find_one({"username": username})