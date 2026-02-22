from urllib.parse import quote

from fastapi.testclient import TestClient
import app as app_module


def test_root_redirects_to_index(client: TestClient):
    # Arrange: client fixture provided
    # Act
    resp = client.get("/", follow_redirects=False)
    # Assert
    assert resp.status_code == 307
    assert resp.headers.get("location") == "/static/index.html"


def test_get_activities_returns_all(client: TestClient):
    # Arrange
    # Act
    resp = client.get("/activities")
    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data
    assert "Tennis Club" in data


def test_signup_success(client: TestClient):
    # Arrange
    email = "testuser@example.com"
    activity = "Tennis Club"
    path = f"/activities/{quote(activity)}/signup"
    # Act
    resp = client.post(path, params={"email": email})
    # Assert
    assert resp.status_code == 200
    assert email in app_module.activities[activity]["participants"]


def test_signup_nonexistent_activity_returns_404(client: TestClient):
    # Arrange
    email = "a@b.com"
    activity = "NoSuchActivity"
    path = f"/activities/{quote(activity)}/signup"
    # Act
    resp = client.post(path, params={"email": email})
    # Assert
    assert resp.status_code == 404


def test_signup_duplicate_returns_400(client: TestClient):
    # Arrange
    activity = "Tennis Club"
    existing = app_module.activities[activity]["participants"][0]
    path = f"/activities/{quote(activity)}/signup"
    # Act
    resp = client.post(path, params={"email": existing})
    # Assert
    assert resp.status_code == 400


def test_unregister_success(client: TestClient):
    # Arrange
    activity = "Chess Club"
    email = app_module.activities[activity]["participants"][0]
    path = f"/activities/{quote(activity)}/signup"
    # Act
    resp = client.delete(path, params={"email": email})
    # Assert
    assert resp.status_code == 200
    assert email not in app_module.activities[activity]["participants"]


def test_unregister_not_registered_returns_400(client: TestClient):
    # Arrange
    activity = "Chess Club"
    email = "not-registered@example.com"
    path = f"/activities/{quote(activity)}/signup"
    # Act
    resp = client.delete(path, params={"email": email})
    # Assert
    assert resp.status_code == 400
