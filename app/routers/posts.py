from .. import models,schema,utils
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from  sqlalchemy.orm import Session
import psycopg2
from ..database import engine,get_db
from psycopg2.extras import RealDictCursor
from  sqlalchemy.orm import Session
from typing import Optional ,List      #       boolean
from .. import oauth
import time
from sqlalchemy.sql.functions import func







router=APIRouter(
    prefix="/posts", #/orm/{id}  the old way was @app.get("/orm/{id}") so we replaced /orm in the below path operators with only "/"
    tags=["posts"]   #----> this is for the swagger ui docs grouping 
)

@router.get("/")
def hello_message():
    return "hello world !!!"

## using ORM sqlalchemy
#on postman we defined an enviroment called dev in with  a URL :http://127.0.0.1:8000/ 

@router.get("/",response_model=list[schema.Get_Posts])
def get_posts(db: Session = Depends(get_db),current_user:int=Depends(oauth.get_current_user),
limit:int=10,skip:int=0,search:Optional[str]=""):# import depends from fastapi/everytime you work with orm you always pass the db: Session = Depends(get_db) in the path operation variable 
    
    posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()#----> if we want to limit the numbers of posts returned to a user 

    #posts=db.query(models.Post).filter(models.Post.content.contains(search)).limit(limit).offset(skip).all()#--> for searching keywords in content
    #results=db.query(models.Post,func.count(models.Vote.post_id).label("votes")
    #.join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id)).all()

    return posts
    # on postman we type {{URL}}posts?limit=5  and get only 5 posts / {{URL}}post-->> default is 10 posts if we didn't provide a number 
    #by defaualt postgres grabs first 10 posts or the no of posts based on the (limit) 
    # to SKIP by 2 or whatever we can define skip in the function and use offset(skip) in the query
    # #in post man type {{URL}}posts?limit=10&skip=2 it skips first 2 posts and fetchest the 3rd and the 4th from the first 10
    #limit:int=10,skip:int=0 those are the default values in case we didin't enter a valuse on postamn 
   # posts=db.query(models.Post).filter(models.Post.user_id==current_user.id).all() #from models file this allows us to access the posts table and query from it /.all means all the posts in the table
    # to use the search type {{URL}}posts?search=irst --> it will get all the titles that contain "irst"



@router.post("/",status_code=status.HTTP_201_CREATED)# on here the user first must be authenticated to post user_id:int=Depends(oauth.get_current_user) 
def create_posts(post:schema.Post,db: Session = Depends(get_db), current_user:int = Depends(oauth.get_current_user)):#---> to solve the error on creating posts without adding the user_id
    # the error and solution for creating posts with user_id column is in 8:17:30 on the video and starts from 7:39:00

    print(current_user.id)

    new_post=models.Post(title=post.title,content=post.content,published=post.published,user_id=current_user.id)


    db.add(new_post)
    db.commit()#------------>>>>> to push the changes
    db.refresh(new_post)
    return{new_post}






@router.get("/{id}")
def get_post(id:int,db: Session = Depends(get_db),current_user:int=Depends(oauth.get_current_user)  ):

    post=db.query(models.Post).filter(models.Post.id==id).first()
    if get_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the post with {id} is not found ")
    
    return{post}

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends(get_db),current_user:int=Depends(oauth.get_current_user) ): 
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()

    if post ==None: #---> here we put .first()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the post with {id} is not found ")

    if post.user_id !=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"You are not the owner , So you can't delete")

    post_query.delete(synchronize_session=False)
    db.commit()     
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}") 
def update_post(id:int,updated_post:schema.Post,db: Session = Depends(get_db),current_user:int=Depends(oauth.get_current_user)):

   post_query= db.query(models.Post).filter(models.Post.id==id) 

   post=post_query.first()#----> means first post no use for .all here 
   
   if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the post with {id} is not found ")
   if post.user_id !=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"You are not the owner , So you can't Update")


   post_query.update(updated_post.dict(),synchronize_session=False)

   db.commit()

   return{"data":post_query.first()}     

