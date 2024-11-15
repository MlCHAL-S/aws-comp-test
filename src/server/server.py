"""
This the server.py module
"""
from flask import Flask, jsonify, request, Response
from boto3 import client

app = Flask(__name__)
client = client('comprehend', region_name='eu-central-1')


@app.route('/sentiment_analysis', methods=('POST',))
def sentiment_analysis() -> (Response, int):
    """
    Makes a call to boto3 client for a sentiment analysis of a text.
    """
    message = request.get_json().get('message')
    if not message:
        return jsonify({'error': 'No message provided'}), 400

    response = client.batch_detect_sentiment(
        TextList=[message],
        LanguageCode='en'
    )
    sentiment_result = response['ResultList'][0]
    return jsonify(sentiment_result), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
