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

def save_to_csv(data, filename):
    fieldnames = ['Adresse', 'X', 'Y', 'Pris', 'Type', 'Værelser', 'Bolig Areal', 'Kvadratmeter Pris', 'Grund Areal', 'Byggeår', 'Internet Hastighed', 'Energimærke']

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def house_data_scrape(postnr):

    data = []
    try:
        with open("./data_2800_test10.csv", "r") as file:
            links = file.readlines()
            print(f'links er : {links}')
    except Exception as e:
        print(e)
        return data
    
    for link in links:
        link = link.strip()
        if not link:
            continue

        print(f'Dette er linket: {link}')
        browser.get(link)
        
        time.sleep(5)

        adresse = browser.find_element(By.XPATH, '/html/body/div[2]/div[4]/div/div[1]/a').text
        x,y = get_coordinates(adresse)
        price = browser.find_element(By.XPATH, '/html/body/div[2]/div[6]/div[1]/div[2]/div[1]/div[1]/div/div[2]/dl/dd[1]').text
        cleaned_price = int(price.replace(".", "").split()[0])
        
        type = browser.find_element(By.XPATH, '//*[@id="ctrldiv"]/div[6]/div[1]/div[2]/div[1]/div[1]/div/div[2]/dl/dd[2]').text
        rooms = int(browser.find_element(By.XPATH, '//*[@id="ctrldiv"]/div[6]/div[1]/div[2]/div[1]/div[1]/div/div[2]/dl/dd[3]').text)
        bolig_areal = browser.find_element(By.XPATH, '//*[@id="ctrldiv"]/div[6]/div[1]/div[2]/div[1]/div[1]/div/div[2]/dl/dd[4]').text
        cleaned_bolig_areal = int(bolig_areal.split()[0])
        kvm_pris = int(int(cleaned_price)/int(cleaned_bolig_areal))   

        grund_areal = browser.find_element(By.XPATH, '//*[@id="ctrldiv"]/div[6]/div[1]/div[2]/div[1]/div[1]/div/div[2]/dl/dd[5]').text
        cleaned_grund_areal = int(grund_areal.replace(".", "").split()[0])
        bygge_år = int(browser.find_element(By.XPATH, '//*[@id="ctrldiv"]/div[6]/div[1]/div[2]/div[1]/div[1]/div/div[2]/dl/dd[6]').text)
        internet_hastighed = browser.find_element(By.XPATH, '//*[@id="ctrldiv"]/div[6]/div[1]/div[2]/div[1]/div[1]/div/div[2]/dl/dd[8]').text

        energi_mærke = browser.find_element(By.XPATH, '/html/body/div[2]/div[6]/div[1]/div[2]/div[22]/div/div[2]/div/div[1]/p[1]').text
        regex_pattern = r"energimærke\s*(A2020|A2015|A2010|A|B|C|D|E|F|G)"
        match = re.search(regex_pattern, energi_mærke)
        if match:
            energimærke = match.group(1)
        else:
            print("Energimærke blev ikke fundet.")
            energimærke = ""

        house_data = {
            'Adresse': adresse,
            'X':x,
            'Y':y,
            'Pris': cleaned_price,
            'Type': type,
            'Værelser': rooms,
            'Bolig Areal': cleaned_bolig_areal,
            'Kvadratmeter Pris': kvm_pris,
            'Grund Areal': cleaned_grund_areal,
            'Byggeår': bygge_år,
            'Internet Hastighed': internet_hastighed,
            'Energimærke': energimærke
        }

        data.append(house_data)

    return data

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Vil hente data fra dit valgte fra dinGeo på huse til salg")
    parser.add_argument("postnr", help="Dansk postnr du vil scrappe huse fra")

    args = parser.parse_args()

    if not args.postnr:
        print("Indtast venligst postnr.")
    else:
        print("Behandler.")
        my_data = house_data_scrape(args.postnr)
        
        filename = f"house_data_{args.postnr}.csv"
        save_to_csv(my_data, filename)
        print(f"Data er gemt i filen: {filename}")