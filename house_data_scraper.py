from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import time
import argparse
import re
from accept_terms import accept_terms
from coordinates import get_coordinates

browser = webdriver.Firefox()
browser.get('https://www.dingeo.dk')
time.sleep(2)

accept_terms(browser)

def scrape_byggeår(browser):
    try:
        bygge_år = int(browser.find_element(By.XPATH, '//*[@id="ctrldiv"]/div[6]/div[1]/div[2]/div[1]/div[1]/div/div[2]/dl/dd[6]').text)
    except:
        try:
            bygge_år = int(By.XPATH, '/html/body/div[2]/div[6]/div[1]/div[2]/div[1]/div[1]/div/div[2]/dl/dd[5]').text
        except:
            bygge_år = 0
            print('Ikke noget byggeår')
    return bygge_år

def save_to_csv(data, filename):
    fieldnames = ['Address', 'X', 'Y', 'Price', 'Type', 'Size', 'Squaremeter price', 'Energy class', 'Url']

    with open(filename, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        #writer.writeheader()
        writer.writerow(data)

def house_data_scrape(postnr):

    visited_urls = []
    data = []
    filename = f"house_data_{postnr}.csv"
    with open (filename) as file:
        
        lines = file.readlines()
        
        for line in lines:
            parts = line.split(',')
            visited_urls.append(parts[-1].rstrip())

    try:
        with open(f"data_{postnr}.csv", "r") as file:
            links = file.readlines()
            print(f'links er : {links}')
    except Exception as e:
        print(e)
        return data
    
    print(f'visited_urls: {visited_urls}')

    for link in links:

        link = link.strip()
        if not link:
            continue
        if link in visited_urls:
            continue

        print(f'Dette er linket: {link}')
        browser.get(link)
        
        time.sleep(3)
        try:
            try:
                adresse = browser.find_element(By.XPATH, '/html/body/div[2]/div[4]/div/div[1]/a').text
            except:
                print("Ingen adresse fundet")
                continue

            stripped_address = adresse.split(',')[0].strip()
                            
            x,y = get_coordinates(stripped_address)       
            price = browser.find_element(By.XPATH, '/html/body/div[2]/div[6]/div[1]/div[2]/div[1]/div[1]/div/div[2]/dl/dd[1]').text
            cleaned_price = int(price.replace(".", "").split()[0])
            
            type = browser.find_element(By.XPATH, '//*[@id="ctrldiv"]/div[6]/div[1]/div[2]/div[1]/div[1]/div/div[2]/dl/dd[2]').text
            # rooms = int(browser.find_element(By.XPATH, '//*[@id="ctrldiv"]/div[6]/div[1]/div[2]/div[1]/div[1]/div/div[2]/dl/dd[3]').text)
            bolig_areal = browser.find_element(By.XPATH, '//*[@id="ctrldiv"]/div[6]/div[1]/div[2]/div[1]/div[1]/div/div[2]/dl/dd[4]').text
            cleaned_bolig_areal = int(bolig_areal.split()[0])
            kvm_pris = int(int(cleaned_price)/int(cleaned_bolig_areal))   

            # grund_areal = browser.find_element(By.XPATH, '//*[@id="ctrldiv"]/div[6]/div[1]/div[2]/div[1]/div[1]/div/div[2]/dl/dd[5]').text
            # cleaned_grund_areal = int(grund_areal.replace(".", "").split()[0])
            
            # byggeår = scrape_byggeår(browser)
            
            # internet_hastighed = browser.find_element(By.XPATH, '//*[@id="ctrldiv"]/div[6]/div[1]/div[2]/div[1]/div[1]/div/div[2]/dl/dd[8]').text

            energi_mærke = browser.find_element(By.XPATH, '/html/body/div[2]/div[6]/div[1]/div[2]/div[22]/div/div[2]/div/div[1]/p[1]').text
            regex_pattern = r"energimærke\s*(A2020|A2015|A2010|A|B|C|D|E|F|G)"
            match = re.search(regex_pattern, energi_mærke)
            if match:
                energimærke = match.group(1)
            else:
                print("Energimærke blev ikke fundet.")
                continue

            house_data = {
               
                'Address': adresse,
                'X':x,
                'Y':y,
                'Price': cleaned_price,
                'Type': type,
                #'Værelser': rooms,
                'Size': cleaned_bolig_areal,
                'Squaremeter price': kvm_pris,
                #'Grund Areal': cleaned_grund_areal,
                #'Byggeår': byggeår,
                #'Internet Hastighed': internet_hastighed,
                'Energy class': energimærke,
                'Url': link
            }
            save_to_csv(house_data, filename)
        except Exception as e:
            print(f"Url skipped")
            print(e)
            continue
    #     data.append(house_data)
    browser.quit()

    # return data

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Vil hente data fra dit valgte fra dinGeo på huse til salg")
    parser.add_argument("postnr", help="Dansk postnr du vil scrappe huse fra")

    args = parser.parse_args()

    if not args.postnr:
        print("Indtast venligst postnr.")
    else:
        print("Behandler.")
        my_data = house_data_scrape(args.postnr)
        
        #filename = f"house_data_{args.postnr}.csv"
        #save_to_csv(my_data, filename)
        print(f"Data er gemt i filen:")