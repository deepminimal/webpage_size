from browsermobproxy import Server
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import os
import json
import urlparse
import re
#dict = {'port': 3343}
server = Server("/home/work/webpage_size/browsermob-proxy-2.1.4/bin/browsermob-proxy")#, options=dict)
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
proxy.new_har("https://ostin.com/", options={'captureHeaders': True, 'captureContent':True, 'captureBinaryContent':True})
driver.get("https://ostin.com/")    
WebDriverWait(driver, 60).until(lambda driver: driver.execute_script("return document.readyState == 'complete'"))
S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
driver.set_window_size(S('Width'),S('Height')) # May need manual adjustment
result = json.dumps(proxy.har, ensure_ascii=True, indent=2)
r = re.findall(r'bodySize\":(.*?),', str(result))
var =0
for num in r:
  var = var + int(num)
print("bodySize: ", str(var))

r = re.findall(r'headersSize\":(.*?),', str(result))
print(tipe(r))
var1 =0
for num in r:
  var1 = var1 + int(num)
print("headersSize: ", str(var))
print("Without headersSize: ", str(var - var1))
#r = re.findall(r'url\":(.*?),', str(result))



with open('/usr/share/zabbix/result.json', 'w') as outfile:
  outfile.write(json.dumps(proxy.har, ensure_ascii=True, indent=2))
driver.find_element_by_tag_name('body').screenshot('/usr/share/zabbix/screenshot.png')
server.stop()    
driver.quit()
