from passlib.context import CryptContext  #for hashing the passwords stored in the db 


pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")#--> Hashing algorithm

def hash(password:str):
    return pwd_context.hash(password)

# function to compare the hashes of the user password 
def verify(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)
