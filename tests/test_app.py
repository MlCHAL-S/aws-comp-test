import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_analyze_text(client):
    response = client.post('/analyze', json={'text': 'I love Flask.'})
    json_data = response.get_json()

    assert response.status_code == 200
    assert 'sentiment' in json_data
    assert json_data['sentiment'] == 'POSITIVE'

def test_invalid_input(client):
    response = client.post('/analyze', json={'text': ''})

    assert response.status_code == 400
