import requests


MY_LAT = 37.338207
MY_LONG = -121.886330

MY_EMAIL = "YOUR EMAIL"
MY_PASSWORD = "YOUR PASSWORD"
RECIPIENTS = ["ENTER RECIPIENT'S EMAIL"]

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
