from geopy.geocoders import Nominatim


def get_coordinates(address):
    geolocator = Nominatim(user_agent="my-app")
    location = geolocator.geocode(address)
    
    if location is not None:
        x = location.latitude
        y = location.longitude
    else:
        x = None
        y = None

    return x, y