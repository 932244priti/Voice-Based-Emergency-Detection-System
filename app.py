import os
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import speech_recognition as sr
import pickle
import requests
import pydeck as pdk
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
from dotenv import load_dotenv
import os

load_dotenv()

TOPIC = os.getenv("NTFY_TOPIC")
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

    /* =========================
       SAFEHER AI LIGHT THEME
       ========================= */

    .stApp {
        background: #f5f7fb;
        color: #172033;
    }

    [data-testid="stHeader"] {
        background: #f5f7fb;
    }

    [data-testid="stToolbar"] {
        background: transparent;
    }

    .main .block-container {
        max-width: 900px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Main title */
    .main-title {
        text-align: center;
        color: #d90429 !important;
        font-size: 42px;
        font-weight: 800;
        letter-spacing: 0.3px;
        margin-bottom: 4px;
    }

    .subtitle {
        text-align: center;
        color: #526071 !important;
        font-size: 18px;
        margin-bottom: 20px;
    }

    /* Protection flow card */
    .card {
        padding: 24px 28px;
        border-radius: 18px;
        background: #ffffff !important;
        color: #172033 !important;
        border: 1px solid #e1e6ef;
        box-shadow: 0 8px 24px rgba(20, 35, 60, 0.08);
        margin-bottom: 24px;
    }

    .card h3 {
        color: #172033 !important;
        font-size: 24px;
        margin: 0 0 14px 0;
        font-weight: 750;
    }

    .card p {
        color: #344054 !important;
        font-size: 16px;
        line-height: 1.8;
        margin: 0;
        font-weight: 600;
    }

    /* Streamlit headings and normal text */
    h1, h2, h3, h4, h5, h6 {
        color: #172033 !important;
    }

    p, label, .stMarkdown, .stText {
        color: #344054;
    }

    /* Emergency / warning / safe result cards */
    .emergency-box {
        padding: 25px;
        border-radius: 18px;
        text-align: center;
        background: #fff1f2 !important;
        color: #7f1d1d !important;
        border: 2px solid #ff4d4d;
        margin: 20px 0;
        box-shadow: 0 6px 18px rgba(255, 77, 77, 0.12);
    }

    .emergency-box h2,
    .emergency-box h3,
    .emergency-box p {
        color: #991b1b !important;
    }

    .warning-box {
        padding: 25px;
        border-radius: 18px;
        text-align: center;
        background: #fff8e1 !important;
        color: #7a4b00 !important;
        border: 2px solid #ffb300;
        margin: 20px 0;
        box-shadow: 0 6px 18px rgba(255, 179, 0, 0.12);
    }

    .warning-box h2,
    .warning-box h3,
    .warning-box p {
        color: #7a4b00 !important;
    }

    .safe-box {
        padding: 25px;
        border-radius: 18px;
        text-align: center;
        background: #edf8ef !important;
        color: #166534 !important;
        border: 2px solid #66bb6a;
        margin: 20px 0;
        box-shadow: 0 6px 18px rgba(76, 175, 80, 0.12);
    }

    .safe-box h2,
    .safe-box h3,
    .safe-box p {
        color: #166534 !important;
    }

    /* Buttons */
    .stButton > button,
    .stLinkButton > a {
        border-radius: 10px !important;
        font-weight: 700 !important;
        min-height: 46px;
    }

    .stLinkButton > a {
        background: #e63946 !important;
        color: #ffffff !important;
        border: none !important;
        text-decoration: none !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    .stLinkButton > a:hover {
        background: #c92535 !important;
        color: #ffffff !important;
    }

    /* Primary listening button */
    .stButton > button[kind="primary"] {
        background: #e63946 !important;
        color: white !important;
        border: none !important;
    }

    .stButton > button[kind="primary"]:hover {
        background: #c92535 !important;
        color: white !important;
    }

    /* Metric cards */
    [data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e1e6ef;
        border-radius: 14px;
        padding: 14px;
        box-shadow: 0 4px 14px rgba(20, 35, 60, 0.06);
    }

    [data-testid="stMetricLabel"] {
        color: #526071 !important;
    }

    [data-testid="stMetricValue"] {
        color: #172033 !important;
    }

    /* Info / success / warning messages */
    [data-testid="stAlert"] {
        border-radius: 12px;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #667085 !important;
        font-size: 14px;
        margin-top: 30px;
        padding: 15px;
    }

    .footer b {
        color: #d90429 !important;
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
                # DETAILED LIGHT MAP
                # --------------------------------------------

                map_zoom = 16.0

                view_state = pdk.ViewState(
                    latitude=float(latitude),
                    longitude=float(longitude),
                    zoom=map_zoom,
                    pitch=0,
                    bearing=0
                )

                # OpenStreetMap light tiles provide a clearer street-level
                # view than Streamlit's theme-dependent st.map.
                osm_layer = pdk.Layer(
                    "TileLayer",
                    data="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
                    min_zoom=0,
                    max_zoom=19,
                    tile_size=256
                )

                location_layer = pdk.Layer(
                    "ScatterplotLayer",
                    data=[{
                        "lat": float(latitude),
                        "lon": float(longitude)
                    }],
                    get_position="[lon, lat]",
                    get_radius=35,
                    radius_min_pixels=7,
                    radius_max_pixels=18,
                    pickable=False,
                    stroked=True,
                    filled=True,
                    get_fill_color=[230, 57, 70, 230],
                    get_line_color=[140, 20, 35, 255],
                    line_width_min_pixels=2
                )

                location_text_layer = pdk.Layer(
                    "TextLayer",
                    data=[{
                        "lat": float(latitude),
                        "lon": float(longitude),
                        "label": "You are here"
                    }],
                    get_position="[lon, lat]",
                    get_text="label",
                    get_size=14,
                    get_color=[40, 40, 40, 255],
                    get_alignment_baseline="bottom",
                    get_pixel_offset=[0, -12]
                )

                deck = pdk.Deck(
                    layers=[osm_layer, location_layer, location_text_layer],
                    initial_view_state=view_state,
                    map_provider="carto",
                    map_style="light",
                    tooltip={"text": "Current location"}
                )

                st.pydeck_chart(
                    deck,
                    use_container_width=True
                )

                st.caption(
                    "© OpenStreetMap contributors • Live browser location"
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