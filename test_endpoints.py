import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# tokenize endpoint tests
@pytest.mark.parametrize("text, expected_tokens", [
    ("Hello world!", ["Hello", "world", "!"]),
    ("This is a test message.", ["This", "is", "a", "test", "message", "."]),
    ("Gyros is the best street food!", ["Gyros", "is", "the", "best", "street", "food", "!"]),

])
def test_tokenize_text(text, expected_tokens):
    response = client.post("/tokenize/", json={"text": text})
    assert response.status_code == 200
    assert response.json() == expected_tokens


@pytest.mark.parametrize("invalid_input, expected_status_code, expected_type, expected_msg", [
    (123, 422, "string_type", "Input should be a valid string"),                     # Integer input
    (["This", "is", "an", "array"], 422, "string_type", "Input should be a valid string"),  # Array of strings
])
def test_tokenize_text_invalid_input(invalid_input, expected_status_code, expected_type, expected_msg):
    response = client.post("/tokenize/", json={"text": invalid_input})
    assert response.status_code == expected_status_code
    assert response.json()["detail"][0]["type"] == expected_type
    assert response.json()["detail"][0]["msg"] == expected_msg


def test_tokenize_text_invalid_format():
    response = client.post("/tokenize/", data={"text": "This is a test."})
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "model_attributes_type"
    assert response.json()["detail"][0]["msg"] == "Input should be a valid dictionary or object to extract fields from"
    assert "text" in response.json()["detail"][0]["input"]

