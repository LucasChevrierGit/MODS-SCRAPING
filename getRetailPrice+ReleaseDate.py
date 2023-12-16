from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)

# https://stockx.com/search/dunk?page=2

url = 'https://stockx.com/nike-kobe-6-protro-reverse-grinch' # /product id

driver.get(url)

html_content = driver.page_source


soup = BeautifulSoup(html_content, 'html.parser')

soup = soup.body
info = soup.find('div', {'data-component': 'ProductDetails'})

info = info.find('div', {'data-component': 'ProductTraits'}).text

index = info.find('Retail Price')
index2 = info.find('Release Date')


retailPrice = info[index + len('Retail Price$'):index2]
date = info[ index2 + len('Release Date'): index2 + len('Release Date$') + 9]

print(retailPrice, date)




# One of the Xpath list all product id in the page
#exercise_cards = driver.find_elements(By.XPATH, '/html/body')
#print(exercise_cards[0].text)
driver.quit()