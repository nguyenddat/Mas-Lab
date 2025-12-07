import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()
class Config(BaseSettings):
    # Directory
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Resources
    BACKEND_URL: str = os.getenv("BACKEND_URL")
    BACKEND_API_URL: str = f"{BACKEND_URL}/api"

config = Config()