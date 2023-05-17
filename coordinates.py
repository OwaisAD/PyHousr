from geopy.geocoders import Nominatim
import pandas as pd

def get_coordinates(address):
    geolocator = Nominatim(user_agent="my-app")

    data = []
    
    location = geolocator.geocode(address)
    if location is not None:
        data.append({'address': address, 'latitude': location.latitude, 'longitude': location.longitude})
    else:
        data.append({'address': address, 'latitude': None, 'longitude': None})

    df = pd.DataFrame(data)
    return df.set_index('address').to_dict(orient='index')