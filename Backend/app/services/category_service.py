from datetime import datetime
from app.repositories.category_repository import CategoryRepository
from app.schemas.category_schema import CategoryCreateSchema, CategoryUpdateSchema


class CategoryService:
    def __init__(self):
        self.category_repo = CategoryRepository()

    def create_category(self, category_data: CategoryCreateSchema):
        data = category_data.dict()
        data["created_at"] = datetime.now()
        data["updated_at"] = datetime.now()
        category_id = self.category_repo.create_category(data)
        return {
            "id": category_id,
            "message": "Tạo category thành công"
        }

    def get_all_categories(self):
        return self.category_repo.get_all_categories()

    def update_category(self, category_id: str, category_data: CategoryUpdateSchema):
        update_data = category_data.dict(exclude_unset=True)
        if not update_data:
            return {"message": "Không có dữ liệu để cập nhật"}
        self.category_repo.update_category(category_id, update_data)
        return {"message": "Cập nhật category thành công"}

    def delete_category(self, category_id: str):
        deleted_count = self.category_repo.delete_category(category_id)
        return {
            "deleted_count": deleted_count,
            "message": "Xóa category thành công" if deleted_count else "Không tìm thấy category"
        }
