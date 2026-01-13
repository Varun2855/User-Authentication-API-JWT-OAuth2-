from passlib.context import CryptContext
from jose import jwt,JWTError
from datetime import datetime,timedelta,timezone
from fastapi import Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from getdb import get_db
import models
import os
from dotenv import load_dotenv

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

def hashpassword(password:str)->str:
    return pwd_context.hash(password)

def verifypassword(password:str,hashed_password:str)->bool:
    return pwd_context.verify(password,hashed_password)


load_dotenv() 

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

def create_access_token(data:dict,expires_delta:timedelta|None=None):
    to_encode=data.copy()

    expire=datetime.now(timezone.utc)+(expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp":expire})

    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithm=ALGORITHM)
        user_id:str=payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401)
    except JWTError:
        raise HTTPException(status_code=401)
    
    user=db.query(models.User).filter(models.User.id==int(user_id)).first
    if user is None:
        raise HTTPException(status_code=401)
    return user



