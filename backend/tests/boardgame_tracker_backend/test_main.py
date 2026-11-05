from fastapi.testclient import TestClient

from boardgame_tracker_backend.main import square


def test_square():
    assert square(3) == 9
    assert square(-4) == 16
    assert square(0) == 0


def test_home_answers_when_no_frontend_is_served(client: TestClient) -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Boardgame Tracker API!"}
