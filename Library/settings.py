import os
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret
from db import database as databases

# Load from .env or environment
config = Config(".env")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = config("DEBUG", cast=bool, default=True)
TESTING = config("TESTING", cast=bool, default=False)
SECRET_KEY = config("SECRET_KEY", cast=Secret, default="super-secret-key")
ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=CommaSeparatedStrings, default="*")
PROJECT_NAME = "Library Management System"
PREFIX = ""
VERSION = "0.1.0"

# Database setup
if TESTING:
    DATABASE_URL = databases.DatabaseURL("sqlite:///test.db")
else:
    DATABASE_URL = config("DATABASE_URL", cast=databases.DatabaseURL)
