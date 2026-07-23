from app.repositories.user_repository import create_user
from app.utils.password import get_password_hash

def register_user(db, user_data):
    hashed_pw = get_password_hash(user_data.password)
    return create_user(db, user_data, hashed_pw)