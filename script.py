from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
import os

URL = "https://apps.urv.cat/Fitxar/Inici.do"
HOLIDAYS_FILE = "holidays.txt"

USERNAME = os.getenv("CLOCK_IN_USERNAME")
PASSWORD = os.getenv("CLOCK_IN_PASSWORD")

def is_holiday(today):
    try:
        with open(HOLIDAYS_FILE, "r") as f:
            holidays = {line.strip() for line in f}
        return today in holidays
    except FileNotFoundError:
        print(f"The file {HOLIDAYS_FILE} does not exist. Proceeding with clock-in.")
        return False

def main():
    today = datetime.date.today().strftime("%Y-%m-%d")
    
    print("Checking if today is a holiday")
    if is_holiday(today):
        print(f"Today ({today}) is a holiday. Clock-in will not be performed.")
        return
    print(f"Today ({today}) is not a holiday. Proceeding with clock-in.")
    
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--remote-debugging-port=9222')
    
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get(URL)
    
        if driver.title == "SSO URV Login":
            print("Logging in")
            driver.find_element(By.ID, "username").send_keys(USERNAME)
            driver.find_element(By.ID, "password").send_keys(PASSWORD, Keys.RETURN)
            time.sleep(2)
    
        print("Loaded page '{}'".format(driver.title))
    
        # Save the page state before clicking for checking if the page has changed
        page_state_before = driver.page_source
    
        # Click the "Fitxar" button
        driver.find_element(By.XPATH, '//input[@value="Fitxar"]').click()
    
        # Wait for the page to change
        WebDriverWait(driver, 3).until(lambda d: d.page_source != page_state_before)
    
        print("Loaded page '{}'".format(driver.title))
    
        print("Clock-in successful")
    
    except Exception as e:
        print("An error occurred: ", e)
    
    finally:
        driver.quit() 
        print("Driver closed successfully")



if __name__ == "__main__":
    main()
