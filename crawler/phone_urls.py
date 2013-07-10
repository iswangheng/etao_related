# coding:utf-8
import time
import codecs
import logging
import os
import logging.config
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
    total_phone_pages = 40
    to_visit_urls = []
    while total_phone_pages:
        to_visit_urls.append(next_page_url)
        ori_page = int(next_page_url[next_page_url.find("&p=")+len("&p="):])
        new_page = ori_page + 1
        ori_substr = "&p=%d" % ori_page
        new_substr = "&p=%d" % new_page
        next_page_url = next_page_url.replace(ori_substr, new_substr)
        total_phone_pages -= 1
    workers = [i+1 for i in range(len(to_visit_urls))]
    worker_index = 0
    for to_visit in to_visit_urls:
        worker_index += 1
        varys.add_async(url=to_visit, callback=process_single_page, data=None,
                        args=[all_phone_urls, worker_index, workers, to_visit])
    while len(workers) > 1:
        time.sleep(3)
        print 'current workers: ', workers
    print 'Done!!! Length of all_phone_urls is: ', len(all_phone_urls)
    return all_phone_urls


def process_single_page(content, args):
    """ get all the phone urls in the phone search page (36 phone urls in one single search page)
    """
    all_phone_urls = args[0]
    worker_index = args[1]
    workers = args[2]
    visit_url = args[3]
    # save_page(str(worker_index) + 'worker.html', content)
    single_page_soup = BeautifulSoup(content, 'lxml')
    product_table = single_page_soup.findAll("table", {"class": "product-table"})[0]
    product_trs = product_table.findAll("tr")
    index = 0
    app_str = "?tab=comment#J_detail_tabs_label"
    for product_tr in product_trs:
        if index > 0:
            product_url = product_tr.findAll("td")[1].find("a").get("href") + app_str
            all_phone_urls.append(product_url)
        index += 1
    workers.remove(worker_index)
    print 'worker: ', worker_index, ' len(all_phone_urls) is: ', len(all_phone_urls)


def save_page(file_name, content):
    """ save the page, used to test whether the pages are the same
    """
    print '-------save %s --------' % file_name
    save_file = codecs.open(file_name, 'w', 'gbk')
    save_file.write(content)
    save_file.close()


def phone_total_num():
    phone_file = open('all_phone_urls.txt', 'r')
    all_urls = [line for line in phone_file.readlines()]
    all_phone = []
    for phone_url in all_urls:
        all_phone.append(phone_url[phone_url.find('item/')+len('item/'): phone_url.find('.html?')])
    print 'length of all_phone list is: ', len(all_phone)
    all_phone_set = set(all_phone)
    print 'length of all_phone set is: ', len(all_phone_set)
    phone_file.close()
    print '-----------------DONE-------------------------'


def main():
    init_url = config.get('crawler', 'init_url')
    all_phone_urls = get_phone_urls(init_url)
    phone_urls_file = open('all_phone_urls.txt', 'w')
    for phone_url in all_phone_urls:
        phone_urls_file.write(phone_url)
        phone_urls_file.write('\r\n')
    phone_urls_file.close()


if __name__ == '__main__':
    # main()
    phone_total_num()
