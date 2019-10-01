import re
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import chromedriver_binary
from selenium.webdriver.support.ui import WebDriverWait

print("start new")
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--headless')
options.add_argument('--disable-dev-shm-usage')
d = DesiredCapabilities.CHROME
d['goog:loggingPrefs'] = { 'performance':'ALL' }
browser = webdriver.Chrome(desired_capabilities=d, options=options)
browser.implicitly_wait(60)
browser.set_page_load_timeout(60)
browser.get('https://www.google-analytics.com/analytics.js')
WebDriverWait(browser, 60).until(lambda driver: driver.execute_script("return document.readyState == 'complete'"))
total_bytes = []
newtwork_logs = []
newtwork_logs = browser.execute_script("var network = performance.getEntries() || {}; return network;")
print(newtwork_logs)
print("--------------------------------------------------")
for entry in newtwork_logs:
  if "transferSize" in str(entry):
    r = re.search(r"transferSize\':(.*?),", str(entry))
    total_bytes.append(int(r.group(1)))
print("transferSize: %s", str(sum(total_bytes1)))
#logs = browser.get_log('performance')
#for entry in browser.get_log('performance'):
#        if "encodedDataLength" in str(entry):
#            r = re.search(r"encodedDataLength\':(.*?),", str(entry))
#            total_bytes.append(int(r.group(1)))
#print("encodedDataLength: ", str(sum(total_bytes)))

browser.save_screenshot("screenshot.png")
browser.close()
browser.quit()
