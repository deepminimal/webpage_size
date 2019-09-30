from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import chromedriver_binary

options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--headless')
options.add_argument('--disable-dev-shm-usage')
d = DesiredCapabilities.CHROME
d['goog:loggingPrefs'] = { 'performance':'ALL', 'detach': False }


browser = webdriver.Chrome(desired_capabilities=d, options=options)
browser.get('https://automatetheboringstuff.com')
logs = browser.execute('getLog', {'type': 'performance'})['value']
print(logs)
browser.close()
