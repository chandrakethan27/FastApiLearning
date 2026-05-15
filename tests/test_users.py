"""
User route tests — profile and protected access.
"""


def test_get_my_profile(client, auth_headers):
    response = client.get("/users/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["role"] == "user"


def test_get_profile_without_auth_fails(client):
    response = client.get("/users/me")
    assert response.status_code == 401


def test_list_users_requires_admin(client, auth_headers):
    # Regular user tries to list all users — should be forbidden
    response = client.get("/users/", headers=auth_headers)
    assert response.status_code == 403
