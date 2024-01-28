"""This is the main file that runs the Flask app.
It contains the routes and the logic for the sentiment analysis."""

# Importing the libraries
from flask import Flask, render_template, request
from googletrans import Translator
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Initializing the Flask app
app = Flask(__name__)

# Initializing the Google Translator and the NLTK Sentiment Intensity Analyzer
translator = Translator()
nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

# Defining the routes
@app.route('/')
def index():
    return render_template('index.html')

# Analyze route
@app.route('/analyze', methods=['POST'])
def analyze():
    if request.method == 'POST':
        review = request.form['review']
        new_review = review 

        # Detecting the language of the input text
        detected_language = translator.detect(review).lang

        # Translating the input text to English if it's not already in English
        if detected_language != 'en':
            translation = translator.translate(review, dest='en')
            new_review = translation.text

        # Performing sentiment analysis
        sentiment_score = sia.polarity_scores(new_review)['compound']

        if sentiment_score > 0.05:
            sentiment = "Positive 😀"
        elif sentiment_score < -0.05:
            sentiment = "Negative 😞"
        else:
            sentiment = "Neutral 😐"

        print(f"Review: {review}")
        print(f"Detected Language: {detected_language}")
        print(f"Sentiment: {sentiment}")

        return render_template('result.html', review=review, sentiment=sentiment, detected_language=detected_language)

# Running the app
if __name__ == '__main__':
    app.run(debug=True)
