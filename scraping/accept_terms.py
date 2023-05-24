from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

def accept_terms(browser):
    try:
        # Find allow_all_button, this has an Id, which is used in find_element By:ID
        allow_all_button = browser.find_element(By.ID,"CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll")
        time.sleep(2)
        allow_all_button.click()
        print("Conditions were accepted")
    except NoSuchElementException:
        print("It weren't necessary to accept conditions")