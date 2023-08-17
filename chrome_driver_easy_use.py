from xml.dom.minidom import Element
from selenium import webdriver
#from webdriver_manager import driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from datetime import datetime, date, timedelta
from selenium.webdriver.chrome.service import Service as ChromeService
import time
import os
import sys
import glob
import re
import chromedriver_binary
from selenium.webdriver.chrome.options import Options
from pathlib import Path
import shutil
from webdriver_manager.chrome import ChromeDriverManager


# WARNING非表示
import warnings
warnings.filterwarnings('ignore')

#旧バージョン
#def include_path(filename):
#    if hasattr(sys, "_MEIPASS"):
#        return os.path.join(sys._MEIPASS, filename)
#    return os.path.join(filename)

def include_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

class ChromeDriverEasyUse():
    
    def __init__(self):
        self.include_path = ''
        self.driver = ''
        self.driver_wait = ''
        self.prefs = {}
        self.dl_path = '{}\\temp'.format(os.getcwd())
        self.save_path = '{}\\save'.format(os.getcwd())
        
    def intialize(self, driver_path:str, wait_sec=0, dl_path:str=None, profile=None):
        
        options = webdriver.ChromeOptions()
        #options = Options()
        if driver_path:
            options.binary_location
            chrome_service = ChromeService(executable_path = driver_path)

            
        
        #save_path
        if dl_path:
            self.dl_path = dl_path
            self.prefs['download.default_directory'] = self.dl_path
            #self.prefs['download.prompt_for_download'] = False
            #self.prefs['download.directory_upgrade'] = True
            
            # Options for downloading without opening the PDF
            # PDFを開かずに、ダウンロードするためのオプション
            self.prefs['plugins.plugins_disabled'] = ["Chrome PDF Viewer"]
            self.prefs['plugins.always_open_pdf_externally'] = True
    
        if self.prefs:
            options.add_experimental_option("prefs", self.prefs)
        
        #User Profile
        if profile:
            options.add_argument("--no-sandbox")
            options.add_argument('--user-data-dir=C:\\Users\\{}\\AppData\\Local\\Google\\Chrome\\User Data'.format(os.getlogin()))
            options.add_argument('--profile-directory={}'.format(profile))
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-infobars")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-gpu")
            options.binary_location ='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
        
        if driver_path:
            self.driver = webdriver.Chrome(service=chrome_service, options=options)
        else:
            #self.driver = webdriver.Chrome(service=ChromeDriverManager().install(), options=options)
            self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        self.driver_wait = WebDriverWait(self.driver, wait_sec)

    def click(self,type,selector):
        element = self.driver_wait.until(EC.visibility_of_element_located((type, selector)))   
        element.click()
        
    def send_keys(self, type, selector, value, clear:bool=None):
        element = self.driver_wait.until(EC.visibility_of_element_located((type, selector)))
        if clear:
            element.clear()
            element.send_keys(Keys.CONTROL + "a")
            element.send_keys(Keys.DELETE)
        element.send_keys(value)
        
    def dropdown(self, type, selector, value:str=None, option:str=None):
        dropdown = self.driver_wait.until(EC.visibility_of_element_located((type, selector)))

        if value:
            select = Select(dropdown)
            select.select_by_value(value)
            
        elif option:
            dropdown.find_element(By.XPATH, "//option[. = '"+ option +"']").click()
    
    def wait(self, type, selector):
        self.driver_wait.until(EC.visibility_of_element_located((type, selector)))
    
    #== Download ================================================
    # ダウンロードボタンを押下する前に実行する関数
    def clear_temp_dir(self):
        temp_dir_filelist = glob.glob(self.dl_path + '\\*' )
        if temp_dir_filelist :
            
            print('[  temp  ] tempフォルダにファイルが存在します。')
            for file in temp_dir_filelist:
                os.remove(file)
            
            print('[  temp  ] tempフォルダ内のファイルを削除しました。')
        

        print('[  temp  ] tempフォルダは空です。')

    # ダウンロードボタンを押下した後に実行する関数
    def download(self, filename_format:str='*', timeout_sec:int=60, save_path:str=None):
        start_at = datetime.now()
        timeout_at = start_at + timedelta(seconds=timeout_sec)

        while True:
            now_at = datetime.now()
            
            if now_at >= timeout_at:
                print('[timeout ] 時間内にダウンロードが完了しませんでした。')
                break
            
            elif glob.glob(self.dl_path + '\\' + filename_format):
                print('[ 1 / 2  ]ファイルのダウンロードが完了しました。')
                return glob.glob(self.dl_path + '\\' + filename_format)
                #break
            
    #　ダウンロードしたファイルを指定のパスへ変更
    def move_to_save_path(self, src_path:str, dst_path:str=None):
        
        if dst_path:
            
            # dst_pathのディレクトリが存在するか確認。存在しなければ作成、
            m = re.search('\S*(\\\)', dst_path)
            dst_dir = m.group()
            if not os.path.exists(dst_dir):
                os.mkdir(dst_dir)
            
            shutil.move(Path(src_path), Path(dst_path))
            #os.rename(src_path, dst_path)

        
        # dst_pathの指定がなかった場合はインスタンス変数のsave_pathに同じファイル名で保存
        else:
            # save_pathが存在しなければ作成
            if not os.path.exists(self.save_path):
                os.mkdir(self.save_path)
                
            m = re.findall('[^\\\]*', src_path)
            filename = m[-2]
            os.rename(src_path, self.save_path + '\\' + filename)
        
        print('[ 2 / 2  ]ファイルの移動(リネーム)が完了しました。')

