from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

def accept_terms(browser):
    try:
        
        #Find tillad_alt_knap, denne har et Id, så der bruges find_element By:ID
        allow_all_button = browser.find_element(By.ID,"CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll")
        time.sleep(2)
        allow_all_button.click()
        print("Vilkår er blevet accepteret")
    except NoSuchElementException:
        print("Det var ikke nødvendigt at acceptere vilkår")

