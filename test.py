#!/usr/bin/env python
# encoding: utf-8

from gevent import monkey; monkey.patch_all()
import requests

def run_website(method, url, **kwargs):
    try:
        result = requests.request(method, url, **kwargs)
    except Exception as e:
        result = str(e)
    return "<%s> %s" %(url, result)

