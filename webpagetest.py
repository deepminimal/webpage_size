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

def page_has_loaded(self):
    print("URL=%s", str(driver.current_url))
    page_state = self.driver.execute_script('return document.readyState;')
    return page_state == 'complete'

WebDriverWait(browser, 50).until(page_has_loaded(browser))
#logs = browser.execute('getLog', {'type': 'performance'})['value']
#re_encdatalen = re.compile(r'.*encodedDataLength":(-?[0-9]+),.*$')
#loading_finished = [l['message'] for l in logs if
#                        'INFO' == l['level'] and 'Network.loadingFinished' in l['message']]
#lf_enc_data_len = [int(re_encdatalen.match(m)[1]) for m in loading_finished]
#lf_enc_data_len = 0
#for m in loading_finished:
#  x = re.findall(r'.*"encodedDataLength":([0-9]+),', m)
#  lf_enc_data_len += int(x[0])

total_bytes = []
for entry in browser.get_log('performance'):
        if "Network.dataReceived" in str(entry):
            r = re.search(r'encodedDataLength\":(.*?),', str(entry))
            total_bytes.append(int(r.group(1)))
            mb = round((float(sum(total_bytes) / 1000) / 1000), 2)
print(str(sum(total_bytes)))
browser.close()
