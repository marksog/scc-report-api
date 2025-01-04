import pytest
from app import create_app, db
from app.models import User

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_register_login(client):
    # Register
    resp = client.post('/auth/register', json={
        "username":"tester",
        "email":"test@example.com",
        "password_hash":"pass123"
    })
    assert resp.status_code == 201

    # Login
    resp = client.post('/auth/login', json={
        "email":"test@example.com",
        "password":"pass123"
    })
    assert resp.status_code == 200
    data = resp.get_json()
    assert "access_token" in data