from datetime import datetime, timezone, timedelta
from typing import Optional, Union
from dateutil import parser

# Múi giờ chuẩn Việt Nam (UTC+7 / Asia/Ho_Chi_Minh)
VIETNAM_TZ = timezone(timedelta(hours=7), name="Asia/Ho_Chi_Minh")


def get_vietnam_now() -> datetime:
    """Lấy thời gian hiện tại theo múi giờ Việt Nam (UTC+7)."""
    return datetime.now(VIETNAM_TZ)


def get_utc_now() -> datetime:
    """Lấy thời gian hiện tại chuẩn UTC."""
    return datetime.now(timezone.utc)


def parse_vietnam_datetime_to_utc(dt_val: Union[datetime, str, None]) -> Optional[datetime]:
    """
    Chuyển đổi chuỗi hoặc đối tượng datetime (do người dùng nhập theo giờ Việt Nam)
    thành đối tượng datetime có timezone UTC chuẩn để lưu trữ DB và so sánh với UTC now.
    """
    if dt_val is None:
        return None
    
    if isinstance(dt_val, datetime):
        if dt_val.tzinfo is None:
            # Naive datetime -> Mặc định là giờ Việt Nam (UTC+7)
            dt_vn = dt_val.replace(tzinfo=VIETNAM_TZ)
            return dt_vn.astimezone(timezone.utc)
        return dt_val.astimezone(timezone.utc)
        
    elif isinstance(dt_val, str):
        dt_val = dt_val.strip()
        if not dt_val:
            return None
        try:
            dt = parser.parse(dt_val)
            if dt.tzinfo is None:
                # Nếu chuỗi không chứa offset múi giờ -> gán múi giờ Việt Nam (UTC+7)
                dt = dt.replace(tzinfo=VIETNAM_TZ)
            return dt.astimezone(timezone.utc)
        except Exception:
            return None
            
    return None


def to_vietnam_datetime(dt_val: Union[datetime, str, None]) -> Optional[datetime]:
    """
    Chuyển đổi datetime hoặc chuỗi ISO sang đối tượng datetime theo múi giờ Việt Nam (UTC+7).
    Nếu datetime là naive (ví dụ lấy từ MongoDB BSON date), mặc định coi là UTC.
    """
    if dt_val is None:
        return None
        
    if isinstance(dt_val, str):
        dt_val = dt_val.strip()
        if not dt_val:
            return None
        try:
            dt = parser.parse(dt_val)
        except Exception:
            return None
    elif isinstance(dt_val, datetime):
        dt = dt_val
    else:
        return None

    if dt.tzinfo is None:
        # Naive datetime từ MongoDB mặc định là UTC
        dt = dt.replace(tzinfo=timezone.utc)
        
    return dt.astimezone(VIETNAM_TZ)


def format_to_vietnam_str(dt_val: Union[datetime, str, None], fmt: str = "%H:%M ngày %d/%m/%Y") -> str:
    """
    Format thời gian sang chuỗi hiển thị thân thiện theo múi giờ Việt Nam (ví dụ: '19:10 ngày 15/08/2026').
    """
    dt_vn = to_vietnam_datetime(dt_val)
    if not dt_vn:
        return str(dt_val) if dt_val is not None else ""
    return dt_vn.strftime(fmt)
