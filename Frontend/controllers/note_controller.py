from Frontend.services.upload_api import UploadAPI

class NoteController:
    def __init__(self, view=None):
        self.view = view  # view hiện tại (ví dụ: AddNoteWindow)

    def upload_image(self, filepath: str):
        """Gọi UploadAPI để tải ảnh lên server và trả về kết quả."""
        return UploadAPI.upload_image(filepath)
