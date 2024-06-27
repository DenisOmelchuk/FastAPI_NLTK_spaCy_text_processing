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


# Test cases for /pos_tag endpoint
@pytest.mark.parametrize("text, expected_tokens", [
    ("Hello world!", [{"token": "Hello", "tag": "NNP"}, {"token": "world", "tag": "NN"}, {"token": "!", "tag": "."}]),
    ("This is a test message.", [{"token": "This", "tag": "DT"}, {"token": "is", "tag": "VBZ"}, {"token": "a", "tag": "DT"},
                                 {"token": "test", "tag": "NN"}, {"token": "message", "tag": "NN"}, {"token": ".", "tag": "."}]),
    ("Gyros is the best street food!", [{"token": "Gyros", "tag": "NNP"}, {"token": "is", "tag": "VBZ"}, {"token": "the", "tag": "DT"},
                                        {"token": "best", "tag": "JJS"}, {"token": "street", "tag": "NN"}, {"token": "food", "tag": "NN"}, {"token": "!", "tag": "."}]),
])
def test_pos_tag_text_valid_input(text, expected_tokens):
    response = client.post("/pos_tag", json={"text": text})
    assert response.status_code == 200
    assert response.json() == expected_tokens


@pytest.mark.parametrize("invalid_input, expected_status_code, expected_type, expected_msg", [
    (123, 422, "string_type", "Input should be a valid string"),                     # Integer input
    (["This", "is", "an", "array"], 422, "string_type", "Input should be a valid string"),  # Array of strings
])
def test_pos_tag_text_invalid_input(invalid_input, expected_status_code, expected_type, expected_msg):
    response = client.post("/pos_tag", json={"text": invalid_input})
    assert response.status_code == expected_status_code
    assert response.json()["detail"][0]["type"] == expected_type
    assert response.json()["detail"][0]["msg"] == expected_msg


def test_pos_tag_text_invalid_format():
    response = client.post("/pos_tag", data={"text": "This is a test."})
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "model_attributes_type"
    assert response.json()["detail"][0]["msg"] == "Input should be a valid dictionary or object to extract fields from"
    assert "text" in response.json()["detail"][0]["input"]


"""
Test cases for /ner endpoint
"""
@pytest.mark.parametrize("text, expected_entities", [
    (
        "Barack Obama and Denis are my new best friends. We met in the London city",
        [["Barack Obama", "PERSON"], ["Denis", "PERSON"], ["London", "GPE"]]
    ),
    (
        "Apple is located in California. Tim Cook is the CEO.",
        [["Apple", "ORG"], ["California", "GPE"], ["Tim Cook", "PERSON"]]
    ),
])
def test_ner_text_valid_input(text, expected_entities):
    response = client.post("/ner", json={"text": text})
    assert response.status_code == 200
    assert response.json() == expected_entities


@pytest.mark.parametrize("invalid_input, expected_status_code, expected_type, expected_msg", [
    (123, 422, "string_type", "Input should be a valid string"),                     # Integer input
    (["This", "is", "an", "array"], 422, "string_type", "Input should be a valid string"),  # Array of strings
])
def test_ner_text_invalid_input(invalid_input, expected_status_code, expected_type, expected_msg):
    response = client.post("/ner/", json={"text": invalid_input})
    assert response.status_code == expected_status_code
    assert response.json()["detail"][0]["type"] == expected_type
    assert response.json()["detail"][0]["msg"] == expected_msg


def test_ner_text_invalid_format():
    response = client.post("/ner", data={"text": "This is a test."})
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "model_attributes_type"
    assert response.json()["detail"][0]["msg"] == "Input should be a valid dictionary or object to extract fields from"
    assert "text" in response.json()["detail"][0]["input"]
