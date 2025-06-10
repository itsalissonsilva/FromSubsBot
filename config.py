from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
    API_TOKEN: str
    MODERATOR_CHAT_ID: int
    CHANNEL_ID: int

    class Config:
        env_file = ".env"

settings = Settings(
    API_TOKEN=os.getenv("API_TOKEN"),
    MODERATOR_CHAT_ID=int(os.getenv("MODERATOR_CHAT_ID")),
    CHANNEL_ID=int(os.getenv("CHANNEL_ID"))
)