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

print("start browser")
browser = webdriver.Chrome(desired_capabilities=d, options=options)
browser.implicitly_wait(60)
browser.set_page_load_timeout(60)
print("start get")
browser.get('https://www.google-analytics.com/analytics.js')
WebDriverWait(browser, 60).until(lambda driver: driver.execute_script("return document.readyState == 'complete'"))
total_bytes = []
total_bytes2 = []
total_bytes3 = []
total_bytes4 = []
counter = 0
count = 0
#decodedBodySize - size resources

newtwork_logs = []
newtwork_logs = browser.execute_script("var network = performance.getEntries() || {}; return network;")
print(newtwork_logs)
print("--------------------------------------------------")
for entry2 in newtwork_logs:
  if "transferSize" in str(entry2):
    #count += 1
    #if (count == 1):
      #print(entry2)
    r3 = re.search(r"transferSize\':(.*?),", str(entry2))
    total_bytes3.append(int(r3.group(1)))
print("transferSize: %s", str(sum(total_bytes3)))
logs = browser.get_log('performance')
mb = 0
for entry in browser.get_log('performance'):
        if "Network.dataReceived" in str(entry):
            r = re.search(r'encodedDataLength\":(.*?),', str(entry))

            total_bytes.append(int(r.group(1)))

print(logs)

print("encodedDataLength: ", str(sum(total_bytes)))

browser.save_screenshot("screenshot.png")
browser.close()
browser.quit()
