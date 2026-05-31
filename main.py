import requests
import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("OWN_API_KEY")
SENDER_EMAIL = os.environ.get("EMAIL_SENDER")
SENDER_PASSWORD = os.environ.get("EMAIL_PASSWORD")
RECEIVER_EMAIL = os.environ.get("EMAIL_RECEIVER")
LAT = float(os.environ.get("LATITUDE"))
LON = float(os.environ.get("LONGITUDE"))

parameters = {
    "lon" : LON,
    "lat" : LAT,
    "appid" : API_KEY,
    "units" : "metric",
    "cnt" : 4

}
print(f"DEBUG: API Key Length is {len(API_KEY) if API_KEY else 0} characters.")
response = requests.get(url="https://api.openweathermap.org/data/2.5/forecast",params=parameters)
response.raise_for_status()
weather_data = response.json()

will_rain = False
for hour in weather_data["list"]:
    condition_code = hour["weather"][0]["id"]
    if condition_code < 600:
        will_rain = True
        break
if will_rain:
    msg = EmailMessage()
    msg["Subject"] = "☔ Weather Alert: Rain Expected Today!"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg.set_content("Hi there,\n\nIt looks like rain is in the forecast for the next few hours. Don't forget to grab your umbrella before you head out!\n\nBest,\nYour Weather Bot")
    try:
        with smtplib.SMTP("smtp.gmail.com",587) as connection :
            connection.starttls()
            connection.login(user=SENDER_EMAIL,password=SENDER_PASSWORD)
            connection.send_message(msg)
        print("Email sent successfully!")

    except Exception as e:
        print(f"Failed to send email: {e}")

else:
    print("No rain predicted. No email sent.")

