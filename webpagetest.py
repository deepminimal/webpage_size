import re
import json
import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import chromedriver_binary
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import bs4 as bs

print("start new")
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--headless')

#options.add_argument('--disable-dev-shm-usage')
d = DesiredCapabilities.CHROME
d['goog:loggingPrefs'] = { 'performance':'ALL' }
browser = webdriver.Chrome(desired_capabilities=d, options=options)
browser.set_page_load_timeout(120)
browser.maximize_window()
browser.set_window_size(1920, 1080)
browser.get('https://ostin.com')
browser.implicitly_wait(60)
wait_time = 0

#WebDriverWait(browser, 60).until(lambda driver: driver.execute_script("return document.readyState == 'complete'"))
browser.execute_script("window.scrollTo(0, 5000);")
#WebDriverWait(browser, 60).until(EC.visibility_of_all_elements_located(By.CLASS_NAME, 'o-footer-contacts-social__container')))
WebDriverWait(browser,30).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "o-footer-contacts-social__container")))
network_logs = browser.execute_script("return window.performance.getEntries();")
total_bytes = []
total_bytes2 = []
total_bytes3 = []
for entry in network_logs:
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
with open('/usr/share/zabbix/network_logs.json', 'w') as outfile:
    json.dump(network_logs, outfile)
    
browser_preformance_log_clean = json.dumps(str(browser_preformance_log).replace('\"','"'))
with open('/usr/share/zabbix/browser_preformance_log.json', 'w') as outfile:
    outfile.write(browser_preformance_log_clean)

browser.execute_script("window.scrollTo(0, 2000);")
browser.save_screenshot("/usr/share/zabbix/screenshot.png")
browser.execute_script("window.scrollTo(0, 3000);")
browser.save_screenshot("/usr/share/zabbix/screenshot2.png")
browser.execute_script("window.scrollTo(0, 4000);")
browser.save_screenshot("/usr/share/zabbix/screenshot3.png")
browser.close()
browser.quit()
os.system("pkill -9 -f chrom")
