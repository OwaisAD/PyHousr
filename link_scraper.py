from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import csv
import time
import argparse
from accept_terms import accept_terms


browser = webdriver.Firefox()
browser.get('https://www.dingeo.dk')
time.sleep(2)

accept_terms(browser)

def scrape_links(postnr):
    try:
        browser.get(f'https://www.dingeo.dk/salg/#?postnr={postnr}')
        
        time.sleep(8)

        # Find knappen "Hent flere" og klik på den       
        hent_flere_knap = browser.find_element(By.XPATH, '/html/body/div[5]/div/div/div/div/div[3]/div/div/div[13]/div/div[1]/a')
        time.sleep(3)

        hent_flere_knap.click()

        last_height = browser.execute_script('return document.body.scrollHeight')

        # Scroll nedad gentagne gange for at indlæse yderligere data
        while True:
            # Scroll nedad ved hjælp af JavaScript
            browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            
            # Vent lidt for at give tid til at indlæse data
            time.sleep(7)

            new_height = browser.execute_script('return document.body.scrollHeight')

            if new_height == last_height:
                break
            last_height = new_height

        time.sleep(3)

        elements = browser.find_elements(By.XPATH, '//div[@class="ng-scope"]/a')
        href_values = [element.get_attribute('href') for element in elements]

        if not href_values:
            raise Exception('No links found')

        links = set()

        for href in href_values:
            links.add(href)


        with open(f'data_{postnr}.csv', 'w',newline='') as file:
            writer = csv.writer(file)
            for link in links:
                if link != f'https://www.dingeo.dk/salg/kort/#?postnr={postnr}':
                    writer.writerow([link.rstrip(',')])
    except NoSuchElementException:
    # Handling the error
        print("Postnummeret findes ikke")
    except Exception as e:
        print(e)

    browser.quit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Vil hente links fra dinGeo på huse til salg")
    parser.add_argument("postnr", help="Dansk postnr du vil scrappe")

    args = parser.parse_args()

    if not args.postnr:
        print("Indtast venligst postnr.")
    else:
        print("Behandler.")
        scrape_links(args.postnr)
