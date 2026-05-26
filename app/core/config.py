from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "CV Analyzer API"
    GROQ_API_KEY: str
    GROQ_MODEL: str = "llama-3.3-70b-versatile" 

    class Config:
        env_file = ".env"
        # This ensures the app crashes immediately on startup 
        # if GROQ_API_KEY is missing from the .env file
        extra = "ignore" 

# Instantiate it once so it's cached in memory
settings = Settings()