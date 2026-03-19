"""Tests for the High School Management System API"""

from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_root_redirects_to_static():
    # Arrange
    expected_location = "/static/index.html"

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == expected_location


def test_get_activities():
    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_new_student():
    # Arrange
    activity = "Chess Club"
    new_email = "newemail@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": new_email}
    )

    # Assert
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]
    assert new_email in response.json()["message"]


def test_signup_duplicate_student():
    # Arrange
    activity = "Chess Club"
    existing_email = "michael@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": existing_email}
    )

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_unregister_existing_participant():
    # Arrange
    activity = "Chess Club"
    existing_email = "michael@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity}/participants",
        params={"email": existing_email}
    )

    # Assert
    assert response.status_code == 200
    assert "Unregistered" in response.json()["message"]
    assert existing_email in response.json()["message"]


def test_unregister_nonexistent_participant():
    # Arrange
    activity = "Chess Club"
    missing_email = "noone@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity}/participants",
        params={"email": missing_email}
    )

    # Assert
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]

