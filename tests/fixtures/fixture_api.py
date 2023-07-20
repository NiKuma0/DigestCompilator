import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.main import init_app


@pytest.fixture
def app():
    return init_app()


@pytest.fixture
def testclient(app: FastAPI):
    return TestClient(app)
