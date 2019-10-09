from browsermobproxy import Server
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import os
import json
import urlparse
import json
import time
from collections import defaultdict
from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse
import logging
import datetime
try:
  from io import BytesIO
except ImportError:
  from StringIO import StringIO as BytesIO
  
proxy_optoins = {'port': 3344}
server = Server("./browsermob-proxy-2.1.4/bin/browsermob-proxy", options=proxy_optoins)
server.start()

app = Flask(__name__)
api = Api(app)
class GET_PAGE_SIZE(Resource):
  def get(self,URL):
    try:
      proxy = server.create_proxy()
      chromedriver = "./chromedriver"
      os.environ["webdriver.chrome.driver"] = chromedriver
      url = urlparse.urlparse(proxy.proxy).path
      chrome_options = webdriver.ChromeOptions()
      chrome_options.add_argument('--no-sandbox')
      chrome_options.add_argument('--headless')
      chrome_options.add_argument('--disable-dev-shm-usage')
      chrome_options.add_argument("--proxy-server={0}".format(url))
      driver = webdriver.Chrome(chromedriver,chrome_options =chrome_options)
      driver.set_window_size(1920, 1080)
      try:
        proxy.new_har(str(URL),options={'captureHeaders': True, 'captureContent':True, 'captureBinaryContent':True})
        driver.get(URL)
        status_code = proxy.wait_for_traffic_to_stop(100, 20000)
      except Exception as err:
        print("ERROR: %s" % str(err))
      #WebDriverWait(driver, 30).until(lambda driver: driver.execute_script("return document.readyState == 'complete'"))
      #S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
      #driver.set_window_size(S('Width'),S('Height'))
      #har = proxy.har['log']['entries']
      #mimeType = []
      bodySize = []
      download_time = []
      counter = 0
      for entry in proxy.har['log']['entries']:
        counter += 1
        #mimeType.append(entry['response']['content']['mimeType'])
        bodySize.append(int(entry['response']['bodySize']))
        download_time.append(int(entry['time']))
      #example = defaultdict(dict)
      #keys = defaultdict(dict)
      #for i in range(1, len(mimeType)):
      #  for entries in range(1, len(har)):
      #    if (mimeType[i] == har[entries]['response']['content']['mimeType']):
      #      keys[mimeType[i]][entries] = {'bodySize': int(har[entries]['response']['bodySize']),'URL': str(har[entries]['request']['url'])}
      #example['result'] = keys 
      driver.quit()
      startDownloadTime = datetime.datetime.strptime(str(proxy.har['log']['entries'][0]['startedDateTime']), '%Y-%m-%dT%H:%M:%S.%fZ')
      LastStartDownloadTime = datetime.datetime.strptime(str(proxy.har['log']['entries'][counter-1]['startedDateTime']), '%Y-%m-%dT%H:%M:%S.%fZ')
      proxy.close()
      server.stop()
      return {'bodySize':str(sum(bodySize)), 'time':str(sum(download_time)), 'LastStartDownloadTime': str(LastStartDownloadTime), 'startDownloadTime': str(startDownloadTime), 'total_download_time': str((LastStartDownloadTime - startDownloadTime).total_seconds())}
    except Exception as e:
      print("ERROR: %s" % str(e))
try:        
    #app.logger.disabled = True
    #log = logging.getLogger('werkzeug')
    #log.disabled = True
    api.add_resource(GET_PAGE_SIZE, "/webpage_size/<path:URL>")
    app.run(host='0.0.0.0',port=5001, debug=True)
except Exception as exc:
  print ("ERROR: %s" % str(exc))
