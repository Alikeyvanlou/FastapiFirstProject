import os

os.environ["TESTING"] = "true"

from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database.db import Base
from dependencies.dependencies import get_db
from main import app


@pytest.fixture(scope="session")
def engine():
    return create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )


@pytest.fixture
def db(engine):
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app, base_url="https://testserver") as client:
        yield client
    app.dependency_overrides.clear()


@pytest.fixture
def register_user(client):
    payload = {
        "username": "ali",
        "email": "ali@example.com",
        "password": "string",
        "password_repeat": "string",
    }
    response = client.post("/users/register", json=payload)
    assert response.status_code == 201, f"Register failed: {response.status_code} - {response.text}"
    return response


@pytest.fixture
def login_user(client, register_user):
    response = client.post("/users/login", data={"username": "ali", "password": "string"})
    assert response.status_code == 200, f"Login failed: {response.status_code} - {response.text}"
    return response


@pytest.fixture
def auth_user(client, login_user):
    data_login = login_user.json()
    access_token = data_login["access_token"]
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def create_cost(client, auth_user):
    cost_data = {
        "title": "gym",
        "amount": 2.1,
        "create_at": datetime.now().strftime("%a %d %b %Y, %I:%M%p"),
    }
    response = client.post("/costs/", headers=auth_user, json=cost_data)
    assert response.status_code == 201, (
        f"Create cost failed: {response.status_code} - {response.text}"
    )
    return response
