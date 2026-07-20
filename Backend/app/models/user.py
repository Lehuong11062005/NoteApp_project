from datetime import datetime

# Đây là hàm tạo dict chuẩn để insert vào MongoDB
# Không dùng class ORM vì PyMongo làm việc trực tiếp với dict

def create_user_document(username: str, hashed_password: str,
                         email: str = None, full_name: str = None) -> dict:
    """Tạo document User theo đúng cấu trúc lưu vào MongoDB collection 'users'."""
    return {
        "username": username,           # Tên đăng nhập (unique)
        "password": hashed_password,    # Mật khẩu đã được bcrypt hash
        "email": email,                 # Email (tuỳ chọn)
        "full_name": full_name,         # Họ và tên (tuỳ chọn)
        "created_at": datetime.utcnow() # Thời điểm tạo tài khoản (UTC)
    }
