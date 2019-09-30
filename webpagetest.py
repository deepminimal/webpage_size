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
browser.implicitly_wait(30)
browser.set_page_load_timeout(30)
print("start get")
browser.get('https://ostin.com')
#WebDriverWait(browser, 60).until(lambda driver: driver.execute_script("return document.readyState == 'complete'"))
total_bytes = []
total_bytes2 = []
total_bytes3 = []
total_bytes4 = []
counter = 0
count = 0

newtwork_logs = []
newtwork_logs = browser.execute_script("var network = performance.getEntries() || {}; return network;")
for entry2 in newtwork_logs:
  if "encodedBodySize" in str(entry2):
    #count += 1
    #if (count == 1):
      #print(entry2)
    r3 = re.search(r"encodedBodySize\':(.*?),", str(entry2))
    total_bytes3.append(int(r3.group(1)))
print("encodedBodySize: %s", str(sum(total_bytes3)))
for entry in browser.get_log('performance'):
        if "Network.loadingFinished" in str(entry):
            print(str(entry))
            r = re.search(r'encodedDataLength\":(.*?),', str(entry))
            #r2 = re.search(r'headersText\":(.*?),', str(entry))
            total_bytes.append(int(r.group(1)))
            #total_bytes2.append(int(r2.group(1)))
print("encodedDataLength: ", str(sum(total_bytes)))
print("headersText: ", str(sum(total_bytes2)))
print("Transferred size: ", str(sum(total_bytes2)-sum(total_bytes)))
browser.save_screenshot("screenshot.png")
browser.close()
browser.quit()
