from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import sys
import os
import glob
import time
from datetime import datetime,timedelta
import chromedriver_binary
from bs4 import BeautifulSoup as bs4
import lxml

sys.path.append('../')
from chrome_driver_easy_use import ChromeDriverEasyUse,include_path

#driver_path = include_path('../include_files/chromedriver.exe')

cdeu = ChromeDriverEasyUse()
cdeu.intialize(driver_path='../include_files/py.exe',
               wait_sec = 30,
               dl_path='C:\\Users\\{}\\Desktop\\dl'.format(os.getlogin()))
                #profile = 'Profile 5')

cdeu.driver.maximize_window()
cdeu.driver.get('https://google.com')

html = cdeu.driver.page_source.encode('utf-8')
soup = bs4(html,'lxml')

# 検索ボックスの入力
element = cdeu.send_keys(By.CSS_SELECTOR, 'textarea[aria-label="検索"]', '情報通信白書')
cdeu.send_keys(By.CSS_SELECTOR, 'textarea[aria-label="検索"]', Keys.ENTER)

cdeu.driver.close()

