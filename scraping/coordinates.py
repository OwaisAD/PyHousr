from geopy.geocoders import Nominatim
import time
import csv
import shutil

def get_coordinates(address, postnr):
    geolocator = Nominatim(user_agent="my-app")
    location = geolocator.geocode(f'{address} {postnr} Danmark')
    time.sleep(1)
    if location is not None:
        x = location.latitude
        y = location.longitude
    else:
        x = None
        y = None

    return x, y


def validate_coordinates():
    fieldnames = ['Address', 'X', 'Y', 'Price', 'Type', 'Size', 'Squaremeter price', 'Energy class', 'Url']
    
    zipCode = 3460 # Change value to clean data for each city
    filename = f'../data/house_data/house_data_{zipCode}.csv'
    output_file = f'../data/house_data/house_data_{zipCode}_output.csv'
    with open(filename, 'r') as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            address = row[0]
            stripped_address = address.split(',')[0].strip() 
            x,y = get_coordinates(stripped_address,zipCode)
            price = row[3]
            type = row[4]
            size = row[5]
            squaremeter=row[6]
            energy_class= row[7]
            url= row[8]
            
            house_data = {
                'Address': address,
                'X':str(x),
                'Y':str(y),
                'Price': price,
                'Type': type,
                'Size': size,
                'Squaremeter price': squaremeter,
                'Energy class': energy_class,
                'Url': url
        }
            with open(output_file, 'a', newline='') as output:
                writer = csv.DictWriter(output, fieldnames=fieldnames)
                writer.writerow(house_data)

    shutil.move(output_file, filename)

#validate_coordinates() #should only be used when cleaning x,y coordinates


if __name__ == '__main__':
    print("MAIN")