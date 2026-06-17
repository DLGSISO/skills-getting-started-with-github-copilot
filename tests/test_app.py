"""
Test suite for the Mergington High School API

Tests the FastAPI application endpoints with proper state management
between test cases.
"""

from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    original_activities = deepcopy({
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"],
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"],
        },
        "Basketball Team": {
            "description": "Learn teamwork and compete against other schools in basketball",
            "schedule": "Mondays, Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 18,
            "participants": ["liam@mergington.edu", "ava@mergington.edu"],
        },
        "Swim Club": {
            "description": "Practice swimming techniques and prepare for swim meets",
            "schedule": "Tuesdays and Thursdays, 5:00 PM - 6:30 PM",
            "max_participants": 20,
            "participants": ["noah@mergington.edu", "mia@mergington.edu"],
        },
        "Drama Club": {
            "description": "Develop acting and production skills for school performances",
            "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
            "max_participants": 25,
            "participants": ["isabella@mergington.edu", "lucas@mergington.edu"],
        },
        "Art Workshop": {
            "description": "Explore drawing, painting, and creative design techniques",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 15,
            "participants": ["harper@mergington.edu", "elijah@mergington.edu"],
        },
        "Science Olympiad": {
            "description": "Prepare for science competitions with experiments and problem solving",
            "schedule": "Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 16,
            "participants": ["amelia@mergington.edu", "jack@mergington.edu"],
        },
        "Debate Team": {
            "description": "Build public speaking and critical thinking skills through debate",
            "schedule": "Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 20,
            "participants": ["sophia@mergington.edu", "benjamin@mergington.edu"],
        },
    })

    original_copy = deepcopy(original_activities)
    activities.clear()
    activities.update(original_copy)

    yield

    activities.clear()
    activities.update(deepcopy(original_activities))


def test_get_activities(client):
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert len(data) == 9


def test_signup_for_activity(client):
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "newstudent@mergington.edu"},
    )
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]

    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    assert "newstudent@mergington.edu" in activities_data["Chess Club"]["participants"]


def test_signup_duplicate_email(client):
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "michael@mergington.edu"},
    )
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_nonexistent_activity(client):
    response = client.post(
        "/activities/Fake Activity/signup",
        params={"email": "student@mergington.edu"},
    )
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_remove_participant(client):
    response = client.delete(
        "/activities/Chess Club/participants",
        params={"email": "michael@mergington.edu"},
    )
    assert response.status_code == 200
    assert "Removed" in response.json()["message"]

    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    assert "michael@mergington.edu" not in activities_data["Chess Club"]["participants"]


def test_remove_nonexistent_participant(client):
    response = client.delete(
        "/activities/Chess Club/participants",
        params={"email": "notarealstudent@mergington.edu"},
    )
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]
