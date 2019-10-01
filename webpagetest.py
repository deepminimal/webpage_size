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
browser.set_window_size(1920, 1080)
browser.get('https://ostin.com/')
WebDriverWait(browser, 60).until(lambda driver: driver.execute_script("return document.readyState == 'complete'"))
total_bytes = []
newtwork_logs = []
newtwork_logs = browser.execute_script("var network = performance.getEntries() || {}; return network;")
for entry in newtwork_logs:
  if "transferSize" in str(entry):
    r = re.search(r"transferSize\':(.*?),", str(entry))
    if (int(r.group(1)) == 0):
      r = re.search(r"transferSize\':(.*?),", str(entry))
      total_bytes.append(
    total_bytes.append(int(r.group(1)))
print("transferSize: ", str(sum(total_bytes)))
total_bytes = []
browser_preformance_log = browser.get_log('performance')
for entry in browser_preformance_log:
        if "Network.loadingFinished" in str(entry):
            r = re.search(r'encodedDataLength\":(.*?),', str(entry))
            total_bytes.append(int(r.group(1)))
print("encodedDataLength: ", str(sum(total_bytes)))
with open('/usr/share/zabbix/newtwork_logs.json', 'w') as outfile:
    json.dump(newtwork_logs, outfile)
with open('/usr/share/zabbix/browser_preformance_log.json', 'w') as outfile:
    json.load(browser_preformance_log, outfile)
#browser.save_screenshot("/usr/share/zabbix/screenshot.png")
#browser.find_element_by_tag_name('body').screenshot("/usr/share/zabbix/screenshot2.png")
browser.close()
browser.quit()
