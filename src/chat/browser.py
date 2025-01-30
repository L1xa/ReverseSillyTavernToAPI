from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from ..config import CHROME_PATH, CHROME_DRIVER_PATH

def create_browser():
    options = webdriver.ChromeOptions()
    options.binary_location = CHROME_PATH
    options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
    
    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    
    return driver 