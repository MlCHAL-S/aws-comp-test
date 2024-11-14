"""
This the server.py module
"""
from flask import Flask, json, request, Response
from boto3 import client

app = Flask(__name__)
client = client('comprehend', region_name='eu-central-1')

@app.route('/sentiment_analysis', methods=('POST',))
def sentiment_analysis():
    message = request.get_json().get('message')

    if message:
        response = client.batch_detect_sentiment(
            TextList=[message],
            LanguageCode='en'
        )
        sentiment = response['ResultList'][0]['Sentiment']

        return Response(json.dumps({'sentiment': sentiment}), status=200, content_type='application/json')

    return Response(json.dumps({'error': 'No message provided'}), status=400, content_type='application/json')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
