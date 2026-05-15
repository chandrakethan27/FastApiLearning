"""
Book CRUD tests — create, read, update, delete.
Uses the auth_headers fixture for protected routes.
"""


SAMPLE_BOOK = {
    "title": "Dune",
    "author": "Frank Herbert",
    "pages": 412,
    "price": 14.99,
}


# --- List (public, no auth needed) ---

def test_list_books_empty(client):
    response = client.get("/books/")
    assert response.status_code == 200
    assert response.json() == []


# --- Create (auth required) ---

def test_create_book_success(client, auth_headers):
    response = client.post("/books/", json=SAMPLE_BOOK, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Dune"
    assert data["author"] == "Frank Herbert"
    assert "id" in data


def test_create_book_without_auth_fails(client):
    response = client.post("/books/", json=SAMPLE_BOOK)
    assert response.status_code == 401


# --- Read ---

def test_get_book_by_id(client, auth_headers):
    # Create a book first
    create_resp = client.post("/books/", json=SAMPLE_BOOK, headers=auth_headers)
    book_id = create_resp.json()["id"]

    # Fetch it
    response = client.get(f"/books/{book_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Dune"


def test_get_book_not_found(client):
    response = client.get("/books/999")
    assert response.status_code == 404


# --- Update ---

def test_update_book_partial(client, auth_headers):
    # Create
    create_resp = client.post("/books/", json=SAMPLE_BOOK, headers=auth_headers)
    book_id = create_resp.json()["id"]

    # Update only the price
    response = client.patch(
        f"/books/{book_id}",
        json={"price": 19.99},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["price"] == 19.99
    assert data["title"] == "Dune"  # unchanged!


# --- Delete ---

def test_delete_book(client, auth_headers):
    # Create
    create_resp = client.post("/books/", json=SAMPLE_BOOK, headers=auth_headers)
    book_id = create_resp.json()["id"]

    # Delete
    response = client.delete(f"/books/{book_id}", headers=auth_headers)
    assert response.status_code == 204

    # Verify it's gone
    response = client.get(f"/books/{book_id}")
    assert response.status_code == 404


def test_delete_nonexistent_book(client, auth_headers):
    response = client.delete("/books/999", headers=auth_headers)
    assert response.status_code == 404
