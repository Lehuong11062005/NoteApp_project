import requests

BASE_URL = "http://127.0.0.1:8000" # Port mặc định của FastAPI

def call_register_api(username, password):
    url = f"{BASE_URL}/register"
    payload = {
        "username": username,
        "password": password
    }
    try:
        response = requests.post(url, json=payload)
        return response.status_code, response.json()
    except requests.exceptions.ConnectionError:
        return 500, {"detail": "Không thể kết nối đến Server Backend!"}