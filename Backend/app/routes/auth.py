from fastapi import APIRouter, HTTPException, status
from app.schemas.auth_schema import RegisterSchema
from app.services.auth_service import AuthService

router = APIRouter(tags=["Auth"])
auth_service = AuthService()

@router.post("/register")
def register(payload: RegisterSchema):
    try:
        success, message = auth_service.register_user(
            username=payload.username, 
            email=payload.email, 
            password=payload.password
        )
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=message
            )
        return {"message": message}
    except HTTPException as e:
        raise e
    except Exception as e:
        # Nếu Backend có lỗi chưa lường trước, trả về JSON detail thay vì để FastAPI báo lỗi 500 crash
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi Server: {str(e)}"
        )