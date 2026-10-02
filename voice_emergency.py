import speech_recognition as sr
import pickle


# -----------------------------------
# Load Trained ML Model
# -----------------------------------

with open("emergency_model.pkl", "rb") as file:
    model = pickle.load(file)

with open("vectorizer.pkl", "rb") as file:
    vectorizer = pickle.load(file)


# -----------------------------------
# Voice Recognition
# -----------------------------------

recognizer = sr.Recognizer()

print("\n====================================")
print("🚨 AI VOICE EMERGENCY DETECTION")
print("====================================")

print("\n🎤 Speak your message...")

with sr.Microphone() as source:

    recognizer.adjust_for_ambient_noise(
        source,
        duration=1
    )

    print("Listening...")

    audio = recognizer.listen(source)


# -----------------------------------
# Convert Voice → Text
# -----------------------------------

try:

    print("\nProcessing voice...")

    text = recognizer.recognize_google(audio)

    print("\n📝 You said:")
    print(text)


    # -----------------------------------
    # AI Prediction
    # -----------------------------------

    text_vector = vectorizer.transform([text])

    prediction = model.predict(text_vector)[0]

    probability = model.predict_proba(text_vector)[0]

    confidence = max(probability) * 100


    print("\n====================================")

    if prediction == "emergency":

        print("🚨 EMERGENCY DETECTED!")

    else:

        print("🟢 NORMAL")

    print("Confidence:", round(confidence, 2), "%")

    print("====================================")


# -----------------------------------
# Error Handling
# -----------------------------------

except sr.UnknownValueError:

    print("\n❌ Could not understand the voice.")

except sr.RequestError as e:

    print("\n❌ Speech recognition error:")
    print(e)