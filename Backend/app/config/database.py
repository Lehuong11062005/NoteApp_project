import os
from pymongo import MongoClient
from dotenv import load_dotenv
from pymongo.errors import ConnectionFailure


# load bien moi truong
load_dotenv()

MONGO_URI=os.getenv("MONGO_URI")
DB_NAME=os.getenv("MONGO_DB_NAME")

# Ta0  mot bien ben ngoai de hứng kết nối
_client=None

def get_database():
    # khai bao bien _client la bien toan cục tranh hiểu là biên  mới 
    global _client

    # cần check xem  đã kết  nối chưa mới kết nối
    if _client is None:
        try:
            print("Start connect database")
            # khổi tạo client để kết nối database
            _client=MongoClient(MONGO_URI,serverSelectionTimeoutMS=5000)

            # kiểm tra kết nối bằng cách ping 
            _client.admin.command('ping')
            print("Ket noi database thanh cong")
        except ConnectionFailure as cf:
            print(f"Loi ket noi database: {cf}") 
            # nếu lỗi cần phải reset lại cái _client để tránh lỗi biến kết nối sau  nay
            _client=None
            raise cf
        except Exception as ex:
            print(f"Loi cau hinh database: {ex}")
            _client=None
            raise ex
    return _client[DB_NAME]
# thêm một hàm tắt kết nối nêys cần 
def close_database():
    global _client
    if _client is not None:
        _client.close()
        print("Close thanh cong")
        _client=None

if __name__ == "__main__":
    get_database()
    close_database()