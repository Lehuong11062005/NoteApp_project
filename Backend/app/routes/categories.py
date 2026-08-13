from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.category_schema import CategoryCreateSchema, CategoryUpdateSchema
from app.services.category_service import CategoryService

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_category(
    category: CategoryCreateSchema,
    category_service: CategoryService = Depends() 
):
    try:
        return category_service.create_category(category)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", status_code=status.HTTP_200_OK)
def get_categories(
    category_service: CategoryService = Depends() 
):
    try:
        return category_service.get_all_categories()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{category_id}", status_code=status.HTTP_200_OK)
def update_category(
    category_id: str, 
    category: CategoryUpdateSchema,
    category_service: CategoryService = Depends() ):
    try:
        return category_service.update_category(category_id, category)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{category_id}", status_code=status.HTTP_200_OK)
def delete_category(
    category_id: str,
    category_service: CategoryService = Depends() 
):
    try:
        return category_service.delete_category(category_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))