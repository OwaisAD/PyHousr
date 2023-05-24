import csv
import time
import argparse
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from accept_terms import accept_terms
from coordinates import get_coordinates

browser = webdriver.Firefox()
browser.get('https://www.dingeo.dk')
time.sleep(2)

accept_terms(browser)

def save_to_csv(data, filename):
    fieldnames = ['Address', 'X', 'Y', 'Price', 'Type', 'Size', 'Squaremeter price', 'Energy class', 'Url']

    with open(filename, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(data)

def load_visited_urls(filename):
    visited_urls = []
    with open (filename) as file:
        lines = file.readlines()
        for line in lines:
            parts = line.split(',')
            visited_urls.append(parts[-1].rstrip())
    return visited_urls

def scrape_address(browser):
    try:
        address = browser.find_element(By.XPATH, '/html/body/div[2]/div[4]/div/div[1]/a').text
        return address
    except:
        print("No address found")
        return

def scrape_price(browser):
    try:
        price = browser.find_element(By.XPATH, '/html/body/div[2]/div[6]/div[1]/div[2]/div[1]/div[1]/div/div[2]/dl/dd[1]').text
        return price
    except:
        print("No price found")
        return
    
def scrape_type(browser):
    try:
        type = browser.find_element(By.XPATH, '//*[@id="ctrldiv"]/div[6]/div[1]/div[2]/div[1]/div[1]/div/div[2]/dl/dd[2]').text
        return type
    except:
        print("No type found")
        return

def scrape_squaremetres(browser):
    try:
        scrape_squaremetres = browser.find_element(By.XPATH, '//*[@id="ctrldiv"]/div[6]/div[1]/div[2]/div[1]/div[1]/div/div[2]/dl/dd[4]').text
        return scrape_squaremetres
    except:
        print("No square metres found")
        return

def scrape_energy_class(browser):
    try:
        energy_class = browser.find_element(By.XPATH, '/html/body/div[2]/div[6]/div[1]/div[2]/div[22]/div/div[2]/div/div[1]/p[1]').text
        regex_pattern = r"energimærke\s*(A2020|A2015|A2010|A|B|C|D|E|F|G)"
        match = re.search(regex_pattern, energy_class)
        if match:
            return match.group(1)
        else:
            print("Energy class not found")
            return
    except:
        print("Energy class not found")
        return

def house_data_scrape(zip_code):
    filename = f"../data/house_data/house_data_{zip_code}.csv"
    visited_urls = load_visited_urls(filename)

    try:
        with open(f"../data/link_data/data_{zip_code}.csv", "r") as file:
            links = file.readlines()
    except Exception as e:
        print(e)
    
    for link in links:
        link = link.strip()
        if not link or link in visited_urls:
            continue
       
        browser.get(link)
        time.sleep(3)
        try:
            address = scrape_address(browser)
            
            if not address:
                continue
            
            stripped_address = address.split(',')[0].strip()
            x,y = get_coordinates(stripped_address, zip_code)   
            price = scrape_price(browser)
            
            if not price:
                continue

            cleaned_price = int(price.replace(".", "").split()[0])
            type = scrape_type(browser)
            
            if not type:
                continue

            squaremetres = scrape_squaremetres(browser)
            
            if not squaremetres:
                continue

            cleaned_squaremetres = int(squaremetres.split()[0])
            price_sqrtmetres = int(int(cleaned_price)/int(cleaned_squaremetres))   

            energy_class = scrape_energy_class(browser)
            
            if not energy_class:
                continue

            house_data = {
                'Address': address,
                'X':x,
                'Y':y,
                'Price': cleaned_price,
                'Type': type,
                'Size': cleaned_squaremetres,
                'Squaremeter price': price_sqrtmetres,
                'Energy class': energy_class,
                'Url': link
            }

            save_to_csv(house_data, filename)

        except Exception as e:
            print(f"Url skipped")
            print(e)
            continue
    browser.quit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Fetches house data from dinGeo")
    parser.add_argument("zip_code", help="Danish zip code to scrappe data with")

    args = parser.parse_args()

    if not args.zip_code:
        print("Please enter a valid zip code")
    else:
        print("Processing")
        my_data = house_data_scrape(args.zip_code)
        print("Data has been saved")