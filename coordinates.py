from geopy.geocoders import Nominatim
import time

def get_coordinates(address):
    geolocator = Nominatim(user_agent="my-app")
    location = geolocator.geocode(address)
    time.sleep(2)
    if location is not None:
        x = location.latitude
        y = location.longitude
    else:
        x = None
        y = None

    return x, y