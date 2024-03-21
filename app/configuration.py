import os
from dotenv import load_dotenv

load_dotenv()


# Base Configurations
class BaseConfig:
    DEBUG = True
    TESTING = False
    SECRET_KEY = os.getenv("SECRET_KEY")

    API_TITLE = "Store API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.2"
    OPENAPI_JSON_PATH = "api-spec.json"
    OPENAPI_URL_PREFIX = "/api/v1/"
    OPENAPI_REDOC_PATH = "/redoc"
    OPENAPI_REDOC_URL = (
        "https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"
    )
    OPENAPI_SWAGGER_UI_PATH = "/docs"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    OPENAPI_RAPIDOC_PATH = "/rapidoc"
    OPENAPI_RAPIDOC_URL = "https://unpkg.com/rapidoc/dist/rapidoc-min.js"


# Development Configurations
class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@localhost:5432/store-flask-smorest"


# Staging Configurations
class StagingConfig(BaseConfig):
    DEBUG = True
    TESTING = True


# Production Configurations
class ProductionConfig(BaseConfig):
    DEBUG = False
