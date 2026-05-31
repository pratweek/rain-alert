import requests
import os
api_key = "1d2d41681ae0ed8325dc89b517dac6cd"


parameters = {
    "lon" : 84.201187,
    "lat" : 25.755299,
    "appid" : api_key,
    "units" : "metric",
    "cnt" : 4

}
response = requests.get(url="https://api.openweathermap.org/data/2.5/forecast",params=parameters)
response.raise_for_status()
weather_data = response.json()

will_rain = False
for hour in weather_data["list"]:
    condition_code = hour["weather"][0]["id"] < 700
    if int(condition_code) < 700:
        will_rain = True
if will_rain:
    print("It will rain today")
