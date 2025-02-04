from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options 

options = Options()
options.headless = True
options.binary_location = './chrome-linux64/chrome'
service = Service('./chromedriver-linux64/chromedriver')

driver = webdriver.Chrome(service=service, options=options)
driver.get('http://127.0.0.1:8000') # URL that selenium scrapes

print(driver.page_source)

driver.quit()