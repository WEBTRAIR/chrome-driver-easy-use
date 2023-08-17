from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import sys
import os
#import glob
import time
from datetime import datetime
sys.path.append('../')
from chrome_driver_easy_use import ChromeDriverEasyUse, include_path

#def resource_path(relative_path):
#    try:
#        base_path = sys._MEIPASS
#    except Exception:
#        base_path = os.path.dirname(__file__)
#    return os.path.join(base_path, relative_path)

driver_path = include_path('../include_files/py.exe')
#driver_path = resource_path('../include_files/chromedriver.exe')

# Except
#try:
    
cdeu = ChromeDriverEasyUse()
cdeu.intialize(driver_path = None,
                wait_sec = 30,
                dl_path='C:\\Users\\{}\\Desktop\\dl'.format(os.getlogin()))

cdeu.driver.maximize_window()
cdeu.driver.get('https://google.com')

# 検索ボックスの入力
# Chrome、Google側のアップデートにより、以下のCSS_SELECTORで検索ボックスを見つけられないことがある。
cdeu.send_keys(By.CSS_SELECTOR, 'textarea[aria-label="検索"]', '情報通信白書')
cdeu.send_keys(By.CSS_SELECTOR, 'textarea[aria-label="検索"]', Keys.ENTER)

# 検索結果の一番上をクリック
cdeu.click(By.CSS_SELECTOR, 'h3')
#cdeu.click(By.CSS_SELECTOR, '#rso > div:nth-child(1) > div > div > div > div > div > div > div:nth-child(1) > a > h3')


# 「情報通信白書令和4年版 PDF版」をクリック
cdeu.click(By.CSS_SELECTOR, '#container > table:nth-child(2) > tbody > tr > td > table > tbody > tr:nth-child(3) > td > table > tbody > tr > td:nth-child(5) > table > tbody > tr:nth-child(18) > td > a')



n=0
while n < 3:
    n+=1
    cdeu.clear_temp_dir()
    time.sleep(5)
    # ■　ダウンロードアクション
    # 「本編【全体】(16.7MB)」をクリック
    cdeu.click(By.CSS_SELECTOR, '#contents > div > table:nth-child(5) > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(1) > td > div > a')

    dled_filepath = cdeu.download(filename_format='*pdf', timeout_sec=60)
    
    if dled_filepath:
        cdeu.move_to_save_path(dled_filepath[0],"C:\\Users\\info\\git\\chrome-driver-easy-use\\tests\\save\\{}.pdf".format(datetime.strftime(datetime.now(), '%y%m%d-%H%M%S')))
        break
    
    #再試行する前に待機
    print('[ retry ] 再試行待機中')
    time.sleep(30)
    print('[ retry ] 再試します')

cdeu.driver.close()

#except:
#    pass