import logging
from datetime import datetime, timezone
from dateutil import parser
from app.config.database import get_database
from app.models.notification import create_notification_document
from app.services.email_service import EmailService
from app.utils.datetime_helper import (
    get_utc_now,
    parse_vietnam_datetime_to_utc,
    format_to_vietnam_str
)
from bson import ObjectId

logger = logging.getLogger(__name__)

def parse_datetime_flexible(dt_val) -> datetime:
    """Chuyển đổi chuỗi hoặc datetime (giờ Việt Nam) sang đối tượng datetime có timezone UTC chuẩn."""
    return parse_vietnam_datetime_to_utc(dt_val)

def check_and_trigger_reminders():
    """
    Hàm scheduler chạy định kỳ mỗi 60 giây:
    1. Quét ghi chú (notes) và lịch nhắc (reminders) đến giờ hẹn (<= now).
    2. Lấy email người dùng từ MongoDB.
    3. Gửi email qua Brevo.
    4. Tạo bản ghi thông báo trong collection 'notifications'.
    5. Cập nhật cờ 'reminder_notified = True'.
    """
    try:
        db = get_database()
        if db is None:
            return

        now = get_utc_now()
        email_svc = EmailService()

        # -------------------------------------------------------------
        # 1. XỬ LÝ GHI CHÚ (Collection 'notes')
        # -------------------------------------------------------------
        notes_collection = db["notes"]
        users_collection = db["users"]
        notifications_collection = db["notifications"]

        # Tìm các note có reminder_time mà chưa gửi thông báo
        cursor_notes = notes_collection.find({
            "reminder_time": {"$exists": True, "$ne": None},
            "reminder_notified": {"$ne": True},
            "status": {"$ne": "Đã hoàn thành"}
        })

        for note in cursor_notes:
            raw_reminder = note.get("reminder_time")
            reminder_dt = parse_datetime_flexible(raw_reminder)
            if not reminder_dt:
                continue

            # Nếu đã đến hoặc quá giờ hẹn
            if reminder_dt <= now:
                user_id_raw = note.get("user_id")
                user_doc = None
                if user_id_raw:
                    try:
                        user_doc = users_collection.find_one({"_id": ObjectId(str(user_id_raw))})
                    except Exception:
                        pass
                    if not user_doc:
                        user_doc = users_collection.find_one({"_id": user_id_raw})

                user_email = ""
                user_name = "Bạn"
                if user_doc:
                    user_email = user_doc.get("email", "").strip()
                    user_name = user_doc.get("fullname") or user_doc.get("username", "Bạn")

                note_title = note.get("title", "Ghi chú")
                note_content = note.get("content", "")
                reminder_display_str = format_to_vietnam_str(raw_reminder, "%H:%M ngày %d/%m/%Y")

                # Gửi email qua Brevo nếu có email
                if user_email:
                    try:
                        email_svc.send_reminder_email(
                            to_email=user_email,
                            to_name=user_name,
                            title=note_title,
                            content=note_content,
                            reminder_time=reminder_display_str
                        )
                    except Exception as e:
                        logger.error(f"Lỗi khi gửi email nhắc nhở note {note.get('_id')}: {e}")

                # Tạo thông báo in-app
                notif_doc = create_notification_document(
                    user_id=str(user_id_raw),
                    title=f"⏰ Lịch hẹn: {note_title}",
                    message=f"Đã đến giờ nhắc nhở ({reminder_display_str}): {note_content[:80] if note_content else note_title}",
                    notification_type="reminder",
                    source_id=str(note["_id"])
                )
                notifications_collection.insert_one(notif_doc)

                # Đánh dấu note đã được thông báo và cập nhật status sang Quá hạn (nếu chưa hoàn thành)
                notes_collection.update_one(
                    {"_id": note["_id"]},
                    {"$set": {
                        "reminder_notified": True,
                        "status": "Quá hạn",
                        "update_at": now
                    }}
                )
                logger.info(f"Đã kích hoạt thông báo cho Note: {note_title} ({note['_id']})")

        # -------------------------------------------------------------
        # 2. XỬ LÝ LỊCH NHẮC (Collection 'reminders' nếu có)
        # -------------------------------------------------------------
        reminders_collection = db["reminders"]
        cursor_reminders = reminders_collection.find({
            "reminder_time": {"$exists": True, "$ne": None},
            "reminder_notified": {"$ne": True},
            "status": "pending"
        })

        for rem in cursor_reminders:
            raw_reminder = rem.get("reminder_time")
            reminder_dt = parse_datetime_flexible(raw_reminder)
            if not reminder_dt:
                continue

            if reminder_dt <= now:
                user_id_raw = rem.get("user_id")
                user_doc = None
                if user_id_raw:
                    try:
                        user_doc = users_collection.find_one({"_id": ObjectId(str(user_id_raw))})
                    except Exception:
                        pass
                    if not user_doc:
                        user_doc = users_collection.find_one({"_id": user_id_raw})

                user_email = user_doc.get("email", "").strip() if user_doc else ""
                user_name = user_doc.get("fullname") or user_doc.get("username", "Bạn") if user_doc else "Bạn"

                rem_title = rem.get("title", "Lịch nhắc")
                rem_desc = rem.get("description", "")
                reminder_display_str = format_to_vietnam_str(raw_reminder, "%H:%M ngày %d/%m/%Y")

                if user_email:
                    try:
                        email_svc.send_reminder_email(
                            to_email=user_email,
                            to_name=user_name,
                            title=rem_title,
                            content=rem_desc,
                            reminder_time=reminder_display_str
                        )
                    except Exception as e:
                        logger.error(f"Lỗi khi gửi email nhắc nhở reminder {rem.get('_id')}: {e}")

                notif_doc = create_notification_document(
                    user_id=str(user_id_raw),
                    title=f"⏰ Lịch nhắc: {rem_title}",
                    message=f"Đã đến giờ nhắc nhở ({reminder_display_str}): {rem_desc[:80] if rem_desc else rem_title}",
                    notification_type="reminder",
                    source_id=str(rem["_id"])
                )
                notifications_collection.insert_one(notif_doc)

                reminders_collection.update_one(
                    {"_id": rem["_id"]},
                    {"$set": {
                        "reminder_notified": True,
                        "status": "overdue",
                        "updated_at": now
                    }}
                )
                logger.info(f"Đã kích hoạt thông báo cho Reminder: {rem_title} ({rem['_id']})")

    except Exception as e:
        logger.error(f"Lỗi trong quá trình chạy check_and_trigger_reminders: {e}")
