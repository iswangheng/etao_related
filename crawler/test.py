# coding:utf-8
from bs4 import BeautifulSoup
import varys
# from http_helper import get_html
# from jft import etao_f2j

__author__ = 'chenzhao'


def f2j_example():
    url = 'http://etao.com'
    html = get_html(url)
    print type(html) #html is a ustr
    soup = BeautifulSoup(html)
    u = soup.get_text()
    print type(u) #u is a unicode string
    print u #u is fanti
    su = etao_f2j(u)
    print su #su is jianti


def f2j_test():
    ju = u'库巴雅诗兰黛经典六件套全网最低价166，完爆其它网站了！'
    print etao_f2j(ju)


def afunc(content, args):
    print args
    print content

def main():
    for i in range(10):
        varys.add_async(url='http://jsonip.com', callback=afunc, args = i)
    print 'main end'
    # f2j_test()
    # f2j_example()
    pass


if __name__ == '__main__':
    main()
