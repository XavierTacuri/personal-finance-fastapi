import os
import sys
import uuid

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine

from app.main import app
from app.api.deps import get_session


DATABASE_URL_TEST = "postgresql+psycopg2://postgres:postgres@localhost:5432/personal_finance_testdb"
if not DATABASE_URL_TEST:
    raise RuntimeError("Set  env var for tests")


engine_test = create_engine(DATABASE_URL_TEST, echo=False)


@pytest.fixture(scope="session", autouse=True)
def create_test_db():
    # OJO: Esto crea todas las tablas según tus modelos.
    SQLModel.metadata.drop_all(engine_test)
    SQLModel.metadata.create_all(engine_test)
    yield
    SQLModel.metadata.drop_all(engine_test)


@pytest.fixture()
def session():
    with Session(engine_test) as s:
        yield s


@pytest.fixture()
def client(session):
    # override dependency get_session para usar la session de tests
    def _override_get_session():
        yield session

    app.dependency_overrides[get_session] = _override_get_session

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


def auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def user_payload():
    unique = uuid.uuid4().hex[:10]
    return {
        "name_user": "OscarTest",
        "last_name": "TacuriTest",
        "email": f"test_{unique}@example.com",
        "password": "12345678",
    }

@pytest.fixture()
def token(client, user_payload):
    r = client.post("/auth/register", json=user_payload)
    if r.status_code != 201:
        print("REGISTER STATUS:", r.status_code)
        print("REGISTER BODY:", r.text)
    assert r.status_code == 201

    r = client.post("/auth/login", json={
        "email": user_payload["email"],
        "password": user_payload["password"],
    })
    if r.status_code != 200:
        print("LOGIN STATUS:", r.status_code)
        print("LOGIN BODY:", r.text)
    assert r.status_code == 200

    return r.json()["access_token"]