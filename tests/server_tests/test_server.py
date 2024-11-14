"""
Testing module for server.py
"""
import pytest
from unittest.mock import patch
from src.server.server import app


@pytest.fixture
def server():
    """ Fixture returning testing flask object """
    yield app.test_client()

@patch('src.server.server.client')
def test_sentiment_analysis_with_message(mock_client, server):
    """ This should test sentiment analysis function with a positive statement """
    test_message: dict = {
        'message': 'I love Python'
    }

    mock_response: dict = {
        'ResultList': [
            {
                'Sentiment': 'POSITIVE'
            }
        ]
    }
    mock_client.batch_detect_sentiment.return_value = mock_response

    response = server.post('/sentiment_analysis', json=test_message)

    assert response.status_code == 200
    assert response.json == {
        'sentiment': 'POSITIVE'
    }

@patch('src.server.server.client')
def test_sentiment_analysis_with_no_message(mock_client, server):
    """ This should test sentiment analysis function with no message """
    response = server.post('/sentiment_analysis', json={})

    assert response.status_code == 400
    assert response.json == {'error': 'No message provided'}
