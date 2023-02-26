

from datetime import datetime
from pydantic import BaseModel,EmailStr,conint
from typing import Optional


class Post(BaseModel):  # forcing str inputs only from pydentic packadge(pydentic)
    title:str
    content:str
    published:bool=True #---> so we don't have to enter the published column in the request (default is true)


# Handling the response from us to the user 
#creating a schema for what should the user see 

class PostResponse(BaseModel):
    title: str
    content: str
    user_id:int
    created_at:datetime

    class Config:
        orm_mode = True   #we added this here to translate sqlalchemy response to pydantic dictionary beacause pydentic only understands dicts()

        #Notice it's assigning a value with =, like:
         #orm_mode = True  

         #It doesn't use : as for the type declarations before.
         
         #Pydantic's orm_mode will tell the Pydantic model to read the data even if it is not a dict, but an ORM model (or any other arbitrary object with attributes).

         #This is setting a config value, not declaring a type.

class user_create(BaseModel):
    email:EmailStr
    password:str


#schema for the response for the user  !!!!DON'T FORGET YH BELOW CODE !!! when creating a response 
#class Config:
        #orm_mode = True


class UserOut(BaseModel):
    id :int
    email:EmailStr
    class Config:
        orm_mode = True

class Get_Posts(BaseModel):     
    id:int
    title:str
    content:str
    created_at:datetime
    owner:UserOut
    

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email:EmailStr
    password:str


class Token(BaseModel):
    access_token:str
    token_type: str
    class Config:
        orm_mode = True

class TokenData(BaseModel):
    id:Optional[str]=None


class Vote(BaseModel):
    post_id:int
    dir:conint(le=1)#--> for voting and removing the vote 1 or zero (less than 1 ) so the nefatives are allowd !


