# selenium 4
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver_wait = WebDriverWait(driver, 30)

driver.maximize_window()
driver.get('https://google.com')

#element:WebElement= driver_wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'textarea[aria-label="検索"]')))
#element.send_keys("aaaaaa")

element = driver.find_element(By.CSS_SELECTOR, 'textarea[aria-label="検索"]')
element.send_keys("aaaaaa")