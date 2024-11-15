"""
Module for client.py
"""
from flask import Flask, render_template, request
import requests

app = Flask(__name__)
BACKEND_URL = 'http://backend-server:5000'

@app.route('/')
def home():
    """
    Renders the home page with a form
    for sending messages and displaying the sentiment analysis result1s.
    """
    return render_template('index.html')

@app.route('/send_message', methods=('POST',))
def send_message():
    """
    Handles form submission, extracts message from form data,
    and sends it as JSON to the backend for sentiment analysis.
    """
    message = request.form.get('message')

    if not message:
        return render_template('index.html', result={'error': 'Please enter a message'})

    response = requests.post(
        f'{BACKEND_URL}/sentiment_analysis',
        json={'message': message},
        timeout=10
    )
    sentiment_data = response.json()
    result = {
        'index': sentiment_data.get('Index'),
        'sentiment': sentiment_data.get('Sentiment'),
        'sentiment_score': sentiment_data.get('SentimentScore'),
    }
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
