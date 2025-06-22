from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl

class Settings(BaseSettings):
    agent_id: str = "agent-001"
    nacfy_server: AnyHttpUrl = "http://localhost:3000"
    fetch_interval: int = 60    # heartbeat 주기(초)
    class Config:
        env_file = ".env"

settings = Settings()
