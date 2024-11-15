"""
Testing module for client.py
"""
from unittest.mock import patch
import pytest
from src.client.client import app, BACKEND_URL


@pytest.fixture
def client():
    """ Fixture returning testing flask object """
    yield app.test_client()

def test_home(client):
    """ This should test sending get request to the home page """
    response = client.get('/')
    assert response.status_code == 200

@patch('requests.post')
def test_send_valid_message(mock_post, client):
    """ This should test sending a valid message """
    test_message = {'message': 'I love Flask'}
    mock_response = {
        'Sentiment': 'POSITIVE',
        'SentimentScore': {
            'Positive': 0.95,
            'Negative': 0.01,
            'Neutral': 0.02,
            'Mixed': 0.02
        }
    }

    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = mock_response

    response = client.post('/send_message', data=test_message)
    assert response.status_code == 200
    assert b'POSITIVE' in response.data
    mock_post.assert_called_once_with(
        f'{BACKEND_URL}/sentiment_analysis',
        json=test_message,
        timeout=10
    )

@patch('requests.post')
def test_send_empty_message(mock_post, client):
    """ This should test submitting an empty message """
    response = client.post('/send_message', data={'message': ''})
    assert response.status_code == 200
    assert b'Please enter a message' in response.data
