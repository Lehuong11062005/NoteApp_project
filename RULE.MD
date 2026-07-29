# 📌 RULE.MD — Quy tắc làm việc trong dự án NoteApp

> Tất cả thành viên và AI assistant phải tuân thủ tuyệt đối các quy tắc dưới đây.

---

## 1. Bắt buộc đọc trước khi làm việc

- **Luôn luôn đọc file `CauTruc`** trước khi bắt đầu bất kỳ công việc nào.
- **Luôn luôn đọc file `task.md`** để nắm rõ yêu cầu công việc cần làm.
- Thông báo xác nhận đã đọc và hiểu trước khi bắt tay thực hiện.

---

## 2. Không được tạo file mới

- **Tuyệt đối không tạo thêm file mới** ngoài danh sách file đã có trong `CauTruc`.
- Nếu cần thêm chức năng, **chỉ được thêm hàm/method vào các file đã tồn tại** đúng layer.
- Mọi thay đổi phải nằm trong phạm vi các file được quy định.

---

## 3. Hạn chế chỉnh sửa file đã có code

- **Hạn chế tối đa việc sửa đổi** các file đã có code sẵn.
- Chỉ **thêm** (append) code mới, không được xóa hoặc thay đổi logic cũ nếu không được yêu cầu rõ ràng.
- Các hàm/method cũ phải được giữ nguyên, không được đổi tên hay thay đổi signature.

---

## 4. Chỉ gọi hàm từ các file đã có

- Không được viết logic trực tiếp vào tầng không phù hợp.
- **Chỉ gọi hàm** từ các file/layer dưới — không tự xử lý logic ở tầng trên.
- Ví dụ: `View` chỉ gọi `Controller`, `Controller` chỉ gọi `Service/API`, không được nhảy cóc tầng.

---

## 5. Tuân thủ kiến trúc phân tầng (Layered Architecture)

Thứ tự gọi bắt buộc theo một chiều từ trên xuống:

```
Frontend:
  View  →  Controller  →  API (services)  →  APIClient  →  Backend

Backend:
  Route  →  Service  →  Repository  →  Database
```

- **Tuyệt đối không** để tầng dưới gọi ngược lên tầng trên.
- **Tuyệt đối không** để `View` gọi thẳng `Repository` hay `Database`.

---

## 6. Quy tắc đặt file đúng thư mục

Mọi file phải nằm đúng thư mục theo cấu trúc trong `CauTruc`:

| Loại file | Thư mục |
|---|---|
| Routes (endpoint) | `Backend/app/routes/` |
| Service (logic) | `Backend/app/services/` |
| Repository (DB) | `Backend/app/repositories/` |
| Middleware | `Backend/app/middleware/` |
| Schema (Pydantic) | `Backend/app/schemas/` |
| View (UI Tkinter) | `Frontend/views/` |
| Controller | `Frontend/controllers/` |
| API calls | `Frontend/services/` |
| Model (data class) | `Frontend/models/` |

---

## 7. Quy tắc commit Git

- Commit message phải **ngắn gọn**, rõ ràng theo format:
  ```
  feat: mô tả ngắn chức năng thêm vào
  fix: mô tả ngắn lỗi đã sửa
  refactor: mô tả ngắn việc tái cấu trúc
  ```
- Mỗi tính năng phải làm trên **nhánh riêng**, không commit thẳng vào `main`.

---

## 8. Môi trường chạy

- Sử dụng **venv chung** đặt ở thư mục gốc (`NoteApp_project/venv/`).
- Kích hoạt venv trước khi chạy Backend hoặc Frontend:
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- Chạy Backend:
  ```powershell
  cd Backend
  $env:PYTHONUTF8="1"; uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
  ```
- Chạy Frontend:
  ```powershell
  cd Frontend
  $env:PYTHONUTF8="1"; python main.py
  ```

---

> ⚠️ **Vi phạm bất kỳ quy tắc nào ở trên đều phải hoàn tác và làm lại đúng cách.**
