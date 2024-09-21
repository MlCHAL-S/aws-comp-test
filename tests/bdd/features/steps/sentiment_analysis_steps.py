"""
Blah blah
"""
from behave import given, when, then
from app import app  # Import your Flask app
from bs4 import BeautifulSoup

# This fixture sets up a test client to simulate requests to your Flask app.
@given('the application is running')
def step_impl(context):
    """Start the Flask app for testing."""
    context.client = app.test_client()  # Use Flask's test client to simulate the app

# Visit the homepage of the application
@when('I visit the "Home Page"')
def step_impl(context):
    """Simulate visiting the home page."""
    context.response = context.client.get('/')  # Send GET request to home page

# Enter text in the input field
@when('I enter "{text}" in the input field')
def step_impl(context, text):
    """Simulate entering text in the input field."""
    context.entered_text = text  # Store the entered text in context for later
    # print(context.text)

# Press the "Analyze" button (submit the form)
@when('I press the "Analyze" button')
def step_impl(context):
    """Simulate pressing the analyze button."""
    # Check if context.entered_text exists, otherwise send an empty form.
    if hasattr(context, 'entered_text'):
        context.response = context.client.post(
            '/',
            data={'text': context.entered_text},
            content_type='application/x-www-form-urlencoded'
        )
    else:
        context.response = context.client.post(
            '/',
            data={'text': ''},  # Simulate an empty input
            content_type='application/x-www-form-urlencoded'
        )

@then('I should see "{expected_sentiment}" as the sentiment result')
def step_impl(context, expected_sentiment):
    """Check if the correct sentiment is displayed in the HTML response."""
    soup = BeautifulSoup(context.response.data, 'html.parser')
    result_element = soup.find(id="sentiment-result")
    assert result_element is not None, "Sentiment result element not found in the page."
    result = result_element.get_text().strip().split(": ")[1]  # Extract sentiment after "Sentiment: "
    assert result == expected_sentiment, f"Expected {expected_sentiment}, but got {result}"

# Handle empty input error
@then('I should see an error message "{expected_error}"')
def step_impl(context, expected_error):
    """Check if the correct error message is displayed in the HTML response."""
    soup = BeautifulSoup(context.response.data, 'html.parser')
    error_message = soup.find(id="error-message").get_text().strip()
    assert error_message == expected_error, f"Expected error message '{expected_error}', but got '{error_message}'"
