import test
from sqlalchemy import create_engine
from utils import database_exists, create_database
from starlette.config import environ
from starlette.testclient import TestClient

# This line must come **before** importing settings to set testing environment
environ['TESTING'] = 'TRUE'

import settings
from db.database import Base
from main import app

@test.fixture(autouse=True, scope="session")
def setup_test_database():
    """
    Create a clean test database every time the tests are run.
    """
    url = str(settings.DATABASE_URL)
    engine = create_engine(url, connect_args={"check_same_thread": False})
    if not database_exists(url):
        create_database(url)  # Create the test database if it doesn't exist.
    Base.metadata.create_all(bind=engine)  # Create the tables.
    yield  # Run the tests.
    Base.metadata.drop_all(bind=engine)  # Drop the tables after tests.

@test.fixture()
def client():
    """
    Provide a test client for the FastAPI app.
    """
    with TestClient(app) as test_client:
        yield test_client
