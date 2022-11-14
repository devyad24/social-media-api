from passlib.context import CryptContext

##using bcrypt hashing algo
pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash(pswrd: str):
    return pwd_context.hash(pswrd)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password,hashed_password) #.verify will automatically convert plain_pass to hash and then compare 