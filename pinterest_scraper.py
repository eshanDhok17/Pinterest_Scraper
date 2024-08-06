import os
import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
username = input("Enter username: ")
board_name = input("Enter boardname: ")


url = f'https://in.pinterest.com/{username}/{board_name}/'

response = requests.get(url)



print(response.status_code)

soup = BeautifulSoup(response.content, 'html.parser')



def download_image(url, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            file_name = os.path.join(folder, url.split('/')[-1])
            with open(file_name, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded {file_name}")
            
    except Exception as e:
        print(f"download failed {url}: {e}")





time.sleep(3)

images = soup.find_all("img")

print('start')

time.sleep(2)

file = open('img.txt', 'w')
driver.get(url)
time.sleep(2)

# Wait for the element to be present
div_element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'div.vbI.XiG'))
)

# Get the height of the div element using JavaScript
div_height = driver.execute_script("return arguments[0].offsetHeight;", div_element)

# Scroll to the specified height
driver.execute_script(f"window.scrollTo(0, {div_height});")

for image in images:
    img_url = image.get("src")
    if img_url and img_url[8:9] != 's':
        original_img_url = img_url.replace(img_url.split("/")[3], "originals")
        file.write(original_img_url + "\n")
        
        download_image(original_img_url, "output")
        time.sleep(2)

print('end')
