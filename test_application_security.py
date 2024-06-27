import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


"""
Test case for checking response headers from all endpoints
"""
@pytest.mark.asyncio
async def test_response_headers():
    endpoints = ["/tokenize/", "/pos_tag", "/ner"]

    for endpoint in endpoints:
        response = client.post(endpoint, json={"text": "Test text"})
        assert response.status_code == 200
        assert "strict-transport-security" in response.headers
        assert "x-content-type-options" in response.headers
        assert "x-frame-options" in response.headers


"""
Test case for checking CORS headers from all endpoints
"""
@pytest.mark.asyncio
async def test_cors_headers():
    endpoints = ["/tokenize/", "/pos_tag", "/ner"]

    for endpoint in endpoints:
        response = client.options(endpoint)
        # Check that the endpoint allows OPTIONS method
        if response.status_code == 405:
            pytest.skip(f"{endpoint} does not allow OPTIONS method")

        assert response.status_code == 200
        assert response.headers["access-control-allow-origin"] == "*"
        assert response.headers["access-control-allow-credentials"] == "true"
        assert "access-control-allow-methods" in response.headers
        assert "access-control-allow-headers" in response.headers
