from selenium import webdriver
import time
from accept_terms import accept_terms

browser = webdriver.Firefox()
browser.get('https://www.dingeo.dk')
time.sleep(2)

accept_terms(browser)




browser.get('https://www.dingeo.dk/adresse/2800-kongens%20lyngby/gammel%20bagsv%C3%A6rdvej-24f/2-th/')
time.sleep(4)

browser.save_screenshot('screenshot.png')