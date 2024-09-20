"""
sdfkjsdojkf
"""
from unittest import mock
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


def test_get_homepage(client_fixture):
    """
    Test case for the GET request on the homepage.
    This will test the last return statement that renders index.html.
    """
    # Perform a GET request to the root route
    response = client_fixture.get('/')

    # Check if the response status is 200 (OK)
    assert response.status_code == 200

    # Check if the rendered template contains the expected content (index.html)
    assert b"Sentiment Analyzer" in response.data  # Assuming this string is in your HTML


def test_analyze_text(client_fixture):
    """
    Test case for analyzing text with sentiment analysis.
    """
    # Mock the AWS Comprehend response
    with mock.patch('boto3.client') as mock_comprehend:
        mock_comprehend.return_value.detect_sentiment.return_value = {
            'Sentiment': 'POSITIVE'
        }

        # Perform a POST request with text data
        response = client_fixture.post('/', data={'text': 'I love Flask.'})

        # Check the response status and sentiment in rendered template
        assert response.status_code == 200
        assert b'POSITIVE' in response.data


def test_invalid_input(client_fixture):
    """
    Test case for handling invalid input (empty text).
    """
    # Perform a POST request with empty text
    response = client_fixture.post('/', data={'text': ''})

    # Check if the response contains an error message
    assert response.status_code == 200
    assert b'Text is required' in response.data
