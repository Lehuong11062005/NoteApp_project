from pydantic import BaseModel, EmailStr, Field

class UserRegisterSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    fullname: str = Field(..., min_length=2)
    email: EmailStr

class UserLoginSchema(BaseModel):
    username: str
    password: str
class UserGetInforSchema(BaseModel):
    username: str  
    fullname: str 
    email: EmailStr