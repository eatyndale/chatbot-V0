from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_url: str = "sqlite:///./test.db"
    secret_key: str = ""
    OPENAI_API_KEY: str = ""
    # Add other settings as needed

    class Config:
        env_file = ".env"

def get_settings():
    return Settings()
