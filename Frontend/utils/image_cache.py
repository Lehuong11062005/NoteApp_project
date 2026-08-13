"""
image_cache.py - Cache ảnh trong RAM cho Frontend.
Ảnh được tải một lần và lưu theo URL, giải phóng khi gọi clear().
"""
import io
import threading
import requests
from PIL import Image

# Cache chính: URL (str) -> PIL.Image object
_cache: dict = {}
_lock = threading.Lock()
_pending: set = set()  # Các URL đang được fetch để tránh fetch trùng


def get(url: str):
    """Lấy ảnh từ cache. Trả về PIL.Image hoặc None nếu chưa có."""
    with _lock:
        return _cache.get(url)


def put(url: str, img: Image.Image):
    """Lưu ảnh vào cache."""
    with _lock:
        _cache[url] = img
        _pending.discard(url)


def prefetch(url: str, on_done=None):
    """
    Tải ảnh từ URL vào cache trong background thread.
    on_done(url, img): callback tùy chọn khi tải xong.
    """
    if not url:
        return
    with _lock:
        if url in _cache or url in _pending:
            return
        _pending.add(url)

    def _fetch():
        img = _load_from_url_or_path(url)
        if img:
            put(url, img)
        else:
            with _lock:
                _pending.discard(url)
        if on_done:
            on_done(url, img)

    threading.Thread(target=_fetch, daemon=True).start()


def prefetch_many(urls: list):
    """Pre-fetch danh sách URL ảnh cùng lúc (không cần callback)."""
    for url in urls:
        prefetch(url)


def clear():
    """Xóa toàn bộ cache ảnh khỏi RAM (gọi khi logout hoặc đóng app)."""
    with _lock:
        _cache.clear()
        _pending.clear()


def _load_from_url_or_path(url_or_path: str):
    """Tải PIL.Image từ HTTP URL hoặc đường dẫn file cục bộ."""
    try:
        if url_or_path.startswith("http://") or url_or_path.startswith("https://"):
            resp = requests.get(url_or_path, timeout=8)
            if resp.status_code == 200:
                img = Image.open(io.BytesIO(resp.content))
                img.load()  # Đọc toàn bộ pixel data vào RAM
                return img
        else:
            img = Image.open(url_or_path)
            img.load()
            return img
    except Exception:
        pass
    return None
