# coding:utf-8
import logging
import os
import logging.config
from ConfigParser import ConfigParser
from bs4 import BeautifulSoup
from http_helper import get_html


__author__ = 'swarm'


logging.config.fileConfig('logging.conf')
# create logger
logger = logging.getLogger('Crawler')

config_filename = os.path.join('.', 'crawler_config.ini')
config = ConfigParser()
config.read(config_filename)


def get_phone_urls(init_url):
    """ get all the phones urls according to the init url
    :param init_url:
    """
    init_page = get_html(init_url, proxy=True, cache=False)
    init_soup = BeautifulSoup(init_page)
    # product_listitems = init_soup.find("tr", {"class": "product-listitem"})
    # print product_listitems
    prefix_str = "http://s.etao.com"
    append_str = "&tab=comment#J_detail_tabs_label"
    urls = []
    return urls


def get_pos_neg_url(phone_url):
    """ get both positive comment url
                 and negative comment url
                 according to the phone url
    :param phone_url:
    """
    phone_html = get_html(phone_url, proxy=True)
    phone_soup = BeautifulSoup(phone_html)
    j_comment_div = phone_soup.find("div", {"id": "J_comment"})
    j_comment_url = j_comment_div.get('data-url')
    phone_comment_html = get_html(j_comment_url, proxy=True)
    phone_comment_soup = BeautifulSoup(phone_comment_html)
    phone_filter_div = phone_comment_soup.find("div", {"class": "comment-filter"})
    print phone_filter_div
    pos_url = neg_url = ''
    for child in phone_filter_div:
        if (u'好評' in child.text) or (u'好评' in child.text):
            pos_url = child.get('href')
        elif (u'差評' in child.text) or (u'差评' in child.text):
            neg_url = child.get('href')
        else:
            pass
    return pos_url, neg_url


def visit_comment_page(comment_url):
    """ visit the comment url page
        UNTIL there is no more [next page]
    :param comment_url:
    """
    comment_html = get_html(comment_url, proxy=True)
    comment_soup = BeautifulSoup(comment_html)
    next_page_tag = comment_soup.find("a", {"class": "page-next"})
    next_page_url = None
    if next_page_tag:
        next_page_url = next_page_tag.get('href')
        logger.info('next_page_url: %s' % str(next_page_url))
        print next_page_url
    else:
        print 'NO MORE NEXT PAGE'
    return next_page_url


def all_comment_pages(comment_url):
    count = 10
    while 1:
        if (not comment_url) or (0 == count):
            break
        comment_url = visit_comment_page(comment_url)
        count -= 1

def test_pos_neg_url():
    phone_url = 'http://s.etao.com/item/8184790.html?spm=1002.8.0.50.VtduKf&sku=3call&tab=comment#J_detail_tabs_label'
    pos_url, neg_url = get_pos_neg_url(phone_url)
    print "pos_url: ", pos_url
    print "neg_url: ", neg_url


def test_visit_comment():
    # all comments
    comment_url = "http://dianping.etao.com/popup-comment-list-8184790-1-0-1-1.htm?wordId="
    # all comments and page = 80
    # comment_url = "http://dianping.etao.com/popup-comment-list-8184790-1-0-1-1.htm?page=80&wordId="
    # the last page
    # comment_url = "http://dianping.etao.com/popup-comment-list-8184790-1-0-3-1.htm?wordId="
    # gbk wrong encode page
    # comment_url = "http://dianping.etao.com/popup-comment-list-8184790-1-0-3-1.htm?page=81&wordId="
    count = 10
    while 1:
        if (not comment_url) or (0 == count):
            break
        comment_url = visit_comment_page(comment_url)
        count -= 1


def test_get_phone_urls():
    init_url = config.get('crawler', 'init_url')
    print 'init_url: ', init_url
    phone_urls = get_phone_urls(init_url)
    print len(phone_urls)


def test():
    # test_pos_neg_url()
    # test_visit_comment()
    test_get_phone_urls()
    # logger.info('test logger, haha, LOL, hello logger world!')
    # phone_url = 'http://s.etao.com/item/8184790.html?spm=1002.8.0.50.VtduKf&sku=3call&tab=comment#J_detail_tabs_label'
    # pos_url, neg_url = get_pos_neg_url(phone_url)
    # print 'pos ' * 10
    # all_comment_pages(pos_url)
    # print 'neg ' * 10
    # all_comment_pages(neg_url)


def main():
    print 'hello from master.py'
    #@todo: main
    test()

if __name__ == '__main__':
    main()
