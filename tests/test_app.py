"""
Test docstring
"""
from unittest.mock import patch
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


@patch('boto3.client')
def test_analyze_text(mock_boto_client, client_fixture):
    """
    Test case for analyzing text with sentiment analysis.
    """
    # Set up the mock
    mock_comprehend = mock_boto_client.return_value
    mock_comprehend.detect_sentiment.return_value = {'Sentiment': 'POSITIVE'}

    # Perform the test
    response = client_fixture.post('/analyze', json={'text': 'I love Flask.'})

    # Check the response
    assert response.status_code == 200
    assert response.json['sentiment'] == 'POSITIVE'


def test_invalid_input(client_fixture, mock_aws_setup):
    """
    Test case for handling invalid input (empty text).
    """
    response = client_fixture.post('/analyze', json={'text': ''})

    assert response.status_code == 400
