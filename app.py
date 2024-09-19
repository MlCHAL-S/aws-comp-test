"""
Module Docstring
"""
from flask import Flask, request, jsonify
import boto3

app = Flask(__name__)
comprehend = boto3.client('comprehend', region_name='eu-central-1')

@app.route('/analyze', methods=['POST'])
def hello_world():  # put application's code here
    """ Function Docstring """
    data = request.json
    text = data.get('text')

    if not text:
        return jsonify({'error': 'Text is required'}), 400

    response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    sentiment = response['Sentiment']

    return jsonify({'sentiment': sentiment})
