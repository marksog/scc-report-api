import pytest
from app import create_app, db
from app.models import User

@pytest.fixture
def test_client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_user_creation(test_client):
    with test_client.application.app_context():
        user = User(username="testuser", email="test@example.com", password_hash="hashed")
        db.session.add(user)
        db.session.commit()
        assert user.id is not None