from collections.abc import Iterator

import app_main
import pytest
from app_database import get_session
from fastapi.testclient import TestClient


@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    monkeypatch.setattr(app_main, "init_db", lambda: None)
    app_main.app.dependency_overrides[get_session] = lambda: object()
    with TestClient(app_main.app) as test_client:
        yield test_client
    app_main.app.dependency_overrides.clear()


def test_root_identifies_albumbot(client: TestClient) -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the AlbumBot API"}


def test_search_returns_album_placeholders(client: TestClient) -> None:
    response = client.post("/search", params={"query": "ambient music"})

    assert response.status_code == 200
    assert response.json() == {
        "query": "ambient music",
        "matches": ["Album A", "Album B", "Album C"],
    }


def test_chat_returns_listening_recommendation(client: TestClient) -> None:
    response = client.post("/chat", params={"query": "dance music"})

    assert response.status_code == 200
    assert response.json() == {
        "query": "dance music",
        "recommendation": (
            "Based on your search, you should listen to Album A because..."
        ),
    }
