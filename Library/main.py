import sys
from os.path import abspath, dirname

# Add parent directory to sys.path before any imports that rely on it
parent_path = dirname(dirname(abspath(__file__)))
sys.path.append(parent_path)

from fastapi import FastAPI
import settings
from api import api_router
from db.database import Base, engine
from student.models import Student
from book.models import Book
from order.models import Order

def get_application() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        debug=settings.DEBUG,
        version=settings.VERSION,
    )

    app.include_router(api_router, prefix=settings.PREFIX)

    @app.on_event("startup")
    def on_startup():
        Base.metadata.create_all(bind=engine)
        print("Welcome to the Library Management System!")

    return app

app = get_application()