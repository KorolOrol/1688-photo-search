import pytest
import requests
from ..image_recognition import send_image_recognition_request

class DummyResponse:
    def __init__(self, data):
        self._data = data
        self.status_code = 200

    def json(self):
        return self._data

def dummy_post_success(url, headers, json):
    # Validate headers are set correctly.
    assert headers == {"Content-Type": "application/json"}
    # Check expected values in the payload.
    assert json.get("model") == "gemma-3-4b-it"
    messages = json.get("messages")
    assert isinstance(messages, list) and len(messages) == 1
    content = messages[0].get("content")
    # The content should contain two items, text and image_url.
    assert isinstance(content, list) and len(content) == 2
    # Return dummy response simulating a successful API call.
    return DummyResponse({'choices': [{'message': {'content': 'extracted_keywords'}}]})

def dummy_post_invalid(url, headers, json):
    # Return a response with missing 'choices' key to simulate an invalid response.
    return DummyResponse({})

def test_send_image_recognition_success(monkeypatch):
    monkeypatch.setattr(requests, 'post', dummy_post_success)
    # Теперь вместо URL используется строка с данными в формате base64.
    image_base64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA"
    service_url = "http://dummy-api-url"
    result = send_image_recognition_request(image_base64, service_url)
    assert result == 'extracted_keywords'

def test_send_image_recognition_invalid_response(monkeypatch):
    monkeypatch.setattr(requests, 'post', dummy_post_invalid)
    with pytest.raises(KeyError):
        send_image_recognition_request("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA", "http://dummy-api-url")