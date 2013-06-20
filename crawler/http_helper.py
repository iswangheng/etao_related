# coding:utf-8
import leveldb
import requests
import time
import datetime
import json

import os.path
from dateutil.parser import parse

HTTP_CACHE_PATH = os.path.join(os.path.dirname(__file__), 'http-cache')
html_cache_ldb = leveldb.LevelDB(HTTP_CACHE_PATH)


CACHE_VALID = datetime.timedelta(days=100)
HTTP_RETRY_LIMIT = 5

def get_html(url, cache=True, retry_seconds = 1):
    cache_key = 'html-'+url
    try:
        cached = json.loads(html_cache_ldb.Get(cache_key))
    except KeyError as e:
        cached = {}
    now = datetime.datetime.now()
    if cached and now - parse(cached['time'])<CACHE_VALID:
        # print 'cache get', url
        return cached['html']
    else:
        # print 'http get', url
        resp = requests.get(url)
        if resp.status_code == 200:
            html_cache_ldb.Put(cache_key, json.dumps({'html':resp.text, 'time': str(now)}))
            return resp.text
        else:
            print 'wrong', resp.status_code
            if retry_seconds>HTTP_RETRY_LIMIT:
                raise Exception('server error')
            print 'sleep and retry..'
            time.sleep(retry_seconds)
            return get_html(url, cache, retry_seconds+2)

















