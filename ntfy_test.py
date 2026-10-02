import requests
import os
from dotenv import load_dotenv

load_dotenv()

TOPIC = os.getenv("NTFY_TOPIC")
latitude = 18.5196
longitude = 73.8554

maps_link = f"https://www.google.com/maps?q={latitude},{longitude}"

message = f"""🚨 WOMEN SAFETY EMERGENCY ALERT!

⚠️ Emergency Detected!

📍 CURRENT LOCATION
Latitude: {latitude}
Longitude: {longitude}

🗺️ GOOGLE MAPS LOCATION
{maps_link}

Please check the location immediately.
"""

response = requests.post(
    f"https://ntfy.sh/{TOPIC}",
    data=message.encode("utf-8"),
    headers={
        "Title": "WOMEN SAFETY EMERGENCY",
        "Priority": "urgent",
        "Tags": "warning"
    }
)

print("Status Code:", response.status_code)
print("Response:", response.text)

if response.status_code == 200:
    print("SUCCESS: Emergency notification sent!")
else:
    print("FAILED:", response.text)