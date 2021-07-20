import pytest
from fastapi.testclient import TestClient

from backend.buffer.main import app

user = ("repview", "654321")


@pytest.fixture(scope="module")
def test_app_basic():
    client = TestClient(app)
    yield client


def test_auth_basic(test_app_basic):
    res = test_app_basic.get("/auth/user", auth=user)  # auth=(user, password))
    assert res.status_code == 200

# @pytest.fixture(scope="module")
# def test_app_oauth2():
#     client = TestClient(app_oauth2)
#     yield client
