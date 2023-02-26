from fastapi import APIRouter,Depends,status,HTTPException,Response
from sqlalchemy.orm import Session
from .. import schema,models,utils
from .. import database,oauth
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


# in postman when we send the data to be authenticated we user the form data field and pass the username and password in thr Body section
#on postamn and on the Tests to automate the access token we pass pm.environment.set("JWT", pm.response.json().access_token); in json
# 




router=APIRouter(tags=["Authentication"]) #-----> REMEMBER TO INCLUDE THIS ROUTER INTO THE MAIN FILE app.include_router(Auth.Response)


@router.post("/login") #this AUTHENTICATION function verifies and creates a token for the user to be able to post/query/delete 
def login(user_credentials:OAuth2PasswordRequestForm=Depends(), db: Session = Depends(database.get_db)):

    user=db.query(models.User).filter(models.User.email==user_credentials.username).first() # in our schema w have email but on oautg pw request form it stores the email field in a username 
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"invaild credentials")

    if not utils.verify(user_credentials.password,user.password):#----> this function only compares between the data in the db with user data

        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"invaild credentials")

    #define token 
    #return token 
    access_token=oauth.create_access_token( data = { "user_id" :user.id})#--> data we want to pass in the payload

    return {"access_token": access_token , "token_type":"bearer"}

