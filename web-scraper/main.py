from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.by import By

# Configure Selenium options
options = Options()
options.headless = True
options.binary_location = './chrome-linux64/chrome'
service = Service('./chromedriver-linux64/chromedriver')

# Initialize WebDriver
driver = webdriver.Chrome(service=service, options=options)

# Open the target webpage
driver.get('http://192.168.8.128:8000')

# Extract product names and prices
products = driver.find_elements(By.CLASS_NAME, "card-body")

for product in products:
    name_element = product.find_element(By.TAG_NAME, "h5")
    price_element = product.find_element(By.TAG_NAME, "strong")
    
    product_name = name_element.text if name_element else "Unknown"
    product_price = price_element.text if price_element else "Unknown"
    
    print(f"{product_name}: {product_price}")

# Close the WebDriver
driver.quit()
