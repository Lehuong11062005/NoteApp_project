import requests

BASE_URL = "http://127.0.0.1:8000"

class APIClient:
    @staticmethod
    def check_server():
        """Kiểm tra kết nối tới Backend trước khi mở ứng dụng."""
        try:
            # Gọi API root của Backend
            response = requests.get(f"{BASE_URL}/", timeout=3)
            
            if response.status_code == 200:
                return True, "Kết nối thành công"
            else:
                return False, f"Server trả về mã lỗi: {response.status_code}"
                
        except requests.exceptions.ConnectionError:
            return False, "Không thể kết nối đến Backend. Vui lòng kiểm tra lại server!"
        except Exception as e:
            return False, f"Lỗi không xác định: {str(e)}"