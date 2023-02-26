#STEP 2 
# Here we create our tables using python ( no more pgadmin4)
from .database import Base
from sqlalchemy import Column,INTEGER,String,Boolean,ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship



class Post(Base):
    #name your table
    __tablename__="posts"
    # import column from sqlalchemy to create columns and navigate to pgadmin table properties to get your configs
    #import integer from sqlalchemy and Nullable = not null option 
    id=Column(INTEGER,primary_key=True,nullable=False)
    # import string from sqlalchemy
    title=Column(String,nullable=False)
    content=Column(String,nullable=False)
    #import boolean from sqlalchemy
    published=Column(Boolean,nullable=False,server_default="False")#----> server default for default constrain 
    #import timestamp from sqlalchemy
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))#import text from sql alchemy
# then in the main file we import the models 
# then we create the dependency as refferred to in the docs of fastapi sql steps
    user_id=Column (INTEGER,ForeignKey("user.id",ondelete="CASCADE"), nullable=False)#---> this is the foreign key column
    owner=relationship("User") # gets us info about the owner response (built in sql alchemy) based on the relationship between the 2 tables




class User(Base):
    __tablename__="user"
    id=Column(INTEGER,primary_key=True,nullable=False)
    email=Column(String,nullable=False,unique=True)#---> unique value for email 
    password=Column(String,nullable=False) 
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))

class Vote(Base):
    __tablename__="votes"
    user_id=Column(INTEGER,ForeignKey("user.id",ondelete="CASCADE"),primary_key=True,nullable=True)
    post_id=Column(INTEGER,ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True,nullable=True)