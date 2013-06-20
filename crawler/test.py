# coding:utf-8
from bs4 import BeautifulSoup
from http_helper import get_html
from jft import etao_f2j

__author__ = 'chin'

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


def main():
    f2j_example()
    pass


if __name__ == '__main__':
    main()
