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
    init_page = get_html(init_url)
    init_soup = BeautifulSoup(init_page)
    urls = []
    return urls


def get_pos_neg_url(phone_url):
    """ get both positive comment url
                 and negative comment url
                 according to the phone url
    :param phone_url:
    """
    phone_html = get_html(phone_url)
    phone_soup = BeautifulSoup(phone_html)
    j_comment_div = phone_soup.find("div", {"id": "J_comment"})
    j_comment_url = j_comment_div.get('data-url')
    phone_comment_html = get_html(j_comment_url)
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
    comment_html = get_html(comment_url)
    comment_soup = BeautifulSoup(comment_html)
    next_page_tag = comment_soup.find("a", {"class": "page-next"})
    if next_page_tag:
        next_page_url = next_page_tag.get('href')
        print next_page_url
        visit_comment_page(next_page_url)
    else:
        print 'NO MORE NEXT PAGE'


def test_pos_neg_url():
    phone_url = 'http://s.etao.com/item/8184790.html?spm=1002.8.0.50.VtduKf&sku=3call&tab=comment#J_detail_tabs_label'
    pos_url, neg_url = get_pos_neg_url(phone_url)
    print "pos_url: ", pos_url
    print "neg_url: ", neg_url


def test_visit_comment():
    # comment_url = "http://dianping.etao.com/popup-comment-list-8184790-1-0-1-1.htm?wordId="
    # comment_url = "http://dianping.etao.com/popup-comment-list-8184790-1-0-1-1.htm?page=809&wordId="
    comment_url = "http://dianping.etao.com/popup-comment-list-8184790-1-0-3-1.htm?wordId="
    visit_comment_page(comment_url)


def test_get_phone_urls():
    init_url = ''
    phone_urls = get_phone_urls(init_url)
    print phone_urls


def main():
    print 'hello from master.py'
    #@todo: main
    test_pos_neg_url()
    # test_visit_comment()
    # test_get_phone_urls()
    logger.info('test logger, haha, LOL, hello logger world!')

if __name__ == '__main__':
    main()
