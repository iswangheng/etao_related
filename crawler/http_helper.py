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

def get_html(url, cache=True, retry_seconds = 1, proxy = False):
    cache_key = 'html-'+url
    try:
        cached = json.loads(html_cache_ldb.Get(cache_key))
    except KeyError as e:
        cached = {}
    now = datetime.datetime.now()
    if cache and cached and now - parse(cached['time'])<CACHE_VALID:
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
            if retry_seconds>HTTP_RETRY_LIMIT:
                raise Exception('server error')
            print 'sleep and retry..'
            time.sleep(retry_seconds)
            return get_html(url, cache, retry_seconds+2, proxy)


def get_proxies_list():
    proxies_list = []
    # secret = {"v":"3", "m":"4", "a":"2", "l":"9", "q":"0", "b":"5", "i":"7", "w":"6", "r":"8", "c":"1", "+":""}
    # listtb = soup.find(id='proxylisttb')
    # ptable = listtb.find_all('table')[-1]

    src_html = get_html('http://51dai.li/http_anonymous.html')
    soup = BeautifulSoup(src_html)
    listtb = soup.find(id='tb')
    ptable = listtb.find_all('table')[0]

    for tr in ptable.find_all('tr')[1:]:
        # m = re.match('(.+)document\.write\(\"\:\"(.+)\)', tr.find('td').text)
        # ip = str(m.group(1))
        # port = str(''.join(map(lambda c: secret[c], m.group(2))))
        # print ip, port
        tds = tr.find_all('td')
        ip = str(tds[1].text)
        port = str(tds[2].text)
        proxies = {
            "http": "%s:%s"%(ip, port),
            "https": "%s:%s"%(ip, port),
            }
        proxies_list.append(proxies)
    i = 0
    length = len(proxies_list)
    while True:
        yield proxies_list[i%length]
        i += 1

g_proxies_list = get_proxies_list()

class FakeResponse(object):
    def __init__(self, status, text):
        self.status_code = status
        self.text = text

def request_by_proxy(url):
    headers = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36'}
    testing_url = 'http://www.baidu.com/'
    for proxies in g_proxies_list:
        try:
            print proxies
            # proxy = urllib2.ProxyHandler({'http': '222.187.222.118:8080'})
            proxy = urllib2.ProxyHandler(proxies)
            opener = urllib2.build_opener(proxy)
            urllib2.install_opener(opener)
            try:
                r = urllib2.urlopen(testing_url)
            except Exception as e:
                continue
            r = urllib2.urlopen(url)
            return FakeResponse( r.getcode(), unicode(r.read(), 'gbk') )

            # requests.get(url, proxies=proxies, headers=headers)
            # resp = requests.get(url)
            # return resp
        except Exception as e:
            print e
            pass


def main():
    url = 'http://etao.com'
    html = get_html(url, cache=False, proxy=True)
    print html
    # r = request_by_proxy(url)
    # print r.text
    pass


if __name__ == '__main__':
    main()














