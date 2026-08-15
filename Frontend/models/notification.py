class Notification:
    def __init__(self, id, title, message, is_read=False, created_at=None, notification_type="reminder", source_id=None):
        self.id = str(id)
        self.title = title
        self.message = message
        self.is_read = is_read
        self.created_at = created_at
        self.type = notification_type
        self.source_id = source_id

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get("id") or data.get("_id", ""),
            title=data.get("title", ""),
            message=data.get("message", ""),
            is_read=data.get("is_read", False),
            created_at=data.get("created_at"),
            notification_type=data.get("type", "reminder"),
            source_id=data.get("source_id")
        )
