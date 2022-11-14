from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

##connect sqlalchemy to postgres
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
 
##anytime we get a request, we make a session/connection to the server, after the request is over we close it
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ## loop for until we get connected to dbms server
# while True:
#     try:
#         ## cursor_factory helps in including columns from our table cause psycopg2 doesn't include them by default, it includes them in form of a dict
#         conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='sifthewoofer2411!',cursor_factory=RealDictCursor)
#         cursor = conn.cursor() ##used to executing sql statements
#         print("Database connected...")
#         break
#     except Exception as error:
#         print("Failed to connect to database.")
#         print("Error: ",error)
#         time.sleep(2) ##we try to connect after every 2 seconds