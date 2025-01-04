import pytest
from app import create_app, db
import sys

from config.config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

@pytest.fixture
def test_app():
    app = create_app()
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(test_app):
    return test_app.test_client()