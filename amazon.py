from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

s = Service("C:/Users/priya/Downloads/chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service=s)

#Getting prices of a product from amazon
driver.get("https://www.amazon.in/")
try:
    WebDriverWait(driver,5).until(EC.presence_of_element_located((By.ID,"nav-logo"))) #Wait for max 10 sec until element with that id is located
    input_bar = driver.find_element(By.XPATH,"""//*[@id="twotabsearchtextbox"]""")  #finding elements with XPath
    input_bar.click() #clicking

    product = "electric kettle"
    input_bar.send_keys(product) #Giving input

    input_bar.send_keys(Keys.ENTER) #Using Keys from common.keys to simulate keyboard keys
    time.sleep(2)  #Waiting without using WebDriverWait
    prices = driver.find_elements(By.CLASS_NAME,"a-price-whole") #Finding elements by class name
    for price in prices:
        print(price.text)  #using .text to get the text of the element
    
finally:
    driver.close() #closes the driver even if exception is thrown


