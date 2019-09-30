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
WebDriverWait(browser, 50).until(lambda x: 'STIN' in browser.title)
logs = browser.execute('getLog', {'type': 'performance'})['value']
re_encdatalen = re.compile(r'.*encodedDataLength":(-?[0-9]+),.*$')
loading_finished = [l['message'] for l in logs if
                        'INFO' == l['level'] and 'Network.loadingFinished' in l['message']]
#lf_enc_data_len = [int(re_encdatalen.match(m)[1]) for m in loading_finished]
lf_enc_data_len = 0
for m in loading_finished:
  x = re.findall(r'.*"encodedDataLength":([0-9]+),', m)
  lf_enc_data_len += int(x[0])

print(str(lf_enc_data_len))
sizes = browser.execute_script("""
  return performance.getEntries()
    .filter(e => e.entryType==='navigation' || e.entryType==='resource')
    .map(e=> ([e.name, e.transferSize]));
  """)
print(str(sizes))
size = browser.execute_script("""
  return performance.getEntries()
    .filter(e => e.entryType==='navigation' || e.entryType==='resource')
    .reduce((acc, e) => acc + e.transferSize, 0)
  """)
print(str(sizes))
browser.close()
