import streamlit as st
from streamlit_geolocation import streamlit_geolocation

st.set_page_config(
    page_title="Current Location",
    page_icon="📍"
)

st.title("📍 Current Location Test")

st.write("Click the button below and allow location permission.")

location = streamlit_geolocation()

if location:

    latitude = location.get("latitude")
    longitude = location.get("longitude")

    if latitude is not None and longitude is not None:

        st.success("✅ Current Location Detected!")

        st.write("Latitude:", latitude)
        st.write("Longitude:", longitude)

        maps_link = (
            f"https://www.google.com/maps?q="
            f"{latitude},{longitude}"
        )

        st.markdown(
            f"[🗺️ Open Current Location in Google Maps]({maps_link})"
        )

        st.map(
            {
                "lat": [latitude],
                "lon": [longitude]
            }
        )

    else:
        st.warning("📍 Location coordinates not available.")

else:

    st.warning(
        "📍 Please click the location button and allow browser location permission."
    )