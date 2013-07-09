# coding:utf-8
import logging
import os
import logging.config
from ConfigParser import ConfigParser
from bs4 import BeautifulSoup
import varys


__author__ = 'swarm'


logging.config.fileConfig('logging.conf')
# create logger
logger = logging.getLogger('Crawler')

config_filename = os.path.join('.', 'crawler_config.ini')
config = ConfigParser()
config.read(config_filename)


def get_phone_urls():
    phone_urls_file = open('all_phone_urls.txt', 'r')
    all_phone_urls = [line for line in phone_urls_file.readlines()]
    phone_urls_file.close()
    return all_phone_urls


def phone_page(content, args):
    """ the main page of a single mobile phone,
        callback will go to visit the comment page of the mobile phone
    """
    phone_soup = BeautifulSoup(content)
    j_comment_div = phone_soup.find("div", {"id": "J_comment"})
    j_comment_url = j_comment_div.get('data-url')
    print '1 will visit ', j_comment_url
    varys.add_async(url=j_comment_url, callback=phone_comment, data=None, args=args)


def phone_comment(content, args):
    """ the comment page of a single mobile phone,
        callback will go to visit the positive comment and negative comment page, respectively
    """
    phone_comment_soup = BeautifulSoup(content)
    phone_filter_div = phone_comment_soup.find("div", {"class": "comment-filter"})
    pos_url = neg_url = ''
    for child in phone_filter_div:
        if (u'好評' in child.text) or (u'好评' in child.text):
            pos_url = child.get('href')
        elif (u'差評' in child.text) or (u'差评' in child.text):
            neg_url = child.get('href')
        else:
            pass
    print '2 positive: ', pos_url
    varys.add_async(url=pos_url, callback=comment_page, data=None, args=[args, 'pos'])
    print '2 negative: ', neg_url
    varys.add_async(url=neg_url, callback=comment_page, data=None, args=[args, 'neg'])


def comment_page(content, args):
    """ the positive comment OR negative comment page of a single mobile phone,
        callback will call itself,
            to go to visit the next page of positive comment OR negative comment
    """
    phone_url_num = args[0]
    pos_neg = args[1]
    comment_soup = BeautifulSoup(content)
    next_page_tag = comment_soup.find("a", {"class": "page-next"})
    if next_page_tag:
        next_page_url = next_page_tag.get('href')
        print '3: ', next_page_url
        varys.add_async(url=next_page_url, callback=comment_page, data=None, args=args)
    else:
        logger.info('%s of %s is Done' % (pos_neg, str(phone_url_num)))
        print '3: NO MORE NEXT PAGE'


def main():
    all_phone_urls = get_phone_urls()
    print 'there are %d phone urls in total' % len(all_phone_urls)
    for phone_url in all_phone_urls:
        phone_url_num = phone_url[phone_url.find('item/')+len('item/'): phone_url.find('.html?')]
        varys.add_async(url=phone_url, callback=phone_page, data=None, args=phone_url_num)


if __name__ == '__main__':
    main()
