from jose import JWTError,jwt
from datetime import datetime,timedelta
from . import schema
from fastapi import Depends,HTTPException,status
from . import database
from fastapi.security import OAuth2PasswordBearer
from  sqlalchemy.orm import Session
from .config import settings
from .import models
# 1st is creataing the secret key that resides only on our server 
#2nd is the algorithm 
# 3rd the exiration for the token


#follow the instruction in fastapi docs it's the same as here
# if we want to pass the token manually in postman we can use in the authorization section Bearer <the access token > 
# below is the 3 main components we need for any token to be generated 

SECRET_KEY = settings.secret_key # we use this to encode/decode     
ALGORITHM = settings.algorithm 
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")

# this is where we create the access token
def create_access_token(data:dict):
    to_encode=data.copy()
    #an expected error here because minutes in timedelta is expecting a float not a str :
    # expire=datetime.utcnow()+str(timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    #TypeError: unsupported operand type(s) for +: 'datetime.datetime' and 'str'
    #the soloution is change to float
    expire=datetime.utcnow()+timedelta(minutes=float(ACCESS_TOKEN_EXPIRE_MINUTES))
    
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

#this is where we verify the access token given by the user and extarcting the id out of it 
def verfiy_access_token(token:str,credentials_exception):
    try:
        payload= jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])   # here we pass the three main components of the jwt to dycrypt it (decode it)
        id:str= payload.get("user_id") 
        if id is None :
            raise credentials_exception
        token_data=schema.TokenData(id=id)#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!111111
    except JWTError:
        raise credentials_exception
    return token_data #--->the user id  

#this is when want to enforce entering the token generated after the login
def get_current_user(token:str =Depends(oauth2_scheme),db:Session=Depends(database.get_db)):
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"couldnot validate credentials"

    ,headers={"www-Authenticate":"Bearer"})#1!!!!!!!!!!!!!!!!!!!!!11111111

    token=verfiy_access_token(token,credentials_exception)

    user=db.query(models.User).filter(models.User.id==token.id).first()

    return user