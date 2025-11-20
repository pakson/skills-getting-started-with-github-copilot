import pytest
from fastapi.testclient import TestClient
import src.app as app_module


@pytest.fixture
def client():
    with TestClient(app_module.app) as c:
        yield c


def test_get_activities(client):
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # basic key check
    assert "Chess Club" in data


def test_signup_success(client):
    email = "newstudent@mergington.edu"
    activity = "Science Club"
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 200
    assert "Signed up" in resp.json().get("message", "")

    # verify participant actually added
    all_resp = client.get("/activities")
    participants = all_resp.json()[activity]["participants"]
    assert email in participants


def test_signup_duplicate(client):
    email = "michael@mergington.edu"  # already in Chess Club
    activity = "Chess Club"
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 400


def test_signup_not_found(client):
    email = "someone@mergington.edu"
    activity = "Nonexistent Activity"
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 404


def test_unregister_success(client):
    email = "benjamin@mergington.edu"
    activity = "Science Club"
    resp = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert resp.status_code == 200
    assert "Unregistered" in resp.json().get("message", "")


def test_unregister_not_registered(client):
    email = "notregistered@mergington.edu"
    activity = "Science Club"
    resp = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert resp.status_code == 404
