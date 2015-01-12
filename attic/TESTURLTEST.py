#!/usr/bin/python

import urllib,re
import urllib2
from urllib2 import HTTPError, URLError

url = "http://www.supcourt.by/cgi-bin/index.cgi?vm=d&vr=sostavraion&vd=4&at=0&m1=5"

try:
    response = urllib2.urlopen(url,None,15)
except HTTPError as err:
    pass
except URLError as err:
    if err.reason.errno == -2:
        host = urllib.splithost(re.sub("https?:","",url))[0]
        print "Ouch! %s" % host
except Exception as err:
    pass
