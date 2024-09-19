"""
sdfkjsdojkf
"""
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

def test_analyze_text(client_fixture):
    """
    Test case for analyzing text with sentiment analysis.
    """
    # Perform the test
    response = client_fixture.post('/analyze', json={'text': 'I love Flask.'})

    # Check the response
    assert response.status_code == 200
    assert response.json['sentiment'] == 'POSITIVE'

def test_invalid_input(client_fixture):
    """
    Test case for handling invalid input (empty text).
    """
    response = client_fixture.post('/analyze', json={'text': ''})

    assert response.status_code == 400
