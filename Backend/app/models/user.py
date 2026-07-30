from datetime import datetime

def create_user_document(username: str, hashed_password: str,
                         email: str = None, full_name: str = None,
                         avatar_url: str = None) -> dict:
    """Tạo document User chuẩn cho MongoDB collection 'users'."""
    return {
        "username": username,
        "password": hashed_password,
        "email": email,
        "full_name": full_name,
        "avatar_url": avatar_url,
        "created_at": datetime.utcnow()
    }
