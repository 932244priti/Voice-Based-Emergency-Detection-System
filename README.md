# Voice-Based Emergency Detection System

An AI-powered personal safety system that detects emergency situations from voice input and provides location-based emergency alerts.

## Features

- Voice input using Speech Recognition
- AI-based emergency detection
- Risk classification: Normal, Suspicious, Emergency
- Confidence score for predictions
- Live browser-based GPS location
- Google Maps location link
- OpenStreetMap-based location display
- Emergency alerts using NTFY
- Emergency SOS functionality
- Machine Learning-based text classification

## Technologies Used

- Python
- Streamlit
- SpeechRecognition
- Scikit-learn
- TF-IDF
- Logistic Regression
- Streamlit Geolocation
- PyDeck
- NTFY
- Google Maps

## Machine Learning

The system uses Natural Language Processing (NLP) to analyze spoken sentences.

The voice is converted into text using Speech Recognition. The text is then transformed into numerical features using TF-IDF and classified using a Logistic Regression model.

The model classifies input into:

- Normal
- Suspicious
- Emergency

## Project Structure

```text
AI_Emergency_Detection/
│
├── app.py
├── app_backup.py
├── create_dataset.py
├── current_location.py
├── emergency_model.pkl
├── emergency_voice_dataset.csv
├── location_test.py
├── ntfy_test.py
├── train_model.py
├── vectorizer.pkl
├── voice_emergency.py
├── voice_test.py
├── .gitignore
└── README.md