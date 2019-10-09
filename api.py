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
  

app = Flask(__name__)
api = Api(app)

class GET_PAGE_SIZE(Resource):
  def get(self,URL):
    try:
      return "OK"
    except Exception as e:
      print("ERROR: %s" % str(e))
try:        
    #app.logger.disabled = True
    #log = logging.getLogger('werkzeug')
    #log.disabled = True
    print("start main")
    api.add_resource(GET_PAGE_SIZE, "/webpage_size/<path:URL>")
    app.run(host='0.0.0.0',port=5001, debug=True)
except Exception as exc:
  print ("ERROR: %s" % str(exc))
