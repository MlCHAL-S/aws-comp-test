"""
Testing module for client.py
"""

import pytest
from unittest.mock import patch

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
def test_send_message(mock_post, client):
    """ This should send a post request to the sentiment analysis endpoint """
    test_message = {'message': 'I love Flask'}
    mock_response = {'sentiment': 'POSITIVE'}

    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = mock_response

    response = client.post('/send_message', json=test_message)

    assert response.status_code == 200
    # Check that 'POSITIVE' sentiment appears in the rendered HTML
    assert b'POSITIVE' in response.data
    mock_post.assert_called_once_with(f'{BACKEND_URL}/sentiment_analysis', json=test_message)

