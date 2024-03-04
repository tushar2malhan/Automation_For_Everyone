import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import numpy as np

def train_ethnicity_():
    data = [
        'White / Caucasian',
        'Hispanic, Latino, or Spanish origin',
        'Black or African American',
        'Asian',
        'Indian',
        'American'
        'Native Hawaiian or other Pacific Islander',
        'Indigenous Peoples, First Nations, Native American, or Alaska Native',
        'Middle Eastern or North African',
        'Some other race, ethnicity, or origin'
    ]

    # Creating labels for the data
    labels = [f'ethnicity_{i}' for i in range(len(data))]

    # Creating a list of tuples where each tuple is (text, label)
    training_data = [(item, label) for item, label in zip(data, labels)]

    # Creating a bag-of-words model
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform([item[0] for item in training_data])
    y = np.array([item[1] for item in training_data])

    # Training a Naive Bayes classifier
    classifier = MultinomialNB()
    classifier.fit(X, y)

    # Save the model and vectorizer
    joblib.dump(vectorizer, 'job_portal_automation/training_data/vectorizer_ethnicity.joblib')
    joblib.dump(classifier, 'job_portal_automation/training_data/classifier_ethnicity.joblib')
    return data


def train_countries_data():
    # Training data for countries
    countries_data = [
        'Select...',
        'India',
        'Bangalore, India',
        'United States',
        'Canada',
        'United Kingdom',
        'Australia',
        'England',
        'China',
        'Russia'
    ]

    # Creating labels for the data
    labels = [f'country_{i}' for i in range(len(countries_data))]

    # Creating a list of tuples where each tuple is (text, label)
    training_data = [(item, label) for item, label in zip(countries_data, labels)]

    # Creating a bag-of-words model
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform([item[0] for item in training_data])
    y = np.array([item[1] for item in training_data])

    # Training a Naive Bayes classifier
    classifier = MultinomialNB()
    classifier.fit(X, y)

    # Save the model and vectorizer with updated paths
    joblib.dump(vectorizer, 'job_portal_automation/training_data/vectorizer_countries.joblib')
    joblib.dump(classifier, 'job_portal_automation/training_data/classifier_countries.joblib')

    return countries_data