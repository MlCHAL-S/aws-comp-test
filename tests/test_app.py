"""
Test module for the Flask application.
"""
import pytest
from unittest.mock import patch
from app import app

@pytest.fixture
def client_fixture():
    """
    Fixture for creating a test client for the Flask application.
    """
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch('app.boto3.client')
def test_analyze_text(mock_boto_client, client_fixture):
    """
    Test case for analyzing text with sentiment analysis.
    """
    mock_comprehend = mock_boto_client.return_value
    mock_comprehend.detect_sentiment.return_value = {'Sentiment': 'POSITIVE'}

    response = client_fixture.post('/analyze', json={'text': 'I love Flask.'})
    json_data = response.get_json()

    assert response.status_code == 200
    assert 'sentiment' in json_data

def test_invalid_input(client_fixture):
    """
    Test case for handling invalid input (empty text).
    """
    response = client_fixture.post('/analyze', json={'text': ''})

    assert response.status_code == 400
