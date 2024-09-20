"""https://orteil.dashnet.org/cookieclicker/"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import time 

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://orteil.dashnet.org/cookieclicker/")

cookie_id = "cookies"

# TO CHOOSE THE LANGUAGE ENG
WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.XPATH, "//*[@id='langSelect-EN']"))
)
language = driver.find_element(By.XPATH, "//*[@id='langSelect-EN']")
language.click()

# TO CLICK ON THE COOKIE
WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.ID, "bigCookie"))
)
cookie = driver.find_element(By.ID, "bigCookie")

# Function to handle clicking the cookie
def click_cookie():
    global cookie  # Use the global cookie reference
    for attempt in range(5):  # Retry up to 5 times
        try:
            cookie.click()  # Try to click the cookie
            break  # Exit loop if successful
        except StaleElementReferenceException:
            print("Cookie element is stale, retrying...")
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.ID, "bigCookie"))
            )
            cookie = driver.find_element(By.ID, "bigCookie")  # Re-find the cookie

# TO PRINT COOKIE-CLICKS NUMBERS
while True:
    click_cookie()  # Call the function to click the cookie safely
    cookies_count = driver.find_element(By.ID, cookie_id).text.split(" ")[0]
    print(cookies_count)

time.sleep(40)
