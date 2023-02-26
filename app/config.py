# on this file we set the enviroment variables so we don't hard code them in the code 

from pydantic import BaseSettings

class Settings(BaseSettings):
    database_hostname:str
    database_port:str
    database_password:str
    database_name:str
    database_username:str
    secret_key:str
    algorithm:str
    access_token_expire_minutes:str

    class Config:
        env_file=".env"  #---> to refer to the file that we have on our local machine 

settings=Settings()    
