# tests/integration/test_endpoints.py
from uuid import UUID

"""
# tests/integration/test_endpoints.py
def test_create_and_get_user_via_api(client):
    data = {
        "username": "raj",
        "email": "raj@example.com",
        "password": "Secure123",
        "first_name": "Rajat",
        "last_name": "Pednekar"
    }
    res = client.post("/users/", json=data)
    assert res.status_code in (200, 201), res.text  # include res.text for debugging if fails
    body = res.json()
    assert "id" in body
    assert body["username"] == "raj"
    assert body["email"] == "raj@example.com"

    user_id = body["id"]
    get_res = client.get(f"/users/{user_id}")
    assert get_res.status_code == 200
    assert get_res.json()["username"] == "raj"
"""


def test_root_or_docs(client):
    response = client.get("/docs")
    assert response.status_code == 200

