# coding:utf-8
import logging
import os
import logging.config
import threading
from ConfigParser import ConfigParser
from bs4 import BeautifulSoup
# http_helper is deprecated from July 9th, 2013
#from http_helper import get_html
# should use varys which is very powerful
import varys


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
    all_phone_urls = []
    next_page_url = init_url
    total_phone_pages = 30
    ONE_PAGE_NUM = 36
    to_visit_urls = []
    while total_phone_pages:
        print 'total_phone_pages: ', total_phone_pages
        to_visit_urls.append(next_page_url)
        ori_phone_index = int(next_page_url[next_page_url.find("&s=")+len("&s="): next_page_url.find("&size=")])
        new_phone_index = ori_phone_index + ONE_PAGE_NUM
        ori_substr = "&s=%d" % ori_phone_index
        new_substr = "&s=%d" % new_phone_index
        next_page_url = next_page_url.replace(ori_substr, new_substr)
        total_phone_pages -= 1
    for to_visit in to_visit_urls:
        varys.add_async(url=to_visit, callback=process_single_page, data=None, args=all_phone_urls)
    while len(all_phone_urls) < 1008:
        pass
    print 'length of all_phone_urls is: ', len(all_phone_urls)
    return all_phone_urls


def process_single_page(content, args):
    """ get all the phone urls in the phone search page (36 phone urls in one single search page)
    """
    single_page_soup = BeautifulSoup(content, 'lxml')
    products = single_page_soup.findAll("tr", {"class": "product-listitem"})
    pre_str = "http://s.etao.com"
    app_str = "?tab=comment#J_detail_tabs_label"
    temp_urls = [pre_str + product.find("td", {"class": "cell2"}).a.get('href') + app_str for product in products]
    print len(args)
    args.extend(temp_urls)


def main():
    init_url = config.get('crawler', 'init_url')
    all_phone_urls = get_phone_urls(init_url)
    phone_urls_file = open('all_phone_urls.txt', 'w')
    for phone_url in all_phone_urls:
        phone_urls_file.write(phone_url)
        phone_urls_file.write('\r\n')
    phone_urls_file.close()


if __name__ == '__main__':
    main()
