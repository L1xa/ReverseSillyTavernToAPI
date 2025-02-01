from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from ..config import CHROME_PATH, CHROME_DRIVER_PATH
import os

def create_browser():
    options = webdriver.ChromeOptions()
    options.binary_location = CHROME_PATH
    options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
    
    # 添加抑制日志的选项
    options.add_argument('--log-level=3')  # 只显示致命错误
    options.add_argument('--silent')
    options.add_argument('--disable-logging')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    # 重定向错误输出
    if os.name == 'nt':  # Windows系统
        os.environ['WDM_LOG_LEVEL'] = '0'
    
    service = Service(CHROME_DRIVER_PATH, log_output=os.devnull)
    driver = webdriver.Chrome(service=service, options=options)
    
    return driver 