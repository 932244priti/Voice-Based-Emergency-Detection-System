import streamlit as st
import speech_recognition as sr
import pickle
import requests
from streamlit_geolocation import streamlit_geolocation


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SafeHer AI",
    page_icon="🚨",
    layout="centered"
)


# ============================================================
# CONFIGURATION
# ============================================================

TOPIC = "priti_women_safety_1004"
NTFY_URL = f"https://ntfy.sh/{TOPIC}"


# ============================================================
# LOAD MODEL
# ============================================================

@st.cache_resource
def load_model():

    with open("emergency_model.pkl", "rb") as file:
        model = pickle.load(file)

    with open("vectorizer.pkl", "rb") as file:
        vectorizer = pickle.load(file)

    return model, vectorizer


try:
    model, vectorizer = load_model()

except Exception as e:

    st.error("❌ Could not load AI model.")
    st.code(str(e))
    st.stop()


# ============================================================
# SESSION STATE
# ============================================================

if "voice_text" not in st.session_state:
    st.session_state.voice_text = ""

if "prediction" not in st.session_state:
    st.session_state.prediction = ""

if "confidence" not in st.session_state:
    st.session_state.confidence = 0.0

if "alert_sent" not in st.session_state:
    st.session_state.alert_sent = False


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        color: #d90429;
        font-size: 42px;
        font-weight: 800;
    }

    .subtitle {
        text-align: center;
        color: #666;
        font-size: 18px;
        margin-bottom: 20px;
    }

    .card {
        padding: 22px;
        border-radius: 18px;
        background: white;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        margin-bottom: 20px;
    }

    .emergency-box {
        padding: 25px;
        border-radius: 18px;
        text-align: center;
        background: #ffe5e5;
        border: 2px solid #ff4d4d;
        margin: 20px 0;
    }

    .warning-box {
        padding: 25px;
        border-radius: 18px;
        text-align: center;
        background: #fff8e1;
        border: 2px solid #ffb300;
        margin: 20px 0;
    }

    .safe-box {
        padding: 25px;
        border-radius: 18px;
        text-align: center;
        background: #e8f5e9;
        border: 2px solid #66bb6a;
        margin: 20px 0;
    }

    .footer {
        text-align: center;
        color: #777;
        font-size: 14px;
        margin-top: 30px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🛡️ SafeHer AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-Powered Voice Emergency Detection & Women Safety System'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# ============================================================
# SYSTEM FLOW
# ============================================================

st.markdown(
    """
    <div class="card">

    <h3>🔐 SafeHer AI Protection Flow</h3>

    <p>
    🎤 Voice Input
    →
    📝 Speech-to-Text
    →
    🤖 AI Prediction
    →
    🚨 Emergency Detection
    →
    📍 Live Location
    →
    📱 NTFY Alert
    </p>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# VOICE INPUT
# ============================================================

st.subheader("🎤 Voice Emergency Detection")

st.write(
    "Press the button and speak your situation clearly."
)

start_button = st.button(
    "🎙️ START LISTENING",
    use_container_width=True,
    type="primary"
)


# ============================================================
# VOICE + AI
# ============================================================

if start_button:

    recognizer = sr.Recognizer()

    try:

        # ----------------------------------------------------
        # MICROPHONE
        # ----------------------------------------------------

        with sr.Microphone() as source:

            st.info(
                "🎤 Listening... Please speak now."
            )

            recognizer.adjust_for_ambient_noise(
                source,
                duration=0.5
            )

            audio = recognizer.listen(
                source,
                timeout=15,
                phrase_time_limit=15
            )


        # ----------------------------------------------------
        # SPEECH → TEXT
        # ----------------------------------------------------

        st.info(
            "🤖 Processing your voice..."
        )

        text = recognizer.recognize_google(
            audio,
            language="en-IN"
        )


        # ----------------------------------------------------
        # SAVE TEXT
        # ----------------------------------------------------

        st.session_state.voice_text = text


        # ----------------------------------------------------
        # AI MODEL PREDICTION
        # ----------------------------------------------------

        text_vector = vectorizer.transform([text])

        prediction = model.predict(
            text_vector
        )[0]

        probability = model.predict_proba(
            text_vector
        )[0]

        confidence = max(probability) * 100


        # ----------------------------------------------------
        # NORMALIZE PREDICTION
        # ----------------------------------------------------

        prediction = str(
            prediction
        ).strip().lower()


        # ----------------------------------------------------
        # SAVE RESULT
        # ----------------------------------------------------

        st.session_state.prediction = prediction

        st.session_state.confidence = confidence

        # New prediction = allow new alert
        st.session_state.alert_sent = False


        st.success(
            "✅ Voice converted and AI prediction completed!"
        )


    # ========================================================
    # ERROR HANDLING
    # ========================================================

    except sr.WaitTimeoutError:

        st.error(
            "❌ No voice detected. Please try again."
        )


    except sr.UnknownValueError:

        st.error(
            "❌ Could not understand your voice. "
            "Please speak clearly."
        )


    except sr.RequestError as e:

        st.error(
            f"❌ Speech recognition service error: {e}"
        )


    except Exception as e:

        st.error(
            f"❌ Error: {e}"
        )


# ============================================================
# SHOW RECOGNIZED VOICE
# ============================================================

if st.session_state.voice_text:

    st.subheader("📝 Recognized Voice")

    st.info(
        f"🎤 {st.session_state.voice_text}"
    )


# ============================================================
# SHOW AI RESULT
# ============================================================

if st.session_state.prediction:

    prediction = st.session_state.prediction

    confidence = st.session_state.confidence


    st.subheader("🤖 AI Prediction Result")


    col1, col2 = st.columns(2)


    with col1:

        st.metric(
            "Prediction",
            prediction.upper()
        )


    with col2:

        st.metric(
            "Confidence",
            f"{confidence:.2f}%"
        )


    # ========================================================
    # EMERGENCY
    # ========================================================

    if prediction == "emergency":

        st.markdown(
            f"""
            <div class="emergency-box">

            <h2>🚨 EMERGENCY DETECTED</h2>

            <p>
            AI detected an emergency situation.
            </p>

            <h3>
            Confidence: {confidence:.2f}%
            </h3>

            </div>
            """,
            unsafe_allow_html=True
        )


        st.warning(
            "⚠️ Emergency detected. "
            "Allow browser location permission."
        )


        # ====================================================
        # LIVE LOCATION
        # ====================================================

        st.subheader(
            "📍 Current Live Location"
        )


        location = streamlit_geolocation()


        if location:

            latitude = location.get(
                "latitude"
            )

            longitude = location.get(
                "longitude"
            )


            if (
                latitude is not None
                and longitude is not None
            ):

                st.success(
                    "✅ Live location detected!"
                )


                # --------------------------------------------
                # COORDINATES
                # --------------------------------------------

                col1, col2 = st.columns(2)


                with col1:

                    st.metric(
                        "Latitude",
                        f"{latitude:.6f}"
                    )


                with col2:

                    st.metric(
                        "Longitude",
                        f"{longitude:.6f}"
                    )


                # --------------------------------------------
                # GOOGLE MAPS
                # --------------------------------------------

                maps_link = (
                    "https://www.google.com/maps?q="
                    f"{latitude},{longitude}"
                )


                st.link_button(
                    "🗺️ OPEN LIVE LOCATION",
                    maps_link,
                    use_container_width=True
                )


                # --------------------------------------------
                # MAP
                # --------------------------------------------

                st.map(
                    {
                        "lat": [latitude],
                        "lon": [longitude]
                    }
                )


                # =================================================
                # NTFY
                # =================================================

                st.subheader(
                    "📱 Emergency Notification"
                )


                if not st.session_state.alert_sent:

                    message = f"""🚨 WOMEN SAFETY EMERGENCY ALERT!

⚠️ AI Emergency Detected!

📝 VOICE MESSAGE:
{st.session_state.voice_text}

🤖 AI PREDICTION:
{prediction.upper()}

📊 CONFIDENCE:
{confidence:.2f}%

📍 CURRENT LOCATION:

Latitude: {latitude}
Longitude: {longitude}

🗺️ GOOGLE MAPS LOCATION:

{maps_link}

Please check the location immediately.
"""


                    try:

                        response = requests.post(
                            NTFY_URL,

                            data=message.encode(
                                "utf-8"
                            ),

                            headers={
                                "Title":
                                "WOMEN SAFETY EMERGENCY",

                                "Priority":
                                "urgent",

                                "Tags":
                                "warning"
                            },

                            timeout=10
                        )


                        if response.status_code == 200:

                            st.session_state.alert_sent = True

                            st.success(
                                "✅ Emergency alert sent successfully!"
                            )

                            st.info(
                                "📱 Check your ntfy app."
                            )


                        else:

                            st.error(
                                "❌ NTFY alert failed."
                            )

                            st.write(
                                "Status Code:",
                                response.status_code
                            )

                            st.write(
                                response.text
                            )


                    except requests.RequestException as e:

                        st.error(
                            "❌ Could not connect to NTFY."
                        )

                        st.write(
                            str(e)
                        )


                else:

                    st.success(
                        "📱 Emergency alert already sent."
                    )


            else:

                st.warning(
                    "📍 Location coordinates unavailable."
                )


        else:

            st.warning(
                "📍 Please click the location button "
                "and allow browser permission."
            )


    # ========================================================
    # SUSPICIOUS
    # ========================================================

    elif prediction == "suspicious":

        st.markdown(
            f"""
            <div class="warning-box">

            <h2>⚠️ SUSPICIOUS SITUATION</h2>

            <p>
            AI detected a suspicious situation.
            </p>

            <h3>
            Confidence: {confidence:.2f}%
            </h3>

            </div>
            """,
            unsafe_allow_html=True
        )


        st.warning(
            "⚠️ Stay alert and move to a safe location."
        )


    # ========================================================
    # NORMAL
    # ========================================================

    else:

        st.markdown(
            f"""
            <div class="safe-box">

            <h2>🟢 NO EMERGENCY DETECTED</h2>

            <p>
            AI Prediction: {prediction.upper()}
            </p>

            <h3>
            Confidence: {confidence:.2f}%
            </h3>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# RESET
# ============================================================

st.divider()


if st.button(
    "🔄 RESET DETECTION",
    use_container_width=True
):

    st.session_state.voice_text = ""

    st.session_state.prediction = ""

    st.session_state.confidence = 0.0

    st.session_state.alert_sent = False

    st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">

    🛡️ <b>SafeHer AI</b><br>

    Voice Emergency Detection • AI Prediction •
    Live Location • NTFY Alert

    </div>
    """,
    unsafe_allow_html=True
)