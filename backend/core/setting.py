import os

from pydantic_settings import BaseSettings

class Config(BaseSettings):
    # Directory
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ARTIFACT_DIR: str = os.path.join(BASE_DIR, "artifacts")
    LOG_DIR: str = os.path.join(BASE_DIR, "logs")

    PAPER_DIR: str = os.path.join(ARTIFACT_DIR, "papers")

    # Resources
    DATABASE_URL: str = os.getenv("DATABASE_URL")

config = Config()
os.makedirs(config.ARTIFACT_DIR, exist_ok=True)
os.makedirs(config.LOG_DIR, exist_ok=True)
os.makedirs(config.PAPER_DIR, exist_ok=True)