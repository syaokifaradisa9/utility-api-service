import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.getenv("ENV_PATH", ".env"))

class Settings:
    API_KEY: str = os.getenv("API_KEY")
    RATE_LIMIT: str = os.getenv("RATE_LIMIT", "5/minute")

settings = Settings()