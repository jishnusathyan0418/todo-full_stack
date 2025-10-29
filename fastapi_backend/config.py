from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    class Config():
        env_file = ".env"
        extra = "ignore"
        
        
settings = Settings()
