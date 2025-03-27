import os
from dotenv import load_dotenv


load_dotenv()


class Settings:
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
    DATABASE_URL = os.getenv("DATABASE_URL")
    ACCESS_TOKEN_EXPIRE_MINUTES = 30


settings = Settings()
