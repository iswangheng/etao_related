# coding:utf-8
import requests
import mechanize 
__author__ = 'swarm'


def test():
    request = mechanize.Request("http://s.etao.com/item/8184790.html?spm=1002.8.0.50.VtduKf&sku=3call&tab=comment#J_detail_tabs_label")
    # request = mechanize.Request("http://www.google.com")
    response = mechanize.urlopen(request)
    #@todo: test
    # print response.geturl()
    # print '-' * 80
    # print response.info()  # headers
    # print '-' * 80
    # print type(response.read())
    # print response.read()  # body (readline and readlines work too)
    print response.read().decode('GBK')  # body (readline and readlines work too)


def main():
    print 'test'
    #@todo: main
    test()
    pass

if __name__ == '__main__':
    main()