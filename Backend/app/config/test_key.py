from google import genai

import os
from dotenv import load_dotenv
load_dotenv()
API_KEY=os.getenv('GEMINI_API_KEY')

try:
    client = genai.Client(api_key=API_KEY)
    print("=== DANH SÁCH MODEL ĐƯỢC PHÉP DÙNG ===")
    
    # Liệt kê các model mà key này được phép gọi
    for model in client.models.list():
        # Chỉ in ra các model có chữ "gemini"
        if "gemini" in model.name.lower():
            print(f"- {model.name}")
            
    print("\nNếu bạn thấy 'models/gemini-1.5-flash' ở trên, Key này đã sẵn sàng!")
    
except Exception as e:
    print(f"Lỗi kiểm tra Key: {e}")