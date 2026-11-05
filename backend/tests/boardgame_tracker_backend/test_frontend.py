from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from boardgame_tracker_backend.frontend import mount_frontend


@pytest.fixture
def frontend_client(tmp_path: Path) -> TestClient:
    static_dir = tmp_path / "static"
    (static_dir / "assets").mkdir(parents=True)
    (static_dir / "index.html").write_text("<html>spa</html>")
    (static_dir / "assets" / "app.js").write_text("console.log('app')")
    (static_dir / "favicon.svg").write_text("<svg/>")
    (tmp_path / "secret.txt").write_text("secret")

    app = FastAPI()

    @app.get("/api/v1/ping")
    def ping() -> dict[str, str]:
        return {"ping": "pong"}

    mount_frontend(app, static_dir, "/api/v1")
    return TestClient(app)


def test_root_serves_index(frontend_client: TestClient) -> None:
    response = frontend_client.get("/")
    assert response.status_code == 200
    assert response.text == "<html>spa</html>"


def test_unknown_route_falls_back_to_index(frontend_client: TestClient) -> None:
    response = frontend_client.get("/games/42")
    assert response.status_code == 200
    assert response.text == "<html>spa</html>"


def test_assets_are_served(frontend_client: TestClient) -> None:
    response = frontend_client.get("/assets/app.js")
    assert response.status_code == 200
    assert response.text == "console.log('app')"


def test_root_level_file_is_served(frontend_client: TestClient) -> None:
    assert frontend_client.get("/favicon.svg").text == "<svg/>"


def test_api_routes_still_work(frontend_client: TestClient) -> None:
    assert frontend_client.get("/api/v1/ping").json() == {"ping": "pong"}


@pytest.mark.parametrize(
    "path", ["/api", "/api/v1/unknown", "/api/unknown", "/api/v2/games"]
)
def test_unknown_api_route_is_404_not_index(
    frontend_client: TestClient, path: str
) -> None:
    assert frontend_client.get(path).status_code == 404


def test_unknown_api_route_is_404_for_any_method(frontend_client: TestClient) -> None:
    assert frontend_client.post("/api/v1/unknown").status_code == 404
    assert frontend_client.delete("/api/v2/games").status_code == 404


def test_path_traversal_does_not_leak_files(frontend_client: TestClient) -> None:
    response = frontend_client.get("/%2e%2e/secret.txt")
    assert response.text == "<html>spa</html>"


def test_nul_byte_in_path_falls_back_to_index(frontend_client: TestClient) -> None:
    response = frontend_client.get("/%00")
    assert response.status_code == 200
    assert response.text == "<html>spa</html>"
