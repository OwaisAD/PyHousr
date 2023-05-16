from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import requests
from lxml import etree
import time


driver = webdriver.Firefox()
driver.get('https://www.dingeo.dk')

time.sleep(2.24)

# # Find og klik på "Tillad alle" knappen
# tillad_alle = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
 
# tillad_alle.click()






# # Vent i 5 sekunder, indtil siden indlæses fuldt ud
# time.sleep(5)

# # Naviger til en anden URL efter at have accepteret vilkårene
# driver.get('https://www.boligsiden.dk/postnummer/2800/tilsalg/villa?sortAscending=true')


# Vent i 5 sekunder, indtil siden indlæses fuldt ud
# time.sleep(5)





# # Hent HTML-indholdet fra elementet
# html = element.get_attribute('innerHTML')

# # Opret en BeautifulSoup-instans og analyser HTML-indholdet
# soup = BeautifulSoup(html, 'html.parser')

# # Find alle boliger på siden
# boliger = soup.select('.address')

# # Loop igennem de første 5 boliger og udtræk data
# for bolig in boliger[:5]:
#     adresse = bolig.text.strip()
#     print('Adresse:', adresse)
#     # Udtræk yderligere data om boligen efter behov

# Luk driveren
#driver.quit()

url = "https://www.boligsiden.dk/postnummer/2800/tilsalg/villa"
webpage = requests.get(url)
soup = BeautifulSoup(webpage.content, "html.parser")
dom = etree.HTML(str(soup))

for i in range(100):
    path = f'/html/body/div[1]/div[1]/main/div/div[3]/div[1]/div/div[2]/div[{i}]/div/div[1]/div[2]/div/div[1]/text()'
    print(dom.xpath(path))
    energimaerke = dom.xpath(f'/html/body/div[1]/div[1]/main/div/div[3]/div[1]/div/div[2]/div[1]/div/div[1]/div[2]/div/div[2]/div/svg/title')
    print(energimaerke)





# energimaerker = dom.xpath('//*[@id="Lag_1"]/title')
# adresser = dom.xpath(path)

# print(len(energimaerker))
# for energim in energimaerker:
#     print(energim.text)