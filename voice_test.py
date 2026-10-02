import speech_recognition as sr

recognizer = sr.Recognizer()

print("🎤 Voice Test Started")
print("Speak something after the beep...")

with sr.Microphone() as source:

    recognizer.adjust_for_ambient_noise(source, duration=1)

    print("\nListening...")

    audio = recognizer.listen(source)

try:
    print("\nProcessing your voice...")

    text = recognizer.recognize_google(audio)

    print("\nYou said:")
    print(text)

except sr.UnknownValueError:
    print("\n❌ Sorry, I could not understand your voice.")

except sr.RequestError as e:
    print("\n❌ Speech recognition service error:")
    print(e)