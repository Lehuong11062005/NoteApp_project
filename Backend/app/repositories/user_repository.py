from app.config.database import get_database

class UserRepository:
    def __init__(self):
        # Lấy instance của database thông qua hàm get_database()
        self.db = get_database()
        self.collection = self.db["users"]

    def find_by_username(self, username: str):
        return self.collection.find_one({"username": username})

    def find_by_email(self, email: str):
        return self.collection.find_one({"email": email})

    def create_user(self, user_data: dict):
        result = self.collection.insert_one(user_data)
        return str(result.inserted_id)