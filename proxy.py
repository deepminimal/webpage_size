from browsermobproxy import Server
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import os
import json
import urlparse
import json
from collections import defaultdict
from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse
import logging
try:
  from io import BytesIO
except ImportError:
  from StringIO import StringIO as BytesIO
  
proxy_optoins = {'port': 3343}
server = Server("./browsermob-proxy-2.1.4/bin/browsermob-proxy", options=proxy_optoins)
server.start()

app = Flask(__name__)
api = Api(app)
class GET_PAGE_SIZE(Resource):
  def get(self,URL):
    try:
      #os.popen("pkill -9 -f browsermob-proxy")
      #os.popen("pkill -9 -f chrom")
      #proxy_optoins = {'port': 3343}
      #server = Server("./browsermob-proxy-2.1.4/bin/browsermob-proxy", options=proxy_optoins)
      #server.start()
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
      proxy.new_har(options={'captureHeaders': True, 'captureContent':True, 'captureBinaryContent':True})
      try:
        driver.get(URL)
      except Exception as err:
        return (str(err))
      WebDriverWait(driver, 30).until(lambda driver: driver.execute_script("return document.readyState == 'complete'"))
      S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
      driver.set_window_size(S('Width'),S('Height'))
      result = json.dumps(proxy.har, ensure_ascii=True, indent=1)
      har = proxy.har['log']['entries']
      mimeType = []
      bodySize = []
      for entry in proxy.har['log']['entries']:
        mimeType.append(entry['response']['content']['mimeType'])
        bodySize.append(int(entry['response']['bodySize']))
      example = defaultdict(dict)
      keys = defaultdict(dict)
      for i in range(1, len(mimeType)):
        for entries in range(1, len(har)):
          if (mimeType[i] == har[entries]['response']['content']['mimeType']):
            keys[mimeType[i]][entries] = {'bodySize': int(har[entries]['response']['bodySize']),'URL': str(har[entries]['request']['url'])}
      example['result'] = keys 
      server.stop()  
      proxy.stop()
      driver.quit()
      #os.popen("pkill -9 -f browsermob-proxy")
      #os.popen("pkill -9 -f chrom")
      return {'bodySize':str(sum(bodySize))}
    except Exception as e:
      print("ERROR: %s" % str(e))
try:        
    #app.logger.disabled = True
    #log = logging.getLogger('werkzeug')
    #log.disabled = True
    api.add_resource(GET_PAGE_SIZE, "/webpage_size/<path:URL>")
    app.run(host='0.0.0.0',port=5001, debug=True)
except Exception as exc:
  print "ERROR: %s" % str(exc)
