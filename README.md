# 🚨 Voice-Based Emergency Detection System

<p align="center">

### 🛡️ AI-Powered Personal Safety Guardian

**Detect • Analyze • Locate • Alert**

An AI-powered personal safety system that detects emergency situations from voice input, analyzes the spoken language using Machine Learning, identifies the user's location, and sends location-based emergency alerts.

</p>

---

## 🌟 Project Overview

The **Voice-Based Emergency Detection System** is an AI-based personal safety application designed to detect potential emergency situations through natural spoken language.

The system converts voice into text using Speech Recognition, analyzes the text using NLP and Machine Learning, classifies the situation into **Normal, Suspicious, or Emergency**, obtains the user's browser-based location, and sends an emergency notification through NTFY.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🎤 Voice Input | Captures voice through the microphone |
| 🧠 AI Detection | Analyzes spoken language using Machine Learning |
| 🚦 Risk Classification | Normal, Suspicious, or Emergency |
| 📊 Confidence Score | Displays prediction confidence |
| 📍 Live GPS | Gets browser-based location |
| 🗺️ Location Map | Displays detected location |
| 🔗 Google Maps | Generates location link |
| 🚨 NTFY Alert | Sends emergency notification |
| 🆘 Emergency SOS | Emergency response functionality |

---

## 🔄 System Workflow

```text
🎤 Voice Input
      ↓
📝 Speech Recognition
      ↓
🧠 NLP Processing
      ↓
📊 TF-IDF Vectorization
      ↓
🤖 Logistic Regression
      ↓
🚦 Risk Classification
      ↓
📍 Live GPS Location
      ↓
🚨 Emergency Alert
      ↓
📱 NTFY Notification
🧠 Machine Learning

The system uses Natural Language Processing (NLP) and Machine Learning for emergency detection.

Processing Pipeline
Voice
  ↓
Speech-to-Text
  ↓
Text Processing
  ↓
TF-IDF Vectorization
  ↓
Logistic Regression
  ↓
Prediction + Confidence
Risk Categories

🟢 Normal

🟡 Suspicious

🔴 Emergency

🛠️ Technologies Used
Programming & Framework
🐍 Python
🌐 Streamlit
AI & Machine Learning
Scikit-learn
Natural Language Processing
TF-IDF
Logistic Regression
Voice & Location
SpeechRecognition
Streamlit Geolocation
PyDeck
Google Maps
OpenStreetMap
Notification
NTFY
Python Requests
## 📸 Application Screenshots

### 🏠 Home Screen
<img src="https://raw.githubusercontent.com/932244priti/Voice-Based-Emergency-Detection-System/main/screenshots/home%20page.png" alt="Home Screen" width="700">

### 🎤 Voice Input
<img src="https://raw.githubusercontent.com/932244priti/Voice-Based-Emergency-Detection-System/main/screenshots/voice_input.png" alt="Voice Input" width="700">

### 🚨 Emergency Detection
<img src="https://raw.githubusercontent.com/932244priti/Voice-Based-Emergency-Detection-System/main/screenshots/Emergency_detect.png" alt="Emergency Detection" width="700">

### ⚠️ Suspicious Condition Detection
<img src="https://raw.githubusercontent.com/932244priti/Voice-Based-Emergency-Detection-System/main/screenshots/Suspesious_condition%20_detect.png" alt="Suspicious Condition Detection" width="700">

### ✅ Normal Voice Detection
<img src="https://raw.githubusercontent.com/932244priti/Voice-Based-Emergency-Detection-System/main/screenshots/Normal_voice_detect.png" alt="Normal Voice Detection" width="700">

### 📍 Current Location
<img src="https://raw.githubusercontent.com/932244priti/Voice-Based-Emergency-Detection-System/main/screenshots/current_location.png" alt="Current Location" width="700">

### 🗺️ Exact Location
<img src="https://raw.githubusercontent.com/932244priti/Voice-Based-Emergency-Detection-System/main/screenshots/exact_location.png" alt="Exact Location" width="700">

### 🚨 Location Alert
<img src="https://raw.githubusercontent.com/932244priti/Voice-Based-Emergency-Detection-System/main/screenshots/location_alert.png" alt="Location Alert" width="700">

### 📱 NTFY Notification
<img src="https://raw.githubusercontent.com/932244priti/Voice-Based-Emergency-Detection-System/main/screenshots/NTFY%20Noification.jpeg" alt="NTFY Notification" width="700">

📂 Project Structure
Voice-Based-Emergency-Detection-System/
│
├── app.py
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
│
├── screenshots/
│   ├── Emergency_detect.png
│   ├── NTFY Noification.jpeg
│   ├── Normal_voice_detect.png
│   ├── Suspesious_condition _detect.png
│   ├── current_location.png
│   ├── exact_location.png
│   ├── home page.png
│   ├── location_alert.png
│   └── voice_input.png
│
├── .gitignore
├── requirements.txt
└── README.md
⚙️ Installation
1. Clone the Repository
git clone https://github.com/932244priti/Voice-Based-Emergency-Detection-System.git
2. Open the Project
cd Voice-Based-Emergency-Detection-System
3. Create Virtual Environment
python -m venv venv
4. Activate Virtual Environment

For Windows PowerShell:

venv\Scripts\Activate.ps1
5. Install Dependencies
pip install -r requirements.txt
🔐 Environment Configuration

Create a .env file in the project directory:

NTFY_TOPIC=your_ntfy_topic

⚠️ Never upload your real .env file or private credentials to GitHub.

▶️ Run the Application
streamlit run app.py

The application will open in your browser.

🔒 Privacy

The system is designed with privacy in mind.

📍 Location is accessed when required by the application.
🔐 Private configuration values are stored using environment variables.
🚫 .env files are excluded from Git using .gitignore.
🚀 Future Scope

Possible future improvements include:

🤖 AI chatbot assistance
📞 Automated emergency calling
👥 Multiple emergency contacts
📱 Mobile application
☁️ Cloud deployment
🌍 Multi-language voice detection
📈 Advanced risk analysis
🔔 Additional notification channels
🎯 Project Objective

The objective of this project is to develop a lightweight AI-based safety system capable of understanding natural spoken language, detecting potential emergency situations, identifying the user's location, and providing timely alerts.

👩‍💻 Author
Priti Gawai

GitHub:
https://github.com/932244priti
