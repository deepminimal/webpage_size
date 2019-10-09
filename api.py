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
  
#os.popen("pkill -9 java")
#os.popen("pkill -9 brows")

app = Flask(__name__)
api = Api(app)
class GET_PAGE_SIZE(Resource):
  def get(self,URL):
    try:
      print("start get fed")
      server = Server("./browsermob-proxy-2.1.4/bin/browsermob-proxy", options={'port': 5100})
      server.start()
      proxy = server.create_proxy()
    except Exception as e:
      error2 = "ERROR1: " + str(e)
      return error2
    try:
      chromedriver = "./chromedriver"
      os.environ["webdriver.chrome.driver"] = chromedriver
      url = urlparse.urlparse(proxy.proxy).path
      chrome_options = webdriver.ChromeOptions()
      chrome_options.add_argument('--no-sandbox')
      chrome_options.add_argument('--headless')
      chrome_options.add_argument('--disable-dev-shm-usage')
      chrome_options.add_argument("--proxy-server={0}".format(url))
    except Exception as e:
      error2 = "ERROR2: " + str(e)
      return error2
      print("driver")
      driver = webdriver.Chrome(chromedriver,chrome_options =chrome_options)
      driver.set_window_size(1920, 1080)
      print("try")
      try:
        print("proxy.new_har")
        proxy.new_har(str(URL),options={'captureHeaders': True, 'captureContent':True, 'captureBinaryContent':True})
        print("driver.get")
        driver.get(URL)
        status_code = proxy.wait_for_traffic_to_stop(100, 20000)
        
      except Exception as err:
        error1 = "ERROR3: " + str(err)
        return str(error1)
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
      print("driver.quit")
      driver.quit()
      startDownloadTime = datetime.datetime.strptime(str(proxy.har['log']['entries'][0]['startedDateTime']), '%Y-%m-%dT%H:%M:%S.%fZ')
      LastStartDownloadTime = datetime.datetime.strptime(str(proxy.har['log']['entries'][counter-1]['startedDateTime']), '%Y-%m-%dT%H:%M:%S.%fZ')
      proxy.close()
      print("end")
      return {'bodySize':str(sum(bodySize)), 'time':str(sum(download_time)), 'LastStartDownloadTime': str(LastStartDownloadTime), 'startDownloadTime': str(startDownloadTime), 'total_download_time': str((LastStartDownloadTime - startDownloadTime).total_seconds())}
    except Exception as e:
      error2 = "ERROR4: " + str(e)
      return error2
try:        
    #app.logger.disabled = True
    #log = logging.getLogger('werkzeug')
    #log.disabled = True
    print("start main")
    api.add_resource(GET_PAGE_SIZE, "/webpage_size/<path:URL>")
    app.run(host='0.0.0.0',port=5001, debug=True)
except Exception as exc:
  error3 = "ERROR3: " + str(exc)
  print "PLOHO"
