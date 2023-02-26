# make sure you're in the venv by typing source /home/hazem/Documents/FastApi/venv/bin/activate
#first we put the main filr in app folder and to trest it as a python pacKage we add a file __init__.py and the run 
# uvicorn app.main:app --reload 
#always make sure your app runs in venv not Global ( view>commnd palette >select interpeter)
# To check the documention of your Fastapu you use the url /docs 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from  .routers import posts,users,Auth,votes
from.config import settings #---> for the class of the env variables 


origins = ["*"]
#######################################################################################
models.Base.metadata.create_all(bind=engine)# this is the code to create the tables in [sql alcehmy ]
# WE don't need the above line in case we used alembic bc alembic is the one who creates tables in this case not the engine for sqlalchemy
#######################################################################################
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(posts.router)    # importing the files from the router folder and check for a match if a HTTP request happens 
app.include_router(users.router)
app.include_router(Auth.router)
app.include_router(votes.router)
















