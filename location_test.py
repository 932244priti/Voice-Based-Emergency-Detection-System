import streamlit as st
import streamlit.components.v1 as components
import requests
import os
from dotenv import load_dotenv

load_dotenv()

TOPIC = os.getenv("NTFY_TOPIC")

st.set_page_config(
    page_title="NTFY Live Location Test",
    page_icon="🚨"
)

st.title("🚨 NTFY + Live Location Test")

st.write("Click the button and allow browser location permission.")

components.html(
    """
    <html>
    <body>

        <button onclick="sendLocation()"
        style="
            background:#e11d48;
            color:white;
            border:none;
            padding:15px 25px;
            border-radius:10px;
            font-size:16px;
            cursor:pointer;
        ">
        🚨 SEND EMERGENCY ALERT
        </button>

        <div id="result" style="margin-top:20px;"></div>

        <script>

        function sendLocation() {

            const result = document.getElementById("result");

            result.innerHTML =
                "📍 Getting your live location...";

            if (!navigator.geolocation) {

                result.innerHTML =
                    "❌ Geolocation is not supported.";

                return;
            }

            navigator.geolocation.getCurrentPosition(

                function(position) {

                    const latitude =
                        position.coords.latitude;

                    const longitude =
                        position.coords.longitude;

                    const mapsLink =
                        "https://www.google.com/maps?q="
                        + latitude + ","
                        + longitude;

                    result.innerHTML = `

                        <h3>✅ Live Location Detected</h3>

                        <p>
                        Latitude: ${latitude}
                        </p>

                        <p>
                        Longitude: ${longitude}
                        </p>

                        <p>
                        📱 Sending NTFY alert...
                        </p>

                    `;

                    /*
                    Send coordinates back to Streamlit
                    */

                    const data = {
                        latitude: latitude,
                        longitude: longitude
                    };

                    window.parent.postMessage(
                        {
                            type: "streamlit:setComponentValue",
                            value: data
                        },
                        "*"
                    );

                },

                function(error) {

                    result.innerHTML =
                        "❌ Could not get your location. "
                        + error.message;

                },

                {
                    enableHighAccuracy: true,
                    timeout: 15000,
                    maximumAge: 0
                }
            );
        }

        </script>

    </body>
    </html>
    """,
    height=350
)