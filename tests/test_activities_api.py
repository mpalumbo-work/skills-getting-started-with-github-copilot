def test_root_redirects_to_static_application(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_activity_details(client):
    response = client.get("/activities")

    assert response.status_code == 200
    activities = response.json()
    assert "Chess Club" in activities
    assert activities["Chess Club"] == {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": [
            "michael@mergington.edu",
            "daniel@mergington.edu",
        ],
    }


def test_signup_adds_new_participant(client):
    response = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": "alex@mergington.edu"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Signed up alex@mergington.edu for Chess Club"
    }

    activities_response = client.get("/activities")
    assert "alex@mergington.edu" in activities_response.json()["Chess Club"]["participants"]


def test_signup_rejects_existing_participant(client):
    response = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": "michael@mergington.edu"},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up"}


def test_signup_rejects_unknown_activity(client):
    response = client.post(
        "/activities/Unknown%20Club/signup",
        params={"email": "alex@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_removes_existing_participant(client):
    response = client.delete(
        "/activities/Chess%20Club/participants/michael%40mergington.edu"
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Unregistered michael@mergington.edu from Chess Club"
    }

    activities_response = client.get("/activities")
    assert (
        "michael@mergington.edu"
        not in activities_response.json()["Chess Club"]["participants"]
    )


def test_unregister_rejects_participant_not_signed_up(client):
    response = client.delete(
        "/activities/Chess%20Club/participants/alex%40mergington.edu"
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Student is not signed up"}


def test_unregister_rejects_unknown_activity(client):
    response = client.delete(
        "/activities/Unknown%20Club/participants/alex%40mergington.edu"
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}