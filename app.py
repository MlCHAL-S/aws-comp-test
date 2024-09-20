"""
Module Docstring
"""
from flask import Flask, request, render_template
import boto3

app = Flask(__name__)
comprehend = boto3.client('comprehend', region_name='eu-central-1')


@app.route('/', methods=('GET', 'POST'))
def index():
    """Handle GET and POST requests for the homepage."""
    if request.method == 'POST':
        text = request.form.get('text')

        if not text:
            error = 'Text is required'
            return render_template('index.html', error=error)

        # Call AWS Comprehend to analyze sentiment
        response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
        sentiment = response['Sentiment']

        return render_template('index.html', sentiment=sentiment, text=text)

    return render_template('index.html')
