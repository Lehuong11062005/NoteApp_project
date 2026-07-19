from app.config.database import get_database
from app.utils.password import (
    get_password_hash,  # Lưu ý: Nếu trong file password.py của bạn đặt tên hàm là hash_password thì sửa lại ở đây nhé
)

# Kết nối vào MongoDB
db = get_database()
users_collection = db["users"]

# Thông tin tài khoản muốn tạo
test_username = "admin"
test_password = "123"

# Mã hóa mật khẩu
hashed_pw = get_password_hash(test_password)

# Xóa tài khoản 'admin' cũ nếu đã tồn tại để tránh lỗi trùng lặp
users_collection.delete_one({"username": test_username})

# Thêm tài khoản mới vào MongoDB
users_collection.insert_one({"username": test_username, "password": hashed_pw})

print(f"🎉 Đã tạo thành công tài khoản test!")
print(f"👉 Tài khoản: {test_username}")
print(f"👉 Mật khẩu: {test_password}")