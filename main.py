from fastapi import FastAPI,HTTPException,Depends
from fastapi.security import OAuth2PasswordRequestForm
from database import session,engine
import models
import schemas 
from sqlalchemy.orm import Session
from typing import Annotated
import auth
from getdb import get_db

app=FastAPI()

models.Base.metadata.create_all(bind=engine)




#create user
@app.post("/users",response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate,db:Session=Depends(get_db)):
    db_user=models.User(username=user.username,hashpass=auth.hashpassword(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/{user_id}",response_model=schemas.UserOut)
def get_user(user_id:int ,db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==user_id).first()
    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    return user

#old login with only JWT (wont work with Oauth)
# @app.post("/login") #Login proves identity once JWT proves it for every upcoming request
# def login(data:schemas.LoginRequest,db:Session=Depends(get_db)):
#     user=db.query(models.User).filter(models.User.username==data.username).first()

#     if not user or not auth.verifypassword:
#         raise HTTPException(status_code=401,detail="Invalid username")
    
#     if not auth.verifypassword(data.password,user.hashpass):
#         raise HTTPException(status_code=401,detail="Invalid password")
    
#     token=auth.create_access_token(data={"sub:": str(user.id)})

#     return {
#     "access_token": token,
#     "token_type": "bearer"
# }


@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(
        models.User.username == form_data.username
    ).first()

    if not user or not auth.verifypassword(form_data.password, user.hashpass):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = auth.create_access_token(
        data={"sub": str(user.id)}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@app.get("/me")
def me(user:Annotated[models.User,Depends(auth.get_current_user)]):
    return {"id":user.id,"username":user.username}



             
         