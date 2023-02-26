#STEP 1 
# WE NEED TO TALK TO THE ORM USING PYTHON AND THE ORM WILL TALK TO THE DB USING SQL(no more pgadmin4) 
#SQLALCHEMY IS ONE OF THE MOST POPULAR PYTHON ORMS
#ITS A STANDALONE LIBRARY AND HAS NO ASSOSIATION WITH FASTAPI /IT CAN BE USED WITH ANY WEB FRAMEWORK
#SQLALCHEMY DOESN'T KNOW HOW TO SPEAK TO THE DB ---> IT NEED THE UNDERLYING DRIVER TO DO SO(psycopg2)
#navigate to fastapi docs for sql dbs https://fastapi.tiangolo.com/tutorial/sql-databases/ and follow the steps 



from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi.params import Body #retrive data posted
from.config import settings


#######IF WE WANT TO USE [SQL ALCHMEY] USE THE BELOW CODE #########

# cut and paste this code for anyfuture project
#SQLALCHEMY_DATABASE_URL_FORMAT="postgresql://<username>:<password>@<ip-address/hostname>/<databas_name>"
SQLALCHEMY_DATABASE_URL=f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}" # --> don't hardcode the un and pw 
# then we need to create an engine to establis a connection
engine=create_engine(SQLALCHEMY_DATABASE_URL)
# then we create a seesion to talk to the SQL db
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()

#then we create a model file to store all the models we create (models)


# Dependency to be passed to the path variable to make a session and close everytime we make a connection to an api endpoint
def get_db():
    db = SessionLocal()# ----> from database file
    try:
        yield db
    finally:
        db.close()


############IF WE WANT TO RUN [RAW SQL] WE CAN RUN THE BLEOW COMMAND#---->TO WORK [import time AND import psycopg2 AND from psycopg2.extras import RealDictCursor]

#while True: 
   # try:
       # conn = psycopg2.connect(host=f'{settings.database_hostname}',database=f'{settings.database_name}',user=f'{settings.database_username}',password=f'{settings.database_password}',cursor_factory=RealDictCursor)
        #cursor = conn.cursor()
       # print("Database connection was successful")
       # break
    #except Exception as error :
      #  print("connecting to database failed")
        #print("error was :", error)
        #time.sleep(2)
###################################-----------------------------------------#######################################

  # WE FIRST INCLUDE THE ROUTER IN THE (main) file   INSTEAD OF APP AND app.include_router(database.router) AND HERE ON database use router=APIRouter( prefix="/sql")
   
        
#app.post("/sqlposts",status_code=status.HTTP_201_CREATED) #POST API and retrieving thr data out if it
#EVERY TIME YOU CREATE A POST IT SHOULD RETURN 201 STATUS CODE
#def create_post(post:schema.Post):
   # WE used the %s as a placeholder so that we don't hardcode our entry to avoid sql ingection
   # new_post=cursor.fetchone() #here we just in the staging area so we need to commit the new post to the DB like below :
    #conn.commit() # comminting to save the changes we made to the database 
    #return { "data" : new_post}




#@app.get("/sqlposts/{id}") # get a specific post using it's id 
#def get_post(id:int): #------> here we inforce the users to enter an integer
  #  cursor.execute(""" SELECT * FROM posts WHERE id=%s """,(str(id),)) #------> str of id bc id is int in the function and it should be passed as a string in the SQL 
   # post= cursor.fetchone()
    #if not post : # Here we should give a correct status code to the frontend
     #   raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id :{id} was not found")
    #return(post)
   



#@app.delete("/sqlposts/{id}",status_code=status.HTTP_204_NO_CONTENT) #when ever you delete u use 204 status code
#def delete_post(id:int):

  #  cursor.execute(""" DELETE  FROM posts WHERE id = %s RETURNING * """, (str(id)),)
   # deleted_post=cursor.fetchone()

    #if deleted_post==None:
     #   raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the post with {id} is not found ")
    #conn.commit()
    #return Response(status_code=status.HTTP_204_NO_CONTENT)  # when deleting something you shouldn't send/return any data back to the frontend 


#@app.put("/sqlposts/{id}")
#def update_post(id:int,post:schema.Post):
 #   cursor.execute(""" UPDATE posts SET title =%s ,content=%s,published=%s WHERE id = %s RETURNING *""",(post.title,post.content,post.published,(str(id))))
  #  updated_post=cursor.fetchone()
   # if updated_post==None:
    #    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the post with {id} is not found ")
    #conn.commit()
    #print(post)
    #return{'data':updated_post}

