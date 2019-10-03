from browsermobproxy import Server
from selenium import webdriver
import os
import json
import urlparse
import re

server = Server("/home/work/webpage_size/browsermob-proxy-2.1.4/bin/browsermob-proxy")
server.start()
proxy = server.create_proxy()


chromedriver = "./chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
url = urlparse.urlparse (proxy.proxy).path
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--proxy-server={0}".format(url))
driver = webdriver.Chrome(chromedriver,chrome_options =chrome_options)
driver.set_window_size(1920, 1080)
proxy.new_har("https://ostin.com", options={'captureHeaders': True, 'captureContent':True, 'captureBinaryContent':True})
driver.get("https://ostin.com")    
S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
total_bytes = []
result = proxy.har
#json.dumps(proxy.har, ensure_ascii=True)
end = 0
print(type(result))

for x, y in result.items():
  print(x)
x = result.keys()
print(x)
for entry in result:
        if "bodySize" in str(result[entry]):
            r = re.search(r'bodySize\":(.*?),', str(result[entry]))
            try:
              total_bytes.append(int(r.group(1)))
            except:
              print("No found")
print("bodySize: ", str(sum(total_bytes)))

with open('/usr/share/zabbix/result.json', 'w') as outfile:
  outfile.write(json.dumps(proxy.har, ensure_ascii=True))

driver.save_screenshot("/usr/share/zabbix/screenshot.png")
proxy.stop()    
driver.quit()