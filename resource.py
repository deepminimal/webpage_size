from browsermobproxy import Server
from selenium import webdriver

# Purpose of this script: List all resources (URLs) that
# Chrome downloads when visiting some page.

### OPTIONS ###
url = "https://ostin.com"
chromedriver_location = "/home/work/webpage_size/chromedriver" # Path containing the chromedriver
browsermobproxy_location = "/home/work/webpage_size/browsermob-proxy-2.1.4/bin/browsermob-proxy" # location of the browsermob-proxy binary file (that starts a server)
chrome_location = "/usr/bin/google-chrome-stable"
###############

# Start browsermob proxy
server = Server(browsermobproxy_location)
server.start()
proxy = server.create_proxy()

# Setup Chrome webdriver - note: does not seem to work with headless On
options = webdriver.ChromeOptions()
options.binary_location = chrome_location
options.add_argument('--no-sandbox')
options.add_argument('--headless')
options.add_argument('--disable-dev-shm-usage')
# Setup proxy to point to our browsermob so that it can track requests
options.add_argument('--proxy-server=%s' % proxy.proxy)
driver = webdriver.Chrome(chromedriver_location, chrome_options=options)

# Now load some page
proxy.new_har("Example")
driver.get(url)

# Print all URLs that were requested
entries = proxy.har['log']["entries"]
for entry in entries:
    if 'request' in entry.keys():
        print entry['request']['url']

server.stop()
driver.quit()
