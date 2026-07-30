import os
import requests

class UploadAPI:
    @staticmethod
    def upload_image(filepath: str):
        """
        Gửi file ảnh từ filepath lên API POST /api/upload/image.
        Yêu cầu Authorization header nếu có JWT token.
        Trả về (is_success: bool, url_or_msg: str)
        """
        import Frontend.services.api_client as api_client
        
        url = f"{api_client.BASE_URL}/api/upload/image"
        headers = {}
        if api_client.CURRENT_JWT_TOKEN:
            headers["Authorization"] = f"Bearer {api_client.CURRENT_JWT_TOKEN}"

        try:
            if not os.path.exists(filepath):
                return False, "File ảnh không tồn tại!"

            with open(filepath, "rb") as f:
                # Gửi file với key 'file' khớp với FastAPI route
                files = {"file": (os.path.basename(filepath), f)}
                response = requests.post(url, files=files, headers=headers, timeout=15)

            if response.status_code == 200:
                data = response.json()
                image_url = data.get("url")
                if image_url:
                    return True, image_url
                return False, "Không tìm thấy URL ảnh trong phản hồi từ server!"
            else:
                try:
                    error_detail = response.json().get("detail", f"Upload thất bại ({response.status_code})")
                except Exception:
                    error_detail = f"Upload thất bại ({response.status_code})"
                return False, error_detail
        except requests.exceptions.ConnectionError:
            return False, "Không thể kết nối đến máy chủ Backend!"
        except Exception as e:
            return False, f"Lỗi upload: {str(e)}"
