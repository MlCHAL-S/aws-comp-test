"""
Test docstring
"""
import boto3
from moto import mock_aws
import pytest
from app import app

@pytest.fixture
def client_fixture():
    """
    Fixture for creating a test client for the Flask application.
    """
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_aws_setup():
    """
    Mock AWS setup for testing.
    """
    with mock_aws():
        yield boto3.client('comprehend', region_name='eu-central-1')

def test_analyze_text(client_fixture, mock_aws_setup):
    """
    Test case for analyzing text with sentiment analysis.
    """
    comprehend = mock_aws_setup
    comprehend.detect_sentiment = lambda Text, LanguageCode: {'Sentiment': 'POSITIVE'}

    response = client_fixture.post('/analyze', json={'text': 'I love Flask.'})
    json_data = response.get_json()

    assert response.status_code == 200
    assert 'sentiment' in json_data
    assert json_data['sentiment'] == 'NEUTRAL'

def test_invalid_input(client_fixture, mock_aws_setup):
    """
    Test case for handling invalid input (empty text).
    """
    response = client_fixture.post('/analyze', json={'text': ''})

    assert response.status_code == 400
