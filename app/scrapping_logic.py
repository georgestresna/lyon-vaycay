import re
import time
import random

from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from app.time_mngmt import str2hour

def init_driver():
    options = Options()
    # options.add_argument("--headless") # Commented out for visual debugging
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    # options.add_argument("--window-size=1920,1080")
    # Avoid detection
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Remote(
        command_executor='http://localhost:4444/wd/hub', 
        options=options
    )
    return driver

def trip_details(driver, url):

    wait = WebDriverWait(driver, 5)
    driver.get(url)
    wait.until(EC.element_to_be_clickable(driver.find_element(By.TAG_NAME, 'body')))
    time.sleep(3)

    listings_today = driver.find_element(By.XPATH, '//*[@id="content"]/div[1]/div[1]/div[2]/div/figure[1]/ul').find_elements(By.TAG_NAME, 'li')
    # listings_tomorrow = driver.find_element(By.XPATH, '//*[@id="content"]/div[1]/div[1]/div[2]/div/figure[2]/ul').find_elements(By.TAG_NAME, 'li')
    # de implementat mai tarziu si pentru cele peste miezu noptii

    departure_list=[]

    for listing in listings_today:
        # time.sleep(999)
        wait.until(EC.presence_of_element_located(listing.find_element(By.XPATH, ".//div[2]/div[1]/div/div/div[1]/div/div[1]/span[2]")))
        time.sleep(random.random())
        departure_hour = listing.find_element(By.XPATH, ".//div[2]/div[1]/div/div/div[1]/div/div[1]/span[2]").get_attribute('innerHTML')

        wait.until(EC.presence_of_element_located(listing.find_element(By.XPATH, ".//div[2]/div[1]/div/div/div[2]/div/span/span[2]")))
        destination_hour = listing.find_element(By.XPATH, ".//div[2]/div[1]/div/div/div[2]/div/span/span[2]").get_attribute('innerHTML')

        wait.until(EC.presence_of_element_located(listing.find_element(By.XPATH, ".//div[2]/div[1]/div/div/div[1]/div/div[2]/div/span[2]")))
        duration_raw = listing.find_element(By.XPATH, ".//div[2]/div[1]/div/div/div[1]/div/div[2]/div/span[2]").get_attribute('innerHTML')
        
        wait.until(EC.presence_of_element_located(listing.find_element(By.XPATH, ".//div[2]/div[1]/button/span/div/span")))
        price_raw = listing.find_element(By.XPATH, ".//div[2]/div[1]/button/span/div/span").get_attribute('innerHTML')
        
        price_pieces = re.split(r'[<,>]',price_raw)

        price = int(price_pieces[0]) + int(price_pieces[3])/100
        duration = re.split( r'[ ]', duration_raw.strip())[0]
        departure_hour = str2hour(departure_hour)
        destination_hour = str2hour(destination_hour)

        trip_data = {
            "departure": departure_hour,
            "arrival": destination_hour,
            "price": price,
            "duration": duration,
            "next_day_arr": bool(destination_hour < departure_hour)
        }

        departure_list.append(trip_data)
    
    return departure_list
