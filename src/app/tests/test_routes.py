import json

from ..api import db_operations
from ..api.models import MindMapEntry, MindMap


def test_create_map(test_client, monkeypatch):
    request_body = {"id": "MY AMAZING MAP WOW"}
    expected_response_object = {"map_id": "MY AMAZING MAP WOW"}

    async def mock_post_map(body):
        return 1

    monkeypatch.setattr(db_operations, "post_map", mock_post_map)

    response = test_client.post("/api/v1/map", data=json.dumps(request_body))

    assert response.status_code == 201
    assert response.json() == expected_response_object


def test_create_map_bad_json(test_client):
    response = test_client.post("/api/v1/map", data=json.dumps({"bad": "nonono"}))
    assert response.status_code == 422


def test_create_leaf(test_client, monkeypatch):
    request_map_id = "MY-MAP"
    request_body = {"path": "BIG/PATH/WOWOWOWOW", "text": "amazing text too"}
    expected_response_object = {
        "map_id": "MY-MAP",
        "leaf": "BIG/PATH/WOWOWOWOW",
        "leaf_message": "amazing text too",
    }

    async def mock_post_leaf(map_id, body):
        return 1

    monkeypatch.setattr(db_operations, "post_leaf", mock_post_leaf)

    response = test_client.post(f"/api/v1/map/{request_map_id}", data=json.dumps(request_body))

    assert response.status_code == 201
    assert response.json() == expected_response_object


def test_create_leaf_bad_json(test_client):
    response = test_client.post("/api/v1/map/MY-MAP", data=json.dumps({"bad": "nonono"}))
    assert response.status_code == 422


def test_update_leaf(test_client, monkeypatch):
    request_map_id = "MY-MAP"
    request_body = {"path": "BIG/PATH/WOWOWOWOW", "text": "amazing text too"}
    expected_response_object = {
        "map_id": "MY-MAP",
        "leaf": "BIG/PATH/WOWOWOWOW",
        "leaf_message": "amazing text too",
    }

    async def mock_get_leaf(map_id, leaf_path):
        return 1

    async def mock_put_leaf(map_id, body):
        return 1

    monkeypatch.setattr(db_operations, "get_leaf", mock_get_leaf)
    monkeypatch.setattr(db_operations, "put_leaf", mock_put_leaf)

    response = test_client.put(f"/api/v1/map/{request_map_id}", data=json.dumps(request_body))

    assert response.status_code == 200
    assert response.json() == expected_response_object


def test_update_leaf_bad_json(test_client):
    response = test_client.put("/api/v1/map/MY-MAP", data=json.dumps({"bad": "nonono"}))
    assert response.status_code == 422


def test_get_map(test_client, monkeypatch):
    expected_pretty_output = ("root/\n\ti/\n\t\tlike/\n\t\t\tpotatoes\n\t\t\tyou\n\t\t\thehehe\n"
                              "\t\teat/\n\t\t\ttomatoes")
    test_data = [
        {"uuid": "1", "id": "my-map", "leaf": "i/like/potatoes", "leaf_message": "big message"},
        {"uuid": "2", "id": "my-map", "leaf": "i/eat/tomatoes", "leaf_message": "big message"},
        {"uuid": "3", "id": "my-map", "leaf": "i/like/you", "leaf_message": "big message"},
        {"uuid": "4", "id": "my-map", "leaf": "i/like/hehehe", "leaf_message": "big message"}, ]

    async def mock_get_map(map_id):
        return MindMap(map_id=map_id, leafs=[MindMapEntry(**row) for row in test_data])

    monkeypatch.setattr(db_operations, "get_map", mock_get_map)

    response = test_client.get("/api/v1/map/my-map")
    assert response.status_code == 200
    assert response.text == expected_pretty_output

    response = test_client.get("/api/v1/map/my-map?pretty=false")
    assert response.status_code == 200


def test_get_leaf(test_client, monkeypatch):
    test_data = {"leaf_message": "big text message"}
    expected_response_object = {
        "map_id": "my-map",
        "path": "i/like/you",
        "text": "big text message"
    }

    async def mock_get_leaf(map_id, leaf_path):
        return test_data
    monkeypatch.setattr(db_operations, "get_leaf", mock_get_leaf)

    response = test_client.get("/api/v1/map/my-map?path=i/like/you")
    assert response.status_code == 200
    assert response.json() == expected_response_object


def test_get_leaf_bad_path(test_client, monkeypatch):
    async def mock_get_leaf(map_id, leaf_path):
        return None
    monkeypatch.setattr(db_operations, "get_leaf", mock_get_leaf)

    response = test_client.get("/api/v1/map/my-map?path=i/dont/exist")
    assert response.status_code == 404
