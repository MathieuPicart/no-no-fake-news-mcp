from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "No No Fake News"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "postgresql://nnfn_user:nnfn_password@localhost:5432/nnfn_db"
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # External APIs
    GOOGLE_FACT_CHECK_API_KEY: str = ""
    NEWS_API_KEY: str = ""
    
    # Scraping
    USER_AGENT: str = "No-No-Fake-News-Bot/0.1 (+https://nonnofakenews.com/about)"
    REQUEST_TIMEOUT: int = 10

    class Config:
        env_file = ".env"

settings = Settings()
