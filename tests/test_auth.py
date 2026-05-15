"""
Auth tests — register, login, token validation.
"""


# --- Registration ---

def test_register_success(client):
    response = client.post("/auth/register", json={
        "username": "alice",
        "password": "secret123",
    })
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "alice"
    assert data["role"] == "user"
    assert "id" in data
    # password should NOT be in the response!
    assert "password" not in data
    assert "hashed_password" not in data


def test_register_duplicate_fails(client):
    # Register once
    client.post("/auth/register", json={
        "username": "alice",
        "password": "secret123",
    })
    # Try to register again with same username
    response = client.post("/auth/register", json={
        "username": "alice",
        "password": "different",
    })
    assert response.status_code == 400
    assert "already taken" in response.json()["detail"]


# --- Login ---

def test_login_success(client):
    # Register first
    client.post("/auth/register", json={
        "username": "alice",
        "password": "secret123",
    })
    # Login (note: form data, not JSON!)
    response = client.post("/auth/login", data={
        "username": "alice",
        "password": "secret123",
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    client.post("/auth/register", json={
        "username": "alice",
        "password": "secret123",
    })
    response = client.post("/auth/login", data={
        "username": "alice",
        "password": "wrongpassword",
    })
    assert response.status_code == 401


def test_login_nonexistent_user(client):
    response = client.post("/auth/login", data={
        "username": "nobody",
        "password": "whatever",
    })
    assert response.status_code == 401
