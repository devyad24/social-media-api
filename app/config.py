from pydantic import BaseSettings

#setting up environment variables using pydantic models

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_mintues: int

    class Config:
        env_file = ".env"

settings = Settings()