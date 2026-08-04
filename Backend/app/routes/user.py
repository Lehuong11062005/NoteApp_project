from fastapi import APIRouter,Depends
from app.repositories.user_repository import UserRepository
from app.middleware.jwt_auth import verify_token
from app.schemas.auth_schema import UserGetInforSchema
router = APIRouter(prefix="/user",tags=["profile"])
@router.get("/profile",response_model=UserGetInforSchema,status_code=200)
def get_inf_user(current_user:dict = Depends(verify_token)):
    username = current_user["sub"]
    user = UserRepository()
    return user.find_by_username(username)
        
    
