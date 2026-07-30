# 📋 fask.md — Trạng thái & Kiểm tra Dự án NoteApp

> Cập nhật: 2026-07-30

---

## ✅ Xác nhận đã đọc

| File | Trạng thái |
|---|---|
| `RULE.MD` | ✅ Đã đọc và hiểu |
| `CauTruc` | ✅ Đã đọc và hiểu |
| `task.md` | ✅ Đã đọc và hiểu |

---

## 🌿 Git – Trạng thái hiện tại

- **Nhánh hiện tại:** `feature/image-upload` ✅ (đúng theo task.md)
- **Remote:** up to date với `origin/feature/image-upload`
- **Các nhánh có:** `feature/authencation`, `feature/image-upload`, `main`

### Working Directory

| Loại | File | Ghi chú |
|---|---|---|
| Staged | `.gitignore` | Đã stage chưa commit |
| Modified (unstaged) | `Backend/app/main.py` | Có thay đổi chưa commit |
| Modified (unstaged) | `Backend/app/routes/upload.py` | Có thay đổi chưa commit |
| Modified (unstaged) | `Backend/app/services/upload_service.py` | Có thay đổi chưa commit |
| Modified (unstaged) | `Frontend/views/add_note_view.py` | Có thay đổi chưa commit |
| Untracked | `Frontend/controllers/note_controller.py` | File mới, chưa được track |
| Untracked | `Frontend/services/upload_api.py` | File mới, chưa được track |

---

## ⚠️ Vấn đề Git Stash

### Stash hiện có:

```
stash@{0}: WIP on feature/authencation: ab6b818 chore: ignore RULE.MD, task.md, CauTruc
```

### 🔴 Phân tích vấn đề:

| # | Vấn đề | Mức độ | Giải thích |
|---|---|---|---|
| 1 | **Stash được tạo trên nhánh sai** | 🔴 Nghiêm trọng | Stash nằm trên `feature/authencation`, nhưng hiện đang làm việc ở `feature/image-upload`. Nội dung stash có thể không liên quan đến task hiện tại. |
| 2 | **Stash chỉ chứa `.gitignore`** | 🟡 Cần chú ý | Stash chỉ sửa 1 file `.gitignore` (+1/-2 dòng). Không có code nghiệp vụ quan trọng nào bị stash. |
| 3 | **Stash bị bỏ quên** | 🟡 Cần xử lý | Stash này được tạo ở nhánh `feature/authencation` nhưng chưa bao giờ được pop/apply. Cần quyết định xử lý. |
| 4 | **Nhiều file chưa commit ở working tree** | 🔴 Rủi ro mất code | `upload_service.py`, `upload.py`, `main.py`, `add_note_view.py`, `note_controller.py`, `upload_api.py` đang thay đổi nhưng chưa được commit. Nếu switch nhánh hoặc reset thì có thể mất code. |

### 🛠️ Hành động khuyến nghị:

```powershell
# Xem chi tiết thay đổi trong stash (chỉ .gitignore - ít rủi ro)
git stash show

# Nếu không cần nữa → xóa stash
git stash drop

# Commit các file đang sửa dở trước khi làm gì khác
git add Backend/app/main.py Backend/app/routes/upload.py `
        Backend/app/services/upload_service.py `
        Frontend/views/add_note_view.py `
        Frontend/controllers/note_controller.py `
        Frontend/services/upload_api.py
git commit -m "feat: upload image API (backend)"
```

---

## 📌 Checklist Task (từ task.md)

### Backend

| Task | File | Trạng thái |
|---|---|---|
| TASK 1 | `upload_service.py` — lưu file, trả URL | ✅ Đã có code (`save_image`, `upload_image_only`, `upload_file_local`) |
| TASK 2 | `routes/upload.py` — `POST /api/upload/image` + JWT | 🟡 Đã sửa (chưa commit) |
| TASK 3 | `main.py` — mount static + register router | 🟡 Đã sửa (chưa commit) |
| TASK 4 | `Backend/requirements.txt` — `python-multipart` | ❓ Chưa kiểm tra |

### Frontend

| Task | File | Trạng thái |
|---|---|---|
| TASK 5 | `upload_api.py` — `upload_image(filepath)` | ✅ Đã có code (untracked, cần `git add`) |
| TASK 6 | `note_controller.py` — `upload_image()` | ✅ Đã có file (untracked, cần `git add`) |
| TASK 7 | `add_note_view.py` — nút chọn ảnh + thumbnail | 🟡 Đã sửa (chưa commit) |
| TASK 8 | `Frontend/requirements.txt` — `Pillow` | ❓ Chưa kiểm tra |

---

## 📐 Kiểm tra tuân thủ RULE.MD

| Quy tắc | Trạng thái | Ghi chú |
|---|---|---|
| Đọc `CauTruc` trước khi làm | ✅ | Đã đọc |
| Không tạo file mới ngoài `CauTruc` | ✅ | `upload_api.py`, `note_controller.py`, `upload_service.py` đều có trong CauTruc |
| Chỉ thêm code, không xóa logic cũ | ✅ | Các file service đang append thêm hàm mới |
| Tuân thủ layered architecture | ✅ | View → Controller → Service → API → Backend |
| Đúng thư mục theo CauTruc | ✅ | Tất cả file đúng vị trí |
| Commit đúng format | ⚠️ | Chưa commit — cần commit theo format `feat:` / `fix:` |
| Làm trên nhánh `feature/image-upload` | ✅ | Đúng nhánh |

---

## 🚦 Tóm tắt ưu tiên cần làm ngay

1. 🔴 **Commit ngay** các file đang sửa dở để không mất code
2. 🟡 **Drop stash** `stash@{0}` nếu không cần (chỉ chứa thay đổi `.gitignore` nhỏ)
3. ❓ Kiểm tra `Backend/requirements.txt` đã có `python-multipart` chưa
4. ❓ Kiểm tra `Frontend/requirements.txt` đã có `Pillow` chưa
