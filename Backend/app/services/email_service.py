import os
import logging
from dotenv import load_dotenv
import brevo
from brevo.transactional_emails.types import (
    SendTransacEmailRequestSender,
    SendTransacEmailRequestToItem
)

load_dotenv()
logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.api_key = os.getenv("BREVO_API", "").strip()
        self.sender_email = os.getenv("BREVO_SENDER_EMAIL", "").strip() or "dangphongaob@gmail.com"
        self.sender_name = os.getenv("BREVO_SENDER_NAME", "Smart Note Reminder").strip()
        self.client = None
        if self.api_key:
            try:
                self.client = brevo.Brevo(api_key=self.api_key)
            except Exception as e:
                logger.error(f"Lỗi khởi tạo Brevo Client: {e}")

    def send_reminder_email(
        self, 
        to_email: str, 
        to_name: str, 
        title: str, 
        content: str, 
        reminder_time: str
    ) -> bool:
        """
        Gửi email thông báo nhắc nhở thông qua Brevo Transactional Email API.
        """
        if not self.client or not to_email:
            logger.warning(f"Không thể gửi email: Brevo Client chưa sẵn sàng hoặc thiếu to_email ({to_email})")
            return False

        subject = f"🔔 [Smart Note] Nhắc nhở lịch hẹn: {title}"

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{
                    font-family: 'Segoe UI', Arial, sans-serif;
                    background-color: #f4f7fc;
                    margin: 0;
                    padding: 20px;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: #ffffff;
                    border-radius: 12px;
                    overflow: hidden;
                    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
                }}
                .header {{
                    background: linear-gradient(135deg, #1976D2, #2196F3);
                    color: #ffffff;
                    padding: 24px;
                    text-align: center;
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 22px;
                    font-weight: 600;
                }}
                .content {{
                    padding: 28px 24px;
                    color: #333333;
                    line-height: 1.6;
                }}
                .greeting {{
                    font-size: 16px;
                    font-weight: 600;
                    color: #2E3A59;
                    margin-bottom: 12px;
                }}
                .card {{
                    background-color: #F8FAFC;
                    border-left: 4px solid #2196F3;
                    border-radius: 6px;
                    padding: 16px;
                    margin: 18px 0;
                }}
                .card-title {{
                    font-size: 17px;
                    font-weight: bold;
                    color: #0D47A1;
                    margin-bottom: 8px;
                }}
                .card-time {{
                    font-size: 14px;
                    color: #E65100;
                    font-weight: 600;
                    margin-bottom: 10px;
                }}
                .card-body {{
                    font-size: 14px;
                    color: #4A5568;
                    white-space: pre-wrap;
                }}
                .footer {{
                    background-color: #F1F5F9;
                    padding: 16px;
                    text-align: center;
                    font-size: 12px;
                    color: #888888;
                    border-top: 1px solid #E2E8F0;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>⏰ Thông Báo Nhắc Nhở</h1>
                </div>
                <div class="content">
                    <div class="greeting">Xin chào {to_name or 'bạn'},</div>
                    <p>Bạn có một lịch hẹn/ghi chú đã đến giờ cần thực hiện:</p>
                    
                    <div class="card">
                        <div class="card-title">📌 {title}</div>
                        <div class="card-time">⏰ Thời gian: {reminder_time}</div>
                        <div class="card-body">📝 {content if content else 'Không có nội dung chi tiết.'}</div>
                    </div>

                    <p>Hãy mở ứng dụng <strong>Smart Note</strong> để xem và cập nhật trạng thái công việc của bạn.</p>
                </div>
                <div class="footer">
                    Email tự động từ hệ thống Smart Note Assistant.<br>Vui lòng không trả lời email này.
                </div>
            </div>
        </body>
        </html>
        """

        try:
            sender_obj = SendTransacEmailRequestSender(
                name=self.sender_name,
                email=self.sender_email
            )
            to_item = SendTransacEmailRequestToItem(
                email=to_email,
                name=to_name or "User"
            )
            response = self.client.transactional_emails.send_transac_email(
                sender=sender_obj,
                to=[to_item],
                subject=subject,
                html_content=html_content
            )
            print(f"📧 [Brevo] Đã gửi email nhắc nhở tới {to_email} (MessageID: {getattr(response, 'message_id', 'OK')})")
            logger.info(f"Đã gửi email nhắc nhở qua Brevo tới {to_email}: {response}")
            return True
        except Exception as e:
            print(f"❌ [Brevo] Lỗi khi gửi email tới {to_email}: {e}")
            logger.error(f"Lỗi khi gửi email Brevo tới {to_email}: {e}")
            return False
