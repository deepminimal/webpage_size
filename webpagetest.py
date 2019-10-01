import re
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import chromedriver_binary
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

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
browser.set_window_size(1920, 1080)
browser.get('https://ostin.com')
WebDriverWait(browser, 60).until(lambda driver: driver.execute_script("return document.readyState == 'complete'"))
WebDriverWait(browser, 15).until(lambda driver: driver.execute_script("window.scrollTo(0, document.body.scrollHeight); return document.body.scrollHeight;"))
newtwork_logs = browser.execute_script("return window.performance.getEntries();")
try:
  WebDriverWait(driver, 30).until(ec.visibility_of_element_located((By.XPATH, "//a[@class='o-footer-legal-info__container']")));
except Exception as e:
  print(str(e))
total_bytes = []
total_bytes2 = []
total_bytes3 = []
newtwork_logs = []
print(len(newtwork_logs))
for entry in newtwork_logs:
  if "transferSize" in str(entry):
    r = re.search(r"transferSize\':(.*?),", str(entry))
    r2 = re.search(r"encodedBodySize\':(.*?),", str(entry))
    total_bytes2.append(int(r2.group(1)))
    total_bytes3.append(int(r.group(1)))
    if (int(r.group(1)) == 0):
      r2 = re.search(r"encodedBodySize\':(.*?),", str(entry))
      total_bytes.append(int(r2.group(1)))
    else:
      total_bytes.append(int(r.group(1)))
print("transferSize if not 0 + encodedBodySize  : ", str(sum(total_bytes)))
print("encodedBodySize only: ", str(sum(total_bytes2)))
print("transferSize only: ", str(sum(total_bytes3)))

total_bytes = []
browser_preformance_log = browser.get_log('performance')
for entry in browser_preformance_log:
        if "encodedDataLength" in str(entry):
            r = re.search(r'encodedDataLength\":(.*?),', str(entry))
            total_bytes.append(int(r.group(1)))
print("encodedDataLength: ", str(sum(total_bytes)))
with open('/usr/share/zabbix/newtwork_logs.json', 'w') as outfile:
    json.dump(newtwork_logs, outfile)
    
browser_preformance_log_clean = json.dumps(browser_preformance_log)
with open('/usr/share/zabbix/browser_preformance_log.json', 'w') as outfile:
    outfile.write(browser_preformance_log_clean)
file = open("/usr/share/zabbix/browser_preformance_log.json", "r") 
string = file.read() 
with open('/usr/share/zabbix/browser_preformance_log.json', 'w') as outfile:
    outfile.write(string.replace('\"', '"'))
browser.save_screenshot("/usr/share/zabbix/screenshot12.png")
browser.close()
browser.quit()
