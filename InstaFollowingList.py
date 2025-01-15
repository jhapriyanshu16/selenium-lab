from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

scraped_data = {
    "Username":[],
    "Profile Name":[]
}

s = Service("C:/Users/priya/Downloads/chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service=s)
# Open a website
driver.get("https://www.instagram.com/")

username = None
pwd = None

login_input = driver.find_element(By.XPATH,"""//*[@id="loginForm"]/div[1]/div[1]/div/label/input""")
pwd_input = driver.find_element(By.XPATH,"""//*[@id="loginForm"]/div[1]/div[2]/div/label/input""")
login_btn = driver.find_element(By.XPATH,"""//*[@id="loginForm"]/div[1]/div[3]""")

element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """//*[@id="loginForm"]/div[1]/div[3]""")))
login_input.click()
login_input.send_keys(username)
pwd_input.click()
pwd_input.send_keys(pwd)
time.sleep(1)
login_btn.click()

not_now_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and text()='Not now']"))
)
not_now_button.click()
profile_link = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, f"//a[@href='/{username}/']"))
)
profile_link.click()
following_link = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, f"//a[@href='/{username}/following/']"))
)
following_link.click()
following_btn = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, """//div[@class='_ap3a _aaco _aacw _aad6 _aade' and text()='Following']"""))
)
following_popup = driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]')

for _ in range(30): 
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", following_popup)
    time.sleep(2) 
following_list = driver.find_elements(By.XPATH, "//span[@class='_ap3a _aaco _aacw _aacx _aad7 _aade' and @dir='auto']")
following_name_list = driver.find_elements(By.XPATH,"//span[@class='x1lliihq x1plvlek xryxfnj x1n2onr6 x1ji0vk5 x18bv5gf x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye xvs91rp xo1l8bm x1roi4f4 x10wh9bi x1wdrske x8viiok x18hxmgj' and @dir = 'auto' and @style = '----base-line-clamp-line-height: 18px; --lineHeight: 18px;']")
print("Following list length ",len(following_list))
print("Following name list length ",len(following_name_list))

for usrname in following_list:
    scraped_data.get("Username").append(usrname.text.strip())

for index,pname in enumerate(following_name_list):
    if(index==0):
        continue
    scraped_data.get("Profile Name").append(pname.text.strip())

 
driver.quit()

df = pd.DataFrame(scraped_data)
df.to_excel('insta.xlsx')

print(scraped_data)