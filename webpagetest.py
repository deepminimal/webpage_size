import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import chromedriver_binary
from selenium.webdriver.support.ui import WebDriverWait

options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--headless')
options.add_argument('--disable-dev-shm-usage')
d = DesiredCapabilities.CHROME
d['goog:loggingPrefs'] = { 'performance':'ALL' }


browser = webdriver.Chrome(desired_capabilities=d, options=options)
browser.get('https://ostin.com')
WebDriverWait(browser, 60).until(lambda driver: driver.execute_script("return document.readyState == 'complete'"))
total_bytes = []
for entry in browser.get_log('performance'):
        if "Network.dataReceived" in str(entry):
            r = re.search(r'encodedDataLength\":(.*?),', str(entry))
            total_bytes.append(int(r.group(1)))
            mb = round((float(sum(total_bytes) / 1000) / 1000), 2)
print(str(sum(total_bytes)))
browser.close()
