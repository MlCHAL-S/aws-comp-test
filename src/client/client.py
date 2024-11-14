"""
Module for client.py
"""
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

BACKEND_URL = 'http://backend-server:5000'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/send_message', methods=('POST',))
def send_message():
    data = request.get_json()
    message = data.get('message') if data else None

    if message:
        response = requests.post(f'{BACKEND_URL}/sentiment_analysis', json={'message': message})

        # Get the sentiment from the server's JSON response
        sentiment = response.json().get('sentiment', 'Error in sentiment analysis')

        # Display sentiment in the HTML template
        return render_template('index.html', sentiment=sentiment)

    return render_template('index.html', sentiment='Please enter a message')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)  # Expose the app on port 5001
