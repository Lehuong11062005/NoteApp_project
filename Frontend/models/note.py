class Note:
    def __init__(self, id, title, content, category, priority, create_at, reminder_time=None, image_url=None):
        self.id = id
        self.title = title
        self.content = content
        self.category = category
        self.priority = priority
        self.create_at = create_at
        self.reminder_time = reminder_time
        self.image_url = image_url