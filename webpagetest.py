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
print("start WebDriverWait")
print("last height")
last_height = browser.execute_script("return document.body.scrollHeight")
print(last_height)
while True:
  browser.execute_script("window.scrollTo(0, document.body.scrollHeight-1000);")
  # Wait to load the page.
  browser.implicitly_wait(30) # seconds
  new_height = browser.execute_script("return document.body.scrollHeight")
  if new_height == last_height:
    break
  last_height = new_height
    # sleep for 30s
  browser.implicitly_wait(30) # seconds
print("new height")
print(browser.execute_script("return document.body.scrollHeight"))
#browser.execute_script("window.scrollTo(0, 3000);")
WebDriverWait(browser, 60).until(lambda driver: driver.execute_script("return document.readyState == 'complete'"))
print("end WebDriverWait")
total_bytes = []
counter = 0
count = 0
for entry in browser.get_log('performance'):
  if "Network.requestWillBeSent" in str(entry):
    count += 1
    if (count == 1):
      print(str(entry))
  if "Network.dataReceived" in str(entry):
    print(str(entry))
    r = re.search(r'encodedDataLength\":(.*?),', str(entry))
    total_bytes.append(int(r.group(1)))
    mb = round((float(sum(total_bytes) / 1000) / 1000), 2)
print(str(sum(total_bytes)))
browser.save_screenshot("screenshot.png")
browser.close()
driver.quit()
