import pytest
from unittest.mock import patch, MagicMock
from duohub import Duohub
from duohub.exceptions import AuthenticationError, APIError
import httpx

@pytest.fixture
def mock_env():
    with patch('duohub.environment.os.getenv', return_value='test_api_key'):
        yield

@pytest.fixture
def client(mock_env):
    return Duohub()

def test_client_initialization(mock_env):
    client = Duohub()
    assert client.environment.api_key == 'test_api_key'
    assert client.environment.base_url == 'https://api.duohub.ai'

def test_client_initialization_with_custom_api_key():
    client = Duohub(api_key='custom_api_key')
    assert client.environment.api_key == 'custom_api_key'

def test_client_initialization_no_api_key():
    with patch('duohub.environment.os.getenv', return_value=None):
        with pytest.raises(AuthenticationError):
            Duohub()

@patch('httpx.Client.get')
def test_query_success(mock_get, client):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": "test result"}
    mock_get.return_value = mock_response

    result = client.query(query="test query", memoryID="test_memory_id")
    assert result == {"result": "test result"}

    mock_get.assert_called_once_with(
        'https://api.duohub.ai/memory/',
        params={'memoryID': 'test_memory_id', 'query': 'test query', 'assisted': 'false'}
    )

@patch('httpx.Client.get')
def test_query_with_assisted_true(mock_get, client):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": "test result"}
    mock_get.return_value = mock_response

    result = client.query(query="test query", memoryID="test_memory_id", assisted=True)
    assert result == {"result": "test result"}

    mock_get.assert_called_once_with(
        'https://api.duohub.ai/memory/',
        params={'memoryID': 'test_memory_id', 'query': 'test query', 'assisted': 'true'}
    )

@patch('httpx.Client.get')
def test_query_api_error(mock_get, client):
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"
    mock_get.return_value = mock_response
    mock_get.side_effect = httpx.HTTPStatusError("500 Internal Server Error", request=MagicMock(), response=mock_response)

    with pytest.raises(APIError, match="API request failed with status code 500: Internal Server Error"):
        client.query(query="test query", memoryID="test_memory_id")

@pytest.fixture(autouse=True)
def no_http_requests(monkeypatch):
    """Prevent any real HTTP requests during tests."""
    monkeypatch.delattr("httpx.Client.send")

if __name__ == '__main__':
    pytest.main()