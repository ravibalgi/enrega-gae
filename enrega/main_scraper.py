#!/usr/bin/python

import simplejson as json
#import gevent
#from gevent import local, monkey
from district_scraper import districtExtract
from taluka_scraper import talukaExtract
from panchayat_scraper import panchayatExtract
import time

monkey.patch_all()

import urllib
from urlparse import urlparse

start = time.time()


def _cleanUrl(url):
    url_parts = urlparse(url.encode('utf-8'))
    query_params = {}
    for part in url_parts.query.split("&"):
        key, value = part.split("=")
        query_params[key] = value
    query_string = urllib.urlencode(query_params)
    encoded_url = "%s://%s%s?%s" % (url_parts.scheme,
                                    url_parts.netloc,
                                    url_parts.path,
                                    query_string)
    return encoded_url


def fetch_panchayat(url, district, taluka):
    encoded_url = _cleanUrl(url)
    data = panchayatExtract(encoded_url)
    if "panchayat" in global_data[district]["taluka"][taluka].keys():
        global_data[district]["taluka"][taluka]["panchayat"] =\
            dict(data.items() +
                 global_data[district]["taluka"][taluka]["panchayat"].items())
    else:
        global_data[district]["taluka"][taluka]["panchayat"] = data


def fetch_taluka(url, district):
    encoded_url = _cleanUrl(url)
    data = talukaExtract(encoded_url)
    if "taluka" in global_data[district].keys():
        global_data[district]["taluka"] =\
        dict(data.items() + global_data[district]["taluka"].items())
    else:
        global_data[district]["taluka"] = data
#    jobs = [gevent.spawn(fetch_panchayat, value['url'], district, key)
#            for key, value in data.iteritems()]
#    gevent.joinall(jobs)
        for value in data.iteritems():
            fetch_panchayat(url, district, value, year)


#global_data = local.local()
#year 11-12
data = districtExtract(districtyear1112, "2011")
global_data = data
#jobs = [gevent.spawn(fetch_taluka,
#                     value["url"], 
#                     key)
#        for key, value in data.iteritems(), "2011"]
#gevent.joinall(jobs)
for value in data.iteritems():
    fetch_taluka(url, value, "2011")
#year 10-11
data = districtExtract(districtyear1011, "2010")
global_data = data
#jobs = [gevent.spawn(fetch_taluka,
#                     value["url"], 
#                     key)
#        for key, value in data.iteritems(), "2010"]
#gevent.joinall(jobs)
for value in data.iteritems():
    fetch_taluka(url, value, "2010")

f = open('database/data.json', 'w')
output = json.dumps(global_data)
print time.time() - start
f.write(output)
