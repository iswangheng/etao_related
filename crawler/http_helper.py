# coding:utf-8
import urllib2
import leveldb
from bs4 import BeautifulSoup
import requests
import time
import datetime
import json
import re

import os.path
from dateutil.parser import parse

HTTP_CACHE_PATH = os.path.join(os.path.dirname(__file__), 'http-cache')
html_cache_ldb = leveldb.LevelDB(HTTP_CACHE_PATH)


CACHE_VALID = datetime.timedelta(days=100)
HTTP_RETRY_LIMIT = 5


def get_html(url, cache=True, retry_seconds=1, proxy=False):
    cache_key = 'html-'+url
    try:
        cached = json.loads(html_cache_ldb.Get(cache_key))
    except KeyError as e:
        cached = {}
    now = datetime.datetime.now()
    if cache and cached and now - parse(cached['time']) < CACHE_VALID:
        # print 'cache get', url
        return cached['html']
    else:
        # print 'http get', url
        if proxy:
            resp = request_by_proxy(url)
        else:
            resp = requests.get(url)
        if resp.status_code == 200:
            html_cache_ldb.Put(cache_key, json.dumps({'html':resp.text, 'time': str(now)}))
            return resp.text
        else:
            print 'wrong', resp.status_code
            if retry_seconds > HTTP_RETRY_LIMIT:
                raise Exception('server error')
            print 'sleep and retry..'
            time.sleep(retry_seconds)
            return get_html(url, cache, retry_seconds+2, proxy)


class ProxyProvider(object):
    def __init__(self):
        self.proxy_src_url = 'http://51dai.li/http_anonymous.html'

    def grab_proxies_from_src_html(self, html):
        self.proxies_list = []
        soup = BeautifulSoup(html)
        listtb = soup.find(id='tb')
        ptable = listtb.find_all('table')[0]
        for tr in ptable.find_all('tr')[1:]:
            tds = tr.find_all('td')
            ip = str(tds[1].text)
            port = str(tds[2].text)
            self.proxies_list.append((ip, port))

    def load_proxies(self, refresh):
        src_html = get_html(self.proxy_src_url, cache=not refresh)
        self.grab_proxies_from_src_html(src_html)
        self.endless_list = self.gen_proxy_iterator()

    def gen_proxy_iterator(self):
        i = 0
        while True:
            ip, port = self.proxies_list[i % len(self.proxies_list)]
            yield {"http": "%s:%s" % (ip, port), "https": "%s:%s" % (ip, port)}
            i += 1

g_pp = ProxyProvider()
g_pp.load_proxies(refresh=False)


class FakeResponse(object):
    def __init__(self, status, text):
        self.status_code = status
        self.text = text


def request_by_proxy(url):
    headers = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36'}
    testing_url = 'http://www.baidu.com/'
    proxy_tried = 0
    for proxies in g_pp.endless_list:
        if proxy_tried > len(g_pp.proxies_list):
            g_pp.load_proxies(refresh=True)
        try:
            # print proxies
            proxy = urllib2.ProxyHandler(proxies)
            opener = urllib2.build_opener(proxy)
            urllib2.install_opener(opener)
            try:
                r = urllib2.urlopen(testing_url)
            except Exception as e:
                proxy_tried += 1
                continue
            r = urllib2.urlopen(url)
            return FakeResponse(r.getcode(), unicode(r.read(), 'gbk', errors='ignore'))

            # requests.get(url, proxies=proxies, headers=headers)
            # resp = requests.get(url)
            # return resp
        except Exception as e:
            print e
            pass


def main():
    url = 'http://jsonip.com'
    url = 'http://etao.com'
    html = get_html(url, cache=False, proxy=True)
    print html

if __name__ == '__main__':
    main()
    main()
    main()
    main()
