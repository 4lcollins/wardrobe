import os
from dotenv import load_dotenv

load_dotenv()

class DevelopmentConfig():
    ENV = "development"
    ENV_CODE = "dev"
    LOG_LEVEL = "DEBUG"
    DATA_PATH = "data/dev"
    OPEN_WEATHER_MAP_KEY = os.getenv("OPENWEATHERMAP_API_SHARED")

class ProductionConfig():
    ENV = "production"
    ENV_CODE = "prod"
    LOG_LEVEL = "INFO"
    DATA_PATH = "data/prod"
    OPEN_WEATHER_MAP_KEY = os.getenv("OPENWEATHERMAP_API_SHARED")

def get_config():
    env = os.getenv("APP_ENV", "prod").lower()
    if env == "prod":
        return ProductionConfig()
    else:
        return DevelopmentConfig()

CONFIG = get_config()