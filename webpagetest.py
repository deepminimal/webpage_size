import re
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import chromedriver_binary
from selenium.webdriver.support.ui import WebDriverWait

print("start new")
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--headless')
options.add_argument('--disable-dev-shm-usage')
d = DesiredCapabilities.CHROME
d['goog:loggingPrefs'] = { 'performance':'ALL' }
browser = webdriver.Chrome(desired_capabilities=d, options=options)
browser.implicitly_wait(60)
browser.set_page_load_timeout(60)
browser.set_window_size(1920, 1080)
browser.get('https://ostin.com/')
WebDriverWait(browser, 60).until(lambda driver: driver.execute_script("return document.readyState == 'complete'"))
total_bytes = []
total_bytes2 = []
total_bytes3 = []
newtwork_logs = []
newtwork_logs = browser.execute_script("var network = performance.getEntries() || {}; return network;")
for entry in newtwork_logs:
  if "transferSize" in str(entry):
    r = re.search(r"transferSize\':(.*?),", str(entry))
    total_bytes3.append(int(r.group(1)))
    if (int(r.group(1)) == 0):
      r2 = re.search(r"decodedBodySize\':(.*?),", str(entry))
      total_bytes.append(int(r2.group(1)))
      total_bytes2.append(int(r2.group(1)))
    else:
      total_bytes.append(int(r.group(1)))
print("transferSize if not 0 + decodedBodySize  : ", str(sum(total_bytes)))
print("decodedBodySize: ", str(sum(total_bytes2)))
print("transferSize only: ", str(sum(total_bytes3)))

total_bytes = []
browser_preformance_log = browser.get_log('performance')
for entry in browser_preformance_log:
        if "Network.loadingFinished" in str(entry):
            r = re.search(r'encodedDataLength\":(.*?),', str(entry))
            total_bytes.append(int(r.group(1)))
print("encodedDataLength: ", str(sum(total_bytes)))
with open('/usr/share/zabbix/newtwork_logs.json', 'w') as outfile:
    json.dump(newtwork_logs, outfile)
    
browser_preformance_log_clean = json.dumps(browser_preformance_log)
with open('/usr/share/zabbix/browser_preformance_log.json', 'w') as outfile:
    outfile.write(browser_preformance_log_clean.replace('\"', '"'))
    
s = """
,\"User-Agent\":\"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/78.0.3902.4 HeadlessChrome/78.0.3902.4 Safari/537.36\"},\"initialPriority\":\"Low\",\"meth
od\":\"GET\",\"mixedContentType\":\"none\",\"referrerPolicy\":\"no-referrer-when-downgrade\",\"url\":\"https://www.google.com/pagead/1p-user-list/961923915/?random=1569920593377&cv=9&fst=156992040
0000&num=2&guid=ON&u_h=600&u_w=800&u_ah=600&u_aw=800&u_cd=24&u_his=2&u_tz=0&u_java=false&u_nplug=0&u_nmime=0&sendb=1&data=ecomm_pagetype%3DMain%3Becomm_totalvalue%3D&frm=0&url=https%3A%2F%2Fostin.
com%2F&tiba=O%E2%80%99STIN%20-%20%D0%B8%D0%BD%D1%82%D0%B5%D1%80%D0%BD%D0%B5%D1%82-%D0%BC%D0%B0%D0%B3%D0%B0%D0%B7%D0%B8%D0%BD%20%D0%BE%D0%B4%D0%B5%D0%B6%D0%B4%D1%8B%3A%20%D0%BC%D1%83%D0%B6%D1%81%D0
%BA%D0%B0%D1%8F%2C%20%D0%B6%D0%B5%D0%BD%D1%81%D0%BA%D0%B0%D1%8F%20%D0%B8&fmt=3&is_vtc=1&random=2620350702&resp=GooglemKTybQhCsO&rmt_tld=0&ipr=y\"},\"requestId\":\"15012.211\",\"timestamp\":71402.2
97378,\"type\":\"Image\",\"wallTime\":1569920593.651964}},\"webview\":\"91AA28CD2108BCAAE4B744EC67DDC74D\"}", "level": "INFO"}, {"timestamp": 1569920593679, "message": "{\"message\":{\"method\":\"
Network.requestWillBeSent\",\"params\":{\"documentURL\":\"https://ostin.com/\",\"frameId\":\"91AA28CD2108BCAAE4B744EC67DDC74D\",\"hasUserGesture\":false,\"initiator\":{\"type\":\"other\"},\"loader
Id\":\"1E456159F6EE468F53921C2D4F65650B\",\"request\":{\"headers\":{\"Referer\":\"https://ostin.com/\",\"Sec-Fetch-Mode\":\"no-cors\",\"User-Agent\":\"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/5
37.36 (KHTML, like Gecko) Ubuntu Chromium/78.0.3902.4 HeadlessChrome/78.0.3902.4 Safari/537.36\"},\"initialPriority\":\"Low\",\"method\":\"GET\",\"mixedContentType\":\"none\",\"referrerPolicy\":\"
no-referrer-when-downgrade\",\"url\":\"https://www.google.de/pagead/1p-user-list/961923915/?random=1569920593377&cv=9&fst=1569920400000&num=2&guid=ON&u_h=600&u_w=800&u_ah=600&u_aw=800&u_cd=24&u_hi
s=2&u_tz=0&u_java=false&u_nplug=0&u_nmime=0&sendb=1&data=ecomm_pagetype%3DMain%3Becomm_totalvalue%3D&frm=0&url=https%3A%2F%2Fostin.com%2F&tiba=O%E2%80%99STIN%20-%20%D0%B8%D0%BD%D1%82%D0%B5%D1%80%D
0%BD%D0%B5%D1%82-%D0%BC%D0%B0%D0%B3%D0%B0%D0%B7%D0%B8%D0%BD%20%D0%BE%D0%B4%D0%B5%D0%B6%D0%B4%D1%8B%3A%20%D0%BC%D1%83%D0%B6%D1%81%D0%BA%D0%B0%D1%8F%2C%20%D0%B6%D0%B5%D0%BD%D1%81%D0%BA%D0%B0%D1%8F%2
0%D0%B8&fmt=3&is_vtc=1&random=2620350702&resp=GooglemKTybQhCsO&rmt_tld=1&ipr=y\"},\"requestId\":\"15012.212\",\"timestamp\":71402.321502,\"type\":\"Image\",\"wallTime\":1569920593.676088}},\"webvi
ew\":\"91AA28CD2108BCAAE4B744EC67DDC74D\"}", "level": "INFO"}, {"timestamp": 1569920593681, "message": "{\"message\":{\"method\":\"Network.requestWillBeSentExtraInfo\",\"params\":{\"blockedCookies
\":[],\"headers\":{\":authority\":\"www.google.de\",\":method\":\"GET\",\":path\":\"/pagead/1p-user-list/961923915/?random=1569920593377&cv=9&fst=1569920400000&num=2&guid=ON&u_h=600&u_w=800&u_ah=6
00&u_aw=800&u_cd=24&u_his=2&u_tz=0&u_java=false&u_nplug=0&u_nmime=0&sendb=1&data=ecomm_pagetype%3DMain%3Becomm_totalvalue%3D&frm=0&url=https%3A%2F%2Fostin.com%2F&tiba=O%E2%80%99STIN%20-%20%D0%B8%D
0%BD%D1%82%D0%B5%D1%80%D0%BD%D0%B5%D1%82-%D0%BC%D0%B0%D0%B3%D0%B0%D0%B7%D0%B8%D0%BD%20%D0%BE%D0%B4%D0%B5%D0%B6%D0%B4%D1%8B%3A%20%D0%BC%D1%83%D0%B6%D1%81%D0%BA%D0%B0%D1%8F%2C%20%D0%B6%D0%B5%D0%BD%D
1%81%D0%BA%D0%B0%D1%8F%20%D0%B8&fmt=3&is_vtc=1&random=2620350702&resp=GooglemKTybQhCsO&rmt_tld=1&ipr=y\",\":scheme\":\"https\",\"accept\":\"image/webp,image/apng,image/*,*/*;q=0.8\",\"accept-encod
ing\":\"gzip, deflate, br\",\"referer\":\"https://ostin.com/\",\"sec-fetch-mode\":\"no-cors\",\"sec-fetch-site\":\"cross-site\",\"user-agent\":\"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 
(KHTML, like Gecko) Ubuntu Chromium/78.0.3902.4 HeadlessChrome/78.0.3902.4 Safari/537.36\"},\"requestId\":\"15012.212\"}},\"webview\":\"91AA28CD2108BCAAE4B744EC67DDC74D\"}", "level": "INFO"}, {"ti
mestamp": 1569920593691, "message": "{\"message\":{\"method\":\"Network.responseReceived\",\"params\":{\"frameId\":\"91AA28CD2108BCAAE4B744EC67DDC74D\",\"loaderId\":\"1E456159F6EE468F53921C2D4F656
50B\",\"requestId\":\"15012.203\",\"response\":{\"connectionId\":951,\"connectionReused\":false,\"encodedDataLength\":341,\"fromDiskCache\":false,\"fromPrefetchCache\":false,\"fromServiceWorker\":
false,\"headers\":{\"Cache-Control\":\"private, no-cache, no-store\",\"Connection\":\"keep-alive\",\"Content-Length\":\"43\",\"Content-Type\":\"image/gif\",\"Date\":\"Tue, 01 Oct 2019 09:03:13 GMT
\",\"Last-Modified\":\"Mon, 28 Sep 1970 06:00:00 GMT\",\"P3P\":\"policyref=\\\"/w3c/p3p.xml\\\", CP=\\\"NOI DSP COR NID PSAo PSDo OUR BUS UNI NAV STA INT\\\"\",\"Server\":\"nginx\",\"Timing-Allow-
Origin\":\"*\"},\"mimeType\":\"image/gif\",\"protocol\":\"http/1.1\",\"remoteIPAddress\":\"[2a00:1148:db00::17]\",\"remotePort\":443,\"securityDetails\":{\"certificateId\":0,\"certificateTranspare
ncyCompliance\":\"unknown\",\"cipher\":\"AES_128_GCM\",\"issuer\":\"GlobalSign Organization Validation CA - SHA256 - G2\",\"keyExchange\":\"ECDHE_ECDSA\",\"keyExchangeGroup\":\"P-256\",\"protocol\
":\"TLS 1.2\",\"sanList\":[\"*.mail.ru\",\"mail.ru\"],\"signedCertificateTimestampList\":[],\"subjectName\":\"*.mail.ru\",\"validFrom\":1547819468,\"validTo\":1610977868},\"securityState\":\"secur
e\",\"status\":200,\"statusText\":\"OK\",\"timing\":{\"connectEnd\":264.786,\"connectStart\":145.222,\"dnsEnd\":145.222,\"dnsStart\":13.693,\"proxyEnd\":-1,\"proxyStart\":-1,\"pushEnd\":0,\"pushSt
art\":0,\"receiveHeadersEnd\":318.612,\"requestTime\":71401.957691,\"sendEnd\":265.838,\"sendStart\":265.703,\"sslEnd\":264.777,\"sslStart\":197.045,\"workerReady\":-1,\"workerStart\":-1},\"url\":
\"https://ad.mail.ru/retarget/?counter=2955741&list=&productid=&pagetype=Main&totalvalue=0&_=0.403026842611236\"},\"timestamp\":71402.32492,\"type\":\"Image\"}},\"webview\":\"91AA28CD2108BCAAE4B74
4EC67DDC74D\"}", "level": "INFO"}, {"timestamp": 1569920593691, "message": "{\"message\":{\"method\":\"Network.dataReceived\",\"params\":{\"dataLength\":43,\"encodedDataLength\":0,\"requestId\":\"
15012.203\",\"timestamp\":71402.325569}},\"webview\":\"91AA28CD2108BCAAE4B744EC67DDC74D\"}", "level": "INFO"}, {"timestamp": 1569920593691, "message": "{\"message\":{\"method\":\"Network.loadingFi
nished\",\"params\":{\"encodedDataLength\":384,\"requestId\":\"15012.203\",\"shouldReportCorbBlocking\":false,\"timestamp\":71402.277416}},\"webview\":\"91AA28CD2108BCAAE4B744EC67DDC74D\"}", "leve
l": "INFO"}, {"timestamp": 1569920593692, "message": "{\"message\":{\"method\":\"Network.responseReceived\",\"params\":{\"frameId\":\"91AA28CD2108BCAAE4B744EC67DDC74D\",\"loaderId\":\"1E456159F6EE
468F53921C2D4F65650B\",\"requestId\":\"15012.209\",\"response\":{\"connectionId\":207,\"connectionReused\":true,\"encodedDataLength\":111,\"fromDiskCache\":false,\"fromPrefetchCache\":false,\"from
ServiceWorker\":false,\"headers\":{\"cache-control\":\"public, max-age=1200\",\"content-encoding\":\"gzip\",\"content-length\":\"79815\",\"content-security-policy\":\"default-src * data: blob:;scr
ipt-src *.facebook.com *.fbcdn.net *.facebook.net *.google-analytics.com *.virtualearth.net *.google.com 127.0.0.1:* *.spotilocal.com:* 'unsafe-inline' 'unsafe-eval' blob: data: 'self';style-src d
ata: blob: 'unsafe-inline' *;connect-src *.facebook.com facebook.com *.fbcdn.net *.facebook.net *.spotilocal.com:* wss://*.facebook.com:* https://fb.scanandcleanlocal.com:* attachment.fbsbx.com ws
://localhost:* blob: *.cdninstagram.com 'self' chrome-extension://boadgeojelhgndaghljhdicfkmllpafd chrome-extension://dliochdbjfkdbacpmhlcpmleaejidimm;\",\"content-type\":\"application/x-javascrip
t; charset=utf-8\",\"date\":\"Tue, 01 Oct 2019 09:03:13 GMT\",\"expires\":\"Sat, 01 Jan 2000 00:00:00 GMT\",\"pragma\":\"public\",\"status\":\"200\",\"strict-transport-security\":\"max-age=3153600
0; preload; includeSubDomains\",\"vary\":\"Accept-Encoding\",\"x-content-type-options\":\"nosniff\",\"x-fb-debug\":\"S6ymwbWABfjaWMMeE0rhLTK/NbVodTK1bfg9jhGclb1XWRJGb42LsrU2YZkJWv1al3rNoDLsUea+5n0
xlfPIxg==\",\"x-fb-trip-id\":\"194532234\",\"x-frame-options\":\"DENY\",\"x-xss-protection\":\"0\"},\"mimeType\":\"application/x-javascript\",\"protocol\":\"h2\",\"remoteIPAddress\":\"[2a03:2880:f
01c:216:face:b00c:0:3]\",\"remotePort\":443,\"securityDetails\":{\"certificateId\":0,\"certificateTransparencyCompliance\":\"unknown\",\"cipher\":\"AES_128_GCM\",\"issuer\":\"DigiCert SHA2 High As
surance Server CA\",\"keyExchange\":\"\",\"keyExchangeGroup\":\"X25519\",\"protocol\":\"TLS 1.3\",\"sanList\":[\"*.facebook.com\",\"fb.com\",\"*.facebook.net\",\"facebook.com\",\"*.messenger.com\"
,\"*.xz.fbcdn.net\",\"*.fbsbx.com\",\"messenger.com\",\"*.xy.fbcdn.net\",\"*.fbcdn.net\",\"*.xx.fbcdn.net\",\"*.fb.com\",\"*.m.facebook.com\"],\"signedCertificateTimestampList\":[],\"subjectName\"
:\"*.facebook.com\",\"validFrom\":1566604800,\"validTo\":1571486400},\"securityState\":\"secure\",\"status\":200,\"statusText\":\"\",\"timing\":{\"connectEnd\":-1,\"connectStart\":-1,\"dnsEnd\":-1
,\"dnsStart\":-1,\"proxyEnd\":-1,\"proxyStart\":-1,\"pushEnd\":0,\"pushStart\":0,\"receiveHeadersEnd\":11.406,\"requestTime\":71402.287741,\"sendEnd\":0.929,\"sendStart\":0.742,\"sslEnd\":-1,\"ssl
Start\":-1,\"workerReady\":-1,\"workerStart\":-1},\"url\":\"https://connect.facebook.net/signals/config/191754474675804?v=2.9.4&r=stable\"},\"timestamp\":71402.333596,\"type\":\"Script\"}},\"webvi
ew\":\"91AA28CD2108BCAAE4B744EC67DDC74D\"}", "level": "INFO"}, {"timestamp": 1569920593692, "message": "{\"message\":{\"method\":\"Network.dataReceived\",\"params\":{\"dataLength\":315078,\"encode
dDataLength\":0,\"requestId\":\"15012.209\",\"timestamp\":71402.334076}},\"webview\":\"91AA28CD2108BCAAE4B744EC67DDC74D\"}", "level": "INFO"}]
"""

print(s.replace('\"', '"'))
print(type(s))

browser.close()
browser.quit()
