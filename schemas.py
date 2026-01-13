from pydantic import BaseModel

class UserBase(BaseModel):
    username:str

class UserCreate(UserBase):
    password:str

class UserOut(UserBase):
    id:int

class LoginRequest(BaseModel):
    username:str;
    password:str;

    class Config:
        from_attributes=True