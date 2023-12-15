#get browse query json file from https://stockx.com/search/dunk
import requests
import json
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)

# https://stockx.com/search/dunk?page=2
url = 'https://stockx.com/search/dunk'

driver.get(url)

html_content = driver.page_source

soup = BeautifulSoup(html_content, 'html.parser')

soup = soup.body
next_data_script = soup.find('script', {'id': '__NEXT_DATA__'}).text

jsonFile = json.loads(next_data_script)


stockx_device_id = jsonFile['props']['pageProps']['req']['stockx_device_id']
sessionId = jsonFile['props']['pageProps']['req']['sessionId']

print(stockx_device_id, sessionId)
with open('JSON/response/getID.json', 'w') as file:
    json.dump(jsonFile, file)


# One of the Xpath list all product id in the page
#exercise_cards = driver.find_elements(By.XPATH, '/html/body')
#print(exercise_cards[0].text)
driver.quit()