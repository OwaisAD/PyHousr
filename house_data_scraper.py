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

def house_data_scrape(postnr):
    try:
        with open(f"./data_{postnr}.csv", "r") as file:
            links = file.readlines()
    except Exception as e:
        print(e)


    #browser.get(f'{links[0]}')
    browser.get('https://www.dingeo.dk/adresse/3000-helsing%C3%B8r/hymersvej-15/')
    
    time.sleep(5)

    adresse = browser.find_element(By.XPATH, '/html/body/div[2]/div[4]/div/div[1]/a').text
    print(adresse.replace(",", "."))
    df = get_coordinates(adresse)
    print(df)

    price = browser.find_element(By.XPATH, '/html/body/div[2]/div[6]/div[1]/div[2]/div[1]/div[1]/div/div[2]/dl/dd[1]').text
    print(price)
    type = browser.find_element(By.XPATH, '//*[@id="ctrldiv"]/div[6]/div[1]/div[2]/div[1]/div[1]/div/div[2]/dl/dd[2]').text
    print(type)
    rooms = browser.find_element(By.XPATH, '//*[@id="ctrldiv"]/div[6]/div[1]/div[2]/div[1]/div[1]/div/div[2]/dl/dd[3]').text
    print(rooms)
    bolig_areal = browser.find_element(By.XPATH, '//*[@id="ctrldiv"]/div[6]/div[1]/div[2]/div[1]/div[1]/div/div[2]/dl/dd[4]').text
    print(bolig_areal)

    cleaned_price = int(price.replace(".", "").split()[0])
    cleaned_bolig_areal = int(bolig_areal.split()[0])
    
    kvm_pris = int(cleaned_price)/int(cleaned_bolig_areal)    
    print(f'Kvadratmeter pris for dette hus er: {kvm_pris}')

    grund_areal = browser.find_element(By.XPATH, '//*[@id="ctrldiv"]/div[6]/div[1]/div[2]/div[1]/div[1]/div/div[2]/dl/dd[5]').text
    print(grund_areal)
    bygge_år = browser.find_element(By.XPATH, '//*[@id="ctrldiv"]/div[6]/div[1]/div[2]/div[1]/div[1]/div/div[2]/dl/dd[6]').text
    print(bygge_år)
    internet_hastighed = browser.find_element(By.XPATH, '//*[@id="ctrldiv"]/div[6]/div[1]/div[2]/div[1]/div[1]/div/div[2]/dl/dd[8]').text
    print(internet_hastighed)
    energi_mærke = browser.find_element(By.XPATH, '/html/body/div[2]/div[6]/div[1]/div[2]/div[22]/div/div[2]/div/div[1]/p[1]').text
    regex_pattern = r"energimærke\s*(A2020|A2015|A2010|A|B|C|D|E|F|G)"
    match = re.search(regex_pattern, energi_mærke)
    if match:
        energimærke = match.group(1)
        print(energimærke)
    else:
        print("Energimærke blev ikke fundet.")
        energimærke = ""


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Vil hente data fra dit valgte fra dinGeo på huse til salg")
    parser.add_argument("postnr", help="Dansk postnr du vil scrappe huse fra")

    args = parser.parse_args()

    if not args.postnr:
        print("Indtast venligst postnr.")
    else:
        print("Behandler.")
        house_data_scrape(args.postnr)