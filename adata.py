import pytesseract
from pytesseract import image_to_string 
from PIL import Image
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import os
import sys
import time
import csv

surveylist=['170/5','191/1','170/5']
def get_captcha_text(location, size):
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
    im = Image.open('screenshot.png') # uses PIL library to open image in memory

    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']


    im = im.crop((left, top, right, bottom)) # defines crop points
    im.save('screenshot.png')
    captcha_text = image_to_string(Image.open('screenshot.png'))
    return captcha_text

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("user-data-dir=C:\\Users\\user\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 7")
DRIVER_PATH = r"C:\Users\user\Downloads\chromedriver_win32\chromedriver.exe"
driver = webdriver.Chrome(options=chrome_options,executable_path=DRIVER_PATH)
driver.maximize_window()
for i in surveylist:
    no=i.split('/')
    try:
        driver.get("https://eservices.tn.gov.in/eservicesnew/land/areg.html")
        driver.implicitly_wait(2)
        district = Select(driver.find_element('xpath','//*[@id="districtCode"]'))
        district.select_by_visible_text('Viluppuram')
        driver.implicitly_wait(2)
        taluk=Select(driver.find_element('xpath','//*[@id="talukCode"]'))
        taluk.select_by_visible_text('Vanur')
        driver.implicitly_wait(2)
        village=Select(driver.find_element('xpath','//*[@id="villageCode"]'))
        village.select_by_visible_text('Thirusitrampalam')
        driver.implicitly_wait(2)
        surveyno=driver.find_element('xpath','//*[@id="surveyNo"]')
        surveyno.send_keys(no[0]) 
        driver.find_element('xpath','//*[@id="auto_off"]/div[6]/div[3]/font[1]').click()
        driver.implicitly_wait(2)

        subno=Select(driver.find_element('xpath','//*[@id="subdivNo"]'))
        subno.select_by_visible_text(no[1])

        element = driver.find_element('xpath','//*[@id="captcha_name"]') 
        location = element.location
        size = element.size
        driver.save_screenshot('screenshot.png')
        captcha_text = get_captcha_text(location, size)
        captcha = driver.find_element('xpath','//*[@id="captcha"]')
        captcha.clear()
        captcha.send_keys(captcha_text)
        driver.find_element('xpath','//*[@wdf-id="id3"]').click()
        driver.implicitly_wait(2)
    except Exception as e:
        print("An exception occurred")
        print(e)
       

    data=[]
    for tr in driver.find_elements('xpath','/html/body/table/tbody/tr[8]/td/table/tbody/tr'):
        tds = tr.find_elements(By.TAG_NAME, 'td')
        for td in tds:
            data.append(td.text)
       
    data=data[1::2] 
    print(data)

    with open('eggs.csv', 'a', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(data)

   




           

