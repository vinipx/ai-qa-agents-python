import pytest
from fastapi.testclient import TestClient
from server import app

client = TestClient(app)

def test_execute_endpoint_removed():
    """
    Ensure the old /execute endpoint returns 404 (removed in favor of WebSockets).
    """
    response = client.post("/execute", json={"requirement": "Test my login API"})
    assert response.status_code == 404

def test_websocket_rejects_non_ws_connections():
    """
    Standard HTTP GET to a WS endpoint should return a 403 or 404.
    """
    response = client.get("/ws/1234")
    assert response.status_code in [403, 404]

def test_cors_enabled():
    """
    Test that CORS middleware is applied.
    """
    response = client.options(
        "/ws/1234", 
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET"
        }
    )
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers

@pytest.mark.asyncio
async def test_websocket_route_exists():
    """
    Test that the websocket endpoint exists in the application routes.
    """
    routes = [route.path for route in app.routes if hasattr(route, "path")]
    assert "/ws/{thread_id}" in routes
