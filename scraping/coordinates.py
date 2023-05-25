from geopy.geocoders import Nominatim
import time

def get_coordinates(address, postnr):
    geolocator = Nominatim(user_agent="PyHousr")
    location = geolocator.geocode(f'{address} {postnr} Danmark')
    time.sleep(1)
    if location is not None:
        x = location.latitude
        y = location.longitude
    else:
        x = None
        y = None

    return x, y