import requests
from datetime import datetime
import time
import smtplib

MY_LAT = "ENTER YOUR LOCATION'S LATITUDE"
MY_LONG = "ENTER YOUR LOCATION'S LONGITUDE"

MY_EMAIL = "ENTER EMAIL ADDRESS"
MY_PASSWORD = "ENTER PASSWORD"
RECIPIENTS = ["ENTER THE RECIPIENT'S EMAIL ADDRESS"]


'''
GET DATA FROM THE ISS API TO ACCESS THE ISS' POSITION AND LATITUDE AND LONGTITUDE.
IF MY LATITUDE AND LONGTITUDE IS WITHIN THE RANGE OF THE ISS, THEN THE FUNCTION WILL RETURN TRUE.
'''
def is_near_me():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    my_lat_plus = MY_LAT + 5
    my_lat_minus = MY_LAT - 5
    my_long_plus = MY_LONG + 5
    my_long_minus = MY_LONG - 5
    if my_lat_minus <= iss_latitude <= my_lat_plus and my_long_minus <= iss_longitude <= my_long_plus:
        return True

'''
By using sunrise-sunset(https://sunrise-sunset.org/api) API, it requires two parameters: longitude and latitude.
Pass in your current location's longitude and latitude to get the sunrise and sunset data. However, there is an extra
parameter in the PARAMETERS -{ "formatted:" 0), which basically means that the data returned is in UNIX time
(12-hr time). Moreover, we also need to access the current time in the current location. 
We can do it by importing datetime. 
'''
def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0]) + 5
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0]) + 5

    time_now = datetime.now()
    hour_now = time_now.hour

    if hour_now >= sunset or hour_now <= sunrise:
        return True


'''
Run a while loop. While True, check if the ISS is near my location and if it is night time (sunrise or sunset),
if one of the conditions is false, then try checking again every 60 seconds; however, if the both conditions are true,
then by using smtplib, send a notification through email.
'''
while True:
    time.sleep(60)

    if is_near_me() and is_night() is True:
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL,
                                to_addrs=RECIPIENTS,
                                msg="Subject:LOOK UP!\n\nThe ISS is right above you! You're welcome. :)")