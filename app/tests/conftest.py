import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi.testclient import TestClient
from app.database import Base, get_db
from app.main import app

TEST_DB_PATH = "./test.db"
TEST_DATABASE_URL = f"sqlite:///{TEST_DB_PATH}"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client(override_get_db):
    engine.dispose()

    if os.path.exists(TEST_DB_PATH):
        try:
            os.remove(TEST_DB_PATH)
        except PermissionError:
            import time
            time.sleep(0.5)
            os.remove(TEST_DB_PATH)

    Base.metadata.create_all(bind=engine)

    app.dependency_overrides[get_db] = lambda: override_get_db
    return TestClient(app)
