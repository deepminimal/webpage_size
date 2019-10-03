from browsermobproxy import Server
from selenium import webdriver
import os
import json
import urlparse

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
for entry in result:
        print(entry)
        if "bodySize" in str(entry):
            r = re.search(r'bodySize\":(.*?),', str(entry))
            total_bytes.append(int(r.group(1)))
print("bodySize: ", str(sum(total_bytes)))

with open('/usr/share/zabbix/result.json', 'w') as outfile:
  outfile.write(result)

driver.save_screenshot("/usr/share/zabbix/screenshot.png")
proxy.stop()    
driver.quit()
